from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

def data_path(nome_arquivo: str, subpasta: str = "") -> Path:
    """
    Retorna o Path completo de um arquivo dentro da pasta 'data'.

    Args:
        nome_arquivo (str): Nome do arquivo.
        subpasta (str, opcional): Subpasta dentro de 'data'. Defaults to "".

    Returns:
        Path: Caminho completo para o arquivo.
    """
    caminho = BASE_DIR / "data" / subpasta / nome_arquivo
    return caminho