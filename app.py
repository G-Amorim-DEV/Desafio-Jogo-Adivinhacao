import streamlit as st
import time

from core.jogador import Jogador
from core.game_manager import GameManager

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Plataforma Cognitiva",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Plataforma de Jogos Cognitivos")

manager = GameManager()

# =============================
# SESSION STATE INIT
# =============================
defaults = {
    "jogador": None,
    "jogo": None,
    "desafio": None,
    "tentativas": 0,
    "inicio_tempo": None,
    "mostrar_memoria": True,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =============================
# LOGIN JOGADOR
# =============================
nome = st.text_input("Nome do jogador")

if nome and not st.session_state.jogador:
    st.session_state.jogador = Jogador(nome)

# =============================
# SIDEBAR STATUS
# =============================
if st.session_state.jogador:

    jogador = st.session_state.jogador

    st.sidebar.title("👤 Status")
    st.sidebar.write("Jogador:", jogador.nome)
    st.sidebar.write("⭐ Pontos:", jogador.pontos)
    st.sidebar.write("🏆 Nível:", jogador.nivel)

    # =============================
    # ESCOLHA DO JOGO
    # =============================
    jogo_nome = st.selectbox(
        "Escolha o jogo",
        manager.listar()
    )

    # =============================
    # INICIAR JOGO
    # =============================
    if st.button("🚀 Iniciar jogo"):

        jogo = manager.criar(jogo_nome, jogador)

        st.session_state.jogo = jogo
        st.session_state.desafio = jogo.gerar_desafio()

        st.session_state.tentativas = 0
        st.session_state.inicio_tempo = time.time()
        st.session_state.mostrar_memoria = True

        st.rerun()

# =============================
# AREA DO JOGO
# =============================
if st.session_state.jogo and st.session_state.desafio:

    jogo = st.session_state.jogo
    desafio = st.session_state.desafio

    st.divider()
    st.subheader("🧩 Desafio")

    # =============================
    # SISTEMA DE TEMPO
    # =============================
    tempo_limite = jogo.tempo_por_nivel()

    tempo_passado = int(time.time() - st.session_state.inicio_tempo)
    restante = max(0, tempo_limite - tempo_passado)

    st.progress(restante / tempo_limite)
    st.write(f"⏳ Tempo restante: {restante}s")

    if restante <= 0:
        st.error("⏰ Tempo esgotado!")
        st.session_state.desafio = jogo.gerar_desafio()
        st.session_state.inicio_tempo = time.time()
        st.rerun()

    # =============================
    # RENDERIZA DESAFIO
    # =============================
    jogo.renderizar(desafio)

    # =============================
    # DICA
    # =============================
    if st.button("💡 Dica"):
        dica = jogo.obter_dica(desafio)
        st.info(dica)

    # =============================
    # RESPOSTA
    # =============================
    resposta = st.text_input("Sua resposta")

    if st.button("✅ Enviar resposta"):

        resultado = jogo.verificar_resposta(resposta)

        st.session_state.tentativas += 1

        if resultado["correto"]:
            st.success("✔ Correto!")

            jogador.ganhar_pontos(resultado["pontos"])

            st.session_state.desafio = jogo.gerar_desafio()
            st.session_state.inicio_tempo = time.time()

        else:
            st.error("❌ Errado")

            if st.session_state.tentativas >= jogo.tentativas_max():
                st.warning("Sem tentativas restantes!")
                st.session_state.desafio = jogo.gerar_desafio()
                st.session_state.tentativas = 0

        st.rerun()

    # =============================
    # NOVO DESAFIO
    # =============================
    if st.button("🔄 Pular desafio"):
        st.session_state.desafio = jogo.gerar_desafio()
        st.session_state.inicio_tempo = time.time()
        st.rerun()