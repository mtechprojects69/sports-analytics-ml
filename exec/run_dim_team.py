from clients.bigquery_client import BigQueryClient
from pipelines.sports.football.team_dimension_pipeline import TeamDimensionPipeline

from config.settings import PROJECT_ID

def main(): 

    client = BigQueryClient(PROJECT_ID)

    pipeline = TeamDimensionPipeline(client)

    rows = pipeline.run()

    print(f"{rows} registros processados.")


if __name__ == "__main__":
    main()
