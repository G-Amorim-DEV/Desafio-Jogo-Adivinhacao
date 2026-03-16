from core.jogo_base import JogoBase
from games.matematica import Game as JogoMatematica
from games.forca.jogo_forca import Game as JogoForca
from games.memoria import Game as JogoMemoria
from games.quiz import Game as JogoQuiz
from games.verdadeiro_falso import Game as JogoVF
from games.scramble import Game as JogoScramble
from games.sequencia import Game as JogoSequencia

class GameAdapter:
    """Carrega e instancia jogos"""

    def __init__(self):
        # Dicionário nome → classe do jogo
        self.jogos = {
            "Matemática": JogoMatematica,
            "Forca": JogoForca,
            "Memória": JogoMemoria,
            "Quiz": JogoQuiz,
            "Sequência": JogoSequencia,
            "Verdadeiro ou Falso": JogoVF,
            "Scramble": JogoScramble
        }

    def criar(self, nome, jogador):
        """Cria uma instância do jogo com o jogador"""
        if nome not in self.jogos:
            raise ValueError(f"Jogo '{nome}' não encontrado")
        jogo_cls = self.jogos[nome]
        return jogo_cls(jogador)  # ✅ jogador passado aqui