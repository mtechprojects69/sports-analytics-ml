from ingestion.external.statsbomb_client import StatsBombClient
from services.storage_service import StorageService
import json

def main():
    client = StatsBombClient()
    storage = StorageService("sports-data-dev")

    competitions = client.get_competitions()

    storage.upload_json(
        "landing/football/statsbomb/competitions/competitions.json",
        json.dumps(competitions, indent=2),
    )

    print("Upload realizado com sucesso.")


if __name__ == "__main__":
    main()