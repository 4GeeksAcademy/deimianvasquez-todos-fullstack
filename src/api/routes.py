"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Todos
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from base64 import b64encode
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


# ruta donde registramos un usuario
@api.route('/register', methods=['POST'])
def add_new_user():
    try:
        body = request.json

        email = body.get("email", None)
        name = body.get("name", None)
        password = body.get("password", None)

        if email is None or password is None or name is None:
            return jsonify("Email, Password and Name required"), 400
        
        else:
            user = User()
            user_exist = user.query.filter_by(email=email).one_or_none()
            
            if user_exist is not None:
                return jsonify("User exists"), 400

            salt = b64encode(os.urandom(32)).decode("utf-8")
            password = generate_password_hash(f"{password}{salt}") # 1234klsflksndlkfnlskdfnlskdnflksndlfknsldkfnlsdknf

            user.name = name
            user.email = email
            user.password = password
            user.salt= salt
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
