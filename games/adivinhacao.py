import random
from core.jogo_base import Jogo


class JogoAdivinhacao(Jogo):

    nome = "Adivinhe o Número"

    def gerar_desafio(self):
        self.numero = random.randint(1, 100)
        return "Adivinhe um número entre 1 e 100"

    def verificar_resposta(self, resposta):

        resposta = int(resposta)

        if resposta == self.numero:
            self.jogador.adicionar_pontos(10)
            return "Acertou!"

        if resposta < self.numero:
            return "Maior"

        return "Menor"