from google.cloud import bigquery


class BigQueryClient:
    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)

    def load_json_from_gcs(
        self,
        dataset_id: str,
        table_id: str,
        gcs_uri: str,
    ) -> None:
        table_ref = f"{self.client.project}.{dataset_id}.{table_id}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        job = self.client.load_table_from_uri(
            gcs_uri,
            table_ref,
            job_config=job_config,
        )

        job.result()