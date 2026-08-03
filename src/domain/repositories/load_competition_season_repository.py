from clients.bigquery_client import BigQueryClient
from config.settings import PROJECT_ID
from config.settings import RAW_DATASET


class CompetitionRepository:

    def __init__(self):
        self.bq = BigQueryClient(PROJECT_ID)

    def find_competition_seasons(self) -> list[dict]:
        
        sql = f"""
        SELECT DISTINCT
            competition_id,
            season_id
        FROM `{PROJECT_ID}.{RAW_DATASET}.competitions`
        ORDER BY
            competition_id,
            season_id
        """

        return self.bq.query(sql)

    
  