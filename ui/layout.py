from typing import List

import streamlit as st


def sidebar(jogos: List[str], dados: dict, player_manager) -> None:
    st.sidebar.title("Arcade Cognitivo")
    st.sidebar.caption("Navegacao rapida do arcade.")
    with st.sidebar.container(border=True):
        st.markdown(f"**Jogador ativo:** {dados.get('nome', 'Anônimo')}")
        st.caption(
            f"Nivel {dados.get('xp', 0) // 100 + 1} • {dados.get('vidas', 0)} vidas • {dados.get('xp', 0)} XP"
        )

    st.sidebar.write("Atalhos")
    if st.sidebar.button("Inicio", use_container_width=True):
        st.session_state.pagina = "🏠 Home"
        st.rerun()

    if st.sidebar.button("Menu da sessao", use_container_width=True):
        st.session_state.pagina = "🧭 Menu da Sessao"
        st.rerun()

    if st.sidebar.button("Ranking", use_container_width=True):
        st.session_state.pagina = "🏆 Ranking"
        st.rerun()

    if st.sidebar.button("Circuito Aleatorio", use_container_width=True):
        st.session_state.pagina = "🎲 Circuito Aleatorio"
        st.rerun()

    if st.sidebar.button("Como usar", use_container_width=True):
        st.session_state.pagina = "📘 Como Usar"
        st.rerun()

    if st.sidebar.button("Ler tela atual", use_container_width=True):
        st.session_state.accessibility_read_now = True
        st.rerun()
