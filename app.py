import streamlit as st

from core.game_manager import GameManager
from core.player_manager import PlayerManager
from ui.layout import sidebar
from ui.theme import aplicar_tema
from ui.components import game_card

# -------------------------
# Tema e configuração
# -------------------------
aplicar_tema()

# Inicializa gerenciadores
manager = GameManager()
player = PlayerManager()
jogos = manager.listar_jogos()

# -------------------------
# Sidebar e navegação
# -------------------------
pagina = sidebar(jogos)

st.title("🧠 Plataforma Cognitiva")

# -------------------------
# HOME
# -------------------------
if pagina == "🏠 Home":
    st.subheader("Escolha um jogo")
    for jogo in jogos:
        game_card(jogo)

# -------------------------
# JOGOS
# -------------------------
else:
    # Inicializa jogo ativo se não existir
    if "jogo_ativo" not in st.session_state:
        # ✅ PASSA O JOGADOR na criação do jogo
        st.session_state.jogo_ativo = manager.criar_jogo(pagina, player)

    jogo = st.session_state.jogo_ativo
    desafio = jogo.gerar_desafio()

    # Renderiza o desafio (cada jogo implementa renderizar)
    jogo.renderizar(desafio)

    # Input do usuário
    resposta = st.text_input("Digite sua resposta").strip()

    if st.button("Enviar") and resposta:
        resultado = jogo.verificar_resposta(resposta)

        # Feedback visual
        if resultado.correto:
            st.success(f"✅ {resultado.mensagem} (+{resultado.pontos} XP)")
            player.adicionar_xp(resultado.pontos)
        else:
            st.error(f"❌ {resultado.mensagem}")

        # Finalização do jogo
        if resultado.finalizado:
            st.balloons()
            st.success("🏆 Jogo concluído!")
            del st.session_state.jogo_ativo

        # Força atualização da página
        st.rerun()