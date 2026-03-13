import json
import random


class JogoForca:

    nome = "Forca"

    def __init__(self, jogador):

        self.jogador = jogador

        with open("data/palavras_forca.json", encoding="utf-8") as f:
            self.lista = json.load(f)

        self.item = random.choice(self.lista)

        self.palavra = self.item["palavra"]

        self.tentativas = self.item["tentativas"]

        self.letras = []

    def gerar_desafio(self):

        progresso = ""

        for l in self.palavra:

            if l in self.letras:
                progresso += l + " "
            else:
                progresso += "_ "

        return {
            "progresso": progresso,
            "categoria": self.item["categoria"],
            "dica": self.item["dica"],
            "tentativas": self.tentativas
        }

    def verificar_resposta(self, letra):

        if letra in self.palavra:

            self.letras.append(letra)

            if all(l in self.letras for l in self.palavra):

                pontos = self.item["pontos"]

                self.jogador.ganhar_pontos(pontos)

                return "Você venceu!"

            return "Letra correta"

        else:

            self.tentativas -= 1

            if self.tentativas <= 0:
                return f"Fim de jogo! Palavra: {self.palavra}"

            return "Letra errada"