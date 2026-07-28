from clients.bigquery_client import BigQueryService

PROJECT_ID = "sports-analytics-ml"
DATASET_ID = "dev_raw"
TABLE_ID = "competitions"

GCS_URI = (
    "gs://sports-data-dev/"
    "processed/football/statsbomb/competitions/competitions.ndjson"
)


def main():
    bq = BigQueryService(PROJECT_ID)

    bq.load_json_from_gcs(
        dataset_id=DATASET_ID,
        table_id=TABLE_ID,
        gcs_uri=GCS_URI,
    )

    print("Tabela carregada com sucesso!")


if __name__ == "__main__":
    main()