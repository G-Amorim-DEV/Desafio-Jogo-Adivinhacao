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
) -> bool:
    """
    Renderiza um card estilizado para um jogo como um botão clicável.

    Args:
        nome (str): Nome do jogo a exibir.
        cor_fundo (str, optional): Cor de fundo do card. Defaults to "#1c1f26".
        cor_texto (str, optional): Cor do texto. Defaults to "#ffffff".
        emoji (str, optional): Emoji antes do nome. Defaults to "🎮".
        font_size (str, optional): Tamanho da fonte. Defaults to "20px".
        padding (str, optional): Espaçamento interno. Defaults to "20px".
        borda (str, optional): Raio da borda. Defaults to "15px".
        margin (str, optional): Espaçamento externo. Defaults to "10px".

    Returns:
        bool: True se o botão foi clicado, False caso contrário.
    """
    # Usar st.button com label estilizado
    button_label = f"{emoji} {nome}"
    
    # Criar um botão que retorna se foi clicado
    return st.button(
        button_label,
        key=f"btn_{nome}",
        help=f"Jogar {nome}",
        use_container_width=True
    )