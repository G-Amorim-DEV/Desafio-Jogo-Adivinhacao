import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo

GAME_NAME = "Matemática"

class JogoMatematica(JogoBase):

    nome = "Matemática"

    def __init__(self, jogador):
        self.jogador = jogador
        self.resposta = None
        self.desafio_texto = None

    # -------------------------
    # GERAR DESAFIO
    # -------------------------
    def gerar_desafio(self):
        """Gera uma operação matemática aleatória baseada no nível do jogador."""
        limite = 10 + self.jogador.nivel() * 10

        a = random.randint(1, limite)
        b = random.randint(1, limite)
        op = random.choice(["+", "-", "*"])

        # Calcula a resposta sem eval
        if op == "+":
            self.resposta = a + b
        elif op == "-":
            self.resposta = a - b
        elif op == "*":
            self.resposta = a * b

        self.desafio_texto = f"{a} {op} {b}"
        return self.desafio_texto

    # -------------------------
    # VERIFICAR RESPOSTA
    # -------------------------
    def verificar_resposta(self, resposta):
        """Verifica se a resposta está correta e retorna um ResultadoJogo"""
        try:
            resposta = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um número válido!", 0, False)

        if resposta == self.resposta:
            self.jogador.adicionar_xp(5)
            return ResultadoJogo(True, f"Correto! {self.desafio_texto} = {self.resposta}", 5, False)

        # Feedback detalhado baseado na diferença
        diferenca = abs(resposta - self.resposta)
        if diferenca <= 2:
            dica = "Muito próximo! Tente ajustar por alguns números."
        elif diferenca <= 10:
            dica = "Próximo! Verifique os cálculos novamente."
        else:
            dica = "Um pouco longe. Reveja a operação."

        return ResultadoJogo(False, f"Errado! {dica} ({self.desafio_texto} = {self.resposta})", 0, False)

    # -------------------------
    # RENDERIZAR (obrigatório)
    # -------------------------
    def renderizar(self, desafio):
        """Renderiza o desafio no Streamlit"""
        st.markdown("""
        <style>
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes wiggle {
            0%, 7% { transform: rotateZ(0); }
            15% { transform: rotateZ(-15deg); }
            20% { transform: rotateZ(10deg); }
            25% { transform: rotateZ(-10deg); }
            30% { transform: rotateZ(6deg); }
            35% { transform: rotateZ(-4deg); }
            40%, 100% { transform: rotateZ(0); }
        }
        .math-header {
            background: linear-gradient(135deg, #4CAF50, #81C784);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);
            animation: zoomIn 0.8s ease-out;
            text-align: center;
        }
        .math-title {
            color: white;
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .calc-emoji {
            animation: wiggle 2s infinite;
            display: inline-block;
        }
        </style>
        <div class="math-header">
            <h2 class="math-title">➗ <span class="calc-emoji">🧮</span> Matemática</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write(desafio)
        
        # Elementos visuais temáticos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🧮 **Calculadora Mental:** Resolva a operação!")
        with col2:
            st.markdown("🔢 **Operações:** +, -, ×")
        with col3:
            st.markdown("🎯 **Precisão:** Digite apenas o resultado!")

    # -------------------------
    # OBTER DICA (obrigatório)
    # -------------------------
    def obter_dica(self):
        """Retorna uma dica para o jogador"""
        operador = self.desafio_texto.split()[1] if self.desafio_texto else "?"
        return f"O operador da operação é '{operador}'"

# -------------------------
# Instância para o GameManager
# -------------------------
Game = JogoMatematica