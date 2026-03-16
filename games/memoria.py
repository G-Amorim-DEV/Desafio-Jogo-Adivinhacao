import json
import random
from core.jogo_base import JogoBase
from core.resultado import ResultadoJogo
import streamlit as st

GAME_NAME = "Memória"

class JogoMemoria(JogoBase):

    nome = "Memória"

    def __init__(self, jogador):
        self.jogador = jogador

        # Carrega os dados apenas uma vez
        with open("data/memoria_palavras.json", encoding="utf-8") as f:
            self.data = json.load(f)

        if "memoria" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        """Reinicia o estado do jogo."""
        st.session_state.memoria = {
            "ordem": [],
            "categoria": "",
            "dificuldade": ""
        }

    def escolher_dificuldade(self):
        """Define dificuldade baseada no nível do jogador."""
        if self.jogador.nivel <= 2:
            return "facil"
        elif self.jogador.nivel <= 4:
            return "medio"
        return "dificil"

    def gerar_desafio(self):
        """Gera um conjunto de palavras aleatórias para o desafio."""
        dificuldade = self.escolher_dificuldade()
        categoria = random.choice(list(self.data[dificuldade].keys()))
        palavras = self.data[dificuldade][categoria]

        quantidade = min(len(palavras), 3 + self.jogador.nivel)
        ordem = random.sample(palavras, quantidade)

        st.session_state.memoria.update({
            "ordem": ordem,
            "categoria": categoria,
            "dificuldade": dificuldade
        })

        return {
            "categoria": categoria,
            "palavras": ordem
        }

    def verificar_resposta(self, resposta):
        """Compara a resposta do jogador com a ordem correta."""
        estado = st.session_state.memoria
        resposta_lista = [r.strip().lower() for r in resposta.split()]

        ordem_correta = [p.lower() for p in estado["ordem"]]

        if resposta_lista == ordem_correta:
            self.jogador.ganhar_pontos(10)
            return ResultadoJogo(True, "Memória perfeita!", 10, True)

        return ResultadoJogo(False, f"Ordem correta: {' '.join(estado['ordem'])}", 0, False)


Game = JogoMemoria