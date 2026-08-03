from pipelines.sports.football.base_pipeline import BasePipeline
from domain.services.season_dimension_service import SeasonDimensionService
from domain.repositories.season_dimension_repository import SeasonDimensionRepository

class SeasonDimensionPipeline(BasePipeline):

    def __init__(self, client):
        repository = SeasonDimensionRepository(client)
        self.service = SeasonDimensionService(repository)

    def extract(self):
            return None
    
    def transform(self, data):
        return data

    def load(self, data):
        return self.service.build_dimension()    
