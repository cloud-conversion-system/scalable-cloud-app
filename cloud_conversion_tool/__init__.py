from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/cloud_conversion_tool'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app
