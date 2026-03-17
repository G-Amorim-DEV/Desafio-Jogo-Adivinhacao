from typing import List

import streamlit as st


def sidebar(jogos: List[str], dados: dict, player_manager) -> None:
    st.sidebar.title("Arcade Cognitivo")
    st.sidebar.caption("Jogos de raciocinio, trilhas de aprendizado e partidas locais com cara de plataforma.")

    jogadores = player_manager.listar_jogadores()
    if jogadores:
        labels = [
            f"{player['nome'] or 'Sem nome'} ({player['xp']} XP)"
            for player in jogadores
        ]
        ids = [player["id"] for player in jogadores]
        indice_atual = ids.index(dados.get("id")) if dados.get("id") in ids else 0
        selecionado = st.sidebar.selectbox(
            "Perfil ativo",
            options=labels,
            index=indice_atual,
            key="perfil_ativo_sidebar",
        )
        player_id = ids[labels.index(selecionado)]
        if player_id != dados.get("id"):
            player_manager.definir_jogador_ativo(player_id)
            st.rerun()

    with st.sidebar.expander("Novo jogador", expanded=not jogadores):
        novo_nome = st.text_input("Nome do novo jogador", key="novo_jogador_sidebar")
        if st.button("Criar perfil", use_container_width=True):
            if novo_nome.strip():
                player_manager.criar_jogador(novo_nome)
                st.rerun()

    if jogadores:
        with st.sidebar.expander("Gerenciar perfis", expanded=False):
            opcoes_exclusao = {
                f"{player['nome'] or 'Sem nome'} ({player['xp']} XP)": player["id"]
                for player in jogadores
            }
            selecionado_exclusao = st.selectbox(
                "Perfil para excluir",
                options=list(opcoes_exclusao.keys()),
                key="excluir_perfil_select",
            )
            confirmar_exclusao = st.checkbox(
                "Confirmo que desejo excluir este perfil local.",
                key="confirmar_exclusao_perfil",
            )
            if st.button("Excluir perfil", use_container_width=True, type="secondary"):
                if confirmar_exclusao:
                    player_manager.excluir_jogador(opcoes_exclusao[selecionado_exclusao])
                    st.session_state.session_player_ids = [
                        player_id
                        for player_id in st.session_state.get("session_player_ids", [])
                        if player_id in [player["id"] for player in player_manager.listar_jogadores()]
                    ]
                    st.rerun()

    if jogadores:
        with st.sidebar.container(border=True):
            st.caption("Sessao multiplayer")
            max_suportado = max(1, min(6, len(jogadores)))
            quantidade = st.selectbox(
                "Quantidade de jogadores na sessao",
                options=list(range(1, max_suportado + 1)),
                index=min(
                    st.session_state.get("session_player_count", 1),
                    max_suportado,
                ) - 1,
                key="session_player_count_select",
            )
            st.session_state.session_player_count = quantidade

            opcoes = {f"{player['nome']} ({player['xp']} XP)": player["id"] for player in jogadores}
            selecionados_padrao = st.session_state.get(
                "session_player_ids",
                ids[:quantidade],
            )
            labels_default = [label for label, player_id in opcoes.items() if player_id in selecionados_padrao]
            escolhidos = st.multiselect(
                "Jogadores da rodada",
                options=list(opcoes.keys()),
                default=labels_default[:quantidade],
                max_selections=quantidade,
                key="session_players_multiselect",
            )
            escolhidos_ids = [opcoes[label] for label in escolhidos][:quantidade]
            if not escolhidos_ids and ids:
                escolhidos_ids = ids[:quantidade]
            elif len(escolhidos_ids) < quantidade:
                for player_id in ids:
                    if player_id not in escolhidos_ids:
                        escolhidos_ids.append(player_id)
                    if len(escolhidos_ids) == quantidade:
                        break
            st.session_state.session_player_ids = escolhidos_ids
            st.write(f"Participantes ativos: {len(st.session_state.session_player_ids)}")

    with st.sidebar.container(border=True):
        st.markdown(f"**Jogador:** {dados.get('nome', 'Anônimo')}")
        st.write(f"XP total: {dados.get('xp', 0)}")
        st.write(f"Nivel: {dados.get('xp', 0) // 100 + 1}")
        st.write(f"Vidas: {dados.get('vidas', 0)} / 5")
        st.write(f"Partidas: {dados.get('jogos_jogados', 0)}")
        st.write(f"Dificuldade atual: {player_manager.dificuldade().title()}")
        if dados.get("modo_dificuldade", "automatico") == "automatico":
            st.caption("A dificuldade acompanha o progresso do perfil.")
        else:
            st.caption("A dificuldade esta travada no modo manual.")

    with st.sidebar.container(border=True):
        st.caption("Configuracao de dificuldade")
        modo_atual = dados.get("modo_dificuldade", "automatico")
        modo = st.radio(
            "Modo",
            options=["automatico", "manual"],
            index=0 if modo_atual == "automatico" else 1,
            horizontal=True,
            key="modo_dificuldade_sidebar",
        )
        dificuldade_manual = st.selectbox(
            "Nivel manual",
            options=["facil", "medio", "dificil"],
            index=["facil", "medio", "dificil"].index(dados.get("dificuldade_manual", "medio")),
            disabled=modo != "manual",
            key="dificuldade_manual_sidebar",
        )
        if (
            modo != modo_atual
            or dificuldade_manual != dados.get("dificuldade_manual", "medio")
        ):
            player_manager.configurar_dificuldade(modo, dificuldade_manual)
            st.rerun()

    with st.sidebar.container(border=True):
        st.caption("Acessibilidade")
        st.toggle("Alto contraste", key="accessibility_high_contrast")
        st.toggle("Fonte ampliada", key="accessibility_large_text")
        st.toggle("Reduzir efeitos visuais", value=True, key="accessibility_reduce_motion")
        st.toggle("Leitura automatica da tela", key="accessibility_auto_read")
        st.select_slider(
            "Velocidade da leitura",
            options=[0.8, 1.0, 1.2, 1.4],
            value=st.session_state.get("accessibility_reader_speed", 1.0),
            key="accessibility_reader_speed",
        )
        if st.button("Ler tela atual", use_container_width=True):
            st.session_state.accessibility_read_now = True
            st.rerun()
        st.caption("Esses ajustes ajudam em contraste, leitura, foco visual e uso com leitores de tela do navegador.")

    st.sidebar.write("Navegacao")
    if st.sidebar.button("Inicio", use_container_width=True):
        st.session_state.pagina = "🏠 Home"
        st.rerun()

    if st.sidebar.button("Ranking", use_container_width=True):
        st.session_state.pagina = "🏆 Ranking"
        st.rerun()

    if st.sidebar.button("Circuito Aleatorio", use_container_width=True):
        st.session_state.pagina = "🎲 Circuito Aleatorio"
        st.rerun()

    if st.sidebar.button("Como usar", use_container_width=True):
        st.session_state.pagina = "📘 Como Usar"
        st.rerun()

    if st.sidebar.button("Mudar nome", use_container_width=True):
        st.session_state.mudar_nome = True
        st.rerun()

    if jogos:
        st.sidebar.divider()
        st.sidebar.caption("Jogos disponiveis")
        for jogo in jogos:
            if st.sidebar.button(jogo, key=f"nav_{jogo}", use_container_width=True):
                st.session_state.pagina = jogo
                st.rerun()
