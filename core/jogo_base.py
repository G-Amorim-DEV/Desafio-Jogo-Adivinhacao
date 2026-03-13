from abc import ABC, abstractmethod


class Jogo(ABC):

    nome = "Base"

    def __init__(self, jogador):
        self.jogador = jogador

    @abstractmethod
    def gerar_desafio(self):
        pass

    @abstractmethod
    def verificar_resposta(self, resposta):
        pass