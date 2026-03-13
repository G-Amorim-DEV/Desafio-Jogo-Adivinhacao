import random
from core.jogo_base import Jogo
from services.data_loader import carregar_json


class JogoVF(Jogo):

    nome = "Verdadeiro ou Falso"

    def gerar_desafio(self):

        self.afirmacao = random.choice(
            carregar_json("data/vf.json")
        )

        return self.afirmacao["texto"]

    def verificar_resposta(self, resposta):

        if resposta.lower() == self.afirmacao["resposta"]:
            self.jogador.adicionar_pontos(5)
            return "Certo!"

        return "Errado!"