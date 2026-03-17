import json

import streamlit as st
import streamlit.components.v1 as components

from core.engine.ui import GameInfo


def metric_card(label: str, value: str, help_text: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-shell">
            <span class="metric-label">{label}</span>
            <strong class="metric-value">{value}</strong>
            {"<span class='metric-help'>" + help_text + "</span>" if help_text else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def game_card(info: GameInfo, button_key: str) -> bool:
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="game-card-shell">
                <div class="game-card-tag">Pronto para jogar</div>
                <div class="game-card-top">
                    <span class="game-card-emoji">{info.emoji}</span>
                    <div>
                        <div class="game-card-title">{info.titulo}</div>
                        <div class="game-card-copy">{info.descricao}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if info.instrucoes:
            st.caption("Como funciona")
            for item in info.instrucoes[:2]:
                st.write(f"- {item}")

        return st.button(
            "Abrir desafio",
            key=button_key,
            use_container_width=True,
        )


def render_game_intro(info: GameInfo) -> None:
    st.markdown(
        f"""
        <section class="game-hero">
            <div class="game-hero-badge">{info.emoji} {info.nome}</div>
            <h2>{info.titulo}</h2>
            <p>{info.descricao}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    if info.instrucoes:
        with st.container(border=True):
            st.caption("Instrucoes da rodada")
            for item in info.instrucoes:
                st.write(f"- {item}")


def render_page_hero(titulo: str, subtitulo: str, destaque: str = "") -> None:
    destaque_html = f"<div class='page-hero-chip'>{destaque}</div>" if destaque else ""
    st.markdown(
        f"""
        <section class="page-hero">
            {destaque_html}
            <h1>{titulo}</h1>
            <p>{subtitulo}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_spotlight_panel(titulo: str, descricao: str, chips: list[str]) -> None:
    chips_html = "".join(f"<span class='spotlight-chip'>{chip}</span>" for chip in chips)
    st.markdown(
        f"""
        <section class="spotlight-panel">
            <div class="spotlight-kicker">Destaque da Sessao</div>
            <h3>{titulo}</h3>
            <p>{descricao}</p>
            <div class="spotlight-chip-row">{chips_html}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_side_panel(titulo: str, itens: list[tuple[str, str]], destaque: str = "") -> None:
    linhas = "".join(
        f"<div class='side-panel-row'><span>{label}</span><strong>{valor}</strong></div>"
        for label, valor in itens
    )
    destaque_html = f"<div class='side-panel-note'>{destaque}</div>" if destaque else ""
    st.markdown(
        f"""
        <aside class="side-panel-shell">
            <div class="side-panel-title">{titulo}</div>
            {linhas}
            {destaque_html}
        </aside>
        """,
        unsafe_allow_html=True,
    )


def render_championship_row(posicao: int, nome: str, score: int, jogo: str = "") -> None:
    medalha = {1: "🥇", 2: "🥈", 3: "🥉"}.get(posicao, f"#{posicao}")
    jogo_html = f"<span class='championship-game'>{jogo}</span>" if jogo else ""
    st.markdown(
        f"""
        <div class="championship-row">
            <div class="championship-position">{medalha}</div>
            <div class="championship-player">
                <strong>{nome}</strong>
                {jogo_html}
            </div>
            <div class="championship-score">{score} pts</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_step_guide(titulo: str, passos: list[tuple[str, str]]) -> None:
    itens = "".join(
        f"""
        <div class="guide-step">
            <div class="guide-step-index">{indice}</div>
            <div class="guide-step-copy">
                <strong>{titulo_passo}</strong>
                <p>{descricao}</p>
            </div>
        </div>
        """
        for indice, (titulo_passo, descricao) in enumerate(passos, start=1)
    )
    st.markdown(
        f"""
        <section class="guide-shell">
            <div class="guide-kicker">Manual rapido</div>
            <h3>{titulo}</h3>
            <div class="guide-list">
                {itens}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_answer_panel(titulo: str, descricao: str, destaque: str = "") -> None:
    destaque_html = f"<div class='answer-zone-chip'>{destaque}</div>" if destaque else ""
    st.markdown(
        f"""
        <section class="answer-zone-shell">
            <div class="answer-zone-kicker">Area de resposta</div>
            <h3>{titulo}</h3>
            <p>{descricao}</p>
            {destaque_html}
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_accessibility_reader(texto: str, forcar_leitura: bool = False, auto: bool = False, velocidade: float = 1.0) -> None:
    payload = json.dumps(texto)
    should_speak = "true" if (forcar_leitura or auto) else "false"
    components.html(
        f"""
        <div aria-live="polite" style="position:absolute;left:-9999px;">{texto}</div>
        <script>
        const content = {payload};
        const shouldSpeak = {should_speak};
        if (shouldSpeak && window.speechSynthesis) {{
            const utterance = new SpeechSynthesisUtterance(content);
            utterance.lang = "pt-BR";
            utterance.rate = {velocidade};
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """,
        height=0,
    )
