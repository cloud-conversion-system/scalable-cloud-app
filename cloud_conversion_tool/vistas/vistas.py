from flask_restful import Resource
from ..modelos import db, User, UserSchema
from flask import request
from flask_jwt_extended import jwt_required, create_access_token

class VistaSignUp(Resource):
    
    def post(self):
        new_user = User(username=request.json["username"], email=request.json["email"], password=request.json["password"])
        access_token = create_access_token(identity=request.json["username"])
        db.session.add(new_user)
        db.session.commit()
        return {'Message':'User created successfully', 'Access token': access_token}, 200

    
class VistaLogIn(Resource):
    def post(self):
            username = request.json["username"]
            password = request.json["password"]
            user = User.query.filter_by(username = username, password = password).all()
            if user:
                access_token = create_access_token(identity=request.json["username"])
                return {'Message':'Login successful', 'Access token': access_token}, 200
            else:
                return {'Message':'Wrong username or password'}, 401