from pipelines.sports.football.collection_pipeline import CollectionPipeline

from clients.sports.football.providers.statsbomb_client import StatsBombClient

from clients.bigquery_client import BigQueryClient

from config.settings import BUCKET_NAME
from config.settings import RAW_DATASET
from config.settings import PROJECT_ID

from clients.storage_client import StorageClient
from domain.repositories.competition_repository import CompetitionRepository


class MatchesPipeline(CollectionPipeline):

    def __init__(self):
        self.provider = StatsBombClient()
        self.storage = StorageClient(BUCKET_NAME)
        self.repository = CompetitionRepository()
        self.bigquery = BigQueryClient(PROJECT_ID)

    def get_work_items(self):
        return self.repository.find_competition_seasons()[:1]   

    def extract(self, item):
        competition_id = item["competition_id"]
        season_id = item["season_id"]

        return self.provider.get_matches(
            competition_id=competition_id,
            season_id=season_id,
        )

    def transform(self, data):
        return data

    def load(self, data, item):
    
        competition_id = item["competition_id"]
        season_id = item["season_id"]
    
        landing_path = (
            "landing/"
            "football/"
            "statsbomb/"
            f"matches/competition={competition_id}/"
            f"season={season_id}/"
            "matches.json"
        )
    
        processed_path = (
            "processed/"
            "football/"
            "statsbomb/"
            f"matches/competition={competition_id}/"
            f"season={season_id}/"
            "matches.ndjson"
        )
    
        # Landing
        self.storage.upload_json(landing_path, data)
    
        # Processed
        self.storage.upload_ndjson(processed_path, data)
    
        # BigQuery
        self.bigquery.load_json_from_gcs(
            dataset_id=RAW_DATASET,
            table_id="statsbomb_matches",
            gcs_uri=f"gs://{BUCKET_NAME}/{processed_path}",
        )
