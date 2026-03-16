import streamlit as st

def aplicar_tema(
    cor_fundo: str = "#0E1117",
    cor_titulo: str = "#FAFAFA",
    cor_botao: str = "#4CAF50",
    cor_texto_botao: str = "#FFFFFF",
    borda_botao: str = "10px"
) -> None:
    """
    Aplica tema customizado ao Streamlit.

    Args:
        cor_fundo (str): Cor de fundo da página principal.
        cor_titulo (str): Cor dos títulos h1, h2, h3.
        cor_botao (str): Cor de fundo dos botões.
        cor_texto_botao (str): Cor do texto dos botões.
        borda_botao (str): Raio das bordas dos botões.
    """
    st.markdown(f"""
        <style>
        /* Fundo principal */
        .main {{
            background-color: {cor_fundo};
        }}

        /* Títulos */
        h1,h2,h3 {{
            color: {cor_titulo};
        }}

        /* Botões */
        .stButton>button {{
            border-radius: {borda_botao};
            background-color: {cor_botao};
            color: {cor_texto_botao};
            border: none;
            padding: 0.5em 1em;
        }}

        /* Inputs */
        .stTextInput>div>div>input {{
            background-color: #1C1F26;
            color: #FAFAFA;
            border-radius: 8px;
            padding: 0.4em;
        }}

        /* Sliders */
        .stSlider>div>div>div>div {{
            background-color: #4CAF50;
        }}

        /* Sidebar */
        .sidebar .sidebar-content {{
            background-color: #16191F;
        }}
        </style>
    """, unsafe_allow_html=True)