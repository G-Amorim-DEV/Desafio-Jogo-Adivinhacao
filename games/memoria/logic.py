import json
import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo

GAME_NAME = "Memória"


class JogoMemoria(JogoBase):
    nome = "Memória"

    def __init__(self, jogador):
        self.jogador = jogador
        with open("data/memoria_palavras.json", encoding="utf-8") as arquivo:
            self.data = json.load(arquivo)

        if "memoria" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.memoria = {
            "ordem": [],
            "categoria": "",
            "dificuldade": "",
            "fase": "mostrar",
            "acertos_seguidos": 0,
        }

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Memoria",
            emoji="🧠",
            descricao="Memorize a ordem das palavras e reproduza a sequencia correta.",
            instrucoes=[
                "Clique em 'Memorizei' depois de observar a lista.",
                "Digite as palavras na mesma ordem.",
                "Separe as palavras com espacos.",
            ],
            max_dicas=2,
            custo_dica_xp=2,
        )

    def configurar_input(self) -> InputConfig:
        fase = st.session_state.memoria.get("fase", "mostrar")
        if fase == "mostrar":
            return InputConfig(tipo="none", label="")

        return InputConfig(
            tipo="text",
            label="Sequencia de palavras",
            placeholder="palavra1 palavra2 palavra3",
        )

    def escolher_dificuldade(self):
        return self.jogador.dificuldade()

    def gerar_desafio(self):
        if st.session_state.memoria.get("ordem"):
            return {
                "categoria": st.session_state.memoria["categoria"],
                "palavras": st.session_state.memoria["ordem"],
            }

        dificuldade = self.escolher_dificuldade()
        palavras = random.choice(self.data[dificuldade])
        quantidade_base = {"facil": 3, "medio": 5, "dificil": 7}[dificuldade]
        quantidade = min(len(palavras), quantidade_base)
        ordem = random.sample(palavras, quantidade)

        st.session_state.memoria.update(
            {
                "ordem": ordem,
                "categoria": "Palavras Gerais",
                "dificuldade": dificuldade,
            }
        )

        return {"categoria": "Palavras Gerais", "palavras": ordem}

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        estado = st.session_state.memoria

        if estado["fase"] == "mostrar":
            st.write(f"**Categoria:** {desafio['categoria']}")
            st.write("**Palavras para memorizar:**")
            st.write(" ".join(desafio["palavras"]))
            st.info("Memorize a ordem das palavras acima.")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("🧠 **Memoria:** Foque nas palavras.")
            with col2:
                st.markdown(f"⏱️ **Ritmo:** Modo {estado.get('dificuldade', 'medio').title()}.")
            with col3:
                st.markdown(f"📝 **Volume:** {len(desafio['palavras'])} palavras.")

            if st.button("Memorizei!", key="memorizei"):
                estado["fase"] = "esconder"
                st.rerun()
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("🔄 **Recupere:** Lembre da sequencia.")
            with col2:
                st.markdown("📋 **Formato:** palavra1 palavra2 palavra3")
            with col3:
                st.markdown("🎯 **Precisao:** Ordem exata.")

    def obter_contexto_resposta(self, desafio):
        estado = st.session_state.memoria
        if estado.get("fase") == "esconder":
            return (
                f"Categoria: {desafio['categoria']}\n"
                "Digite as palavras na ordem correta, separadas por espaco."
            )
        return None

    def verificar_resposta(self, resposta):
        estado = st.session_state.memoria
        resposta_lista = [item.strip().lower() for item in resposta.split()]
        ordem_correta = [palavra.lower() for palavra in estado["ordem"]]

        if resposta_lista == ordem_correta:
            self.jogador.adicionar_xp(10)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            return ResultadoJogo(True, "Memoria perfeita.", 10, True)

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(
                False,
                f"Memoria falhou. Ordem correta: {' '.join(estado['ordem'])}. Voce perdeu todas as vidas.",
                0,
                True,
            )

        corretas_posicao = sum(
            1
            for indice, palavra in enumerate(resposta_lista)
            if indice < len(ordem_correta) and palavra == ordem_correta[indice]
        )
        palavras_corretas = sum(1 for palavra in resposta_lista if palavra in ordem_correta)

        if len(resposta_lista) != len(ordem_correta):
            return ResultadoJogo(
                False,
                f"Quantidade errada de palavras. Sao {len(ordem_correta)} palavras. Vidas restantes: {vidas_restantes}",
                0,
                False,
            )

        return ResultadoJogo(
            False,
            f"{corretas_posicao} palavras na posicao certa, {palavras_corretas} palavras corretas no total. Ordem correta: {' '.join(estado['ordem'])}. Vidas restantes: {vidas_restantes}",
            0,
            False,
        )

    def obter_dica(self) -> str:
        estado = st.session_state.memoria
        if estado["categoria"]:
            if estado.get("dificuldade") == "dificil":
                return f"A sequencia tem {len(estado['ordem'])} palavras."
            return f"As palavras sao da categoria: {estado['categoria']}."
        return "Tente se lembrar da ordem exata das palavras apresentadas."


Game = JogoMemoria
