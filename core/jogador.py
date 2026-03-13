class Jogador:

    def __init__(self, nome):
        self.nome = nome
        self.pontos = 0
        self.nivel = 1
        self.acertos = 0
        self.erros = 0
        self.historico = []

    def ganhar_pontos(self, pontos):
        self.pontos += pontos
        self.acertos += 1
        self.verificar_nivel()

    def perder_pontos(self, pontos):
        self.pontos = max(0, self.pontos - pontos)
        self.erros += 1

    def verificar_nivel(self):

        if self.pontos >= 100:
            self.nivel = 5
        elif self.pontos >= 60:
            self.nivel = 4
        elif self.pontos >= 30:
            self.nivel = 3
        elif self.pontos >= 10:
            self.nivel = 2

    def registrar(self, jogo, resultado):

        self.historico.append({
            "jogo": jogo,
            "resultado": resultado
        })