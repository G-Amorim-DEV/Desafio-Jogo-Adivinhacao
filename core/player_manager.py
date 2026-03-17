from services.persistence.player_repository import PlayerRepository


class PlayerManager:
    def __init__(self):
        self.repository = PlayerRepository()
        self.store = self.repository.load()
        self.player = self._get_active_player()

    def _get_active_player(self):
        active_id = self.store.get("active_player_id")
        for player in self.store.get("players", []):
            if player["id"] == active_id:
                return player
        return None

    def salvar(self):
        self.repository.save(self.store)

    def tem_jogadores(self):
        return bool(self.store.get("players"))

    def listar_jogadores(self):
        return list(self.store.get("players", []))

    def listar_jogadores_por_ids(self, player_ids: list[str]):
        player_map = {player["id"]: player for player in self.store.get("players", [])}
        return [player_map[player_id] for player_id in player_ids if player_id in player_map]

    def criar_jogador(self, nome: str):
        nome = nome.strip()
        if not nome:
            return None

        existente = self.buscar_por_nome(nome)
        if existente:
            self.store["active_player_id"] = existente["id"]
            self.player = existente
            self.salvar()
            return existente

        novo = self.repository._player_base({"nome": nome})
        self.store.setdefault("players", []).append(novo)
        self.store["active_player_id"] = novo["id"]
        self.player = novo
        self.salvar()
        return novo

    def buscar_por_nome(self, nome: str):
        nome = nome.strip().lower()
        for player in self.store.get("players", []):
            if player["nome"].strip().lower() == nome:
                return player
        return None

    def definir_jogador_ativo(self, player_id: str):
        for player in self.store.get("players", []):
            if player["id"] == player_id:
                self.store["active_player_id"] = player_id
                self.player = player
                self.salvar()
                return player
        return None

    def excluir_jogador(self, player_id: str):
        players = self.store.get("players", [])
        restantes = [player for player in players if player["id"] != player_id]
        if len(restantes) == len(players):
            return False

        self.store["players"] = restantes
        if not restantes:
            self.store["active_player_id"] = None
            self.player = None
        else:
            if self.store.get("active_player_id") == player_id:
                self.store["active_player_id"] = restantes[0]["id"]
                self.player = restantes[0]
            else:
                self.player = self._get_active_player()
        self.salvar()
        return True

    def set_nome(self, nome):
        if not self.player:
            self.criar_jogador(nome)
            return
        self.player["nome"] = nome.strip()
        self.salvar()

    def configurar_dificuldade(self, modo: str, dificuldade_manual: str | None = None):
        if not self.player:
            return
        self.player["modo_dificuldade"] = modo
        if dificuldade_manual:
            self.player["dificuldade_manual"] = dificuldade_manual
        self.salvar()

    def adicionar_xp(self, valor):
        if not self.player:
            return
        self.player["xp"] += valor
        self.player["jogos_jogados"] += 1
        self.salvar()

    def ganhar_pontos(self, valor):
        self.adicionar_xp(valor)

    def perder_pontos(self, valor):
        if not self.player:
            return
        self.player["xp"] = max(0, self.player["xp"] - valor)
        self.salvar()

    def perder_vida(self):
        if not self.player:
            return 0
        if self.player["vidas"] > 0:
            self.player["vidas"] -= 1
            self.salvar()
        return self.player["vidas"]

    def ganhar_vida(self):
        if not self.player:
            return 0
        if self.player["vidas"] < 5:
            self.player["vidas"] += 1
            self.salvar()
        return self.player["vidas"]

    def resetar_vidas(self):
        if not self.player:
            return
        self.player["vidas"] = 5
        self.salvar()

    def vidas(self):
        return self.player["vidas"] if self.player else 0

    def dados(self):
        return self.player or {}

    def nivel(self):
        xp = self.player["xp"] if self.player else 0
        return xp // 100 + 1

    def dificuldade(self):
        if not self.player:
            return "facil"
        if self.player.get("modo_dificuldade") == "manual":
            return self.player.get("dificuldade_manual", "medio")

        nivel = self.nivel()
        if nivel <= 2:
            return "facil"
        if nivel <= 4:
            return "medio"
        return "dificil"
