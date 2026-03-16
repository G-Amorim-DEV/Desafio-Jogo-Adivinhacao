import json
from utils.paths import data_path


class PlayerManager:

    def __init__(self):
        self.path = data_path("player.json")
        self.player = self._load()

    def _load(self):

        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
                # Garantir que tenha nome e vidas
                if "nome" not in data:
                    data["nome"] = ""
                if "vidas" not in data:
                    data["vidas"] = 5
                return data

        except (FileNotFoundError, json.JSONDecodeError):
            return {"xp": 0, "jogos_jogados": 0, "nome": "", "vidas": 5}

    def salvar(self):

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.player, f, indent=2)

    def set_nome(self, nome):
        self.player["nome"] = nome.strip()
        self.salvar()

    def adicionar_xp(self, valor):

        self.player["xp"] += valor
        self.player["jogos_jogados"] += 1

        self.salvar()

    def perder_pontos(self, valor):
        """Remove pontos do XP do jogador (não pode ficar negativo)"""
        self.player["xp"] = max(0, self.player["xp"] - valor)
        self.salvar()

    def perder_vida(self):
        """Remove uma vida do jogador"""
        if self.player["vidas"] > 0:
            self.player["vidas"] -= 1
            self.salvar()
        return self.player["vidas"]

    def resetar_vidas(self):
        """Restaura as vidas para 5"""
        self.player["vidas"] = 5
        self.salvar()

    def vidas(self):
        """Retorna o número de vidas atual"""
        return self.player["vidas"]

    def dados(self):
        return self.player

    def nivel(self):
        return self.player["xp"] // 100 + 1