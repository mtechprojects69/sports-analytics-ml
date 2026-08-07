from domain.repositories.match_fact_repository  import MatchFactRepository
from config.settings import PROVIDER_NAME
from datetime import datetime, UTC

class MatchFactService:

    def __init__(self, repository: MatchFactRepository):
        self.repository = repository

    
    def build_fact(self) -> int:

        self.repository.ensure_table()

        raw_matches = self.repository.find_raw_matches()

        match_lookup = self.repository.find_match_keys()

        now = datetime.now(UTC).isoformat()

        rows = []

        for match in raw_matches:

            match_key = match_lookup.get(
                match["match_id"]
            )

            if match_key is None:
                print(f"Match {match['match_id']} didn't find in dim_match.")
                continue

            rows.append(
                {
                    "match_key": match_key,

                    "home_score": match["home_score"],

                    "away_score": match["away_score"],

                    "created_at": now,
                }
            )

        return self.repository.merge(rows)    