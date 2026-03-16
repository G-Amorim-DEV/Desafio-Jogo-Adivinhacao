from dataclasses import dataclass, asdict


@dataclass
class ResultadoJogo:

    correto: bool
    mensagem: str
    pontos: int
    finalizado: bool = False

    def to_dict(self):
        return asdict(self)

    @classmethod
    def erro(cls, mensagem: str = "Resposta inválida"):
        return cls(False, mensagem, 0, False)