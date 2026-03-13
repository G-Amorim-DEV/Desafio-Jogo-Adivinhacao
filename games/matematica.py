import random


class JogoMatematica:

    nome = "Matemática"

    def __init__(self, jogador):

        self.jogador = jogador

    def gerar_desafio(self):

        limite = 10 + self.jogador.nivel * 10

        a = random.randint(1, limite)

        b = random.randint(1, limite)

        op = random.choice(["+", "-", "*"])

        self.resposta = eval(f"{a}{op}{b}")

        return f"{a} {op} {b}"

    def verificar_resposta(self, resposta):

        if int(resposta) == self.resposta:

            self.jogador.ganhar_pontos(5)

            return "Correto!"

        return f"Errado! {self.resposta}"