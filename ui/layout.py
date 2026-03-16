import streamlit as st
from core.player_manager import PlayerManager
from typing import List

def sidebar(jogos: List[str]) -> None:
    """
    Renderiza a sidebar com informações do jogador.

    Args:
        jogos (List[str]): Lista de nomes dos jogos disponíveis.
    """
    # Carrega informações do jogador
    player = PlayerManager()
    dados = player.dados()

    # Informações do jogador
    st.sidebar.title("👤 Jogador")
    nome = dados.get("nome", "Anônimo")
    st.sidebar.markdown(f"**Nome:** {nome}")
    st.sidebar.markdown(f"**XP:** {dados.get('xp', 0)}")
    st.sidebar.markdown(f"**Jogos jogados:** {dados.get('jogos_jogados', 0)}")
    
    if st.sidebar.button("✏️ Mudar Nome"):
        st.session_state.mudar_nome = True
        st.rerun()

    # Divider
    if jogos:
        st.sidebar.divider()

    # Navegação via botões do home
    st.sidebar.markdown("**Navegação:** Use os botões na página inicial.")
    
    if st.sidebar.button("🏠 Voltar ao Home"):
        st.session_state.pagina = "🏠 Home"
        st.rerun()