from flask import request

from ..modelos import db, TaskSchema, Task
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

task_schema = TaskSchema()


class ViewTasks(Resource):
    # TODO: missing add query params
    @jwt_required()
    def get(self):
        return [task_schema.dump(t) for t in Task.query.all()]

    @jwt_required()
    def post(self):
        new_task = Task(
            fileName=request.json["fileName"],
            newFormat=request.json["newFormat"],
        )
        db.session.add(new_task)
        db.session.commit()
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

# TODO: Create file schema
# class ViewFile(Resource):
#     @jwt_required()
#     def get(self, id_file):
#         return file_schema.dump(File.query.get_or_404(id_file))
