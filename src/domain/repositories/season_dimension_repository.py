from clients.bigquery_client import BigQueryClient
import uuid


class SeasonDimensionRepository:

    RAW_TABLE = "sports-analytics-ml.dev_raw.competitions"

    DIM_TABLE = "sports-analytics-ml.dev_core.dim_season"

    DIM_COMPETITION_TABLE = "sports-analytics-ml.dev_core.dim_competition"

    def __init__(self, client:BigQueryClient):
        self.client = client

    def ensure_table(self) -> None:

        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.DIM_TABLE}`
        (
            season_key INT64,

            competition_key INT64,

            provider_name STRING,

            provider_season_id INT64,

            season_name STRING,

            season_start_date DATE,

            season_end_date DATE,

            created_at TIMESTAMP,

            updated_at TIMESTAMP
        )
        CLUSTER BY competition_key
        """

        self.client.execute(sql)    

    def find_raw_seasons(self) -> list[dict]:

        sql = f"""
        SELECT DISTINCT

            competition_id,

            season_id,

            season_name

        FROM `{self.RAW_TABLE}`

        ORDER BY

            competition_id,

            season_id
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

    def find_existing_business_keys(self) -> dict[tuple[str, int], int]:

        sql = f"""
        SELECT

            season_key,

            provider_name,

            provider_season_id

        FROM `{self.DIM_TABLE}`
        """

        rows = self.client.query(sql)

        return {
            (
                row["provider_name"],
                row["provider_season_id"],
            ): row["season_key"]
            for row in rows
        }

    def get_last_key(self) -> int:

        sql = f"""
        SELECT
            COALESCE(MAX(season_key), 0) AS last_key
        FROM `{self.DIM_TABLE}`
        """

        rows = self.client.query(sql)

        return rows[0]["last_key"]

    def merge(self, rows: list[dict]) -> int:

        if not rows:
            return 0

        temp_table = (
            "sports-analytics-ml.dev_core."
            f"_tmp_dim_season_{uuid.uuid4().hex}"
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
        AND T.provider_season_id = S.provider_season_id

        WHEN MATCHED THEN

            UPDATE SET

                competition_key = S.competition_key,

                season_name = S.season_name,

                updated_at = S.updated_at

        WHEN NOT MATCHED THEN

            INSERT (

                season_key,

                competition_key,

                provider_name,

                provider_season_id,

                season_name,

                created_at,

                updated_at

            )

            VALUES (

                S.season_key,

                S.competition_key,

                S.provider_name,

                S.provider_season_id,

                S.season_name,

                S.created_at,

                S.updated_at

            )
        """

        self.client.execute(merge_sql)

        self.client.execute(
            f"DROP TABLE `{temp_table}`"
        )

        return len(rows)