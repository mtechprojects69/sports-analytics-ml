from clients.bigquery_client import BigQueryClient
import uuid

class MatchDimensionRepository:

    RAW_TABLE = "sports-analytics-ml.dev_raw.competitions"
    
    DIM_TABLE = "sports-analytics-ml.dev_core.dim_season"
    
    DIM_COMPETITION_TABLE = "sports-analytics-ml.dev_core.dim_competition"

    DIM_SEASON_TABLE = "sports-analytics-ml.dev_core.dim_season"

    def __init__(self, client:BigQueryClient):
        self.client = client

    def ensure_table(self) -> None:

        sql = f""""
            CREATE TABLE IF NOT EXISTS `sports-analytics-ml.dev_core.dim_match`
                (
                    match_key INT64,

                    competition_key INT64,

                    season_key INT64,

                    home_team_key INT64,

                    away_team_key INT64,

                    provider_name STRING,

                    provider_match_id INT64,

                    match_date DATE,

                    kick_off TIMESTAMP,

                    stadium_name STRING,

                    referee_name STRING,

                    home_score INT64,

                    away_score INT64,

                    match_week INT64,

                    created_at TIMESTAMP,

                    updated_at TIMESTAMP
                )

                CLUSTER BY
                    season_key,
                    competition_key;
                        """    
        self.client.execute(sql)

    def find_raw_teams(self) -> list[dict]:    
        sql = f"""
            SELECT DISTINCT

                home_team_id,
                home_team_name

                FROM dev_raw.matches

                UNION DISTINCT

                SELECT DISTINCT

                away_team_id,
                away_team_name

                FROM dev_raw.statsbom_matches

        """

        return self.client.query(sql)

    def find_competition_keys(self) -> dict[tuple[str, int], int]:
    
            sql = f"""
            SELECT
    
                competition_key,
    
                provider_name,
    
                provider_competition_id
    
            FROM `{self.DIM_COMPETITION_TABLE}`
            """
    
            rows = self.client.query(sql)
    
            return {
                (
                    row["provider_name"],
                    row["provider_competition_id"],
                ): row["competition_key"]
                for row in rows
            }
    
    def find_season_keys(self) -> dict[tuple[str, int], int]:

        sql = f"""
        SELECT

            season_key,

            provider_name,

            provider_season_id

        FROM `{self.DIM_SEASON_TABLE}`
        """

        rows = self.client.query(sql)

        return {
            (
                row["provider_name"],
                row["provider_season_id"],
            ): row["season_key"]
            for row in rows
        }