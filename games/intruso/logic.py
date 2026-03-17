import json
import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo

GAME_NAME = "Palavra Intrusa"


class JogoIntruso(JogoBase):
    nome = "Palavra Intrusa"

    def __init__(self, jogador):
        self.jogador = jogador
        with open("data/intrusos.json", encoding="utf-8") as arquivo:
            self.desafios = json.load(arquivo)

        if "intruso" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.intruso = {"item_atual": None, "acertos_seguidos": 0}

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Palavra Intrusa",
            emoji="🚪",
            descricao="Descubra qual palavra nao pertence ao mesmo grupo das outras.",
            instrucoes=[
                "Observe as quatro opcoes.",
                "Identifique qual item foge ao padrao do grupo.",
                "Use a dica quando precisar revisar a categoria comum.",
            ],
            max_dicas=2,
            custo_dica_xp=2,
        )

    def configurar_input(self) -> InputConfig:
        item = st.session_state.intruso.get("item_atual")
        return InputConfig(
            tipo="radio",
            label="Qual e a palavra intrusa?",
            opcoes=item["opcoes"] if item else [],
        )

    def gerar_desafio(self):
        if st.session_state.intruso.get("item_atual"):
            return st.session_state.intruso["item_atual"]

        dificuldade = self.jogador.dificuldade()
        candidatos = [item for item in self.desafios if item["dificuldade"] == dificuldade]
        item = random.choice(candidatos or self.desafios)
        st.session_state.intruso["item_atual"] = item
        return item

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")

    def obter_contexto_resposta(self, desafio):
        return (
            "Tres palavras pertencem ao mesmo grupo. Uma delas nao pertence.\n"
            + " | ".join(desafio["opcoes"])
        )

    def verificar_resposta(self, resposta):
        item = st.session_state.intruso.get("item_atual")
        if not item:
            return ResultadoJogo(False, "Nenhum desafio carregado.", 0, False)

        estado = st.session_state.intruso
        if resposta.strip().lower() == item["resposta"].strip().lower():
            pontos = item["pontos"]
            self.jogador.adicionar_xp(pontos)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            st.session_state.intruso["item_atual"] = None
            return ResultadoJogo(True, "Voce encontrou a palavra intrusa.", pontos, False)

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(
                False,
                f"Resposta incorreta. A palavra intrusa era {item['resposta']}. Voce perdeu todas as vidas.",
                0,
                True,
            )

        return ResultadoJogo(
            False,
            f"Resposta incorreta. A palavra intrusa era {item['resposta']}. Vidas restantes: {vidas_restantes}",
            0,
            False,
        )

    def obter_dica(self) -> str:
        item = st.session_state.intruso.get("item_atual")
        if item:
            return item.get("dica", "Pense no que tres opcoes tem em comum.")
        return "Observe qual opcao destoa da categoria principal."


Game = JogoIntruso
