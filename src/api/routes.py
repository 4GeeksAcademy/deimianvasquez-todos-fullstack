"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Todos
from api.utils import generate_sitemap, APIException, send_mail
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from base64 import b64encode
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import cloudinary.uploader as uploader 
from datetime import timedelta

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# tiempo a expirar el token de recovery
expire_in_minute = 10
expire_delta = timedelta(minutes=expire_in_minute)


# ruta donde registramos un usuario
@api.route('/register', methods=['POST'])
def add_new_user():
    try:
        body_form = request.form
        body_files = request.files


        email = body_form.get("email", None)
        name = body_form.get("name", None)
        password = body_form.get("password", None)
        avatar = body_files.get("avatar", None)

        print({
            "email":email,
            "name":name,
            "password":password,
            "avatar": avatar
        })

        if email is None or password is None or name is None:
            return jsonify("Email, Password and Name required"), 400
        
        else:
            user = User()
            user_exist = user.query.filter_by(email=email).one_or_none()
            
            if user_exist is not None:
                return jsonify("User exists"), 400

            avatar = uploader.upload(avatar)
            avatar = avatar["secure_url"]

            print(avatar)
            salt = b64encode(os.urandom(32)).decode("utf-8")
            password = generate_password_hash(f"{password}{salt}") # 1234klsflksndlkfnlskdfnlskdnflksndlfknsldkfnlsdknf

            user.name = name
            user.email = email
            user.password = password
            user.salt= salt
            user.avatar=avatar
            db.session.add(user)

            try:
                db.session.commit()
                return jsonify("user created success"), 201
            except Exception as err:
                return jsonify(f"Error: {err.args}"), 500
      
            
    except Exception as err:
        return jsonify(f"Error: {err.args}"), 500
    

@api.route("/login", methods=["POST"])
def login():
    try:
        body = request.json
        email = body.get("email", None)
        password = body.get("password", None)

        if email is None or password is None:
            return jsonify({"message":" Necesitamos email y password"}), 400

        else:
            user = User.query.filter_by(email=email).one_or_none() # {id, email, pass} or None
            
            if user is None:
                return jsonify({"message": "Credenciales erradas"}), 400
            else:
                if check_password_hash(user.password, f"{password}{user.salt}"): # pass_hash, password
                    # generamos un token
                    token = create_access_token(identity=str(user.id))
                    return jsonify({"token":token, "current_user":user.serialize()})

                else:    
                    return jsonify({"message": "Credenciales erradas"}), 400
                
    except Exception as err:
        return jsonify(f"Error: {err}")
    

@api.route("/todos", methods=["POST"])
@jwt_required()
def add_todo():
    try:
        body = request.json
        todos = Todos()
        user_id = get_jwt_identity()

        # user = User.query.filter_by(email=user_id).first()
        print(user_id, "user id")

        if body.get("label") is None:
            return jsonify("debes enviarme un label"), 400
        
        if body.get("is_done") is None:
            return jsonify("debes enviarme un is_done"), 400

     
        todos.label = body["label"]
        todos.is_done = body.get("is_done")
        todos.user_id = user_id
        db.session.add(todos)

        try:
            db.session.commit()
            return jsonify("tarea guardada exitosamente"), 201
        except Exception as err:
            db.session.rollback()
            return jsonify(err.args), 500

    except Exception as err:
        return jsonify(err.args), 500


@api.route("/todos", methods=["GET"])
@jwt_required()
def get_all_todos():
    try:
        todos = Todos.query.filter_by(user_id=get_jwt_identity()).all()
        print(todos)
        return jsonify("trabajando por usted"), 200

    except Exception as err:
        return jsonify(err.args), 500


@api.route("/reset-password", methods=["POST"])
def recovery_password():
    try:
        body = request.json
        print(body)

        recovery_token = create_access_token(identity=str(body.get("email")), expires_delta=expire_delta)

        message = f"""
                    <h1>Se solicito recupetación de contraseña, ingrese en el siguiente link</h1>
                    <a href="https://potential-funicular-ppgwrqgxqvxc76wj-3000.app.github.dev/password-update?token={recovery_token}">
                        ir a recuperar contraseña
                    </a>
                   """



        response = send_mail("Recuperacion de contraseña",body.get("email"), message)
        print(response)  

        return jsonify("Correo enviado exitosamente"),200
    except Exception as err:
        return jsonify(f"Error: {err.args}")
    

@api.route("/update-password", methods=["PUT"])
@jwt_required()
def update_password():
    try:
        email = get_jwt_identity()
        password = request.json

        user = User.query.filter_by(email=email).one_or_none()

        if user is not None:
            salt = b64encode(os.urandom(32)).decode("utf-8")
            password= generate_password_hash(f"{password}{salt}") # 1234klsflksndlkfnlskdfnlskdnflksndlfknsldkfnlsdknf
            user.salt = salt
            user.password = password

            try:
                db.session.commit()
                return jsonify("Clave actualizada bien"), 200
            except Exception as error:
                print(error.args)
                return jsonify("No se puede actualizar el password"), 400

       
        return jsonify("trabajando por usted"), 200

    except Exception as err:
        print(err.args)
        return jsonify(f"Err: {err.args}")