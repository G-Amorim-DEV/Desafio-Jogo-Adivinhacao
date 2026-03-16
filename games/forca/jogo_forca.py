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

    def renderizar(self, desafio):
        """Exibe o progresso da forca com visual aprimorado."""
        estado = st.session_state.forca
        
        st.markdown("""
        <style>
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .forca-header {
            background: linear-gradient(135deg, #FF5722, #FF9800);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 6px 20px rgba(255, 87, 34, 0.3);
            animation: slideIn 0.8s ease-out;
            text-align: center;
        }
        .forca-title {
            color: white;
            font-size: 2.2em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .gallows-emoji {
            animation: pulse 1.5s infinite;
            display: inline-block;
        }
        </style>
        <div class="forca-header">
            <h2 class="forca-title">💀 <span class="gallows-emoji">🪢</span> Forca</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Layout em colunas
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Desenhar a forca
            from games.forca.render_forca import desenhar_forca
            erros = 6 - estado["tentativas"]
            desenhar_forca(erros)
            
            # Status
            st.write(f"**Tentativas restantes:** {estado['tentativas']}")
            if estado["letras"]:
                st.write(f"**Letras usadas:** {' '.join(sorted(estado['letras']))}")
        
        with col2:
            # Palavra
            st.markdown(f"<h2 style='text-align: center; font-family: monospace;'>{desafio['progresso']}</h2>", unsafe_allow_html=True)
            
            # Teclado virtual
            st.write("**Clique em uma letra:**")
            letras_disponiveis = [chr(i) for i in range(ord('A'), ord('Z')+1) if chr(i) not in estado["letras"]]
            
            if letras_disponiveis:
                cols = st.columns(6)  # 6 colunas para o alfabeto
                for i, letra in enumerate(letras_disponiveis):
                    with cols[i % 6]:
                        if st.button(letra, key=f"letra_{letra}"):
                            # Simular input
                            st.session_state.temp_letra = letra
                            st.rerun()
            else:
                st.write("Todas as letras foram usadas!")
        
        # Input manual como fallback
        st.write("**Ou digite uma letra:**")
        letra_input = st.text_input("Letra", max_chars=1, key="letra_input").upper()
        if letra_input and letra_input not in estado["letras"]:
            st.session_state.temp_letra = letra_input
            st.rerun()

    # -------------------------
    # VERIFICAR RESPOSTA
    # -------------------------
    def verificar_resposta(self, letra):
        estado = st.session_state.forca
        letra = letra.upper()

        # Se já perdeu, não permitir mais tentativas
        if estado["tentativas"] <= 0:
            return ResultadoJogo(False, f"Suas tentativas acabaram! A palavra correta era: {estado['palavra']}. Quer tentar outro jogo?", 0, True)

        if letra in estado["palavra"]:
            if letra not in estado["letras"]:  # Evitar duplicatas
                estado["letras"].append(letra)
            venceu = all(l in estado["letras"] for l in estado["palavra"])
            if venceu:
                pontos = 10 + estado["tentativas"]  # Bônus por tentativas restantes
                if self.jogador:
                    self.jogador.adicionar_xp(pontos)
                return ResultadoJogo(True, f"Parabéns! Você acertou a palavra: {estado['palavra']}!", pontos, True)
            else:
                return ResultadoJogo(True, "Letra correta!", 1, False)

        estado["tentativas"] -= 1
        perdeu = estado["tentativas"] <= 0
        if perdeu:
            return ResultadoJogo(False, f"Suas tentativas acabaram! A palavra correta era: {estado['palavra']}. Quer tentar outro jogo?", 0, True)
        else:
            return ResultadoJogo(False, f"Letra errada! Tentativas restantes: {estado['tentativas']}", 0, False)

    # -------------------------
    # OBTER DICA (novo método obrigatório)
    # -------------------------
    def obter_dica(self):
        """Retorna uma dica baseada na categoria da palavra"""
        estado = st.session_state.forca
        # Como não temos categoria salva, dica genérica
        return f"A palavra tem {len(estado['palavra'])} letras. Tente vogais primeiro!"

# Exporta apenas a classe, não a instância
Game = JogoForca