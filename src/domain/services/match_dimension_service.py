from domain.repositories.match_dimension_repository import MatchDimensionRepository
from config.settings import PROVIDER_NAME
from datetime import datetime, UTC

class MatchDimensionService:
    def __init__(
            self,
            repository:MatchDimensionRepository
        ): self.repository = repository

    def build_dimension(self) -> int:

        self.repository.ensure_table()

        raw_matches = self.repository.find_raw_matches()

        existing = self.repository.find_existing_business_keys()
        
        next_key = self.repository.get_last_key() + 1

        competition_lookup = self.repository.find_competition_keys()

        season_lookup = self.repository.find_season_keys()

        team_lookup = self.repository.find_team_keys()

        now = datetime.now(UTC).isoformat()

        rows = []

        for match in raw_matches:
            business_key = (
                PROVIDER_NAME,
                match["match_id"],
            )

            match_key = existing.get(business_key)

            if match_key is None:
                match_key = next_key
                next_key += 1
                
            rows.append(
                {
                    "match_key": match_key,

                    "competition_key": competition_lookup[
                        (PROVIDER_NAME, match["competition_id"])
                    ],

                    "season_key": season_lookup[
                        (PROVIDER_NAME, match["season_id"])
                    ],

                    "home_team_key": team_lookup[
                        (PROVIDER_NAME, match["home_team_id"])
                    ],

                    "away_team_key": team_lookup[
                        (PROVIDER_NAME, match["away_team_id"])
                    ],

                    "provider_name": PROVIDER_NAME,

                    "provider_match_id": match["match_id"],

                    "match_date": match["match_date"].isoformat(),

                    "kick_off": (
                        match["kick_off"].isoformat()
                        if hasattr(match["kick_off"], "isoformat")
                        else match["kick_off"]
                    ),

                    "match_week": match["match_week"],

                    "stadium_name": match["stadium_name"],

                    "referee_name": match["referee_name"],

                    "home_score": match["home_score"],

                    "away_score": match["away_score"],

                    "created_at": now,

                    "updated_at": now,
                }
            )
        return self.repository.merge(rows)    
