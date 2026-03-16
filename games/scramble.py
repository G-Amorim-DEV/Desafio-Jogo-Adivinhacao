import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo
from services.data_loader import carregar_json

GAME_NAME = "Scramble"

class JogoScramble(JogoBase):

    nome = "Palavra Embaralhada"

    def __init__(self, jogador):
        self.jogador = jogador

        if "scramble" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        """Reinicia o estado do jogo."""
        st.session_state.scramble = {
            "original": "",
            "embaralhada": ""
        }

    def gerar_desafio(self):
        """Escolhe uma palavra aleatória e embaralha suas letras."""
        palavras = carregar_json("data/palavras.json")
        original = random.choice(palavras).strip()
        letras = list(original)
        random.shuffle(letras)
        embaralhada = "".join(letras)

        st.session_state.scramble.update({
            "original": original,
            "embaralhada": embaralhada
        })

        return embaralhada

    def verificar_resposta(self, resposta):
        """Verifica se a resposta está correta."""
        estado = st.session_state.scramble
        if not estado["original"]:
            return ResultadoJogo(False, "Nenhuma palavra selecionada!", 0, False)

        if resposta.strip().lower() == estado["original"].lower():
            self.jogador.adicionar_pontos(10)
            return ResultadoJogo(True, f"Acertou! A palavra era {estado['original']}", 10, True)

        return ResultadoJogo(False, "Tente novamente", 0, False)


Game = JogoScramble