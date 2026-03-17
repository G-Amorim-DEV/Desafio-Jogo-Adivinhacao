import json
import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo
from services.loaders.json_loader import carregar_json

GAME_NAME = "Analogias"


class JogoAnalogias(JogoBase):
    nome = "Analogias"

    def __init__(self, jogador):
        self.jogador = jogador
        self.desafios = carregar_json("data/analogias.json") or []
        if not self.desafios:
            raise ValueError("Nenhum desafio de analogias foi encontrado.")

        if "analogias" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.analogias = {"item_atual": None, "acertos_seguidos": 0}

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Analogias",
            emoji="🧩",
            descricao="Complete relacoes logicas entre palavras, objetos ou ideias.",
            instrucoes=[
                "Leia a relacao apresentada.",
                "Escolha a alternativa que completa melhor a analogia.",
                "A dificuldade pode seguir seu nivel ou o modo manual.",
            ],
            max_dicas=2,
            custo_dica_xp=2,
        )

    def configurar_input(self) -> InputConfig:
        item = st.session_state.analogias.get("item_atual")
        return InputConfig(
            tipo="radio",
            label="Escolha a melhor resposta",
            opcoes=item["opcoes"] if item else [],
        )

    def gerar_desafio(self):
        if st.session_state.analogias.get("item_atual"):
            return st.session_state.analogias["item_atual"]

        dificuldade = self.jogador.dificuldade()
        candidatos = [item for item in self.desafios if item["dificuldade"] == dificuldade]
        item = random.choice(candidatos or self.desafios)
        st.session_state.analogias["item_atual"] = item
        return item

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🧠 **Relacao:** Procure o padrao.")
        with col2:
            st.markdown("🔎 **Contexto:** Compare funcao, forma ou significado.")
        with col3:
            st.markdown("✅ **Resposta:** Escolha a melhor analogia.")

    def obter_contexto_resposta(self, desafio):
        return desafio.get("pergunta", "")

    def verificar_resposta(self, resposta):
        item = st.session_state.analogias.get("item_atual")
        if not item:
            return ResultadoJogo(False, "Nenhum desafio carregado.", 0, False)

        estado = st.session_state.analogias
        if resposta.strip().lower() == item["resposta"].strip().lower():
            pontos = item["pontos"]
            self.jogador.adicionar_xp(pontos)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            st.session_state.analogias["item_atual"] = None
            return ResultadoJogo(True, "Analogia correta.", pontos, False)

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(
                False,
                f"Resposta incorreta. A opcao certa era {item['resposta']}. Voce perdeu todas as vidas.",
                0,
                True,
            )

        return ResultadoJogo(
            False,
            f"Resposta incorreta. Analise a relacao com calma e tente novamente. Vidas restantes: {vidas_restantes}",
            0,
            False,
        )

    def obter_dica(self) -> str:
        item = st.session_state.analogias.get("item_atual")
        if item:
            return item.get("dica", "Pense na relacao principal entre os termos.")
        return "Busque uma relacao de significado, funcao ou sequencia."


Game = JogoAnalogias
