from pipelines.sports.football.base_pipeline import BasePipeline
from domain.services.match_fact_service import MatchFactService
from domain.repositories.match_fact_repository import MatchFactRepository

class MatchFactPipeline(BasePipeline):

    def __init__(self, client):
        repository = MatchFactRepository(client)
        self.service = MatchFactService(repository)

    def extract(self):
        return None
    
    def transform(self, data):
        return data

    def load(self, data):
        return self.service.build_fact()  