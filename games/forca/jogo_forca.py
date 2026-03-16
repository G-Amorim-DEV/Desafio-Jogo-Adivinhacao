import json
import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo
from utils.paths import data_path
from games.forca.render_forca import desenhar_forca

GAME_NAME = "Forca"

class JogoForca(JogoBase):

    nome = "Forca"

    def __init__(self, jogador):
        self.jogador = jogador

        if "forca" not in st.session_state:
            with open(data_path("palavras_forca.json"), encoding="utf-8") as f:
                palavras = json.load(f)

            palavra = random.choice(palavras)["palavra"].upper()

            st.session_state.forca = {
                "palavra": palavra,
                "letras": [],
                "tentativas": 6
            }

    # -------------------------
    # GERAR DESAFIO
    # -------------------------
    def gerar_desafio(self):
        estado = st.session_state.forca
        progresso = " ".join(
            l if l in estado["letras"] else "_"
            for l in estado["palavra"]
        )
        return {"progresso": progresso}

    # -------------------------
    # VERIFICAR RESPOSTA
    # -------------------------
    def verificar_resposta(self, letra):
        estado = st.session_state.forca
        letra = letra.upper()

        if letra in estado["palavra"]:
            estado["letras"].append(letra)
            venceu = all(l in estado["letras"] for l in estado["palavra"])
            if venceu and self.jogador:
                self.jogador.ganhar_pontos(10)
            return ResultadoJogo(True, "Letra correta!", 10, venceu)

        estado["tentativas"] -= 1
        perdeu = estado["tentativas"] <= 0
        return ResultadoJogo(False, "Letra errada!", 0, perdeu)

    # -------------------------
    # RENDERIZAR
    # -------------------------
    def renderizar(self, desafio):
        estado = st.session_state.forca
        erros = 6 - estado["tentativas"]
        desenhar_forca(erros)
        st.subheader(desafio["progresso"])
        st.write(f"Tentativas restantes: {estado['tentativas']}")

    # -------------------------
    # OBTER DICA (novo método obrigatório)
    # -------------------------
    def obter_dica(self):
        """Retorna uma dica simples: primeira letra da palavra"""
        estado = st.session_state.forca
        return f"A primeira letra é '{estado['palavra'][0]}'"

# Exporta apenas a classe, não a instância
Game = JogoForca