from clients.bigquery_client import BigQueryClient
import uuid

class MatchDimensionRepository:

    def __init__(self, client: BigQueryClient):
        self.client = client

    RAW_TABLE = "sports-analytics-ml.dev_raw.statsbomb_matches"

    DIM_COMPETITION_TABLE = "sports-analytics-ml.dev_core.dim_competition"

    DIM_SEASON_TABLE = "sports-analytics-ml.dev_core.dim_season"

    DIM_TEAM_TABLE = "sports-analytics-ml.dev_core.dim_team"

    DIM_TABLE = "sports-analytics-ml.dev_core.dim_match"

    def ensure_table(self) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS `sports-analytics-ml.dev_core.dim_match`
            (
                match_key INT64,

                competition_key INT64,

                season_key INT64,

                home_team_key INT64,

                away_team_key INT64,
                
                home_score INT64,

                away_score INT64,

                provider_name STRING,

                provider_match_id INT64,

                match_date DATE,

                kick_off TIME,

                match_week INT64,

                stadium_name STRING,

                referee_name STRING,

                created_at TIMESTAMP,

                updated_at TIMESTAMP
            )

            CLUSTER BY
                competition_key,
                season_key;
        """
        self.client.execute(sql)

    def find_raw_matches(self) -> list[dict]: 
        sql = f"""
                SELECT

                    match_id,

                    competition.competition_id  AS competition_id,

                    season.season_id  AS season_id,

                    home_team.home_team_id  AS home_team_id,

                    away_team.away_team_id AS away_team_id,

                    match_date,

                    home_score,

                    away_score,

                    kick_off,

                    match_week,

                    stadium.name AS stadium_name,

                    referee.name AS referee_name

                FROM `{self.RAW_TABLE}`

                ORDER BY

                    match_date,
                    match_id
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

    def find_season_keys(self) -> dict[tuple[str,int],int]:
        sql = f"""
            SELECT 
                season_key,

                provider_season_id,
                        
                provider_name
                                    
            FROM    `{self.DIM_SEASON_TABLE}`

            ORDER BY 
                season_key
        """

        rows = self.client.query(sql)

        return {
            (
                row["provider_name"],
                row["provider_season_id"],
               
            ): row["season_key"]
            for row in rows
        }

    def find_team_keys(self) -> dict[tuple[str,int],int]:
        sql = f"""
            SELECT 
                team_key,
                provider_name,
                provider_team_id
            FROM `{self.DIM_TEAM_TABLE}` 
        """
        rows = self.client.query(sql)

        return{
            (
                row["provider_name"],
                row["provider_team_id"],
            ): row["team_key"]
            for row in rows
        }

    def find_existing_business_keys(self) -> dict[tuple[str,int],int]:
        sql = f"""
               SELECT
    
                match_key,
    
                provider_name,
    
                provider_match_id
               
                FROM `{self.DIM_TABLE}` 
               """
        
        rows = self.client.query(sql)

        return {
            (
                row["provider_name"],
                row["provider_match_id"],
            ): row["match_key"]
            for row in rows
        }

    def get_last_key(self) -> int:
    
            sql = f"""
            SELECT
                COALESCE(MAX(match_key), 0) AS last_key
            FROM `{self.DIM_TABLE}`
            """
    
            rows = self.client.query(sql)
    
            return rows[0]["last_key"]

    def merge(self, rows: list[dict]) -> int:
        if not rows:
            return 0

        temp_table = (
            "sports-analytics-ml.dev_core."
            f"_tmp_dim_match_{uuid.uuid4().hex}"
        )

        create_sql = f"""
        CREATE TABLE `{temp_table}`
        AS
        SELECT *
        FROM `{self.DIM_TABLE}`
        WHERE FALSE
        """

        self.client.execute(create_sql)
        
        self.client.load_rows(
            table=temp_table,
            rows=rows,
            write_disposition="WRITE_APPEND",
        )

        merge_sql = f""" 
            MERGE `{self.DIM_TABLE}` T
            USING `{temp_table}` S
    
        ON
            T.provider_name = S.provider_name
        AND T.provider_match_id = S.provider_match_id

        WHEN MATCHED THEN

            UPDATE SET

                competition_key = S.competition_key,

                season_key = S.season_key,

                home_team_key = S.home_team_key,

                away_team_key = S.away_team_key,

                home_score = S.home_score,

                away_score = S.away_score,

                match_date = S.match_date,

                kick_off = S.kick_off,

                match_week = S.match_week,

                stadium_name = S.stadium_name,

                referee_name = S.referee_name,

                updated_at = S.updated_at

        WHEN NOT MATCHED THEN

            INSERT (

                match_key,

                competition_key,

                season_key,

                home_score,

                away_score,       

                home_team_key,

                away_team_key,

                provider_name,

                provider_match_id,

                match_date,

                kick_off,

                match_week,

                stadium_name,

                referee_name,

                created_at,

                updated_at

            )

            VALUES (

                S.match_key,

                S.competition_key,

                S.season_key,

                S.home_score,

                S.away_score,

                S.home_team_key,

                S.away_team_key,

                S.provider_name,

                S.provider_match_id,

                S.match_date,

                S.kick_off,

                S.match_week,

                S.stadium_name,

                S.referee_name,

                S.created_at,

                S.updated_at

            )

        """

        self.client.execute(merge_sql)

        self.client.execute(
            f"DROP TABLE `{temp_table}`"
        )

        return len(rows)