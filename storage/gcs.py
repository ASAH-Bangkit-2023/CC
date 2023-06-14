import os
from google.cloud import storage
from uuid import uuid4

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'storage/cert.json'

class GCStorage:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = 'asah'

    def upload_file(self, file_content, file_name):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        # randomize file name
        file_path = "cdn/" +  str(uuid4())[:8] + "-" + file_name
        blob = bucket.blob(file_path)
        blob.upload_from_file(file_content, content_type='image/jpeg')
        file_path = file_path.replace(" ", "%20")
        return f'https://storage.cloud.google.com/{self.bucket_name}/{file_path}'
