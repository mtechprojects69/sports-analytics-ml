from clients.bigquery_client import BigQueryClient
import uuid


class TeamDimensionRepository:

    def __init__(self, client:BigQueryClient):
        self.client = client

    RAW_TABLE = "sports-analytics-ml.dev_raw.statsbomb_matches"

    DIM_TABLE = "sports-analytics-ml.dev_core.dim_team"    

    def ensure_table(self) -> None:

        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.DIM_TABLE}`
        (
            team_key INT64,

            provider_name STRING,

            provider_team_id INT64,

            team_name STRING,

            country_name STRING,

            team_gender STRING,

            team_group STRING,

            created_at TIMESTAMP,

            updated_at TIMESTAMP
        )

        CLUSTER BY provider_team_id
        """

        self.client.execute(sql)

    def find_raw_teams(self) -> list[dict]:

        sql = f"""
        SELECT DISTINCT

            home_team.home_team_id       AS provider_team_id,

            home_team.home_team_name     AS team_name,

            home_team.country.name       AS country_name,

            home_team.home_team_gender   AS team_gender,

            home_team.home_team_group    AS team_group

        FROM `{self.RAW_TABLE}`

        UNION DISTINCT

        SELECT DISTINCT

            away_team.away_team_id,

            away_team.away_team_name,

            away_team.country.name,

            away_team.away_team_gender,

            away_team.away_team_group

        FROM `{self.RAW_TABLE}`

        ORDER BY provider_team_id
        """

        return self.client.query(sql)
    
    def find_existing_business_keys(self) -> dict[tuple[str, int], int]:

        sql = f"""
        SELECT

            team_key,

            provider_name,

            provider_team_id

        FROM `{self.DIM_TABLE}`
        """

        rows = self.client.query(sql)

        return {
            (
                row["provider_name"],
                row["provider_team_id"],
            ): row["team_key"]
            for row in rows
        }
    
    def get_last_key(self) -> int:

        sql = f"""
        SELECT

            COALESCE(MAX(team_key),0) AS last_key

        FROM `{self.DIM_TABLE}`
        """

        rows = self.client.query(sql)

        return rows[0]["last_key"]

    def merge(self, rows: list[dict]) -> int:

        if not rows:
            return 0

        temp_table = (
            "sports-analytics-ml.dev_core."
            f"_tmp_dim_team_{uuid.uuid4().hex}"
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
        AND T.provider_team_id = S.provider_team_id

        WHEN MATCHED THEN

            UPDATE SET

                team_name = S.team_name,

                country_name = S.country_name,

                team_gender = S.team_gender,

                team_group = S.team_group,

                updated_at = S.updated_at

        WHEN NOT MATCHED THEN

            INSERT (

                team_key,

                provider_name,

                provider_team_id,

                team_name,

                country_name,

                team_gender,

                team_group,

                created_at,

                updated_at

            )

            VALUES (

                S.team_key,

                S.provider_name,

                S.provider_team_id,

                S.team_name,

                S.country_name,

                S.team_gender,

                S.team_group,

                S.created_at,

                S.updated_at

            )
        """

        self.client.execute(merge_sql)

        self.client.execute(
            f"DROP TABLE `{temp_table}`"
        )

        return len(rows)