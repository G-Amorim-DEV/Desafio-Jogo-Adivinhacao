from typing import List
from .jogador import Jogador


class Ranking:

    def __init__(self, limite: int = 10):
        self._jogadores: List[Jogador] = []
        self._limite = limite

    def adicionar_jogador(self, jogador: Jogador) -> None:

        for i, j in enumerate(self._jogadores):
            if j.nome.lower() == jogador.nome.lower():
                if jogador.pontuacao > j.pontuacao:
                    self._jogadores[i] = jogador
                return

        self._jogadores.append(jogador)

        self._jogadores.sort(
            key=lambda j: j.pontuacao,
            reverse=True
        )

        self._jogadores = self._jogadores[:self._limite]

    def listar(self) -> List[Jogador]:
        return self._jogadores