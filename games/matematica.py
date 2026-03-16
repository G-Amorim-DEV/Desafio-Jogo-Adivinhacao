import random
import streamlit as st
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo

GAME_NAME = "Matemática"

class JogoMatematica(JogoBase):

    nome = "Matemática"

    def __init__(self, jogador):
        self.jogador = jogador
        self.resposta = None
        self.desafio_texto = None

    # -------------------------
    # GERAR DESAFIO
    # -------------------------
    def gerar_desafio(self):
        """Gera uma operação matemática aleatória baseada no nível do jogador."""
        limite = 10 + self.jogador.nivel * 10

        a = random.randint(1, limite)
        b = random.randint(1, limite)
        op = random.choice(["+", "-", "*"])

        # Calcula a resposta sem eval
        if op == "+":
            self.resposta = a + b
        elif op == "-":
            self.resposta = a - b
        elif op == "*":
            self.resposta = a * b

        self.desafio_texto = f"{a} {op} {b}"
        return self.desafio_texto

    # -------------------------
    # VERIFICAR RESPOSTA
    # -------------------------
    def verificar_resposta(self, resposta):
        """Verifica se a resposta está correta e retorna um ResultadoJogo"""
        try:
            resposta = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um número válido!", 0, False)

        if resposta == self.resposta:
            self.jogador.ganhar_pontos(5)
            return ResultadoJogo(True, f"Correto! {self.desafio_texto} = {self.resposta}", 5, False)

        return ResultadoJogo(False, f"Errado! {self.desafio_texto} = {self.resposta}", 0, False)

    # -------------------------
    # RENDERIZAR (obrigatório)
    # -------------------------
    def renderizar(self, desafio):
        """Renderiza o desafio no Streamlit"""
        st.subheader("Resolva o desafio:")
        st.write(desafio)

    # -------------------------
    # OBTER DICA (obrigatório)
    # -------------------------
    def obter_dica(self):
        """Retorna uma dica para o jogador"""
        operador = self.desafio_texto.split()[1] if self.desafio_texto else "?"
        return f"O operador da operação é '{operador}'"

# -------------------------
# Instância para o GameManager
# -------------------------
Game = JogoMatematica