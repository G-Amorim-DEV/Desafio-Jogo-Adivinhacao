import json
import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo

GAME_NAME = "Quiz"


class JogoQuiz(JogoBase):
    nome = "Quiz"

    def __init__(self, jogador):
        self.jogador = jogador
        with open("data/quiz.json", encoding="utf-8") as arquivo:
            self.perguntas = json.load(arquivo)

        if "quiz" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.quiz = {"pergunta_atual": None, "acertos_seguidos": 0}

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Quiz",
            emoji="❓",
            descricao="Responda perguntas de conhecimento geral com opcoes objetivas.",
            instrucoes=[
                "Escolha uma alternativa.",
                "Perguntas corretas rendem pontos pela dificuldade.",
                "Respostas erradas custam vida e reduzem XP.",
            ],
            max_dicas=2,
            custo_dica_xp=2,
        )

    def configurar_input(self) -> InputConfig:
        pergunta = st.session_state.quiz.get("pergunta_atual")
        if pergunta and pergunta.get("opcoes"):
            return InputConfig(
                tipo="radio",
                label="Escolha uma alternativa",
                opcoes=pergunta["opcoes"],
            )
        return InputConfig(tipo="text", label="Sua resposta", placeholder="Digite sua resposta")

    def escolher_dificuldade(self):
        return self.jogador.dificuldade()

    def gerar_desafio(self):
        if st.session_state.quiz.get("pergunta_atual") is not None:
            return st.session_state.quiz["pergunta_atual"]

        dificuldade = self.escolher_dificuldade()
        filtradas = [pergunta for pergunta in self.perguntas if pergunta["dificuldade"] == dificuldade]
        self.pergunta = random.choice(filtradas)
        st.session_state.quiz["pergunta_atual"] = self.pergunta
        return self.pergunta

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🧠 **Conhecimento:** Teste seu repertorio.")
        with col2:
            st.markdown("🎯 **Precisao:** Escolha a melhor resposta.")
        with col3:
            st.markdown("⏱️ **Ritmo:** Pense e responda.")

    def obter_contexto_resposta(self, desafio):
        return desafio.get("pergunta", "")

    def verificar_resposta(self, resposta):
        pergunta = st.session_state.quiz.get("pergunta_atual")
        if not pergunta:
            return ResultadoJogo(False, "Nenhuma pergunta selecionada.", 0, False)

        estado = st.session_state.quiz
        resposta_limpa = resposta.strip().lower()
        correta = pergunta["resposta"].strip().lower()

        if resposta_limpa == correta:
            pontos = pergunta["pontos"]
            self.jogador.adicionar_xp(pontos)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            st.session_state.quiz["pergunta_atual"] = None
            return ResultadoJogo(True, f"Correto. +{pontos} pontos.", pontos, False)

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(
                False,
                f"Errado. Resposta correta: {pergunta['resposta']}. Voce perdeu todas as vidas.",
                0,
                True,
            )

        self.jogador.perder_pontos(2)
        return ResultadoJogo(
            False,
            f"Resposta incorreta. Tente novamente. Vidas restantes: {vidas_restantes}",
            0,
            False,
        )

    def obter_dica(self) -> str:
        pergunta = st.session_state.quiz.get("pergunta_atual")
        if pergunta and "dica" in pergunta:
            return pergunta["dica"]
        return "Pense na resposta baseada em conhecimento geral."


Game = JogoQuiz
