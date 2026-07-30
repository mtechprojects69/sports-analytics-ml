from domain.repositories.competition_dimension_repository import CompetitionDimensionRepository
from datetime import datetime, UTC

class CompetitionDimensionService:
    PROVIDER_NAME = "StatsBomb"
    def __init__(
        self,
        repository: CompetitionDimensionRepository,
    ):
        self.repository = repository

    def build_dimension(self):

        raw_competitions = self.repository.find_raw_competitions()

        existing = self.repository.find_existing_business_keys()

        next_key = self.repository.get_last_key() + 1

        rows = []

        now = datetime.now(UTC).isoformat()

        for competition in raw_competitions:

            business_key = (
                self.PROVIDER_NAME,
                competition["competition_id"],
            )

          
            competition_key = existing.get(business_key)

        
            if competition_key is None:

                competition_key = next_key
                next_key += 1

            rows.append(
                {
                    "competition_key": competition_key,
                    "provider_name": self.PROVIDER_NAME,
                    "provider_competition_id": competition["competition_id"],
                    "competition_name": competition["competition_name"],
                    "country_name": competition["country_name"],
                    "competition_gender": competition["competition_gender"],
                    "competition_youth": competition["competition_youth"],
                    "competition_international": competition[
                        "competition_international"
                    ],
                    "competition_code": None,
                    "created_at": now,
                    "updated_at": now,
                }
            )

        return self.repository.merge(rows)

