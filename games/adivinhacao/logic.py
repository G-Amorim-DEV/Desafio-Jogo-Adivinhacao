import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo

GAME_NAME = "Adivinhação"


class JogoAdivinhacao(JogoBase):
    nome = "Adivinhe o Número"

    def __init__(self, jogador):
        self.jogador = jogador
        if "adivinhacao" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        dificuldade = self.jogador.dificuldade() if self.jogador else "medio"
        configuracao = {
            "facil": {"intervalo": (1, 50), "tentativas": 10},
            "medio": {"intervalo": (1, 100), "tentativas": 8},
            "dificil": {"intervalo": (1, 200), "tentativas": 7},
        }[dificuldade]
        st.session_state.adivinhacao = {
            "numero": random.randint(*configuracao["intervalo"]),
            "tentativas": configuracao["tentativas"],
            "acertou": False,
            "intervalo": configuracao["intervalo"],
        }

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Adivinhe o Numero",
            emoji="🎲",
            descricao="Descubra o numero secreto com dicas de maior ou menor.",
            instrucoes=[
                "Digite um numero entre 1 e 100.",
                "Cada erro consome uma tentativa.",
                "Use as dicas para se aproximar do numero secreto.",
            ],
            max_dicas=2,
            custo_dica_xp=1,
        )

    def configurar_input(self) -> InputConfig:
        intervalo = st.session_state.adivinhacao.get("intervalo", (1, 100))
        return InputConfig(
            tipo="number",
            label="Seu palpite",
            placeholder="Ex.: 42",
            min_value=intervalo[0],
            max_value=intervalo[1],
        )

    def gerar_desafio(self):
        inicio, fim = st.session_state.adivinhacao.get("intervalo", (1, 100))
        return f"Adivinhe um numero entre {inicio} e {fim}"

    def renderizar(self, desafio):
        estado = st.session_state.adivinhacao
        st.markdown(
            """
        <div style="padding: 1rem 0 0.5rem 0;">
            <h2>🎲 Adivinhe o Numero</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.write(desafio)
        st.info(f"Tentativas restantes: {estado['tentativas']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🎯 **Objetivo:** Acertar o numero secreto.")
        with col2:
            st.markdown(f"🔢 **Faixa:** {estado['intervalo'][0]} a {estado['intervalo'][1]}")
        with col3:
            st.markdown("💡 **Dica:** Use as tentativas com cuidado.")

    def verificar_resposta(self, resposta):
        estado = st.session_state.adivinhacao

        if estado["tentativas"] <= 0:
            return ResultadoJogo(
                False,
                f"Suas tentativas acabaram. O numero correto era {estado['numero']}.",
                0,
                True,
            )

        try:
            resposta = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um numero valido.", 0, False)

        estado["tentativas"] -= 1

        if resposta == estado["numero"]:
            estado["acertou"] = True
            if self.jogador:
                self.jogador.adicionar_xp(10)
            return ResultadoJogo(
                True,
                f"Parabens. Voce acertou o numero {estado['numero']}.",
                10,
                True,
            )

        if estado["tentativas"] <= 0:
            return ResultadoJogo(
                False,
                f"Suas tentativas acabaram. O numero correto era {estado['numero']}.",
                0,
                True,
            )

        dica = "Maior" if resposta < estado["numero"] else "Menor"
        return ResultadoJogo(
            False,
            f"{dica}. Tentativas restantes: {estado['tentativas']}",
            0,
            False,
        )

    def obter_dica(self) -> str:
        numero = st.session_state.adivinhacao["numero"]
        if numero <= 10:
            return "O numero e menor ou igual a 10."
        if numero <= 50:
            return "O numero esta entre 11 e 50."
        return "O numero e maior que 50."


Game = JogoAdivinhacao
