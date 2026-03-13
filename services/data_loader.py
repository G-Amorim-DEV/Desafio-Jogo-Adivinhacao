import json


def carregar_json(path):

    with open(path, encoding="utf-8") as f:
        return json.load(f)