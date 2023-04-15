from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))


class Status(enum.Enum):
    UPLOADED = 1
    PROCESSED = 2


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status), default=Status.UPLOADED)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
    file_name = db.Column(db.String(200))
    new_format = db.Column(db.String(50))


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class TaskSchema(SQLAlchemyAutoSchema):
    status = EnumADiccionario(attribute=("status"))

    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
