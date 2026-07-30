from clients.bigquery_client import BigQueryClient
import uuid


class CompetitionDimensionRepository:

    RAW_TABLE = "sports-analytics-ml.dev_raw.competitions"

    DIM_TABLE = "sports-analytics-ml.dev_core.dim_competition"

    def __init__(self, client: BigQueryClient):
        self.client = client
    
    def find_existing_business_keys(self) -> dict[tuple[str, int], int]:
        sql = f"""
                SELECT
                    competition_key,
                    provider_name,
                    provider_competition_id
                FROM `{self.DIM_TABLE}`
            """

        rows = self.client.query(sql)

        return {
            (
                row["provider_name"],
                row["provider_competition_id"],
            ): row["competition_key"]
            for row in rows
        }

    def find_raw_competitions(self) -> list[dict]:

        sql = f"""
            SELECT DISTINCT
                competition_id,
                competition_name,
                country_name,
                competition_gender,
                competition_youth,
                competition_international
            FROM `{self.RAW_TABLE}`
            ORDER BY competition_id
        """

        return self.client.query(sql)

    def find_by_business_key(
        self,
        provider_name: str,
        provider_competition_id: int,
    ) -> dict | None:

        sql = f"""
            SELECT *
            FROM `{self.RAW_TABLE}`
            WHERE provider_name = @provider_name
            AND provider_competition_id = @provider_competition_id
            LIMIT 1
        """

        params = {
            "provider_name": provider_name,
            "provider_competition_id": provider_competition_id,
        }

        rows = self.client.query(sql, params)

        return rows[0] if rows else None  

    def get_last_key(self) -> int:
        sql = f"""
            SELECT
                COALESCE(MAX(competition_key), 0) AS last_key
            FROM `{self.DIM_TABLE}`
        """

        rows = self.client.query(sql)

        return rows[0]["last_key"]

    def find_raw_competitions(self) -> list[dict]:
        sql = f"""
            SELECT DISTINCT
                competition_id,
                competition_name,
                country_name,
                competition_gender,
                competition_youth,
                competition_international
            FROM `{self.RAW_TABLE}`
            ORDER BY competition_id;
        """
        return self.client.query(sql)


    def merge(self, rows: list[dict]) -> int:

        if not rows:
            return 0

        temp_table = (
            f"sports-analytics-ml.dev_core."
            f"_tmp_dim_competition_{uuid.uuid4().hex}"
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
        AND T.provider_competition_id = S.provider_competition_id

        WHEN MATCHED THEN
            UPDATE SET

                competition_name = S.competition_name,

                country_name = S.country_name,

                competition_gender = S.competition_gender,

                competition_youth = S.competition_youth,

                competition_international = S.competition_international,

                competition_code = COALESCE(
                    S.competition_code,
                    T.competition_code
                ),

                updated_at = S.updated_at

        WHEN NOT MATCHED THEN

            INSERT (

                competition_key,

                provider_name,

                provider_competition_id,

                competition_name,

                country_name,

                competition_gender,

                competition_youth,

                competition_international,

                competition_code,

                created_at,

                updated_at

            )

            VALUES (

                S.competition_key,

                S.provider_name,

                S.provider_competition_id,

                S.competition_name,

                S.country_name,

                S.competition_gender,

                S.competition_youth,

                S.competition_international,

                S.competition_code,

                S.created_at,

                S.updated_at
            )
        """

        self.client.execute(merge_sql)

        self.client.execute(
            f"DROP TABLE `{temp_table}`"
        )

        return len(rows)
