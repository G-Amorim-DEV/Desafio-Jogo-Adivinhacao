from dataclasses import dataclass, field


@dataclass(frozen=True)
class GameInfo:
    nome: str
    titulo: str
    emoji: str
    descricao: str
    instrucoes: list[str] = field(default_factory=list)
    max_dicas: int = 2
    custo_dica_xp: int = 2


@dataclass(frozen=True)
class InputConfig:
    tipo: str = "text"
    label: str = "Digite sua resposta"
    placeholder: str = ""
    opcoes: list[str] = field(default_factory=list)
    max_chars: int | None = None
    min_value: int | None = None
    max_value: int | None = None
