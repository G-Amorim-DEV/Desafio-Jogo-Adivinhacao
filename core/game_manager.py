from core.game_loader import GameLoader

class GameManager:
    """Gerencia criação e listagem de jogos"""

    def __init__(self):
        self.loader = GameLoader()

    def listar_jogos(self):
        """Retorna os nomes dos jogos disponíveis"""
        return list(self.loader.jogos.keys())

    def criar_jogo(self, nome, jogador):
        """Cria uma instância do jogo com o jogador"""
        return self.loader.criar(nome, jogador)