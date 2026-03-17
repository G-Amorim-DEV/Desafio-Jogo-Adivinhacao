import json
from pathlib import Path

from utils.paths import BASE_DIR


def carregar_json(path):
    try:
        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = BASE_DIR / file_path
        if not file_path.is_file():
            return None

        with open(file_path, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return None
    except OSError:
        return None
