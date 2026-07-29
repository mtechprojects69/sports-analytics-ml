from google.cloud import bigquery
from config.settings import BQ_LOCATION


class BigQueryClient:
    def __init__(self, project_id: str):
        self.client = bigquery.Client(
            project=project_id,
            location=BQ_LOCATION,
        )

    def query(self, sql: str) -> list[dict]:
        print("=== SQL ===")
        print(repr(sql))
        print("===========")
        query_job = self.client.query(sql)

        rows = query_job.result()

        return [dict(row.items()) for row in rows]    

    def load_json_from_gcs(
        self,
        dataset_id: str,
        table_id: str,
        gcs_uri: str,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    ) -> None:
        table_ref = f"{self.client.project}.{dataset_id}.{table_id}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            autodetect=True,
            write_disposition=write_disposition
        )

        job = self.client.load_table_from_uri(
            gcs_uri,
            table_ref,
            job_config=job_config,
        )

        job.result() 














        