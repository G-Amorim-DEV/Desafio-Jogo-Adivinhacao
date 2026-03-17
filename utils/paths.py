from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


def data_dir(subpasta: str = "") -> Path:
    caminho = BASE_DIR / "data"
    if subpasta:
        caminho = caminho / subpasta
    return caminho


def data_path(nome_arquivo: str, subpasta: str = "") -> Path:
    return data_dir(subpasta) / nome_arquivo
