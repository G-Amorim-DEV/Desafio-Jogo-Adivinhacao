import json
from pathlib import Path

def carregar_json(path):
    """
    Carrega um arquivo JSON e retorna seu conteúdo.

    Args:
        path (str): Caminho para o arquivo JSON.

    Returns:
        dict ou list: Conteúdo do JSON, ou None se houver erro.
    """
    try:
        file_path = Path(path)
        if not file_path.is_file():
            print(f"Arquivo não encontrado: {path}")
            return None

        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {path}")
        return None
    except Exception as e:
        print(f"Erro ao carregar JSON {path}: {e}")
        return None