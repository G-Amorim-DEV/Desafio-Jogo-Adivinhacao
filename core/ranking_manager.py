from typing import Dict, List

from services.persistence.ranking_repository import RankingRepository

class RankingManager:
    """Gerencia rankings de jogadores por jogo e global."""

    def __init__(self):
        self.repository = RankingRepository()
        self.ranking = self.repository.load()

    def salvar(self):
        self.repository.save(self.ranking)

    def adicionar_score(self, nome_jogador: str, jogo: str, score: int):
        """Adiciona ou atualiza score de um jogador em um jogo."""
        if jogo not in self.ranking["jogos"]:
            self.ranking["jogos"][jogo] = {}
        
        self.ranking["jogos"][jogo][nome_jogador] = max(
            self.ranking["jogos"][jogo].get(nome_jogador, 0), score
        )
        
        # Atualiza ranking global (soma de todos os jogos)
        total = sum(
            jogo_dict.get(nome_jogador, 0) 
            for jogo_dict in self.ranking["jogos"].values()
        )
        self.ranking["global"][nome_jogador] = total
        
        self.salvar()

    def get_ranking_global(self) -> List[tuple]:
        """Retorna ranking global ordenado por score decrescente."""
        ranking = sorted(
            self.ranking["global"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return ranking

    def get_ranking_jogo(self, jogo: str) -> List[tuple]:
        """Retorna ranking de um jogo específico."""
        if jogo not in self.ranking["jogos"]:
            return []
        ranking = sorted(
            self.ranking["jogos"][jogo].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return ranking

    def get_jogos(self) -> List[str]:
        """Retorna lista de jogos com ranking."""
        return list(self.ranking["jogos"].keys())
