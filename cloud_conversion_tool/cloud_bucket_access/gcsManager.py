from google.oauth2 import service_account
from google.cloud import storage
import os

credentials_json = './credentials/google-credentials.txt'
credentials = service_account.Credentials.from_service_account_file(credentials_json)
client = storage.Client(credentials)

# Define bucket instance
bucket = client.get_bucket('cloud_conversion_tool')


def uploadFile(file_path, file_name):
    blob = bucket.blob('files/' + file_name)
    blob.upload_from_filename(file_path)


def downloadFile(download_path, file_name):
    blob = bucket.blob('files/' + file_name)
    blob.download_to_filename(download_path+'/'+file_name)
