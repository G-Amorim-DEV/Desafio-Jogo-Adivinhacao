from typing import List
from .jogador import Jogador


class Ranking:

    def __init__(self, limite: int = 10):
        self._jogadores: List[Jogador] = []
        self._limite = limite

    def adicionar_jogador(self, jogador: Jogador) -> None:
        """
        Adiciona ou atualiza um jogador no ranking.
        """

        for i, j in enumerate(self._jogadores):

            if j.nome.lower() == jogador.nome.lower():

                # Atualiza apenas se a nova pontuação for maior
                if jogador.pontos > j.pontos:
                    self._jogadores[i] = jogador

                self._ordenar()
                return

        self._jogadores.append(jogador)

        self._ordenar()

    def _ordenar(self):
        """
        Ordena o ranking e aplica o limite.
        """

        self._jogadores.sort(
            key=lambda j: j.pontos,
            reverse=True
        )

        self._jogadores = self._jogadores[:self._limite]

    def listar(self) -> List[Jogador]:
        """
        Retorna lista de jogadores.
        """
        return self._jogadores

    def tabela(self):
        """
        Retorna ranking formatado com posição.
        Ideal para mostrar em interface.
        """

        return [
            {
                "posicao": i + 1,
                "nome": j.nome,
                "pontos": j.pontos,
                "nivel": j.nivel
            }
            for i, j in enumerate(self._jogadores)
        ]

    def top(self, n: int = 3):
        """
        Retorna apenas os N melhores jogadores.
        """

        return self._jogadores[:n]

    def limpar(self):
        """
        Limpa o ranking.
        """

        self._jogadores.clear()