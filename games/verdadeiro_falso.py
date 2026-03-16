import random
import streamlit as st
from core.jogo_base import JogoBase
from services.data_loader import carregar_json

GAME_NAME = "Verdadeiro ou Falso"

class JogoVF(JogoBase):

    nome = "Verdadeiro ou Falso"

    def __init__(self, jogador):
        self.jogador = jogador

    def gerar_desafio(self):

        self.afirmacao = random.choice(
            carregar_json("data/vf.json")
        )

        return self.afirmacao["texto"]

    def renderizar(self, desafio):
        """Exibe a afirmação."""
        st.markdown("""
        <style>
        @keyframes flipIn {
            from { opacity: 0; transform: rotateY(-90deg); }
            to { opacity: 1; transform: rotateY(0deg); }
        }
        @keyframes checkX {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }
        .vf-header {
            background: linear-gradient(135deg, #607D8B, #90A4AE);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(96, 125, 139, 0.3);
            animation: flipIn 0.8s ease-out;
            text-align: center;
        }
        .vf-title {
            color: white;
            font-size: 2.2em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .check-emoji, .x-emoji {
            animation: checkX 1.5s infinite;
            display: inline-block;
        }
        </style>
        <div class="vf-header">
            <h2 class="vf-title"><span class="check-emoji">✅</span>❌<span class="x-emoji">❌</span> Verdadeiro ou Falso</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write(desafio)
        st.write("Verdadeiro ou Falso?")
        
        # Elementos visuais temáticos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("✅ **Verdadeiro:** Se a afirmação for correta!")
        with col2:
            st.markdown("❌ **Falso:** Se a afirmação for incorreta!")
        with col3:
            st.markdown("🧠 **Julgamento:** Use seu conhecimento!")

    def verificar_resposta(self, resposta):

        if resposta.lower() == self.afirmacao["resposta"]:
            self.jogador.adicionar_xp(5)
            return "Certo!"

        return "Errado!"

    def obter_dica(self) -> str:
        return "Pense se a afirmação é verdadeira ou falsa baseada em conhecimento geral."
    
Game = JogoVF