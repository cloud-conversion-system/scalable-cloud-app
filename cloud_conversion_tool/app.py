from cloud_conversion_tool import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaLogIn, VistaSignUp, ViewTask, ViewTasks, ViewFile
from flask_jwt_extended import JWTManager

app = create_app('cloud_conversion_tool')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(ViewTasks, '/api/tasks')
api.add_resource(ViewTask, '/api/task/<int:id_task>')
api.add_resource(ViewFile, '/api/files/<string:id_file>')

jwt = JWTManager(app)
