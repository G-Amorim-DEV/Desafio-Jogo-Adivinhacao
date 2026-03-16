import matplotlib.pyplot as plt
import streamlit as st

def desenhar_forca(erros):
    """
    Desenha a forca de acordo com o número de erros.
    :param erros: int de 0 a 6
    """

    fig, ax = plt.subplots(figsize=(3, 4))

    # Estrutura da forca
    ax.plot([0, 1], [0, 0], color="brown", lw=3)      # Base
    ax.plot([0.2, 0.2], [0, 1], color="brown", lw=3)  # Poste
    ax.plot([0.2, 0.6], [1, 1], color="brown", lw=3)  # Viga horizontal
    ax.plot([0.6, 0.6], [1, 0.85], color="brown", lw=3) # Cordão

    # Cabeça
    if erros >= 1:
        ax.add_patch(plt.Circle((0.6, 0.8), 0.05, fill=False, lw=2))

    # Tronco
    if erros >= 2:
        ax.plot([0.6, 0.6], [0.75, 0.6], color="black", lw=2)

    # Braço esquerdo
    if erros >= 3:
        ax.plot([0.6, 0.55], [0.73, 0.65], color="black", lw=2)

    # Braço direito
    if erros >= 4:
        ax.plot([0.6, 0.65], [0.73, 0.65], color="black", lw=2)

    # Perna esquerda
    if erros >= 5:
        ax.plot([0.6, 0.55], [0.6, 0.5], color="black", lw=2)

    # Perna direita
    if erros >= 6:
        ax.plot([0.6, 0.65], [0.6, 0.5], color="black", lw=2)

    # Configurações do gráfico
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_aspect('equal')

    st.pyplot(fig)