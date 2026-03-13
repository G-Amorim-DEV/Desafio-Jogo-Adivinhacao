import random
from core.jogo_base import Jogo
from services.data_loader import carregar_json


class JogoScramble(Jogo):

    nome = "Palavra Embaralhada"

    def gerar_desafio(self):

        palavras = carregar_json("data/palavras.json")
        self.original = random.choice(palavras)

        letras = list(self.original)
        random.shuffle(letras)

        return "".join(letras)

    def verificar_resposta(self, resposta):

        if resposta.lower() == self.original:
            self.jogador.adicionar_pontos(10)
            return "Acertou!"

        return "Tente novamente"