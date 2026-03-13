import json
import random
from pathlib import Path


class WordService:
    """
    Serviço responsável por carregar e fornecer palavras
    para os jogos (Forca, Memória, etc).
    """

    def __init__(self):

        self.base_path = Path(__file__).resolve().parent.parent / "data"

        self.forca_data = self._load_json("palavras_forca.json")
        self.memoria_data = self._load_json("memoria_palavras.json")

        # evita repetir palavras
        self.usadas = set()

    # -------------------------
    # UTILIDADES
    # -------------------------

    def _load_json(self, filename):

        path = self.base_path / filename

        if not path.exists():
            raise FileNotFoundError(f"{filename} não encontrado")

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _filtrar_nao_usadas(self, lista):

        filtradas = [
            item for item in lista
            if item["palavra"] not in self.usadas
        ]

        # se acabou, reinicia ciclo
        if not filtradas:
            self.usadas.clear()
            return lista

        return filtradas

    # -------------------------
    # FORCA
    # -------------------------

    def get_palavra_forca(self, nivel):

        dificuldade = self._nivel_para_dificuldade(nivel)

        candidatos = [
            item for item in self.forca_data
            if item["dificuldade"] == dificuldade
        ]

        candidatos = self._filtrar_nao_usadas(candidatos)

        palavra = random.choice(candidatos)

        self.usadas.add(palavra["palavra"])

        return palavra

    # -------------------------
    # MEMÓRIA
    # -------------------------

    def get_palavras_memoria(self, nivel):

        dificuldade = self._nivel_para_dificuldade(nivel)

        categorias = list(self.memoria_data[dificuldade].keys())

        categoria = random.choice(categorias)

        palavras = self.memoria_data[dificuldade][categoria]

        quantidade = min(3 + nivel, len(palavras))

        selecionadas = random.sample(palavras, quantidade)

        return {
            "categoria": categoria,
            "palavras": selecionadas
        }

    # -------------------------
    # ADAPTAÇÃO DE DIFICULDADE
    # -------------------------

    def _nivel_para_dificuldade(self, nivel):

        if nivel <= 2:
            return "facil"
        elif nivel <= 4:
            return "medio"
        else:
            return "dificil"