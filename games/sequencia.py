import json
import random


class JogoSequencia:

    nome = "Sequência"

    def __init__(self, jogador):

        self.jogador = jogador

        with open("data/sequencias.json", encoding="utf-8") as f:
            self.lista = json.load(f)

    def gerar_desafio(self):

        self.item = random.choice(self.lista)

        return self.item

    def verificar_resposta(self, resposta):

        if int(resposta) == self.item["resposta"]:

            pontos = self.item["pontos"]

            self.jogador.ganhar_pontos(pontos)

            return "Correto!"

        else:

            return f"Errado! {self.item['explicacao']}"