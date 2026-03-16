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
        if self.jogador.nivel() <= 2:
            return "facil"
        elif self.jogador.nivel() <= 4:
            return "medio"
        return "dificil"

    def gerar_desafio(self):
        """Escolhe uma pergunta aleatória da dificuldade correspondente."""
        dificuldade = self.escolher_dificuldade()
        filtradas = [p for p in self.perguntas if p["dificuldade"] == dificuldade]

        self.pergunta = random.choice(filtradas)
        st.session_state.quiz["pergunta_atual"] = self.pergunta

        return self.pergunta

    def renderizar(self, desafio):
        """Exibe a pergunta do quiz."""
        st.markdown("""
        <style>
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes questionMark {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-5deg); }
            75% { transform: rotate(5deg); }
        }
        .quiz-header {
            background: linear-gradient(135deg, #FF9800, #FFC107);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(255, 152, 0, 0.3);
            animation: slideInRight 0.8s ease-out;
            text-align: center;
        }
        .quiz-title {
            color: white;
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .question-emoji {
            animation: questionMark 1.5s infinite;
            display: inline-block;
        }
        </style>
        <div class="quiz-header">
            <h2 class="quiz-title">❓ <span class="question-emoji">🧠</span> Quiz</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write(desafio["pergunta"])
        
        # Elementos visuais temáticos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🧠 **Conhecimento:** Teste seu saber!")
        with col2:
            st.markdown("🎯 **Precisão:** Responda exatamente!")
        with col3:
            st.markdown("⏱️ **Rapidez:** Pense e responda!")

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

    def obter_dica(self) -> str:
        pergunta = st.session_state.quiz.get("pergunta_atual")
        if pergunta and "dica" in pergunta:
            return pergunta["dica"]
        return "Pense na resposta baseada no conhecimento geral."


Game = JogoQuiz