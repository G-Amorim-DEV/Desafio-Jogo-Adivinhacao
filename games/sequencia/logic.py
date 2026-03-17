import json
import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo

GAME_NAME = "Sequencia"


class JogoSequencia(JogoBase):
    nome = "Sequência"

    def __init__(self, jogador):
        self.jogador = jogador
        with open("data/sequencias.json", encoding="utf-8") as arquivo:
            self.lista = json.load(arquivo)

        if "sequencia" not in st.session_state:
            self.resetar_jogo()

    def resetar_jogo(self):
        st.session_state.sequencia = {"item_atual": None, "acertos_seguidos": 0}

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Sequencia",
            emoji="🔢",
            descricao="Descubra o padrao e informe o proximo numero.",
            instrucoes=[
                "Analise a sequencia apresentada.",
                "Descubra a regra de formacao.",
                "Digite apenas o proximo numero.",
            ],
        )

    def configurar_input(self) -> InputConfig:
        return InputConfig(
            tipo="number",
            label="Proximo numero",
            placeholder="Digite o proximo valor",
        )

    def gerar_desafio(self):
        if st.session_state.sequencia.get("item_atual") is not None:
            return st.session_state.sequencia["item_atual"]

        dificuldade = self.jogador.dificuldade()
        candidatos = [item for item in self.lista if item.get("dificuldade") == dificuldade]
        item = random.choice(candidatos or self.lista)
        st.session_state.sequencia["item_atual"] = item
        return item

    def renderizar(self, desafio):
        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        st.write(desafio["sequencia"])
        st.write("Qual e o proximo numero?")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("📊 **Padrao:** Observe a logica da sequencia.")
        with col2:
            st.markdown("🔢 **Regra:** Descubra a transformacao.")
        with col3:
            st.markdown("🎯 **Resposta:** Informe o proximo termo.")

    def verificar_resposta(self, resposta):
        item = st.session_state.sequencia.get("item_atual")
        if not item:
            return ResultadoJogo(False, "Nenhuma sequencia selecionada.", 0, False)

        estado = st.session_state.sequencia

        try:
            resposta_num = int(resposta)
        except ValueError:
            return ResultadoJogo(False, "Digite um numero valido.", 0, False)

        if resposta_num == item["resposta"]:
            pontos = item["pontos"]
            self.jogador.adicionar_xp(pontos)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            st.session_state.sequencia["item_atual"] = None
            return ResultadoJogo(True, f"Correto. {item['explicacao']}", pontos, False)

        vidas_restantes = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas_restantes <= 0:
            return ResultadoJogo(
                False,
                f"Errado. {item['explicacao']}. Voce perdeu todas as vidas.",
                0,
                True,
            )

        diferenca = abs(resposta_num - item["resposta"])
        if diferenca <= 1:
            dica = "Muito proximo. Verifique se errou por 1."
        elif diferenca <= 5:
            dica = "Proximo. Reveja o padrao."
        elif diferenca <= 20:
            dica = "Um pouco longe. Pense na regra novamente."
        else:
            dica = "Muito diferente. Observe melhor o padrao."

        return ResultadoJogo(
            False,
            f"Errado. {dica} ({item['explicacao']}). Vidas restantes: {vidas_restantes}",
            0,
            False,
        )

    def obter_dica(self) -> str:
        item = st.session_state.sequencia.get("item_atual")
        if item and "dica" in item:
            return item["dica"]
        return "Observe o padrao da sequencia e calcule o proximo numero."


Game = JogoSequencia
