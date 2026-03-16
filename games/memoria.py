import json
import random
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo
import streamlit as st

GAME_NAME = "Memória"

class JogoMemoria(JogoBase):

    nome = "Memória"

    def __init__(self, jogador):
        self.jogador = jogador

        # Carrega os dados apenas uma vez
        with open("data/memoria_palavras.json", encoding="utf-8") as f:
            self.data = json.load(f)

        if "memoria" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        """Reinicia o estado do jogo."""
        st.session_state.memoria = {
            "ordem": [],
            "categoria": "",
            "dificuldade": "",
            "fase": "mostrar"
        }

    def escolher_dificuldade(self):
        """Define dificuldade baseada no nível do jogador."""
        if self.jogador.nivel() <= 2:
            return "facil"
        elif self.jogador.nivel() <= 4:
            return "medio"
        return "dificil"

    def gerar_desafio(self):
        """Gera um conjunto de palavras aleatórias para o desafio."""
        dificuldade = self.escolher_dificuldade()
        palavras = random.choice(self.data[dificuldade])  # Escolhe uma lista de palavras

        quantidade = min(len(palavras), 3 + self.jogador.nivel())
        ordem = random.sample(palavras, quantidade)

        st.session_state.memoria.update({
            "ordem": ordem,
            "categoria": "Palavras Gerais",  # Como não há categoria nomeada
            "dificuldade": dificuldade
        })

        return {
            "categoria": "Palavras Gerais",
            "palavras": ordem
        }

    def renderizar(self, desafio):
        """Exibe as palavras para memorização e depois pede a ordem."""
        st.markdown("""
        <style>
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 5px rgba(186, 104, 200, 0.5); }
            50% { text-shadow: 0 0 20px rgba(186, 104, 200, 0.8), 0 0 30px rgba(186, 104, 200, 0.6); }
        }
        .memory-header {
            background: linear-gradient(135deg, #9C27B0, #BA68C8);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(156, 39, 176, 0.3);
            animation: fadeInUp 1s ease-out;
            text-align: center;
        }
        .memory-title {
            color: white;
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .brain-emoji {
            animation: glow 2s infinite;
            display: inline-block;
        }
        </style>
        <div class="memory-header">
            <h2 class="memory-title">🧠 <span class="brain-emoji">💭</span> Memória</h2>
        </div>
        """, unsafe_allow_html=True)
        estado = st.session_state.memoria
        
        if estado["fase"] == "mostrar":
            st.write(f"**Categoria:** {desafio['categoria']}")
            st.write("**Palavras para memorizar:**")
            st.write(" ".join(desafio["palavras"]))
            st.info("Memorize a ordem das palavras acima.")
            
            # Elementos visuais temáticos
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("🧠 **Treine sua memória:** Foque nas palavras!")
            with col2:
                st.markdown("⏱️ **Tempo limitado:** Memorize rapidamente!")
            with col3:
                st.markdown("📝 **Ordem importa:** Anote mentalmente!")
            
            if st.button("Memorizei!", key="memorizei"):
                estado["fase"] = "esconder"
                st.rerun()
        else:
            st.write("Digite as palavras na ordem correta, separadas por espaço:")
            
            # Elementos visuais temáticos na fase de resposta
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("🔄 **Recupere:** Lembre da sequência!")
            with col2:
                st.markdown("📋 **Separe por espaço:** palavra1 palavra2 palavra3")
            with col3:
                st.markdown("🎯 **Precisão:** Ordem exata necessária!")

    def verificar_resposta(self, resposta):
        """Compara a resposta do jogador com a ordem correta."""
        estado = st.session_state.memoria
        resposta_lista = [r.strip().lower() for r in resposta.split()]

        ordem_correta = [p.lower() for p in estado["ordem"]]

        if resposta_lista == ordem_correta:
            self.jogador.adicionar_xp(10)
            return ResultadoJogo(True, "Memória perfeita!", 10, True)

        # Feedback detalhado: contar palavras corretas na posição certa
        corretas_posicao = sum(1 for i, palavra in enumerate(resposta_lista) if i < len(ordem_correta) and palavra == ordem_correta[i])
        palavras_corretas = sum(1 for palavra in resposta_lista if palavra in ordem_correta)
        
        if len(resposta_lista) != len(ordem_correta):
            return ResultadoJogo(False, f"Quantidade errada de palavras. São {len(ordem_correta)} palavras.", 0, False)
        else:
            return ResultadoJogo(False, f"{corretas_posicao} palavras na posição certa, {palavras_corretas} palavras corretas no total. Ordem correta: {' '.join(estado['ordem'])}", 0, False)

    def obter_dica(self) -> str:
        estado = st.session_state.memoria
        if estado["categoria"]:
            return f"As palavras são da categoria: {estado['categoria']}."
        return "Tente se lembrar da ordem exata das palavras apresentadas."


Game = JogoMemoria