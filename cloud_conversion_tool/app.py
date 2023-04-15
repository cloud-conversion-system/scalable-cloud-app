from cloud_conversion_tool import create_app
from flask import request
from flask_restful import Api
from .modelos import db, User, Task
from .vistas import VistaLogIn, VistaSignUp
from flask_jwt_extended import JWTManager
import zipfile
import py7zr
import tarfile

app = create_app('cloud_conversion_tool')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')

jwt = JWTManager(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        algorithm = request.form['algorithm']
        filename = file.filename
        compress_file(filename, algorithm)


def compress_file(filename, algorithm):
    if algorithm == 'zip':
        with zipfile.ZipFile(filename+'.zip', 'w') as zipf:
            zipf.write(filename)
        return f'El archivo {filename} ha sido comprimido con ZIP'
    elif algorithm == '7z':
        with py7zr.SevenZipFile(filename+'.7z', 'w') as szf:
            szf.write(filename)
        return f'El archivo {filename} ha sido comprimido con 7Z'
    elif algorithm == 'targz':
        with tarfile.open(filename+'.tar.gz', 'w:gz') as tgzf:
            tgzf.add(filename)
        return f'El archivo {filename} ha sido comprimido con TAR.GZ'
    elif algorithm == 'tarbz2':
        with tarfile.open(filename+'.tar.bz2', 'w:bz2') as tbzf:
            tbzf.add(filename)
        return f'El archivo {filename} ha sido comprimido con TAR.BZ2'
