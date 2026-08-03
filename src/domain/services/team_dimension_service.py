from domain.repositories.team_dimension_repository   import TeamDimensionRepository
from config.settings import PROVIDER_NAME
from datetime import datetime, UTC

class TeamDimensionService:
        def __init__(
        self,
        repository: TeamDimensionRepository,
    ):
            self.repository = repository


        def build_dimension(self) -> int:

            self.repository.ensure_table()

            raw_teams = self.repository.find_raw_teams()

            existing = self.repository.find_existing_business_keys()

            next_key = self.repository.get_last_key() + 1

            now = datetime.now(UTC).isoformat()

            rows = []

            for team in raw_teams:

                business_key = (
                    PROVIDER_NAME,
                    team["provider_team_id"],
                )

                team_key = existing.get(business_key)

                if team_key is None:
                    team_key = next_key
                    next_key += 1

                rows.append(
                    {
                        "team_key": team_key,

                        "provider_name": PROVIDER_NAME,

                        "provider_team_id": team["provider_team_id"],

                        "team_name": team["team_name"],

                        "country_name": team["country_name"],

                        "team_gender": team["team_gender"],

                        "team_group": team["team_group"],

                        "created_at": now,

                        "updated_at": now,
                    }
                )

            return self.repository.merge(rows)
