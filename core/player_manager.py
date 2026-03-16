import json
from utils.paths import data_path


class PlayerManager:

    def __init__(self):
        self.path = data_path("player.json")
        self.player = self._load()

    def _load(self):

        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):
            return {"xp": 0, "jogos_jogados": 0}

    def salvar(self):

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.player, f, indent=2)

    def adicionar_xp(self, valor):

        self.player["xp"] += valor
        self.player["jogos_jogados"] += 1

        self.salvar()

    def dados(self):
        return self.player

    def nivel(self):
        return self.player["xp"] // 100 + 1