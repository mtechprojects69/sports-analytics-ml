from pipelines.sports.football.base_pipeline import BasePipeline

from domain.services.competition_dimension_service import CompetitionDimensionService

from domain.repositories.competition_dimension_repository import CompetitionDimensionRepository

class CompetitionDimensionPipeline(BasePipeline):

    def __init__(self, client):
        repository = CompetitionDimensionRepository(client)
        self.service = CompetitionDimensionService(repository)

    def extract(self):
        return None

    def transform(self, data):
        return data

    def load(self, data):
        return self.service.build_dimension()
    
