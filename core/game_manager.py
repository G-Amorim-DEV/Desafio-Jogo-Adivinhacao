from games.quiz import JogoQuiz
from games.forca import JogoForca
from games.memoria import JogoMemoria
from games.sequencia import JogoSequencia
from games.matematica import JogoMatematica


class GameManager:

    def __init__(self):

        self.jogos = {
            "Quiz": JogoQuiz,
            "Forca": JogoForca,
            "Memória": JogoMemoria,
            "Sequência": JogoSequencia,
            "Matemática": JogoMatematica
        }

    def listar(self):
        return list(self.jogos.keys())

    def criar(self, nome, jogador):
        return self.jogos[nome](jogador)