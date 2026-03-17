import importlib
import logging
import pkgutil
from pathlib import Path

from core.engine.base import JogoBase


class GameLoader:
    def __init__(self):
        self.jogos = self._descobrir()

    def _descobrir(self):
        jogos = {}
        base = Path(__file__).resolve().parent.parent.parent / "games"

        for mod in pkgutil.walk_packages([str(base)], prefix="games."):
            if mod.name.count(".") != 1:
                continue

            try:
                modulo = importlib.import_module(mod.name)
                if hasattr(modulo, "GAME_NAME") and hasattr(modulo, "Game"):
                    jogos[modulo.GAME_NAME] = modulo.Game
            except Exception as exc:
                logging.warning(f"Erro carregando {mod.name}: {exc}")

        return jogos

    def listar(self):
        return list(self.jogos.keys())

    def criar(self, nome, jogador):
        if nome not in self.jogos:
            raise ValueError(f"Jogo '{nome}' não encontrado")

        jogo = self.jogos[nome](jogador)
        if isinstance(jogo, JogoBase):
            return jogo

        raise TypeError(f"Jogo '{nome}' não implementa JogoBase")
