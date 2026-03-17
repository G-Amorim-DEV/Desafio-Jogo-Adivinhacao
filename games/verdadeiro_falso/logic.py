import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo
from services.loaders.json_loader import carregar_json

GAME_NAME = "Verdadeiro ou Falso"


class JogoVF(JogoBase):
    nome = "Verdadeiro ou Falso"

    def __init__(self, jogador):
        self.jogador = jogador
        if "verdadeiro_falso" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.verdadeiro_falso = {"acertos_seguidos": 0}

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Verdadeiro ou Falso",
            emoji="✅",
            descricao="Julgue se cada afirmacao esta correta ou incorreta.",
            instrucoes=[
                "Leia a afirmacao com atencao.",
                "Escolha verdadeiro ou falso.",
                "Erros reduzem suas vidas.",
            ],
        )

    def configurar_input(self) -> InputConfig:
        return InputConfig(
            tipo="segmented",
            label="Sua escolha",
            opcoes=["verdadeiro", "falso"],
        )

    def gerar_desafio(self):
        dados = carregar_json("data/vf.json")
        dificuldade = self.jogador.dificuldade()
        candidatos = [item for item in dados if item.get("dificuldade") == dificuldade]
        self.afirmacao = random.choice(candidatos or dados)
        return self.afirmacao["texto"]

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("✅ **Verdadeiro:** Se a afirmacao estiver correta.")
        with col2:
            st.markdown("❌ **Falso:** Se a afirmacao estiver incorreta.")
        with col3:
            st.markdown("🧠 **Julgamento:** Use seu conhecimento.")

    def obter_contexto_resposta(self, desafio):
        return f"{desafio}\nVerdadeiro ou falso?"

    def verificar_resposta(self, resposta):
        estado = st.session_state.verdadeiro_falso
        if resposta.lower() == self.afirmacao["resposta"]:
            self.jogador.adicionar_xp(5)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            return ResultadoJogo(True, "Certo.", 5, False)

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(False, "Errado. Voce perdeu todas as vidas.", 0, True)

        return ResultadoJogo(False, f"Errado. Vidas restantes: {vidas_restantes}", 0, False)

    def obter_dica(self) -> str:
        return "Pense se a afirmacao e verdadeira ou falsa com base em conhecimento geral."


Game = JogoVF
