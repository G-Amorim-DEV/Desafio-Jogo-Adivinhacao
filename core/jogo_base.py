from abc import ABC, abstractmethod
from typing import Any


class JogoBase(ABC):

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