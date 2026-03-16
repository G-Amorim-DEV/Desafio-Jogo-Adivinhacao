import importlib
import pkgutil
from pathlib import Path
import logging

from core.jogo_base import JogoBase
from core.game_adapter import GameAdapter


class GameLoader:

    def __init__(self):
        self.jogos = self._descobrir()

    def _descobrir(self):

        jogos = {}

        base = Path(__file__).parent.parent / "games"

        for mod in pkgutil.walk_packages([str(base)], prefix="games."):

            try:
                modulo = importlib.import_module(mod.name)

                if hasattr(modulo, "GAME_NAME") and hasattr(modulo, "Game"):
                    jogos[modulo.GAME_NAME] = modulo.Game

            except Exception as e:
                logging.warning(f"Erro carregando {mod.name}: {e}")

        # Adicionar jogos em subpastas que podem não ser encontrados
        try:
            import games.forca.jogo_forca as forca_mod
            if hasattr(forca_mod, "GAME_NAME") and hasattr(forca_mod, "Game"):
                jogos[forca_mod.GAME_NAME] = forca_mod.Game
        except Exception as e:
            logging.warning(f"Erro carregando forca: {e}")

        return jogos

    def listar(self):
        return list(self.jogos.keys())

    def criar(self, nome, jogador):

        if nome not in self.jogos:
            raise ValueError(f"Jogo '{nome}' não encontrado")

        jogo = self.jogos[nome](jogador)

        if isinstance(jogo, JogoBase):
            return jogo

        return GameAdapter(jogo)