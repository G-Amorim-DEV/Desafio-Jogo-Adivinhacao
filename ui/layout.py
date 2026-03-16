import streamlit as st
from core.player_manager import PlayerManager
from typing import List

def sidebar(jogos: List[str]) -> str:
    """
    Renderiza a sidebar com informações do jogador e navegação entre jogos.

    Args:
        jogos (List[str]): Lista de nomes dos jogos disponíveis.

    Returns:
        str: Página selecionada pelo usuário.
    """
    # Carrega informações do jogador
    player = PlayerManager()
    dados = player.dados()

    # Informações do jogador
    st.sidebar.title("👤 Jogador")
    st.sidebar.markdown(f"**XP:** {dados.get('xp', 0)}")
    st.sidebar.markdown(f"**Jogos jogados:** {dados.get('jogos_jogados', 0)}")

    # Divider
    if jogos:
        st.sidebar.divider()

    # Navegação entre páginas
    pagina = st.sidebar.radio(
        "🏷️ Navegação",
        ["🏠 Home"] + jogos
    )

    return pagina