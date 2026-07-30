from clients.bigquery_client import BigQueryClient
from pipelines.sports.football.competition_dimension_pipeline import (
    CompetitionDimensionPipeline,
)
from config.settings import PROJECT_ID

def main():

    client = BigQueryClient(PROJECT_ID)

    pipeline = CompetitionDimensionPipeline(client)

    rows = pipeline.run()

    print(f"{rows} registros processados.")


if __name__ == "__main__":
    main()