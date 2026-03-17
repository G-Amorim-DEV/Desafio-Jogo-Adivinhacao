from core.engine.loader import GameLoader


class GameManager:
    def __init__(self):
        self.loader = GameLoader()

    def listar_jogos(self):
        return list(self.loader.jogos.keys())

    def criar_jogo(self, nome, jogador):
        return self.loader.criar(nome, jogador)
