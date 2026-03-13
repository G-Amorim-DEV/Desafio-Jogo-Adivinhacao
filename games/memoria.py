import json
import random


class JogoMemoria:

    nome = "Memória"

    def __init__(self, jogador):

        self.jogador = jogador

        with open("data/memoria_palavras.json", encoding="utf-8") as f:
            self.data = json.load(f)

    def escolher_dificuldade(self):

        if self.jogador.nivel <= 2:
            return "facil"
        elif self.jogador.nivel <= 4:
            return "medio"
        return "dificil"

    def gerar_desafio(self):

        dificuldade = self.escolher_dificuldade()

        categoria = random.choice(
            list(self.data[dificuldade].keys())
        )

        palavras = self.data[dificuldade][categoria]

        quantidade = 3 + self.jogador.nivel

        self.ordem = random.sample(palavras, quantidade)

        return {
            "categoria": categoria,
            "palavras": self.ordem
        }

    def verificar_resposta(self, resposta):

        resposta_lista = resposta.lower().split()

        if resposta_lista == self.ordem:

            self.jogador.ganhar_pontos(10)

            return "Memória perfeita!"

        return f"Ordem correta: {self.ordem}"