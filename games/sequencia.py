import json
import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo

GAME_NAME = "Sequencia"

class JogoSequencia(JogoBase):

    nome = "Sequência"

    def __init__(self, jogador):
        self.jogador = jogador

        with open("data/sequencias.json", encoding="utf-8") as f:
            self.lista = json.load(f)

        if "sequencia" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        """Reinicia o estado do jogo."""
        st.session_state.sequencia = {
            "item_atual": None
        }

    def gerar_desafio(self):
        """Escolhe um item aleatório da lista de sequências."""
        item = random.choice(self.lista)
        st.session_state.sequencia["item_atual"] = item
        return item

    def verificar_resposta(self, resposta):
        """Verifica se a resposta do jogador está correta."""
        item = st.session_state.sequencia.get("item_atual")
        if not item:
            return ResultadoJogo(False, "Nenhuma sequência selecionada!", 0, False)

        try:
            resposta_num = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um número válido!", 0, False)

        if resposta_num == item["resposta"]:
            pontos = item["pontos"]
            self.jogador.ganhar_pontos(pontos)
            return ResultadoJogo(True, f"Correto! {item['explicacao']}", pontos, True)

        return ResultadoJogo(False, f"Errado! {item['explicacao']}", 0, False)


Game = JogoSequencia