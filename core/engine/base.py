from abc import ABC, abstractmethod
from typing import Any

from core.engine.ui import GameInfo, InputConfig


class JogoBase(ABC):
    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=self.__class__.__name__,
            titulo=getattr(self, "nome", self.__class__.__name__),
            emoji="🎮",
            descricao="Desafio cognitivo",
            instrucoes=[],
        )

    def configurar_input(self) -> InputConfig:
        return InputConfig()

    @abstractmethod
    def gerar_desafio(self) -> Any:
        pass

    @abstractmethod
    def verificar_resposta(self, resposta: Any):
        pass

    @abstractmethod
    def renderizar(self, desafio: Any):
        pass

    @abstractmethod
    def obter_dica(self) -> str:
        pass
