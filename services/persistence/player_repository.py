import json
import uuid

from utils.paths import data_path


class PlayerRepository:
    def __init__(self):
        self.path = data_path("player.json")

    def load(self):
        try:
            with open(self.path, encoding="utf-8") as arquivo:
                data = json.load(arquivo)
                return self._normalizar_store(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"active_player_id": None, "players": []}

    def save(self, player_data: dict):
        with open(self.path, "w", encoding="utf-8") as arquivo:
            json.dump(player_data, arquivo, indent=2, ensure_ascii=False)

    def _player_base(self, data=None):
        data = data or {}
        return {
            "id": data.get("id", str(uuid.uuid4())),
            "nome": data.get("nome", ""),
            "vidas": data.get("vidas", 5),
            "xp": data.get("xp", 0),
            "jogos_jogados": data.get("jogos_jogados", 0),
            "modo_dificuldade": data.get("modo_dificuldade", "automatico"),
            "dificuldade_manual": data.get("dificuldade_manual", "medio"),
        }

    def _normalizar_store(self, data):
        if "players" in data:
            players = [self._player_base(player) for player in data.get("players", [])]
            active_player_id = data.get("active_player_id")
            if players and active_player_id not in {player["id"] for player in players}:
                active_player_id = players[0]["id"]
            return {"active_player_id": active_player_id, "players": players}

        if not any(data.get(chave) for chave in ("nome", "xp", "vidas", "jogos_jogados")):
            return {"active_player_id": None, "players": []}

        player = self._player_base(data)
        return {"active_player_id": player["id"], "players": [player]}
