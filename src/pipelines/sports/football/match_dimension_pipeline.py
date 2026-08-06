from pipelines.sports.football.base_pipeline import BasePipeline
from domain.services.match_dimension_service import MatchDimensionService
from domain.repositories.match_dimension_repository import MatchDimensionRepository

class MatchDimensionPipeline(BasePipeline):

    def __init__(self, client):
        repository = MatchDimensionRepository(client)
        self.service = MatchDimensionService(repository)

    def extract(self):
        return None
    
    def transform(self, data):
        return data

    def load(self, data):
        return self.service.build_dimension()  