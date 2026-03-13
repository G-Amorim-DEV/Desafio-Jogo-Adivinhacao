import json
import random


class JogoQuiz:

    nome = "Quiz"

    def __init__(self, jogador):

        self.jogador = jogador

        with open("data/quiz.json", encoding="utf-8") as f:
            self.perguntas = json.load(f)

    def escolher_dificuldade(self):

        if self.jogador.nivel <= 2:
            return "facil"

        elif self.jogador.nivel <= 4:
            return "medio"

        return "dificil"

    def gerar_desafio(self):

        dificuldade = self.escolher_dificuldade()

        filtradas = [
            p for p in self.perguntas
            if p["dificuldade"] == dificuldade
        ]

        self.pergunta = random.choice(filtradas)

        return self.pergunta

    def verificar_resposta(self, resposta):

        if resposta == self.pergunta["resposta"]:

            pontos = self.pergunta["pontos"]

            self.jogador.ganhar_pontos(pontos)

            return f"Correto! +{pontos} pontos"

        else:

            self.jogador.perder_pontos(2)

            return f"Errado! Resposta correta: {self.pergunta['resposta']}"