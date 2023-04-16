from flask_restful import Resource
from ..modelos import db, User, Task, TaskSchema
from flask import request, send_from_directory
from flask_jwt_extended import jwt_required, create_access_token
from ..celery import compress_file
import os

UPLOAD_FOLDER = './files'

task_schema = TaskSchema()



class VistaSignUp(Resource):
    def post(self):
        new_user = User(
            username=request.json["username"], email=request.json["email"], password=request.json["password"])
        access_token = create_access_token(identity=request.json["username"])
        db.session.add(new_user)
        db.session.commit()
        return {'Message': 'User created successfully', 'Access token': access_token}, 200


class VistaLogIn(Resource):
    def post(self):
        username = request.json["username"]
        password = request.json["password"]
        user = User.query.filter_by(username=username, password=password).all()
        if user:
            access_token = create_access_token(
                identity=request.json["username"])
            return {'Message': 'Login successful', 'Access token': access_token}, 200
        else:
            return {'Message': 'Wrong username or password'}, 401


class ViewTasks(Resource):
    # TODO: missing add query params
    @jwt_required()
    def get(self):
        return [task_schema.dump(t) for t in Task.query.all()]

    @jwt_required()
    def post(self):
        file = request.files['file']
        file_name = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, file_name))
        new_format = request.form.get("newFormat")
        new_task = Task(file_name=file_name, new_format=new_format)
        db.session.add(new_task)
        db.session.commit()
        compress_file.delay(file_name, new_format, new_task.id)
        return task_schema.dump(new_task)


class ViewTask(Resource):
    @jwt_required()
    def get(self, id_task):
        return task_schema.dump(Task.query.get_or_404(id_task))

    @jwt_required()
    def delete(self, id_task):
        task = Task.query.get_or_404(id_task)
        db.session.delete(task)
        db.session.commit()
        return '', 204


class ViewFile(Resource):
    @jwt_required()
    def get(self, id_file):
        nombres_archivos = os.listdir(os.path.join(UPLOAD_FOLDER))
        filename=""
        for fileName in nombres_archivos:
            name = fileName.split(".")[0]
            if name==id_file:
                filename= fileName
        return send_from_directory(directory=UPLOAD_FOLDER, filename=filename, as_attachment=True)

