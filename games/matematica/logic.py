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
        if "matematica" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.matematica = {
            "acertos_seguidos": 0,
            "resposta": None,
            "desafio_texto": None,
        }

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
        estado = st.session_state.matematica
        if estado.get("desafio_texto") is not None and estado.get("resposta") is not None:
            return estado["desafio_texto"]

        dificuldade = self.jogador.dificuldade()
        limites = {"facil": 20, "medio": 50, "dificil": 120}
        operacoes = {
            "facil": ["+", "-"],
            "medio": ["+", "-", "*"],
            "dificil": ["+", "-", "*", "/"],
        }
        limite = limites[dificuldade]
        a = random.randint(1, limite)
        b = random.randint(1, limite)
        op = random.choice(operacoes[dificuldade])
        pontos = {"facil": 5, "medio": 8, "dificil": 12}[dificuldade]

        if op == "/":
            b = random.randint(2, 12)
            resposta_correta = random.randint(2, 12)
            a = b * resposta_correta
        elif op == "+":
            resposta_correta = a + b
        elif op == "-":
            resposta_correta = a - b
        else:
            resposta_correta = a * b

        desafio_texto = f"{a} {op} {b}"
        estado["pontos"] = pontos
        estado["dificuldade"] = dificuldade
        estado["resposta"] = resposta_correta
        estado["desafio_texto"] = desafio_texto
        return desafio_texto

    def verificar_resposta(self, resposta):
        try:
            resposta = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um numero valido.", 0, False)

        estado = st.session_state.matematica
        resposta_correta = estado.get("resposta")
        desafio_texto = estado.get("desafio_texto")

        if resposta_correta is None or not desafio_texto:
            return ResultadoJogo(False, "Nenhum desafio matematico ativo.", 0, False)

        if resposta == resposta_correta:
            pontos = st.session_state.matematica.get("pontos", 5)
            self.jogador.adicionar_xp(pontos)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            estado["resposta"] = None
            estado["desafio_texto"] = None
            return ResultadoJogo(
                True,
                f"Correto. {desafio_texto} = {resposta_correta}",
                pontos,
                False,
            )

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            estado["resposta"] = None
            estado["desafio_texto"] = None
            return ResultadoJogo(
                False,
                f"Errado. {desafio_texto} = {resposta_correta}. Voce perdeu todas as vidas.",
                0,
                True,
            )

        diferenca = abs(resposta - resposta_correta)
        if diferenca <= 2:
            dica = "Muito proximo. Ajuste por poucos numeros."
        elif diferenca <= 10:
            dica = "Proximo. Revise o calculo."
        else:
            dica = "Um pouco longe. Refaça a operacao."

        return ResultadoJogo(
            False,
            f"Errado. {dica} ({desafio_texto} = {resposta_correta}). Vidas restantes: {vidas_restantes}",
            0,
            False,
        )

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🧮 **Calculo mental:** Resolva a operacao.")
        with col2:
            modo = st.session_state.matematica.get("dificuldade", "medio").title()
            st.markdown(f"🔢 **Modo:** {modo}")
        with col3:
            st.markdown("🎯 **Precisao:** Digite apenas o resultado.")

    def obter_contexto_resposta(self, desafio):
        return desafio

    def obter_dica(self):
        desafio_texto = st.session_state.matematica.get("desafio_texto")
        operador = desafio_texto.split()[1] if desafio_texto else "?"
        return f"O operador da operacao e '{operador}'."


Game = JogoMatematica
