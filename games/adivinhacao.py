import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo

GAME_NAME = "Adivinhação"

class JogoAdivinhacao(JogoBase):

    nome = "Adivinhe o Número"

    def __init__(self):
        if "adivinhacao" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.adivinhacao = {
            "numero": random.randint(1, 100),
            "tentativas": 10,
            "acertou": False
        }

    def gerar_desafio(self):
        return "Adivinhe um número entre 1 e 100"

    def renderizar(self, desafio):
        estado = st.session_state.adivinhacao

        st.subheader(self.nome)
        st.write(desafio)

        st.info(f"Tentativas restantes: {estado['tentativas']}")

    def verificar_resposta(self, resposta):

        estado = st.session_state.adivinhacao

        try:
            resposta = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um número válido!", 0, False)

        estado["tentativas"] -= 1

        if resposta == estado["numero"]:
            estado["acertou"] = True
            return ResultadoJogo(True, f"Parabéns! Você acertou o número {estado['numero']}", 10, True)

        if estado["tentativas"] <= 0:
            return ResultadoJogo(False, f"Fim das tentativas! O número era {estado['numero']}", 0, True)

        dica = "Maior" if resposta < estado["numero"] else "Menor"

        return ResultadoJogo(False, f"{dica}! Tentativas restantes: {estado['tentativas']}", 0, False)
    
Game = JogoAdivinhacao