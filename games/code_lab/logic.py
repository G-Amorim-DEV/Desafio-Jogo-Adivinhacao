import json
import random

import streamlit as st

from core.engine.base import JogoBase
from core.engine.ui import GameInfo, InputConfig
from core.models.result import ResultadoJogo
from utils.paths import data_dir

GAME_NAME = "Code Lab"

LANGUAGE_LABELS = {
    "python": "Python",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "java": "Java",
    "csharp": "C#",
    "sql": "SQL",
    "go": "Go",
    "rust": "Rust",
}

CODE_LANGUAGE_MAP = {
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "java": "java",
    "csharp": "csharp",
    "sql": "sql",
    "go": "go",
    "rust": "rust",
}


class JogoCodeLab(JogoBase):
    nome = "Code Lab"

    def __init__(self, jogador):
        self.jogador = jogador
        self.desafios = self._carregar_desafios()
        if "code_lab" not in st.session_state:
            self.resetar_jogo()

    def _carregar_desafios(self):
        base = data_dir("code_lab")
        desafios = []
        for arquivo in sorted(base.glob("*.json")):
            with open(arquivo, encoding="utf-8") as f:
                desafios.extend(json.load(f))
        if not desafios:
            raise ValueError("Nenhum desafio do Code Lab foi encontrado.")
        return desafios

    def resetar_jogo(self):
        st.session_state.code_lab = {
            "item_atual": None,
            "acertos_seguidos": 0,
            "linguagem": "todas",
            "conceito": "todos",
        }

    def obter_info(self) -> GameInfo:
        return GameInfo(
            nome=GAME_NAME,
            titulo="Code Lab",
            emoji="💻",
            descricao="Aprenda logica e programacao resolvendo desafios curtos em linguagens buscadas pelo mercado.",
            instrucoes=[
                "Escolha uma linguagem especifica ou deixe em todas.",
                "Resolva desafios de sintaxe, logica, estruturas e leitura de codigo.",
                "Leia a explicacao ao final para transformar o erro em aprendizado.",
            ],
            max_dicas=3,
            custo_dica_xp=1,
        )

    def configurar_input(self) -> InputConfig:
        item = st.session_state.code_lab.get("item_atual")
        return InputConfig(
            tipo="radio",
            label="Escolha a melhor resposta",
            opcoes=item["opcoes"] if item else [],
        )

    def _get_conceitos(self, linguagem):
        candidatos = self.desafios
        if linguagem != "todas":
            candidatos = [item for item in self.desafios if item["linguagem"] == linguagem]
        return sorted({item["conceito"] for item in candidatos})

    def _filtrar_desafios(self):
        estado = st.session_state.code_lab
        linguagem = estado.get("linguagem", "todas")
        conceito = estado.get("conceito", "todos")
        dificuldade = self.jogador.dificuldade()

        candidatos = self.desafios
        if linguagem != "todas":
            candidatos = [item for item in candidatos if item["linguagem"] == linguagem]
        if conceito != "todos":
            candidatos = [item for item in candidatos if item["conceito"] == conceito]

        por_dificuldade = [item for item in candidatos if item["dificuldade"] == dificuldade]
        return por_dificuldade or candidatos or self.desafios

    def gerar_desafio(self):
        if st.session_state.code_lab.get("item_atual"):
            return st.session_state.code_lab["item_atual"]

        candidatos = self._filtrar_desafios()
        item = random.choice(candidatos)
        st.session_state.code_lab["item_atual"] = item
        return item

    def renderizar(self, desafio):
        estado = st.session_state.code_lab
        linguagens = ["todas"] + list(LANGUAGE_LABELS.keys())
        linguagem = st.selectbox(
            "Linguagem",
            options=linguagens,
            index=linguagens.index(estado.get("linguagem", "todas")),
            format_func=lambda valor: "Todas as linguagens" if valor == "todas" else LANGUAGE_LABELS[valor],
            key="code_lab_linguagem",
        )
        conceitos = ["todos"] + self._get_conceitos(linguagem)
        conceito_atual = estado.get("conceito", "todos")
        if conceito_atual not in conceitos:
            conceito_atual = "todos"
        conceito = st.selectbox(
            "Conceito",
            options=conceitos,
            index=conceitos.index(conceito_atual),
            format_func=lambda valor: "Todos os conceitos" if valor == "todos" else valor.replace("_", " ").title(),
            key="code_lab_conceito",
        )

        if linguagem != estado.get("linguagem") or conceito != estado.get("conceito"):
            estado["linguagem"] = linguagem
            estado["conceito"] = conceito
            estado["item_atual"] = None
            st.rerun()

        st.write(f"**Vidas restantes:** {self.jogador.vidas()} ❤️")
        st.caption(
            f"Linguagem: {LANGUAGE_LABELS.get(desafio['linguagem'], desafio['linguagem'])} | "
            f"Conceito: {desafio['conceito'].replace('_', ' ').title()} | "
            f"Dificuldade: {desafio['dificuldade'].title()}"
        )
        st.code(
            desafio["codigo"],
            language=CODE_LANGUAGE_MAP.get(desafio["linguagem"], "text"),
        )

    def obter_contexto_resposta(self, desafio):
        return desafio.get("pergunta", "")

    def verificar_resposta(self, resposta):
        item = st.session_state.code_lab.get("item_atual")
        if not item:
            return ResultadoJogo(False, "Nenhum desafio carregado.", 0, False)

        estado = st.session_state.code_lab
        if resposta.strip() == item["resposta"]:
            pontos = item["pontos"]
            self.jogador.adicionar_xp(pontos)
            estado["acertos_seguidos"] += 1
            if estado["acertos_seguidos"] % 5 == 0:
                self.jogador.ganhar_vida()
            st.session_state.code_lab["item_atual"] = None
            return ResultadoJogo(
                True,
                f"Correto. {item['explicacao']}",
                pontos,
                False,
            )

        vidas = self.jogador.perder_vida()
        estado["acertos_seguidos"] = 0
        if vidas <= 0:
            return ResultadoJogo(
                False,
                f"Resposta incorreta. Correta: {item['resposta']}. {item['explicacao']}",
                0,
                True,
            )

        return ResultadoJogo(
            False,
            f"Resposta incorreta. Revise o codigo, use a dica se precisar e tente novamente. Vidas restantes: {vidas}",
            0,
            False,
        )

    def obter_dica(self):
        item = st.session_state.code_lab.get("item_atual")
        if item:
            return item.get("dica", "Observe com atencao o trecho de codigo e o conceito.")
        return "Escolha uma linguagem e concentre-se no conceito mostrado."


Game = JogoCodeLab
