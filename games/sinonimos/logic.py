import json
import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo

GAME_NAME = "Sinônimos"


class JogoSinonimos(JogoBase):
    nome = "Sinônimos"

    def __init__(self, jogador):
        self.jogador = jogador
        with open("data/sinonimos.json", encoding="utf-8") as arquivo:
            self.desafios = json.load(arquivo)
        if "sinonimos" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.sinonimos = {"item_atual": None, "acertos_seguidos": 0}

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Sinonimos",
            emoji="📘",
            descricao="Escolha a palavra com significado semelhante ao termo apresentado.",
            instrucoes=[
                "Leia o termo principal.",
                "Escolha o sinonimo entre as alternativas.",
                "A dica ajuda com o campo de significado.",
            ],
            max_dicas=2,
            custo_dica_xp=2,
        )

    def configurar_input(self) -> InputConfig:
        item = st.session_state.sinonimos.get("item_atual")
        return InputConfig(
            tipo="radio",
            label="Qual palavra e sinonimo?",
            opcoes=item["opcoes"] if item else [],
        )

    def gerar_desafio(self):
        if st.session_state.sinonimos.get("item_atual"):
            return st.session_state.sinonimos["item_atual"]
        dificuldade = self.jogador.dificuldade()
        candidatos = [item for item in self.desafios if item["dificuldade"] == dificuldade]
        item = random.choice(candidatos or self.desafios)
        st.session_state.sinonimos["item_atual"] = item
        return item

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        st.write(f"Selecione o sinonimo de **{desafio['termo']}**")

    def verificar_resposta(self, resposta):
        item = st.session_state.sinonimos.get("item_atual")
        if not item:
            return ResultadoJogo(False, "Nenhum desafio carregado.", 0, False)
        estado = st.session_state.sinonimos
        if resposta.strip().lower() == item["resposta"].strip().lower():
            pontos = item["pontos"]
            self.jogador.adicionar_xp(pontos)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            st.session_state.sinonimos["item_atual"] = None
            return ResultadoJogo(True, "Sinonimo correto.", pontos, False)

        vidas = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas <= 0:
            return ResultadoJogo(False, f"Errado. A resposta correta era {item['resposta']}. Voce perdeu todas as vidas.", 0, True)
        return ResultadoJogo(False, f"Resposta incorreta. Pense em um significado equivalente e tente novamente. Vidas restantes: {vidas}", 0, False)

    def obter_dica(self) -> str:
        item = st.session_state.sinonimos.get("item_atual")
        return item.get("dica", "Pense em uma palavra de significado parecido.") if item else "Busque uma palavra equivalente."


Game = JogoSinonimos
