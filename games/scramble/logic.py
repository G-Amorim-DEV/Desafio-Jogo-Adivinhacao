import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo
from services.loaders.json_loader import carregar_json

GAME_NAME = "Scramble"


class JogoScramble(JogoBase):
    nome = "Palavra Embaralhada"

    def __init__(self, jogador):
        self.jogador = jogador
        if "scramble" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.scramble = {
            "original": "",
            "embaralhada": "",
            "acertos_seguidos": 0,
        }

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Scramble",
            emoji="🔀",
            descricao="Reorganize letras embaralhadas para formar a palavra correta.",
            instrucoes=[
                "Observe as letras embaralhadas.",
                "Digite a palavra correta.",
                "Erros custam uma vida.",
            ],
        )

    def configurar_input(self) -> InputConfig:
        return InputConfig(
            tipo="text",
            label="Palavra correta",
            placeholder="Digite a palavra formada",
        )

    def gerar_desafio(self):
        if st.session_state.scramble.get("original"):
            return st.session_state.scramble["embaralhada"]

        dados = carregar_json("data/palavras_forca.json")
        dificuldade = self.jogador.dificuldade()
        candidatos = [item for item in dados if item.get("dificuldade") == dificuldade]
        palavra_obj = random.choice(candidatos or dados)
        original = palavra_obj["palavra"].strip()
        letras = list(original)
        random.shuffle(letras)
        embaralhada = "".join(letras)

        st.session_state.scramble.update({"original": original, "embaralhada": embaralhada})
        return embaralhada

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🔀 **Embaralhado:** As letras estao misturadas.")
        with col2:
            st.markdown("📝 **Reordene:** Forme uma palavra valida.")
        with col3:
            st.markdown("🎯 **Observacao:** Teste possibilidades.")

    def obter_contexto_resposta(self, desafio):
        return f"Reordene as letras para formar uma palavra: {desafio}"

    def verificar_resposta(self, resposta):
        estado = st.session_state.scramble
        if not estado["original"]:
            return ResultadoJogo(False, "Nenhuma palavra selecionada.", 0, False)

        if resposta.strip().lower() == estado["original"].lower():
            palavra_original = estado["original"]
            self.jogador.adicionar_xp(10)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            st.session_state.scramble["original"] = ""
            st.session_state.scramble["embaralhada"] = ""
            return ResultadoJogo(True, f"Acertou. A palavra era {palavra_original}.", 10, False)

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(
                False,
                f"Errou. A palavra era {estado['original']}. Voce perdeu todas as vidas.",
                0,
                True,
            )

        resposta_lower = resposta.strip().lower()
        original_lower = estado["original"].lower()

        if len(resposta_lower) == len(original_lower):
            corretas_posicao = sum(
                1
                for indice, letra in enumerate(resposta_lower)
                if indice < len(original_lower) and letra == original_lower[indice]
            )
            letras_corretas = sum(1 for letra in resposta_lower if letra in original_lower)
            return ResultadoJogo(
                False,
                f"Quase. {corretas_posicao} letras na posicao certa, {letras_corretas} letras corretas no total. Vidas restantes: {vidas_restantes}",
                0,
                False,
            )

        return ResultadoJogo(
            False,
            f"Palavra com tamanho errado. A palavra tem {len(estado['original'])} letras. Vidas restantes: {vidas_restantes}",
            0,
            False,
        )

    def obter_dica(self) -> str:
        estado = st.session_state.scramble
        if estado["original"]:
            return f"A palavra tem {len(estado['original'])} letras."
        return "Tente reorganizar as letras para formar uma palavra."


Game = JogoScramble
