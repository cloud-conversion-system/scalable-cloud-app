import zipfile
import py7zr
import tarfile
import os

from cloud_conversion_tool.celery_script import app
from ..modelos import Task, TaskSchema, Status
from ..cloud_bucket_access import gcsManager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from google.cloud import pubsub_v1

engine = create_engine(
    'postgresql://postgres:password@10.91.16.3/cloud_conversion_tool')
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
task_schema = TaskSchema()
UPLOAD_FOLDER = '/python-docker/cloud_conversion_tool/files/'


#Credentials and pub/sub instantiation
credentials_json = '/app/credentials/google-credentials.json'
publisher = pubsub_v1.PublisherClient.from_service_account_file(credentials_json)
subscriber = pubsub_v1.SubscriberClient.from_service_account_file(credentials_json)

#Processes performed when a message is received
def callback(message):
    print(f"Received message: {message}")
    # The message will be the file name
    check_database(message)
    message.ack()

subscription_path = subscriber.subscription_path('cloud-conversion-system', 'worker_suscription')
subscriber.subscribe(subscription_path, callback=callback)

#Starts the message receiving loop
subscriber.open(callback=callback)


def check_database(message_file_name):
    tasks = db_session.query(Task).filter_by(status=Status.UPLOADED).filter_by(file_name=message_file_name).all()
    for task in tasks:
        compress_file(task.file_name, task.new_format, task.id)


def compress_file(file_name, algorithm, task_id):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    gcsManager.downloadFile(file_name)
    if algorithm == 'zip':
        with zipfile.ZipFile(file_path+'.zip', 'w') as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))
        gcsManager.uploadFile(file_path, file_name)
        os.remove(file_path)
        update_task(task_id)
        return f'El archivo {file_path} ha sido comprimido con ZIP'
    elif algorithm == '7z':
        with py7zr.SevenZipFile(file_path+'.7z', 'w') as szf:
            szf.write(file_path, arcname=os.path.basename(file_path))
        gcsManager.uploadFile(file_path, file_name)
        os.remove(file_path)
        update_task(task_id)
        return f'El archivo {file_path} ha sido comprimido con 7Z'
    elif algorithm == 'targz':
        with tarfile.open(file_path+'.tar.gz', 'w:gz') as tgzf:
            tgzf.add(file_path, arcname=os.path.basename(file_path))
        gcsManager.uploadFile(file_path, file_name)
        os.remove(file_path)
        update_task(task_id)
        return f'El archivo {file_path} ha sido comprimido con TAR.GZ'
    elif algorithm == 'tarbz2':
        with tarfile.open(file_path+'.tar.bz2', 'w:bz2') as tbzf:
            tbzf.add(file_path, arcname=os.path.basename(file_path))
        gcsManager.uploadFile(file_path, file_name)
        os.remove(file_path)
        update_task(task_id)
        return f'El archivo {file_path} ha sido comprimido con TAR.BZ2'


def update_task(task_id):
    task = db_session.query(Task).filter_by(id=task_id).first()
    task.status = Status.PROCESSED
    db_session.commit()
    task_schema.dump(task)

