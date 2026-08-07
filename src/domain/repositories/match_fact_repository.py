from clients.bigquery_client import BigQueryClient
import uuid

class MatchFactRepository:
    def __init__(self, client:BigQueryClient):
        self.client = client

    RAW_TABLE = "sports-analytics-ml.dev_raw.statsbomb_matches"    

    DIM_MATCH_TABLE = "sports-analytics-ml.dev_core.dim_match"

    FACT_TABLE = "sports-analytics-ml.dev_core.fact_match"


    def ensure_table(self):
        sql = f"""
            CREATE TABLE IF NOT EXISTS `sports-analytics-ml.dev_core.fact_match`
            (
                match_key INT64,

                home_score INT64,

                away_score INT64,

                created_at TIMESTAMP
            )
        """

        self.client.execute(sql)

    def find_raw_matches(self) -> list[dict]:

        sql = f""" 
            SELECT 
                 match_id,

                 home_score,

                 away_score
            FROM `{self.RAW_TABLE}`     
            """
        return self.client.query(sql)

    def find_match_keys(self) -> dict[tuple[str, int], int]:
            sql = f"""
                SELECT

                    match_key,

                    provider_match_id

                FROM `{self.DIM_MATCH_TABLE}`
                """

            rows = self.client.query(sql)

            return {
                (
                    row["provider_match_id"]
                ): row["match_key"]
                for row in rows
            }

    def merge(self, rows: list[dict]) -> int:

        if not rows:
            return 0

        temp_table = (
            "sports-analytics-ml.dev_core."
            f"_tmp_fact_match_{uuid.uuid4().hex}"
        )

        create_sql = f"""
        CREATE TABLE `{temp_table}`
        AS
        SELECT *
        FROM `{self.FACT_TABLE}`
        WHERE FALSE
        """

        self.client.execute(create_sql)

        self.client.load_rows(
            table=temp_table,
            rows=rows,
            write_disposition="WRITE_APPEND",
        )

        merge_sql = f"""
        MERGE `{self.FACT_TABLE}` T
        USING `{temp_table}` S

        ON
            T.match_key = S.match_key

        WHEN MATCHED THEN

            UPDATE SET

                home_score = S.home_score,

                away_score = S.away_score,

                created_at = S.created_at

        WHEN NOT MATCHED THEN

            INSERT (

                match_key,

                home_score,

                away_score,

                created_at

            )

            VALUES (

                S.match_key,

                S.home_score,

                S.away_score,

                S.created_at

            )
        """

        self.client.execute(merge_sql)

        self.client.execute(
            f"DROP TABLE `{temp_table}`"
        )

        return len(rows)