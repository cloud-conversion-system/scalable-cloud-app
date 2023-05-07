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
    blob = bucket.blob(FOLDER_PATH + file_name)
    blob.upload_from_filename(file_path)


def downloadFile(file_name):
    open(FOLDER_PATH+ file_name, 'w').close()  # create empty file
    blob = bucket.blob(file_name)
    blob.download_to_filename('/files/' + file_name)


def listBlobs(file_name):
    blobs = bucket.list_blobs()
    matching_blobs = [
        blob for blob in blobs if blob.name.startswith('files/' + file_name)]
    matching_blobs_sorted = sorted(
        matching_blobs, key=lambda b: b.time_created)
    return matching_blobs_sorted
