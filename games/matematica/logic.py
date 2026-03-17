import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo

GAME_NAME = "Matemática"


class JogoMatematica(JogoBase):
    nome = "Matemática"

    def __init__(self, jogador):
        self.jogador = jogador
        self.resposta = None
        self.desafio_texto = None
        if "matematica" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.matematica = {"acertos_seguidos": 0}

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Matematica",
            emoji="🧮",
            descricao="Resolva contas rapidamente e acumule XP.",
            instrucoes=[
                "Resolva a operacao exibida.",
                "Erros removem uma vida.",
                "A cada 5 acertos seguidos voce recupera uma vida.",
            ],
        )

    def configurar_input(self) -> InputConfig:
        return InputConfig(
            tipo="number",
            label="Resultado",
            placeholder="Digite o resultado",
        )

    def gerar_desafio(self):
        dificuldade = self.jogador.dificuldade()
        limites = {"facil": 20, "medio": 50, "dificil": 100}
        operacoes = {
            "facil": ["+", "-"],
            "medio": ["+", "-", "*"],
            "dificil": ["+", "-", "*"],
        }
        limite = limites[dificuldade]
        a = random.randint(1, limite)
        b = random.randint(1, limite)
        op = random.choice(operacoes[dificuldade])

        if op == "+":
            self.resposta = a + b
        elif op == "-":
            self.resposta = a - b
        else:
            self.resposta = a * b

        self.desafio_texto = f"{a} {op} {b}"
        return self.desafio_texto

    def verificar_resposta(self, resposta):
        try:
            resposta = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um numero valido.", 0, False)

        estado = st.session_state.matematica

        if resposta == self.resposta:
            self.jogador.adicionar_xp(5)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            return ResultadoJogo(
                True,
                f"Correto. {self.desafio_texto} = {self.resposta}",
                5,
                False,
            )

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(
                False,
                f"Errado. {self.desafio_texto} = {self.resposta}. Voce perdeu todas as vidas.",
                0,
                True,
            )

        diferenca = abs(resposta - self.resposta)
        if diferenca <= 2:
            dica = "Muito proximo. Ajuste por poucos numeros."
        elif diferenca <= 10:
            dica = "Proximo. Revise o calculo."
        else:
            dica = "Um pouco longe. Refaça a operacao."

        return ResultadoJogo(
            False,
            f"Errado. {dica} ({self.desafio_texto} = {self.resposta}). Vidas restantes: {vidas_restantes}",
            0,
            False,
        )

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        st.write(desafio)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🧮 **Calculo mental:** Resolva a operacao.")
        with col2:
            st.markdown("🔢 **Operacoes:** +, -, ×")
        with col3:
            st.markdown("🎯 **Precisao:** Digite apenas o resultado.")

    def obter_dica(self):
        operador = self.desafio_texto.split()[1] if self.desafio_texto else "?"
        return f"O operador da operacao e '{operador}'."


Game = JogoMatematica
