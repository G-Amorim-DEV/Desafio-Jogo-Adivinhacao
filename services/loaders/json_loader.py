import json
from pathlib import Path


def carregar_json(path):
    try:
        file_path = Path(path)
        if not file_path.is_file():
            print(f"Arquivo não encontrado: {path}")
            return None

        with open(file_path, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {path}")
        return None
    except Exception as exc:
        print(f"Erro ao carregar JSON {path}: {exc}")
        return None
