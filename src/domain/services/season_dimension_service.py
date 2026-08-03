from domain.repositories.season_dimension_repository   import SeasonDimensionRepository
from datetime import datetime, UTC

class SeasonDimensionService:
        def __init__(
        self,
        repository: SeasonDimensionRepository,
    ):
            self.repository = repository

        PROVIDER_NAME = "StatsBomb"
        DIM_COMPETITION_TABLE = "sports-analytics-ml.dev_core.dim_competition"

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

        def build_dimension(self) -> int: 

          self.repository.ensure_table()
   
          raw_seasons = self.repository.find_raw_seasons()  

          existing = self.repository.find_existing_business_keys()

          competition_lookup = self.repository.find_competition_keys()

          next_key = self.repository.get_last_key() + 1

          now = datetime.now(UTC).isoformat()

          rows = []

          for season in raw_seasons:

            business_key = (
                self.PROVIDER_NAME,
                season["season_id"],
            )

            competition_key = competition_lookup[
                (
                    self.PROVIDER_NAME,
                    season["competition_id"],
                )
            ]

      
            season_key = existing.get(business_key)

            if season_key is None:
                season_key = next_key
                next_key += 1

            rows.append(
                {
                    "season_key": season_key,

                    "competition_key": competition_key,

                    "provider_name": self.PROVIDER_NAME,

                    "provider_season_id": season["season_id"],

                    "season_name": season["season_name"],

                    "created_at": now,

                    "updated_at": now,
                }
            )

          return self.repository.merge(rows)
