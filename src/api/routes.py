"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from werkzeug.security import generate_password_hash, check_password_hash

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

            password = generate_password_hash(password)

            user.name = name
            user.email = email
            user.password = password
            user.salt=1
            db.session.add(user)

            try:
                db.session.commit()
                return jsonify("user created success"), 201
            except Exception as err:
                return jsonify(f"Error: {err.args}"), 500
    except Exception as err:
        return jsonify(f"Error: {err.args}"), 500
    


