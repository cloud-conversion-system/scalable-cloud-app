from google.oauth2.service_account import Credentials
from google.cloud import storage

credentials_json = '/app/credentials/google-credentials.json'
credentials = Credentials.from_service_account_file(credentials_json)
client = storage.Client(project='cloud_conversion_tool',
                        credentials=credentials)

# Define bucket instance
bucket = client.get_bucket('cloud_conversion_tool')
FOLDER_PATH = '/python-docker/cloud_conversion_tool/files/'


def uploadFile(file_path, file_name):
    blob = bucket.blob('files/' + file_name)
    blob.upload_from_filename(file_path)


def downloadFile(file_name):
    blob = bucket.blob('files/' + file_name)
    blob.download_to_filename(FOLDER_PATH + file_name)


def deleteFile(file_name):
    blob = bucket.blob('files/' + file_name)
    blob.delete()


def listBlobs(file_name):
    blobs = bucket.list_blobs()
    matching_blobs = [
        blob for blob in blobs if blob.name.startswith('files/' + file_name)]
    matching_blobs_sorted = sorted(
        matching_blobs, key=lambda b: b.time_created)
    return matching_blobs_sorted
