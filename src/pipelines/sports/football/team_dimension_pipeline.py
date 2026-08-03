from pipelines.sports.football.base_pipeline import BasePipeline
from domain.services.team_dimension_service import TeamDimensionService
from domain.repositories.team_dimension_repository import TeamDimensionRepository

class TeamDimensionPipeline(BasePipeline):

    def __init__(self, client):
        repository = TeamDimensionRepository(client)
        self.service = TeamDimensionService(repository)

    def extract(self):
            return None
    
    def transform(self, data):
        return data

    def load(self, data):
        return self.service.build_dimension()    