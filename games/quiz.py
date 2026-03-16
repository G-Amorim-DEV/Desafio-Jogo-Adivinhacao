import json
import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo

GAME_NAME = "Quiz"

class JogoQuiz(JogoBase):

    nome = "Quiz"

    def __init__(self, jogador):
        self.jogador = jogador

        # Carrega perguntas uma vez
        with open("data/quiz.json", encoding="utf-8") as f:
            self.perguntas = json.load(f)

        if "quiz" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        """Reinicia o estado do jogo."""
        st.session_state.quiz = {
            "pergunta_atual": None
        }

    def escolher_dificuldade(self):
        """Define a dificuldade baseada no nível do jogador."""
        if self.jogador.nivel <= 2:
            return "facil"
        elif self.jogador.nivel <= 4:
            return "medio"
        return "dificil"

    def gerar_desafio(self):
        """Escolhe uma pergunta aleatória da dificuldade correspondente."""
        dificuldade = self.escolher_dificuldade()
        filtradas = [p for p in self.perguntas if p["dificuldade"] == dificuldade]

        self.pergunta = random.choice(filtradas)
        st.session_state.quiz["pergunta_atual"] = self.pergunta

        return self.pergunta

    def verificar_resposta(self, resposta):
        """Verifica a resposta e retorna ResultadoJogo com pontos e mensagem."""
        pergunta = st.session_state.quiz.get("pergunta_atual")
        if not pergunta:
            return ResultadoJogo(False, "Nenhuma pergunta selecionada!", 0, False)

        resposta_limpa = resposta.strip().lower()
        correta = pergunta["resposta"].strip().lower()

        if resposta_limpa == correta:
            pontos = pergunta["pontos"]
            self.jogador.ganhar_pontos(pontos)
            return ResultadoJogo(True, f"Correto! +{pontos} pontos", pontos, True)

        self.jogador.perder_pontos(2)
        return ResultadoJogo(False, f"Errado! Resposta correta: {pergunta['resposta']}", 0, True)


Game = JogoQuiz