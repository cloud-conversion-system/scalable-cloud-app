from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    files = db.relationship('File', cascade='all, delete, delete-orphan')

class State(enum.Enum):
   UPLOADED = 1
   PROCESSED = 2

class File (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.LargeBinary)
    state = db.Column(db.Enum(State))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

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

class FileSchema(SQLAlchemyAutoSchema):
    state = EnumADiccionario(attribute=("state"))
    class Meta:
         model = File
         include_relationships = True
         load_instance = True