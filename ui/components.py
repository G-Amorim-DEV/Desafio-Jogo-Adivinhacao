import streamlit as st

def game_card(
    nome: str,
    cor_fundo: str = "#1c1f26",
    cor_texto: str = "#ffffff",
    emoji: str = "🎮",
    font_size: str = "20px",
    padding: str = "20px",
    borda: str = "15px",
    margin: str = "10px"
) -> None:
    """
    Renderiza um card estilizado para um jogo.

    Args:
        nome (str): Nome do jogo a exibir.
        cor_fundo (str, optional): Cor de fundo do card. Defaults to "#1c1f26".
        cor_texto (str, optional): Cor do texto. Defaults to "#ffffff".
        emoji (str, optional): Emoji antes do nome. Defaults to "🎮".
        font_size (str, optional): Tamanho da fonte. Defaults to "20px".
        padding (str, optional): Espaçamento interno. Defaults to "20px".
        borda (str, optional): Raio da borda. Defaults to "15px".
        margin (str, optional): Espaçamento externo. Defaults to "10px".
    """
    st.markdown(f"""
        <div style="
            padding:{padding};
            border-radius:{borda};
            background:{cor_fundo};
            margin-bottom:{margin};
            text-align:center;
            font-size:{font_size};
            color:{cor_texto};
        ">
            {emoji} {nome}
        </div>
    """, unsafe_allow_html=True)