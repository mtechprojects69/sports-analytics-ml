from google.cloud import storage

class StorageService:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_json(self, blob_name: str, data: str) -> None:
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(
            data,
            content_type="application/json",
        )
    def download_json(self, blob_name: str) -> str:
        blob = self.bucket.blob(blob_name)
        return blob.download_as_text()    

    def upload_text(
    self,
    blob_name: str,
    content: str,
    content_type: str = "text/plain",
) -> None:
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(
            content,
            content_type=content_type,
        )