import json
import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo
from games.forca.render import desenhar_forca
from utils.paths import data_path

GAME_NAME = "Forca"


class JogoForca(JogoBase):
    nome = "Forca"

    def __init__(self, jogador):
        self.jogador = jogador
        if "forca" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        with open(data_path("palavras_forca.json"), encoding="utf-8") as arquivo:
            palavras = json.load(arquivo)

        dificuldade = self.jogador.dificuldade()
        candidatos = [item for item in palavras if item.get("dificuldade") == dificuldade]
        palavra = random.choice(candidatos or palavras)["palavra"].upper()
        configuracao = {
            "facil": {"tentativas": 8, "reveladas": 1},
            "medio": {"tentativas": 6, "reveladas": 0},
            "dificil": {"tentativas": 5, "reveladas": 0},
        }[dificuldade]
        letras_iniciais = []
        if configuracao["reveladas"] > 0:
            letras_iniciais = [palavra[0]]
        st.session_state.forca = {
            "palavra": palavra,
            "letras": letras_iniciais,
            "tentativas": configuracao["tentativas"],
            "tentativas_iniciais": configuracao["tentativas"],
            "dificuldade": dificuldade,
        }

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Forca",
            emoji="🪢",
            descricao="Descubra a palavra secreta antes que as tentativas acabem.",
            instrucoes=[
                "No facil voce comeca com mais tentativas e uma letra revelada.",
                "No medio a partida segue o ritmo padrao da forca.",
                "No dificil voce tem menos tentativas e precisa errar menos.",
            ],
            max_dicas=3,
            custo_dica_xp=1,
        )

    def configurar_input(self) -> InputConfig:
        return InputConfig(
            tipo="text",
            label="Ou digite uma letra",
            placeholder="A",
            max_chars=1,
        )

    def gerar_desafio(self):
        estado = st.session_state.forca
        progresso = " ".join(letra if letra in estado["letras"] else "_" for letra in estado["palavra"])
        return {"progresso": progresso}

    def renderizar(self, desafio):
        estado = st.session_state.forca
        col1, col2 = st.columns([1, 2])

        with col1:
            erros = max(0, estado.get("tentativas_iniciais", estado["tentativas"]) - estado["tentativas"])
            desenhar_forca(erros)
            st.write(f"**Tentativas restantes:** {estado['tentativas']}")
            st.write(f"**Modo:** {estado.get('dificuldade', 'medio').title()}")
            if estado["letras"]:
                st.write(f"**Letras usadas:** {' '.join(sorted(estado['letras']))}")

        with col2:
            st.markdown(
                f"<h2 style='text-align: center; font-family: monospace;'>{desafio['progresso']}</h2>",
                unsafe_allow_html=True,
            )
            st.write("**Clique em uma letra:**")
            letras_disponiveis = [
                chr(i) for i in range(ord("A"), ord("Z") + 1) if chr(i) not in estado["letras"]
            ]

            if letras_disponiveis:
                cols = st.columns(6)
                for indice, letra in enumerate(letras_disponiveis):
                    with cols[indice % 6]:
                        if st.button(letra, key=f"letra_{letra}"):
                            st.session_state.temp_letra = letra
                            st.rerun()
            else:
                st.write("Todas as letras foram usadas.")

    def verificar_resposta(self, letra):
        estado = st.session_state.forca
        letra = letra.strip().upper()

        if estado["tentativas"] <= 0:
            return ResultadoJogo(
                False,
                f"Suas tentativas acabaram. A palavra correta era: {estado['palavra']}.",
                0,
                True,
            )

        if not letra.isalpha() or len(letra) != 1:
            return ResultadoJogo(False, "Digite apenas uma letra valida.", 0, False)

        if letra in estado["letras"]:
            return ResultadoJogo(False, f"A letra {letra} ja foi usada. Tente outra.", 0, False)

        if letra not in estado["letras"]:
            estado["letras"].append(letra)

        if letra in estado["palavra"]:
            venceu = all(char in estado["letras"] for char in estado["palavra"])
            if venceu:
                pontos = 10 + estado["tentativas"]
                if self.jogador:
                    self.jogador.adicionar_xp(pontos)
                return ResultadoJogo(
                    True,
                    f"Parabens. Voce acertou a palavra: {estado['palavra']}.",
                    pontos,
                    True,
                )
            return ResultadoJogo(True, "Letra correta.", 0, False)

        estado["tentativas"] -= 1
        if estado["tentativas"] <= 0:
            return ResultadoJogo(
                False,
                f"Suas tentativas acabaram. A palavra correta era: {estado['palavra']}.",
                0,
                True,
            )

        return ResultadoJogo(
            False,
            f"Letra errada. Tentativas restantes: {estado['tentativas']}",
            0,
            False,
        )

    def obter_dica(self):
        estado = st.session_state.forca
        if estado.get("dificuldade") == "facil":
            return f"A palavra tem {len(estado['palavra'])} letras e comeca com {estado['palavra'][0]}."
        return f"A palavra tem {len(estado['palavra'])} letras. Tente vogais primeiro."


Game = JogoForca
