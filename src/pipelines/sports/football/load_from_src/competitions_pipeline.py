from pipelines.sports.football.base_pipeline import BasePipeline

from clients.sports.football.providers.statsbomb_client import StatsBombClient

from config.settings import BUCKET_NAME
from clients.storage_client import StorageClient

class CompetitionsPipeline(BasePipeline):

    def __init__(self):
        self.provider = StatsBombClient()
        self.storage = StorageClient(BUCKET_NAME)

    def extract(self):
        return self.provider.get_competitions()

    def transform(self, data):
        return data

    def load(self, data):
        self.storage.upload_json(
    "landing/football/statsbomb/competitions/competitions.json",
    data,
)