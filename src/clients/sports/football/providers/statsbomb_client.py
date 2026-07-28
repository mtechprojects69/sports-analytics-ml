from typing import Any

import requests

class StatsBombClient:
    BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

    def get_competitions(self) -> list[dict[str, Any]]:
        response = requests.get(
            f"{self.BASE_URL}/competitions.json",
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    def get_matches(
        self,
        competition_id: int,
        season_id: int,
    ) -> list[dict[str, Any]]:
        response = requests.get(
            f"{self.BASE_URL}/matches/{competition_id}/{season_id}.json",
            timeout=30,
        )
        response.raise_for_status()
        return response.json()