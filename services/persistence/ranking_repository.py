import json
from typing import Dict

from utils.paths import data_path


class RankingRepository:
    def __init__(self):
        self.path = data_path("ranking.json")

    def load(self) -> Dict:
        try:
            with open(self.path, encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"global": {}, "jogos": {}}

    def save(self, ranking_data: dict):
        with open(self.path, "w", encoding="utf-8") as arquivo:
            json.dump(ranking_data, arquivo, indent=2, ensure_ascii=False)
