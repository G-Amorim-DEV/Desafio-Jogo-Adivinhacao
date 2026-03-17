import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo
from services.data_loader import carregar_json

GAME_NAME = "Scramble"

class JogoScramble(JogoBase):

    nome = "Palavra Embaralhada"

    def __init__(self, jogador):
        self.jogador = jogador

        if "scramble" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        """Reinicia o estado do jogo."""
        st.session_state.scramble = {
            "original": "",
            "embaralhada": "",
            "acertos_seguidos": 0
        }

    def gerar_desafio(self):
        """Escolhe uma palavra aleatória e embaralha suas letras."""
        if st.session_state.scramble.get("original"):
            return st.session_state.scramble["embaralhada"]
        
        dados = carregar_json("data/palavras_forca.json")
        palavra_obj = random.choice(dados)
        original = palavra_obj["palavra"].strip()
        letras = list(original)
        random.shuffle(letras)
        embaralhada = "".join(letras)

        st.session_state.scramble.update({
            "original": original,
            "embaralhada": embaralhada
        })

        return embaralhada

    def renderizar(self, desafio):
        """Exibe a palavra embaralhada."""
        st.markdown("""
        <style>
        @keyframes rotateIn {
            from { opacity: 0; transform: rotate(-10deg) scale(0.9); }
            to { opacity: 1; transform: rotate(0deg) scale(1); }
        }
        @keyframes shuffle {
            0%, 100% { transform: translateX(0); }
            10% { transform: translateX(-2px); }
            20% { transform: translateX(2px); }
            30% { transform: translateX(-2px); }
            40% { transform: translateX(2px); }
            50% { transform: translateX(-2px); }
            60% { transform: translateX(2px); }
            70% { transform: translateX(-2px); }
            80% { transform: translateX(2px); }
            90% { transform: translateX(-2px); }
        }
        .scramble-header {
            background: linear-gradient(135deg, #FF5722, #FF8A65);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(255, 87, 34, 0.3);
            animation: rotateIn 0.8s ease-out;
            text-align: center;
        }
        .scramble-title {
            color: white;
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .shuffle-emoji {
            animation: shuffle 1s infinite;
            display: inline-block;
        }
        </style>
        <div class="scramble-header">
            <h2 class="scramble-title">🔀 <span class="shuffle-emoji">🌀</span> Scramble</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        st.write(f"Reordene as letras para formar uma palavra: **{desafio}**")
        
        # Elementos visuais temáticos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🔀 **Embaralhado:** As letras estão misturadas!")
        with col2:
            st.markdown("📝 **Reordene:** Forme uma palavra válida!")
        with col3:
            st.markdown("🎯 **Criatividade:** Pense em possibilidades!")

    def verificar_resposta(self, resposta):
        """Verifica se a resposta está correta."""
        estado = st.session_state.scramble
        if not estado["original"]:
            return ResultadoJogo(False, "Nenhuma palavra selecionada!", 0, False)

        if resposta.strip().lower() == estado["original"].lower():
            self.jogador.adicionar_xp(10)
            estado["acertos_seguidos"] += 1
            # Ganhar vida a cada 5 acertos seguidos
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            st.session_state.scramble["original"] = ""  # Preparar para nova palavra
            return ResultadoJogo(True, f"Acertou! A palavra era {estado['original']}", 10, False)

        # Erro: perder vida
        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(False, f"Errou! A palavra era {estado['original']}. Você perdeu todas as vidas!", 0, True)

        # Feedback detalhado: contar letras corretas na posição certa
        resposta_lower = resposta.strip().lower()
        original_lower = estado["original"].lower()
        
        if len(resposta_lower) == len(original_lower):
            corretas_posicao = sum(1 for i, letra in enumerate(resposta_lower) if i < len(original_lower) and letra == original_lower[i])
            letras_corretas = sum(1 for letra in resposta_lower if letra in original_lower)
            st.session_state.scramble["original"] = ""  # Preparar para nova palavra
            return ResultadoJogo(False, f"Quase! {corretas_posicao} letras na posição certa, {letras_corretas} letras corretas no total. Vidas restantes: {vidas_restantes}", 0, False)
        else:
            st.session_state.scramble["original"] = ""  # Preparar para nova palavra
            return ResultadoJogo(False, f"Palavra com tamanho errado. A palavra tem {len(estado['original'])} letras. Vidas restantes: {vidas_restantes}", 0, False)

    def obter_dica(self) -> str:
        estado = st.session_state.scramble
        if estado["original"]:
            return f"A palavra tem {len(estado['original'])} letras."
        return "Tente reorganizar as letras para formar uma palavra."


Game = JogoScramble