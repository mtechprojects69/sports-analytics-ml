from clients.bigquery_client import BigQueryClient
from pipelines.sports.football.season_dimension_pipeline import SeasonDimensionPipeline

from config.settings import PROJECT_ID

def main(): 

    client = BigQueryClient(PROJECT_ID)

    pipeline = SeasonDimensionPipeline(client)

    rows = pipeline.run()

    print(f"{rows} registros processados.")


if __name__ == "__main__":
    main()
