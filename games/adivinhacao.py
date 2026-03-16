import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo

GAME_NAME = "Adivinhação"

class JogoAdivinhacao(JogoBase):

    nome = "Adivinhe o Número"

    def __init__(self, jogador):
        self.jogador = jogador
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

        st.markdown("""
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        .game-header {
            background: linear-gradient(135deg, #2196F3, #21CBF3);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(33, 150, 243, 0.3);
            animation: fadeIn 1s ease-out;
            text-align: center;
        }
        .game-title {
            color: white;
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .dice-emoji {
            animation: bounce 2s infinite;
            display: inline-block;
            font-size: 1.2em;
        }
        </style>
        <div class="game-header">
            <h2 class="game-title">🎲 <span class="dice-emoji">🎯</span> Adivinhe o Número</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write(desafio)
        st.info(f"Tentativas restantes: {estado['tentativas']}")
        
        # Elementos visuais temáticos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🎯 **Objetivo:** Acertar o número secreto!")
        with col2:
            st.markdown("🔢 **Faixa:** 1 a 100")
        with col3:
            st.markdown("💡 **Dica:** Use as tentativas com sabedoria!")

    def verificar_resposta(self, resposta):
        estado = st.session_state.adivinhacao

        # Se já perdeu, não permitir mais tentativas
        if estado["tentativas"] <= 0:
            return ResultadoJogo(False, f"Suas tentativas acabaram! O número correto era {estado['numero']}. Quer tentar outro jogo?", 0, True)

        try:
            resposta = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um número válido!", 0, False)

        estado["tentativas"] -= 1

        if resposta == estado["numero"]:
            estado["acertou"] = True
            return ResultadoJogo(True, f"Parabéns! Você acertou o número {estado['numero']}", 10, True)

        if estado["tentativas"] <= 0:
            return ResultadoJogo(False, f"Suas tentativas acabaram! O número correto era {estado['numero']}. Quer tentar outro jogo?", 0, True)

        dica = "Maior" if resposta < estado["numero"] else "Menor"
        return ResultadoJogo(False, f"{dica}! Tentativas restantes: {estado['tentativas']}", 0, False)

    def obter_dica(self) -> str:
        estado = st.session_state.adivinhacao
        numero = estado["numero"]
        if numero <= 10:
            return "O número é menor ou igual a 10"
        elif numero <= 50:
            return "O número está entre 11 e 50"
        else:
            return "O número é maior que 50"
    
Game = JogoAdivinhacao