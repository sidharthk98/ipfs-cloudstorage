from google.cloud import storage
from datetime import datetime,timedelta
# Initialize the Google Cloud Storage client
client = storage.Client(project='srini-sandbox-cloudwerx')

# Specify the name of your Google Cloud Storage bucket
bucket_name = 'osis-ipfs-poc-bucket'

def UploadtoCloudStorage(filename, destination_blob_name=None):
    # Use the filename as the destination_blob_name if not provided
    if destination_blob_name is None:
        destination_blob_name = filename

    customTime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+0000')
    customMetadata = {
        'customTime': {customTime},  
    }
    # Upload the file to the bucket
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.custom_time = datetime.now()
    blob.upload_from_filename(filename)
    return f'gs://{bucket_name}/{destination_blob_name}'


def DownloadfromCloudStorage(name, URL):
    parts = URL.split('/')
    blob_name = parts[3]

    # Downloading the blob from bucket as stream
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with open(name, 'wb') as file:
        blob.download_to_file(file)
        return file

def ChangeObjectRetention(name,URL,toggle):

    blob_name = ('/').join(URL.split('/')[3:])
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    if toggle == "pin":
        newCustomTime = datetime.now()+timedelta(days=365)
        blob.patch()

    elif toggle == "unpin":
        newCustomTime = datetime.now()
        DownloadfromCloudStorage(name,URL)
        UploadtoCloudStorage(name)
        blob.custom_time=newCustomTime
        blob.upload_from_filename(filename)
    



