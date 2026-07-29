from google.cloud import storage
import json

class StorageClient:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
    def upload_json(self, blob_name: str, data) -> None:


        if not isinstance(data, str):
            data = json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            )

        blob = self.bucket.blob(blob_name)

        blob.upload_from_string(
            data,
            content_type="application/json",
        )

        print(f"✅ Upload realizado: gs://{self.bucket.name}/{blob_name}")    

    def upload_ndjson(self, blob_name: str, data: list[dict]) -> None:

        ndjson = "\n".join(
            json.dumps(record, ensure_ascii=False)
            for record in data
        )

        blob = self.bucket.blob(blob_name)

        blob.upload_from_string(
            ndjson,
            content_type="application/x-ndjson",
        )

        print(f"✅ Upload realizado: gs://{self.bucket.name}/{blob_name}")