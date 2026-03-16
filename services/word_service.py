import json
import random
from pathlib import Path

class WordService:
    """
    Serviço responsável por fornecer palavras para jogos
    como Forca e Memória, controlando dificuldade e evitando repetições.
    """

    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent / "data"

        self.forca_data = self._load_json("palavras_forca.json")
        self.memoria_data = self._load_json("memoria_palavras.json")

        # controla palavras usadas separadamente
        self.usadas_forca = set()
        self.usadas_memoria = set()

    # -------------------------
    # UTILIDADES
    # -------------------------

    def _load_json(self, filename):
        path = self.base_path / filename
        if not path.exists():
            raise FileNotFoundError(f"{filename} não encontrado")
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _filtrar_nao_usadas(self, lista, usadas_set):
        """
        Filtra itens que já foram usados.
        Reinicia o set caso todos os itens tenham sido usados.
        """
        filtradas = [item for item in lista if item.get("palavra", item) not in usadas_set]
        if not filtradas:
            usadas_set.clear()
            filtradas = lista
        return filtradas

    def _nivel_para_dificuldade(self, nivel):
        """Converte nível numérico em dificuldade textual."""
        if nivel <= 2:
            return "facil"
        elif nivel <= 4:
            return "medio"
        return "dificil"

    # -------------------------
    # FORCA
    # -------------------------

    def get_palavra_forca(self, nivel):
        dificuldade = self._nivel_para_dificuldade(nivel)
        candidatos = [item for item in self.forca_data if item["dificuldade"] == dificuldade]

        candidatos = self._filtrar_nao_usadas(candidatos, self.usadas_forca)

        palavra = random.choice(candidatos)
        self.usadas_forca.add(palavra["palavra"])
        return palavra

    # -------------------------
    # MEMÓRIA
    # -------------------------

    def get_palavras_memoria(self, nivel):
        dificuldade = self._nivel_para_dificuldade(nivel)
        categorias = list(self.memoria_data[dificuldade].keys())
        categoria = random.choice(categorias)

        palavras = self.memoria_data[dificuldade][categoria]
        palavras = self._filtrar_nao_usadas(palavras, self.usadas_memoria)

        quantidade = min(3 + nivel, len(palavras))
        selecionadas = random.sample(palavras, quantidade)

        self.usadas_memoria.update(selecionadas)

        return {
            "categoria": categoria,
            "palavras": selecionadas
        }