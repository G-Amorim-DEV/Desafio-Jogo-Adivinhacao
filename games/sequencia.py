import json
import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo

GAME_NAME = "Sequencia"

class JogoSequencia(JogoBase):

    nome = "Sequência"

    def __init__(self, jogador):
        self.jogador = jogador

        with open("data/sequencias.json", encoding="utf-8") as f:
            self.lista = json.load(f)

        if "sequencia" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        """Reinicia o estado do jogo."""
        st.session_state.sequencia = {
            "item_atual": None
        }

    def gerar_desafio(self):
        """Escolhe um item aleatório da lista de sequências."""
        item = random.choice(self.lista)
        st.session_state.sequencia["item_atual"] = item
        return item

    def renderizar(self, desafio):
        """Exibe a sequência."""
        st.markdown("""
        <style>
        @keyframes bounceIn {
            0% { opacity: 0; transform: scale(0.3); }
            50% { opacity: 1; transform: scale(1.05); }
            70% { transform: scale(0.9); }
            100% { opacity: 1; transform: scale(1); }
        }
        @keyframes numberPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .sequence-header {
            background: linear-gradient(135deg, #F44336, #EF5350);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(244, 67, 54, 0.3);
            animation: bounceIn 0.8s ease-out;
            text-align: center;
        }
        .sequence-title {
            color: white;
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .number-emoji {
            animation: numberPulse 1.5s infinite;
            display: inline-block;
        }
        </style>
        <div class="sequence-header">
            <h2 class="sequence-title">🔢 <span class="number-emoji">📊</span> Sequência</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write(desafio["sequencia"])
        st.write("Qual é o próximo número?")
        
        # Elementos visuais temáticos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("📊 **Padrão:** Identifique o padrão da sequência!")
        with col2:
            st.markdown("🔢 **Lógica:** Qual é a regra matemática?")
        with col3:
            st.markdown("🎯 **Próximo:** Calcule o próximo termo!")

    def verificar_resposta(self, resposta):
        """Verifica se a resposta do jogador está correta."""
        item = st.session_state.sequencia.get("item_atual")
        if not item:
            return ResultadoJogo(False, "Nenhuma sequência selecionada!", 0, False)

        try:
            resposta_num = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um número válido!", 0, False)

        if resposta_num == item["resposta"]:
            pontos = item["pontos"]
            self.jogador.adicionar_xp(pontos)
            return ResultadoJogo(True, f"Correto! {item['explicacao']}", pontos, True)

        # Feedback detalhado baseado na diferença
        diferenca = abs(resposta_num - item["resposta"])
        if diferenca <= 1:
            dica = "Muito próximo! Verifique se não errou por 1."
        elif diferenca <= 5:
            dica = "Próximo! Reveja o padrão da sequência."
        elif diferenca <= 20:
            dica = "Um pouco longe. Pense na regra novamente."
        else:
            dica = "Muito diferente. Observe melhor o padrão."

        return ResultadoJogo(False, f"Errado! {dica} ({item['explicacao']})", 0, False)

    def obter_dica(self) -> str:
        item = st.session_state.sequencia.get("item_atual")
        if item and "dica" in item:
            return item["dica"]
        return "Observe o padrão da sequência e calcule o próximo número."


Game = JogoSequencia