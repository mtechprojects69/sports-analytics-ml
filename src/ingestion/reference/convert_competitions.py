from services.storage_service import StorageService
from utils.json_converter import json_to_ndjson

BUCKET = "sports-data-dev"

SOURCE = "landing/football/statsbomb/competitions/competitions.json"
TARGET = "processed/football/statsbomb/competitions/competitions.ndjson"


def main():
    storage = StorageService(BUCKET)

    json_content = storage.download_json(SOURCE)

    ndjson = json_to_ndjson(json_content)

    storage.upload_text(
        TARGET,
        ndjson,
        content_type="application/x-ndjson",
    )

    print("NDJSON criado com sucesso.")


if __name__ == "__main__":
    main()