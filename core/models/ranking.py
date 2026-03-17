from typing import List

from core.models.player import Jogador


class Ranking:
    def __init__(self, limite: int = 10):
        self._jogadores: List[Jogador] = []
        self._limite = limite

    def adicionar_jogador(self, jogador: Jogador) -> None:
        for i, jogador_existente in enumerate(self._jogadores):
            if jogador_existente.nome.lower() == jogador.nome.lower():
                if jogador.pontos > jogador_existente.pontos:
                    self._jogadores[i] = jogador

                self._ordenar()
                return

        self._jogadores.append(jogador)
        self._ordenar()

    def _ordenar(self):
        self._jogadores.sort(key=lambda jogador: jogador.pontos, reverse=True)
        self._jogadores = self._jogadores[: self._limite]

    def listar(self) -> List[Jogador]:
        return self._jogadores

    def tabela(self):
        return [
            {
                "posicao": i + 1,
                "nome": jogador.nome,
                "pontos": jogador.pontos,
                "nivel": jogador.nivel,
            }
            for i, jogador in enumerate(self._jogadores)
        ]

    def top(self, n: int = 3):
        return self._jogadores[:n]

    def limpar(self):
        self._jogadores.clear()
