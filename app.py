import json
import streamlit as st
from datetime import datetime, timezone
from random import shuffle

from core.engine.manager import GameManager
from core.player_manager import PlayerManager
from core.ranking_manager import RankingManager
from ui.components import (
    render_accessibility_reader,
    render_answer_panel,
    game_card,
    metric_card,
    render_championship_row,
    render_game_intro,
    render_page_hero,
    render_side_panel,
    render_spotlight_panel,
    render_step_guide,
)
from ui.layout import sidebar
from ui.theme import aplicar_tema

CIRCUIT_PAGE = "🎲 Circuito Aleatorio"
GUIDE_PAGE = "📘 Como Usar"
MENU_PAGE = "🧭 Menu da Sessao"
SAVE_BUNDLE_VERSION = 1
SESSION_SAVE_KEYS = {
    "pagina",
    "jogo_atual",
    "session_player_ids",
    "session_player_count",
    "multiplayer_game_mode",
    "multiplayer_turn_mode",
    "accessibility_high_contrast",
    "accessibility_large_text",
    "accessibility_reduce_motion",
    "accessibility_auto_read",
    "accessibility_reader_speed",
    "circuito",
    "adivinhacao",
    "analogias",
    "antonimos",
    "categorias",
    "code_lab",
    "forca",
    "intruso",
    "matematica",
    "memoria",
    "quiz",
    "scramble",
    "sequencia",
    "sinonimos",
    "verdadeiro_falso",
}


def carregar_infos_jogos(manager: GameManager, player: PlayerManager) -> dict:
    infos = {}

    for nome in manager.listar_jogos():
        chaves_antes = set(st.session_state.keys())
        jogo = manager.criar_jogo(nome, player)
        infos[nome] = jogo.obter_info()
        chaves_depois = set(st.session_state.keys())

        for chave in chaves_depois - chaves_antes:
            del st.session_state[chave]

    return infos


def build_progress_snapshot(player_manager: PlayerManager, ranking_manager: RankingManager) -> dict:
    session_data = {}
    for chave in SESSION_SAVE_KEYS:
        if chave in st.session_state:
            session_data[chave] = st.session_state[chave]

    for chave in st.session_state.keys():
        if chave.startswith("controle_") or chave.startswith("turnos_"):
            session_data[chave] = st.session_state[chave]

    return {
        "version": SAVE_BUNDLE_VERSION,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "player_store": player_manager.store,
        "ranking": ranking_manager.ranking,
        "session": session_data,
    }


def restore_progress_snapshot(snapshot: dict, player_manager: PlayerManager, ranking_manager: RankingManager):
    if not isinstance(snapshot, dict):
        raise ValueError("Arquivo invalido: formato de progresso nao reconhecido.")

    version = snapshot.get("version")
    if version is None:
        raise ValueError("Arquivo invalido: versao do progresso ausente.")
    if version > SAVE_BUNDLE_VERSION:
        raise ValueError("Arquivo de progresso criado por uma versao mais nova do app.")

    player_store = snapshot.get("player_store")
    ranking = snapshot.get("ranking")
    session_data = snapshot.get("session", {})

    if not isinstance(player_store, dict) or not isinstance(ranking, dict) or not isinstance(session_data, dict):
        raise ValueError("Arquivo invalido: dados obrigatorios ausentes.")

    player_manager.importar_store(player_store)
    ranking_manager.importar_ranking(ranking)

    for chave in list(st.session_state.keys()):
        del st.session_state[chave]

    for chave, valor in session_data.items():
        st.session_state[chave] = valor

    st.session_state.progress_feedback = "Progresso importado com sucesso."


def get_session_player_ids(player_manager: PlayerManager):
    jogadores = player_manager.listar_jogadores()
    ids_disponiveis = [item["id"] for item in jogadores]
    selecionados = st.session_state.get("session_player_ids", [])
    selecionados = [player_id for player_id in selecionados if player_id in ids_disponiveis]

    quantidade = st.session_state.get("session_player_count", 1)
    if not selecionados and ids_disponiveis:
        selecionados = ids_disponiveis[:quantidade]

    if len(selecionados) < quantidade:
        for player_id in ids_disponiveis:
            if player_id not in selecionados:
                selecionados.append(player_id)
            if len(selecionados) == quantidade:
                break

    st.session_state.session_player_ids = selecionados[:quantidade]
    return st.session_state.session_player_ids


def get_session_players(player_manager: PlayerManager):
    return player_manager.listar_jogadores_por_ids(get_session_player_ids(player_manager))


def multiplayer_ativo(player_manager: PlayerManager) -> bool:
    return st.session_state.get("multiplayer_game_mode", True) and len(get_session_player_ids(player_manager)) > 1


def get_multiplayer_turn_mode() -> str:
    return st.session_state.get("multiplayer_turn_mode", "round")


def multiplayer_turn_mode_label() -> str:
    return {
        "round": "Um desafio por jogador",
        "lose": "Errou, passou a vez",
    }.get(get_multiplayer_turn_mode(), "Um desafio por jogador")


def deve_avancar_turno_apos_resultado(player_manager: PlayerManager, resultado) -> bool:
    if not multiplayer_ativo(player_manager) or not resultado:
        return False

    if get_multiplayer_turn_mode() == "round":
        return resultado.correto or resultado.finalizado

    return not resultado.correto


def get_game_turn_state(pagina: str, player_manager: PlayerManager):
    chave = f"turnos_{pagina}"
    player_ids = get_session_player_ids(player_manager)
    if (
        chave not in st.session_state
        or st.session_state[chave].get("player_ids") != player_ids
    ):
        st.session_state[chave] = {
            "player_ids": player_ids,
            "player_index": 0,
            "round": 1,
        }
    return st.session_state[chave]


def limpar_turnos_jogo(pagina: str):
    chave = f"turnos_{pagina}"
    if chave in st.session_state:
        del st.session_state[chave]


def sincronizar_jogador_do_turno(pagina: str, player_manager: PlayerManager):
    if not multiplayer_ativo(player_manager):
        limpar_turnos_jogo(pagina)
        return

    turno = get_game_turn_state(pagina, player_manager)
    player_ids = turno["player_ids"]
    if not player_ids:
        return
    current_player_id = player_ids[turno["player_index"]]
    if player_manager.dados().get("id") != current_player_id:
        player_manager.definir_jogador_ativo(current_player_id)
        clear_current_game_state()
        st.session_state.jogo_atual = pagina
        st.rerun()


def avancar_turno_jogo(pagina: str, player_manager: PlayerManager):
    if not multiplayer_ativo(player_manager):
        return

    turno = get_game_turn_state(pagina, player_manager)
    total = max(1, len(turno["player_ids"]))
    turno["player_index"] = (turno["player_index"] + 1) % total
    if turno["player_index"] == 0:
        turno["round"] += 1
    clear_current_game_state()
    proximo_id = turno["player_ids"][turno["player_index"]]
    player_manager.definir_jogador_ativo(proximo_id)


def init_circuit_state(jogos: list[str], player_manager: PlayerManager):
    player_ids = get_session_player_ids(player_manager)
    ordem = list(jogos)
    shuffle(ordem)
    st.session_state.circuito = {
        "game_order": ordem,
        "game_index": 0,
        "player_ids": player_ids,
        "player_index": 0,
        "scores": {player_id: 0 for player_id in player_ids},
        "history": [],
        "waiting_next": False,
        "last_result": None,
        "retry_result": None,
        "completed": False,
    }


def clear_current_game_state():
    if "jogo_ativo" in st.session_state:
        del st.session_state.jogo_ativo
    if "ultimo_resultado" in st.session_state:
        del st.session_state.ultimo_resultado
    for chave in list(st.session_state.keys()):
        if chave.startswith("controle_"):
            del st.session_state[chave]


def finalize_circuit_stage(player_manager: PlayerManager, ranking: RankingManager, jogo, jogo_nome: str, resultado):
    circuito = st.session_state.circuito
    player_id = circuito["player_ids"][circuito["player_index"]]
    circuito["scores"][player_id] = circuito["scores"].get(player_id, 0) + max(0, resultado.pontos)
    circuito["history"].append(
        {
            "player_id": player_id,
            "jogo": jogo_nome,
            "correto": resultado.correto,
            "pontos": resultado.pontos,
            "mensagem": resultado.mensagem,
        }
    )
    if resultado.correto and resultado.pontos > 0:
        ranking.adicionar_score(player_manager.dados()["nome"], jogo_nome, resultado.pontos)

    circuito["last_result"] = {
        "player_nome": player_manager.dados()["nome"],
        "jogo": jogo_nome,
        "correto": resultado.correto,
        "pontos": resultado.pontos,
        "mensagem": resultado.mensagem,
    }
    circuito["retry_result"] = None
    circuito["waiting_next"] = True

    if hasattr(jogo, "resetar_jogo"):
        jogo.resetar_jogo()
    clear_current_game_state()


def next_circuit_stage():
    circuito = st.session_state.circuito
    circuito["game_index"] += 1
    circuito["player_index"] = (circuito["player_index"] + 1) % max(1, len(circuito["player_ids"]))
    circuito["waiting_next"] = False
    circuito["last_result"] = None
    circuito["retry_result"] = None
    if circuito["game_index"] >= len(circuito["game_order"]):
        circuito["completed"] = True


def processar_resultado_padrao(jogo, pagina: str, resultado, ranking: RankingManager, player: PlayerManager):
    st.session_state.ultimo_resultado = resultado

    if resultado.correto and resultado.pontos > 0:
        ranking.adicionar_score(player.dados()["nome"], pagina, resultado.pontos)

    if resultado.finalizado and resultado.correto:
        if hasattr(jogo, "resetar_jogo"):
            jogo.resetar_jogo()
        del st.session_state.jogo_ativo
        controle_key = f"controle_{pagina}"
        if controle_key in st.session_state:
            del st.session_state[controle_key]


def processar_resultado_circuito(player_manager: PlayerManager, ranking: RankingManager, jogo, jogo_nome: str, resultado):
    if resultado.correto or resultado.finalizado:
        finalize_circuit_stage(player_manager, ranking, jogo, jogo_nome, resultado)
        return

    st.session_state.circuito["retry_result"] = resultado


def resumo_dificuldade(player: PlayerManager) -> str:
    dados = player.dados()
    if dados.get("modo_dificuldade", "automatico") == "manual":
        return f"Manual: {dados.get('dificuldade_manual', 'medio').title()}"
    return f"Automatico: {player.dificuldade().title()}"


def montar_resumo_acessivel(pagina: str, player: PlayerManager, jogos: list[str]) -> str:
    base = (
        f"Pagina atual: {pagina}. Jogador ativo: {player.dados().get('nome', 'Sem nome')}. "
        f"Nivel {player.nivel()}, {player.vidas()} vidas e {player.dados().get('xp', 0)} pontos de experiencia. "
    )
    if pagina == "🏠 Home":
        return base + f"Home do arcade com {len(jogos)} jogos disponiveis, ranking e circuito aleatorio."
    if pagina == "🏆 Ranking":
        return base + "Tela de ranking com classificacao de jogadores por jogo ou no placar global."
    if pagina == MENU_PAGE:
        return base + "Menu central da sessao com perfis, multiplayer, acessibilidade, dificuldade e atalhos para todos os jogos."
    if pagina == CIRCUIT_PAGE:
        return base + "Tela de circuito aleatorio com rotacao entre os participantes da sessao."
    if pagina == GUIDE_PAGE:
        return base + "Tela de ajuda com manual passo a passo, orientacoes de acessibilidade e fluxo recomendado para usar o arcade."
    return base + f"Voce esta dentro do jogo {pagina}. Use o painel lateral para consultar vidas, dicas e progresso."


def render_circuit_page(manager: GameManager, player_manager: PlayerManager, ranking: RankingManager, jogos: list[str]):
    participantes = get_session_players(player_manager)
    if not participantes:
        st.warning("Crie ao menos um perfil para iniciar o circuito.")
        return

    if "circuito" not in st.session_state or st.session_state.circuito.get("player_ids") != [p["id"] for p in participantes]:
        init_circuit_state(jogos, player_manager)

    circuito = st.session_state.circuito

    if circuito["completed"]:
        st.subheader("Circuito concluido")
        st.write("Todos os jogos do baralho aleatorio foram usados nesta sessao.")
        for participante in participantes:
            pontos = circuito["scores"].get(participante["id"], 0)
            with st.container(border=True):
                st.write(f"**{participante['nome']}**")
                st.caption(f"{pontos} pontos acumulados no circuito")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Reiniciar circuito", use_container_width=True):
                init_circuit_state(jogos, player_manager)
                st.rerun()
        with col2:
            if st.button("Voltar para home", use_container_width=True):
                del st.session_state.circuito
                st.session_state.pagina = "🏠 Home"
                st.rerun()
        return

    current_player_id = circuito["player_ids"][circuito["player_index"]]
    if player_manager.dados().get("id") != current_player_id:
        player_manager.definir_jogador_ativo(current_player_id)
        st.rerun()

    jogo_nome = circuito["game_order"][circuito["game_index"]]
    progresso = st.columns(3)
    with progresso[0]:
        metric_card("Rodada", f"{circuito['game_index'] + 1} / {len(circuito['game_order'])}")
    with progresso[1]:
        metric_card("Jogador da vez", player_manager.dados()["nome"])
    with progresso[2]:
        metric_card("Jogo sorteado", jogo_nome)

    if circuito["waiting_next"]:
        ultimo = circuito["last_result"]
        if ultimo["correto"]:
            st.success(f"{ultimo['player_nome']} acertou em {ultimo['jogo']} e fez {ultimo['pontos']} pontos.")
        else:
            st.error(f"{ultimo['player_nome']} errou em {ultimo['jogo']}.")
        st.write(ultimo["mensagem"])
        if st.button("Proximo desafio", use_container_width=True):
            next_circuit_stage()
            st.rerun()
        return

    if circuito.get("retry_result"):
        st.error(circuito["retry_result"].mensagem)
        st.caption("A rodada continua ativa. Ajuste a resposta atual ou use uma dica antes de enviar novamente.")
        if st.button("Tentar novamente", key="tentar_novamente_circuito", use_container_width=True):
            circuito["retry_result"] = None
            st.rerun()

    if "jogo_ativo" not in st.session_state:
        if player_manager.vidas() <= 0:
            player_manager.resetar_vidas()
        st.session_state.jogo_ativo = manager.criar_jogo(jogo_nome, player_manager)

    jogo = st.session_state.jogo_ativo
    info = jogo.obter_info()
    controle_partida = inicializar_controles_partida(jogo, CIRCUIT_PAGE)
    desafio = jogo.gerar_desafio()

    render_game_intro(info)
    barra = st.columns([1.2, 1, 1])
    with barra[0]:
        metric_card("Dicas restantes", str(max(0, controle_partida["max_dicas"] - controle_partida["dicas_usadas"])))
    with barra[1]:
        metric_card("Custo da dica", f"-{controle_partida['custo_dica_xp']} XP")
    with barra[2]:
        if st.button("Usar dica", key="dica_circuito", use_container_width=True, disabled=controle_partida["dicas_usadas"] >= controle_partida["max_dicas"]):
            dica = jogo.obter_dica()
            if dica:
                controle_partida["dicas_usadas"] += 1
                controle_partida["ultima_dica"] = dica
                player_manager.perder_pontos(controle_partida["custo_dica_xp"])
                st.rerun()

    if controle_partida.get("ultima_dica"):
        st.info(f"Dica ativa: {controle_partida['ultima_dica']}")

    jogo.renderizar(desafio)

    if "temp_letra" in st.session_state:
        resposta = st.session_state.temp_letra
        del st.session_state.temp_letra
        resultado = jogo.verificar_resposta(str(resposta))
        processar_resultado_circuito(player_manager, ranking, jogo, jogo_nome, resultado)
        st.rerun()

    config = jogo.configurar_input()
    if config.tipo != "none":
        render_answer_panel(
            "Envie sua resposta nesta area",
            "Use o campo logo abaixo para responder ao desafio atual. Se errar e a rodada continuar ativa, ajuste a resposta e envie novamente.",
            config.label,
            jogo.obter_contexto_resposta(desafio) or "",
        )
        with st.form(key=f"form_circuito_{jogo_nome}"):
            resposta = renderizar_input(config, f"circuito_{jogo_nome}")
            submitted = st.form_submit_button("Enviar resposta", use_container_width=True)
            if submitted and resposta not in ("", None):
                resultado = jogo.verificar_resposta(str(resposta))
                processar_resultado_circuito(player_manager, ranking, jogo, jogo_nome, resultado)
                st.rerun()
    else:
        st.info("Conclua a etapa atual do jogo para enviar a resposta desta rodada.")


def render_menu_page(jogos: list[str], player_manager: PlayerManager, ranking: RankingManager):
    dados = player_manager.dados()
    jogadores = player_manager.listar_jogadores()

    if st.session_state.get("progress_feedback"):
        st.success(st.session_state.pop("progress_feedback"))
    if st.session_state.get("progress_error"):
        st.error(st.session_state.pop("progress_error"))

    render_page_hero(
        "Menu da Sessao",
        "Use esta pagina como centro de comando do arcade: perfis, dificuldade, multiplayer, acessibilidade e atalhos para os jogos.",
        "Controle Central",
    )

    col_config, col_nav = st.columns([1.35, 1])
    with col_config:
        with st.container(border=True):
            st.subheader("Perfis")
            if jogadores:
                labels = [f"{player['nome'] or 'Sem nome'} ({player['xp']} XP)" for player in jogadores]
                ids = [player["id"] for player in jogadores]
                indice_atual = ids.index(dados.get("id")) if dados.get("id") in ids else 0
                selecionado = st.selectbox(
                    "Perfil ativo",
                    options=labels,
                    index=indice_atual,
                    key="perfil_ativo_menu",
                )
                player_id = ids[labels.index(selecionado)]
                if player_id != dados.get("id"):
                    player_manager.definir_jogador_ativo(player_id)
                    clear_current_game_state()
                    st.rerun()

            novo_nome = st.text_input("Criar novo perfil", key="novo_jogador_menu")
            acoes_perfil = st.columns(2)
            with acoes_perfil[0]:
                if st.button("Criar perfil", key="criar_perfil_menu", use_container_width=True) and novo_nome.strip():
                    player_manager.criar_jogador(novo_nome)
                    st.rerun()
            with acoes_perfil[1]:
                if st.button("Editar nome atual", key="editar_nome_menu", use_container_width=True):
                    st.session_state.mudar_nome = True
                    st.rerun()

            if jogadores:
                opcoes_exclusao = {
                    f"{player['nome'] or 'Sem nome'} ({player['xp']} XP)": player["id"]
                    for player in jogadores
                }
                selecionado_exclusao = st.selectbox(
                    "Perfil para excluir",
                    options=list(opcoes_exclusao.keys()),
                    key="excluir_perfil_menu",
                )
                confirmar_exclusao = st.checkbox(
                    "Confirmo a exclusao deste perfil local.",
                    key="confirmar_exclusao_menu",
                )
                if st.button("Excluir perfil", key="excluir_perfil_botao_menu", use_container_width=True):
                    if confirmar_exclusao:
                        player_manager.excluir_jogador(opcoes_exclusao[selecionado_exclusao])
                        st.session_state.session_player_ids = [
                            player_id
                            for player_id in st.session_state.get("session_player_ids", [])
                            if player_id in [player["id"] for player in player_manager.listar_jogadores()]
                        ]
                        clear_current_game_state()
                        st.rerun()

        with st.container(border=True):
            st.subheader("Dificuldade e multiplayer")
            modo_atual = dados.get("modo_dificuldade", "automatico")
            modo = st.radio(
                "Modo de dificuldade",
                options=["automatico", "manual"],
                index=0 if modo_atual == "automatico" else 1,
                horizontal=True,
                key="modo_dificuldade_menu",
            )
            dificuldade_manual = st.selectbox(
                "Nivel manual",
                options=["facil", "medio", "dificil"],
                index=["facil", "medio", "dificil"].index(dados.get("dificuldade_manual", "medio")),
                disabled=modo != "manual",
                key="dificuldade_manual_menu",
            )
            if modo != modo_atual or dificuldade_manual != dados.get("dificuldade_manual", "medio"):
                player_manager.configurar_dificuldade(modo, dificuldade_manual)
                st.rerun()

            if jogadores:
                ids = [player["id"] for player in jogadores]
                max_suportado = max(1, min(6, len(jogadores)))
                quantidade = st.selectbox(
                    "Quantidade de jogadores na sessao",
                    options=list(range(1, max_suportado + 1)),
                    index=min(st.session_state.get("session_player_count", 1), max_suportado) - 1,
                    key="session_player_count_menu",
                )
                st.session_state.session_player_count = quantidade

                opcoes = {f"{player['nome']} ({player['xp']} XP)": player["id"] for player in jogadores}
                selecionados_padrao = st.session_state.get("session_player_ids", ids[:quantidade])
                labels_default = [label for label, player_id in opcoes.items() if player_id in selecionados_padrao]
                escolhidos = st.multiselect(
                    "Jogadores da rodada",
                    options=list(opcoes.keys()),
                    default=labels_default[:quantidade],
                    max_selections=quantidade,
                    key="session_players_menu",
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

            st.toggle(
                "Ativar modo multiplayer nos jogos individuais",
                value=st.session_state.get("multiplayer_game_mode", True),
                key="multiplayer_game_mode",
            )
            if st.session_state.get("multiplayer_game_mode", True):
                st.radio(
                    "Regra de troca de jogador",
                    options=["round", "lose"],
                    index=0 if get_multiplayer_turn_mode() == "round" else 1,
                    format_func=lambda valor: {
                        "round": "Cada jogador responde um desafio",
                        "lose": "Errou, passou a vez",
                    }[valor],
                    key="multiplayer_turn_mode",
                )
                st.caption(
                    "No primeiro modo, a vez troca quando o desafio termina. No segundo, qualquer erro passa a vez para o proximo jogador."
                )
            else:
                st.caption("Ative o multiplayer para alternar jogadores nos desafios individuais.")

        with st.container(border=True):
            st.subheader("Acessibilidade")
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
            if st.button("Ler tela atual", key="ler_tela_menu", use_container_width=True):
                st.session_state.accessibility_read_now = True
                st.rerun()

        with st.container(border=True):
            st.subheader("Salvar e retomar progresso")
            snapshot = build_progress_snapshot(player_manager, ranking)
            st.caption("Exporte um arquivo para continuar depois ou importe um progresso salvo anteriormente.")
            col_download, col_upload = st.columns(2)
            with col_download:
                st.download_button(
                    "Baixar progresso",
                    data=json.dumps(snapshot, ensure_ascii=False, indent=2),
                    file_name="arcade-cognitivo-save.json",
                    mime="application/json",
                    use_container_width=True,
                )
                st.caption("Inclui perfis, ranking, sessao ativa, configuracoes e parte do estado dos jogos.")
            with col_upload:
                arquivo_importado = st.file_uploader(
                    "Selecionar arquivo de progresso",
                    type=["json"],
                    key="progress_import_file",
                    help="Use um arquivo exportado pelo proprio app para continuar de onde parou.",
                )
                if arquivo_importado:
                    st.caption(f"Arquivo selecionado: {arquivo_importado.name}")
                else:
                    st.caption("Nenhum arquivo selecionado.")
                if st.button(
                    "Restaurar progresso",
                    key="restaurar_progresso_menu",
                    use_container_width=True,
                    disabled=arquivo_importado is None,
                ):
                    try:
                        snapshot_importado = json.loads(arquivo_importado.getvalue().decode("utf-8"))
                        restore_progress_snapshot(snapshot_importado, player_manager, ranking)
                    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                        st.session_state.progress_error = f"Nao foi possivel importar o progresso: {exc}"
                    st.rerun()

    with col_nav:
        render_side_panel(
            "Resumo da Sessao",
            [
                ("Jogador ativo", dados.get("nome", "Anônimo")),
                ("XP total", str(dados.get("xp", 0))),
                ("Nivel", str(player_manager.nivel())),
                ("Vidas", f"{player_manager.vidas()} / 5"),
                ("Participantes", str(len(get_session_players(player_manager)))),
                ("Modo multi", "Ligado" if multiplayer_ativo(player_manager) else "Desligado"),
                ("Troca de vez", multiplayer_turn_mode_label() if multiplayer_ativo(player_manager) else "Nao se aplica"),
            ],
            "Use este menu para ajustar a sessao e depois volte para Home ou abra qualquer jogo diretamente.",
        )
        render_step_guide(
            "Fluxo recomendado da sessao",
            [
                ("Escolha o perfil ativo", "Defina quem esta com a vez principal antes de abrir um jogo."),
                ("Monte a sessao", "Selecione os jogadores que participarao do multiplayer local."),
                ("Ajuste a dificuldade", "Deixe automatico para progressao ou use o manual para controlar o nivel."),
                ("Abra um jogo", "Volte para a Home ou entre direto em um desafio pela lista abaixo."),
            ],
            kicker="Sessao",
        )
        st.markdown("### Atalhos rapidos")
        if st.button("Ir para Home", key="atalho_home_menu", use_container_width=True):
            st.session_state.pagina = "🏠 Home"
            st.rerun()
        if st.button("Ir para Ranking", key="atalho_rank_menu", use_container_width=True):
            st.session_state.pagina = "🏆 Ranking"
            st.rerun()
        if st.button("Ir para Circuito Aleatorio", key="atalho_circuito_menu", use_container_width=True):
            st.session_state.pagina = CIRCUIT_PAGE
            st.rerun()

        st.markdown("### Abrir jogo")
        for jogo in jogos:
            if st.button(jogo, key=f"menu_jogo_{jogo}", use_container_width=True):
                st.session_state.pagina = jogo
                st.rerun()


def inicializar_controles_partida(jogo, pagina: str):
    controle_key = f"controle_{pagina}"
    info = jogo.obter_info()
    if controle_key not in st.session_state:
        st.session_state[controle_key] = {
            "dicas_usadas": 0,
            "ultima_dica": "",
            "max_dicas": info.max_dicas,
            "custo_dica_xp": info.custo_dica_xp,
        }
    return st.session_state[controle_key]


def renderizar_input(config, pagina: str):
    key_base = f"input_{pagina}"

    if config.tipo == "none":
        return ""

    if config.tipo == "radio":
        return st.radio(
            config.label,
            options=config.opcoes,
            key=f"{key_base}_radio",
            horizontal=True,
        )

    if config.tipo == "segmented":
        if hasattr(st, "segmented_control"):
            return st.segmented_control(
                config.label,
                options=config.opcoes,
                key=f"{key_base}_segmented",
                selection_mode="single",
            )
        return st.radio(
            config.label,
            options=config.opcoes,
            key=f"{key_base}_segmented_fallback",
            horizontal=True,
        )

    if config.tipo == "number":
        return st.number_input(
            config.label,
            min_value=config.min_value,
            max_value=config.max_value,
            step=1,
            key=f"{key_base}_number",
        )

    return st.text_input(
        config.label,
        placeholder=config.placeholder or "Digite sua resposta aqui",
        max_chars=config.max_chars,
        key=f"{key_base}_text",
    ).strip()


def exibir_feedback(jogo) -> bool:
    jogo_perdido = False

    if "ultimo_resultado" not in st.session_state:
        return jogo_perdido

    resultado = st.session_state.ultimo_resultado
    if resultado.correto:
        st.success(f"{resultado.mensagem} (+{resultado.pontos} XP)")
    else:
        st.error(resultado.mensagem)
        st.caption("O desafio continua ativo. Ajuste sua resposta ou use uma dica antes de tentar de novo.")
        if not resultado.finalizado:
            if st.button("Tentar novamente", key="tentar_novamente_padrao", use_container_width=True):
                del st.session_state.ultimo_resultado
                st.rerun()
        if resultado.finalizado:
            jogo_perdido = True

    return jogo_perdido


def encerrar_jogo(jogo):
    if "ultimo_resultado" in st.session_state:
        del st.session_state.ultimo_resultado
    if hasattr(jogo, "resetar_jogo"):
        jogo.resetar_jogo()
    if "jogo_ativo" in st.session_state:
        del st.session_state.jogo_ativo
    pagina = st.session_state.get("pagina")
    if pagina:
        controle_key = f"controle_{pagina}"
        if controle_key in st.session_state:
            del st.session_state[controle_key]


aplicar_tema()

manager = GameManager()
player = PlayerManager()
ranking = RankingManager()
jogos = manager.listar_jogos()

if st.session_state.get("active_player_id") != player.dados().get("id"):
    st.session_state.active_player_id = player.dados().get("id")
    if "jogo_ativo" in st.session_state:
        del st.session_state.jogo_ativo
    if "ultimo_resultado" in st.session_state:
        del st.session_state.ultimo_resultado
    for chave in list(st.session_state.keys()):
        if chave.startswith("controle_"):
            del st.session_state[chave]

if "catalogo_jogos" not in st.session_state:
    st.session_state.catalogo_jogos = carregar_infos_jogos(manager, player)

if not player.tem_jogadores() or st.session_state.get("mudar_nome"):
    render_page_hero(
        "Arcade Cognitivo",
        "Crie ou edite perfis locais para jogar sozinho, em rotacao entre amigos ou em circuitos multiplayer.",
        "Perfis Locais",
    )

    nome_atual = player.dados().get("nome", "")
    nome = st.text_input("Nome do jogador", value=nome_atual, key="nome_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Salvar perfil", use_container_width=True) and nome.strip():
            if player.tem_jogadores():
                player.set_nome(nome)
            else:
                player.criar_jogador(nome)
            if "mudar_nome" in st.session_state:
                del st.session_state.mudar_nome
            st.rerun()
    with col2:
        if st.session_state.get("mudar_nome") and st.button("Cancelar", use_container_width=True):
            del st.session_state.mudar_nome
            st.rerun()

    st.stop()

sidebar(jogos, player.dados(), player)
pagina = st.session_state.get("pagina", "🏠 Home")
resumo_acessivel = montar_resumo_acessivel(pagina, player, jogos)

forcar_leitura = st.session_state.pop("accessibility_read_now", False)
if st.session_state.get("accessibility_auto_read"):
    if st.session_state.get("accessibility_last_summary") != resumo_acessivel:
        st.session_state.accessibility_last_summary = resumo_acessivel
        forcar_leitura = True

render_accessibility_reader(
    resumo_acessivel,
    forcar_leitura=forcar_leitura,
    auto=False,
    velocidade=st.session_state.get("accessibility_reader_speed", 1.0),
)

topo = st.columns(4)
with topo[0]:
    metric_card("Jogador", player.dados()["nome"])
with topo[1]:
    metric_card("XP Total", str(player.dados()["xp"]))
with topo[2]:
    metric_card("Nivel", str(player.nivel()))
with topo[3]:
    metric_card("Vidas", f"{player.vidas()} / 5", f"Dificuldade: {player.dificuldade().title()}")
st.caption(f"Sessao com {len(get_session_players(player))} jogador(es) ativo(s).")

if pagina == "🏠 Home":
    render_page_hero(
        "Escolha o Proximo Desafio",
        "Explore o catalogo, entre no circuito aleatorio ou siga a trilha de programacao no Code Lab.",
        "Hub Principal",
    )
    destaque, atalhos = st.columns([1.35, 1])
    with destaque:
        render_spotlight_panel(
            "Catálogo premium para raciocínio e tecnologia",
            "A home agora funciona como um hub de arcade: escolha partidas rápidas, avance pelo Code Lab ou monte uma maratona com todos os jogos.",
            [
                f"{len(jogos)} jogos ativos",
                f"{len(get_session_players(player))} jogadores na sessao",
                resumo_dificuldade(player),
            ],
        )
    with atalhos:
        render_side_panel(
            "Resumo da Sessao",
            [
                ("Jogador ativo", player.dados()["nome"]),
                ("XP total", str(player.dados()["xp"])),
                ("Nivel atual", str(player.nivel())),
                ("Vidas", f"{player.vidas()} / 5"),
            ],
            "Use o circuito aleatorio para transformar todo o catalogo em uma partida unica com rotacao entre perfis.",
        )

    guia_home, acoes_rapidas = st.columns([1.35, 1])
    with guia_home:
        render_step_guide(
            "Comece em menos de 2 minutos",
            [
                ("Crie ou selecione um perfil", "Use a sidebar para definir o jogador ativo, configurar dificuldade e montar a sessao multiplayer."),
                ("Escolha um modo de jogo", "Abra um desafio individual, experimente o Code Lab ou rode o Circuito Aleatorio com todos os jogos."),
                ("Use vidas, dicas e feedback", "Cada rodada mostra progresso, dicas restantes e mensagens de acerto ou erro para orientar a partida."),
                ("Acompanhe o ranking", "Compare pontuacoes no ranking global ou por jogo para medir evolucao individual e entre amigos."),
            ],
            kicker="Inicio rapido",
        )
    with acoes_rapidas:
        render_side_panel(
            "Fluxo Recomendado",
            [
                ("1", "Criar perfil"),
                ("2", "Escolher dificuldade"),
                ("3", "Montar sessao"),
                ("4", "Abrir jogo"),
            ],
            "Se quiser um tour completo, abra a pagina Como Usar no menu lateral.",
        )

    st.markdown("<div class='home-grid-note'>Modos disponiveis no arcade</div>", unsafe_allow_html=True)
    colunas = st.columns(3)

    for indice, jogo_nome in enumerate(jogos):
        info = st.session_state.catalogo_jogos[jogo_nome]
        with colunas[indice % 3]:
            if game_card(info, button_key=f"card_{jogo_nome}"):
                st.session_state.pagina = jogo_nome
                st.rerun()

    st.divider()
    acoes = st.columns(2)
    with acoes[0]:
        if st.button("Ver ranking", use_container_width=True):
            st.session_state.pagina = "🏆 Ranking"
            st.rerun()
    with acoes[1]:
        if st.button("Iniciar circuito aleatorio", use_container_width=True):
            if "circuito" in st.session_state:
                del st.session_state.circuito
            clear_current_game_state()
            st.session_state.pagina = CIRCUIT_PAGE
            st.rerun()

elif pagina == "🏆 Ranking":
    render_page_hero(
        "Ranking de Jogadores",
        "Compare a pontuacao dos perfis locais por jogo ou no acumulado geral.",
        "Competicao Local",
    )

    filtro = st.selectbox(
        "Filtrar por",
        ["Global"] + ranking.get_jogos(),
        key="filtro_ranking",
    )

    if filtro == "Global":
        rank = ranking.get_ranking_global()
        titulo = "Ranking global"
    else:
        rank = ranking.get_ranking_jogo(filtro)
        titulo = f"Ranking de {filtro}"
    painel_rank, painel_stats = st.columns([1.55, 1])
    with painel_rank:
        st.write(f"### {titulo}")
        if rank:
            for i, (nome, score) in enumerate(rank[:10], 1):
                render_championship_row(i, nome, score, "" if filtro == "Global" else filtro)
        else:
            st.info("Ainda nao ha pontuacoes registradas.")
    with painel_stats:
        total_jogos_rank = len(ranking.get_jogos())
        lider = rank[0][0] if rank else "Sem lider"
        melhor_score = str(rank[0][1]) if rank else "0"
        render_side_panel(
            "Painel do Campeonato",
            [
                ("Visao atual", titulo),
                ("Jogos no ranking", str(total_jogos_rank)),
                ("Lider", lider),
                ("Melhor marca", melhor_score),
            ],
            "O ranking guarda a melhor pontuacao registrada por jogador em cada jogo e soma isso no quadro global.",
        )

elif pagina == MENU_PAGE:
    render_menu_page(jogos, player, ranking)

elif pagina == GUIDE_PAGE:
    render_page_hero(
        "Como Usar o Arcade Cognitivo",
        "Guia completo da plataforma com onboarding, regras de multiplayer, salvamento de progresso, acessibilidade e suporte para cada etapa da sessao.",
        "Manual Completo",
    )

    guia_principal, guia_lateral = st.columns([1.45, 1])
    with guia_principal:
        render_step_guide(
            "Comecando do jeito certo",
            [
                ("Crie ou selecione um perfil", "Cada participante joga com um perfil local proprio, com XP, vidas, nivel e preferencia de dificuldade."),
                ("Escolha a dificuldade", "Use o modo automatico para progressao por nivel ou o modo manual para travar em facil, medio ou dificil."),
                ("Monte a sessao", "Defina quantos jogadores participam e selecione os perfis ativos antes de abrir qualquer jogo."),
                ("Defina a regra do multiplayer", "Escolha entre alternar a cada desafio ou trocar a vez quando alguem errar."),
                ("Salve seu progresso", "No Menu da Sessao, use o download do arquivo de progresso para continuar depois exatamente com seus perfis, ranking e configuracoes."),
                ("Abra um jogo ou circuito", "Na Home, entre em um desafio individual, no Code Lab ou no Circuito Aleatorio."),
                ("Leia o feedback da rodada", "A interface mostra vidas, dicas, custo de ajuda, mensagens de acerto ou erro e a proxima acao recomendada."),
            ],
            kicker="Onboarding",
        )

        render_step_guide(
            "Entendendo cada area do app",
            [
                ("Home", "Central do arcade com cards dos jogos, atalhos e resumo da sessao atual."),
                ("Menu da Sessao", "Lugar para trocar perfil, configurar dificuldade, montar multiplayer e ativar recursos de acessibilidade."),
                ("Jogos Individuais", "Tela principal da rodada com instrucoes, area de resposta, dica, feedback e controle de turnos."),
                ("Circuito Aleatorio", "Maratona que usa o catalogo inteiro e alterna automaticamente entre os jogadores da sessao."),
                ("Ranking", "Quadro global e por jogo, sempre considerando a melhor pontuacao de cada perfil."),
                ("Code Lab", "Modo de aprendizado com filtros por linguagem e conceito para treinar leitura de codigo."),
            ],
            kicker="Navegacao",
        )

        render_step_guide(
            "Como funciona o multiplayer",
            [
                ("Cada jogador responde um desafio", "A vez troca quando o desafio do jogador atual termina, seja por acerto ou por fim da rodada."),
                ("Errou, passou a vez", "Qualquer erro ja transfere a vez para o proximo participante da sessao."),
                ("Jogador ativo", "O nome exibido no topo e no placar lateral sempre indica quem esta com a vez naquele momento."),
                ("Quando alguem perde todas as vidas", "No multiplayer, a tela oferece avancar para o proximo jogador sem reiniciar a sessao inteira."),
            ],
            kicker="Multiplayer",
        )

        render_step_guide(
            "Salvar de onde parou",
            [
                ("Exportar progresso", "Baixe o arquivo JSON de progresso pelo Menu da Sessao para guardar perfis, ranking, configuracoes e parte do estado atual da sessao."),
                ("Importar depois", "Use o uploader do mesmo menu para restaurar esse arquivo no futuro."),
                ("O que volta junto", "Perfis, ranking, jogadores da sessao, configuracoes de acessibilidade, multiplayer, circuito e varios estados dos jogos."),
                ("Boa pratica", "Sempre exporte novamente depois de uma sequencia importante de partidas para manter o backup atualizado."),
            ],
            kicker="Progresso",
        )

        render_step_guide(
            "Regras importantes da rodada",
            [
                ("Dicas custam XP", "Cada jogo informa quantas dicas ainda restam e quanto custa usar uma ajuda."),
                ("Nem todo erro encerra a rodada", "Em varios jogos voce pode tentar novamente, ajustando a resposta com base no feedback recebido."),
                ("Acertos podem manter o fluxo", "Alguns jogos geram novo desafio logo depois do acerto, enquanto outros concluem a etapa atual."),
                ("As vidas sao o limite da tentativa", "Quando acabam, a tela oferece o fluxo adequado para solo ou multiplayer."),
            ],
            kicker="Rodadas",
        )

        render_step_guide(
            "Se algo parecer errado",
            [
                ("Confira o jogador ativo", "No multiplayer, sempre veja o nome no topo e no placar lateral antes de responder."),
                ("Revise o modo da sessao", "Confirme se a regra de troca esta em 'Cada jogador responde um desafio' ou 'Errou, passou a vez'."),
                ("Use o arquivo de progresso", "Se estiver alternando de ambiente, importe o save mais recente antes de continuar."),
                ("Volte ao menu da sessao", "Quase toda configuracao principal pode ser ajustada sem perder o restante da sessao."),
            ],
            kicker="Suporte",
        )
    with guia_lateral:
        render_side_panel(
            "Resumo do Manual",
            [
                ("Perfil ativo", player.dados()["nome"]),
                ("Jogadores na sessao", str(len(get_session_players(player)))),
                ("Dificuldade", resumo_dificuldade(player)),
                ("Modo multiplayer", multiplayer_turn_mode_label() if multiplayer_ativo(player) else "Desligado"),
            ],
            "Se a ideia for aprender a plataforma rapido, ajuste a sessao no menu e depois teste um jogo individual antes de abrir o circuito.",
        )

        render_step_guide(
            "Acessibilidade e boas praticas",
            [
                ("Ative a leitura automatica", "O app pode narrar o resumo da tela atual usando a sintese de voz do navegador."),
                ("Use alto contraste e fonte ampliada", "Essas opcoes ajudam principalmente em leitura longa, baixa visao e uso em telas menores."),
                ("Responda perto do enunciado", "A area de resposta foi organizada para manter o desafio visivel durante a interacao."),
                ("Exporte o progresso regularmente", "Isso facilita retomar a experiencia em outro momento ou em outro ambiente sem perder a sessao."),
                ("Use dicas com estrategia", "As dicas ajudam a manter o fluxo da rodada, mas consomem XP."),
                ("Revise o ranking com frequencia", "Ele ajuda a acompanhar evolucao individual e desempenho por jogo."),
            ],
            kicker="Boas praticas",
        )

elif pagina == CIRCUIT_PAGE:
    render_page_hero(
        "Circuito Aleatorio",
        "Uma maratona que mistura todo o catalogo e alterna automaticamente entre os participantes da sessao.",
        "Modo Maratona",
    )
    render_circuit_page(manager, player, ranking, jogos)

else:
    sincronizar_jogador_do_turno(pagina, player)
    if "jogo_atual" not in st.session_state or st.session_state.jogo_atual != pagina:
        if "jogo_ativo" in st.session_state:
            if hasattr(st.session_state.jogo_ativo, "resetar_jogo"):
                st.session_state.jogo_ativo.resetar_jogo()
            del st.session_state.jogo_ativo
        st.session_state.jogo_atual = pagina

    if "jogo_ativo" not in st.session_state:
        if player.vidas() <= 0:
            player.resetar_vidas()
        st.session_state.jogo_ativo = manager.criar_jogo(pagina, player)
        if "ultimo_resultado" in st.session_state:
            del st.session_state.ultimo_resultado

    jogo = st.session_state.jogo_ativo
    info = jogo.obter_info()
    controle_partida = inicializar_controles_partida(jogo, pagina)
    desafio = jogo.gerar_desafio()
    area_jogo, area_lateral = st.columns([1.7, 0.9])

    with area_lateral:
        turno = get_game_turn_state(pagina, player) if multiplayer_ativo(player) else None
        render_side_panel(
            "Placar da Partida",
            [
                ("Jogador", player.dados()["nome"]),
                ("Jogo", pagina),
                ("XP total", str(player.dados()["xp"])),
                ("Nivel", str(player.nivel())),
                ("Vidas", f"{player.vidas()} / 5"),
                ("Modo", "Multiplayer local" if multiplayer_ativo(player) else "Solo"),
                ("Troca", multiplayer_turn_mode_label() if multiplayer_ativo(player) else "Nao se aplica"),
                ("Rodada", str(turno["round"]) if turno else "1"),
                ("Dicas restantes", str(max(0, controle_partida["max_dicas"] - controle_partida["dicas_usadas"]))),
                ("Custo da dica", f"-{controle_partida['custo_dica_xp']} XP"),
            ],
            "O placar fica sempre visivel enquanto voce responde, para dar contexto sem poluir a area principal.",
        )
        if turno:
            participantes = get_session_players(player)
            ordem = ", ".join(item["nome"] for item in participantes)
            st.caption(f"Ordem atual dos turnos: {ordem}")
        if st.button("Usar dica", use_container_width=True, disabled=controle_partida["dicas_usadas"] >= controle_partida["max_dicas"]):
            dica = jogo.obter_dica()
            if dica:
                controle_partida["dicas_usadas"] += 1
                controle_partida["ultima_dica"] = dica
                player.perder_pontos(controle_partida["custo_dica_xp"])
                st.rerun()
        if controle_partida.get("ultima_dica"):
            st.info(f"Dica ativa: {controle_partida['ultima_dica']}")

    with area_jogo:
        render_game_intro(info)
        barra = st.columns(3)
        with barra[0]:
            metric_card("Modo de dificuldade", resumo_dificuldade(player))
        with barra[1]:
            metric_card("Participantes ativos", str(len(get_session_players(player))))
        with barra[2]:
            metric_card("Turno atual", player.dados()["nome"] if multiplayer_ativo(player) else f"Nivel {player.nivel()}")

        jogo.renderizar(desafio)
        jogo_perdido = False

        if not jogo_perdido:
            if "temp_letra" in st.session_state:
                resposta = st.session_state.temp_letra
                del st.session_state.temp_letra

                if "ultimo_resultado" in st.session_state:
                    del st.session_state.ultimo_resultado

                resultado = jogo.verificar_resposta(str(resposta))
                processar_resultado_padrao(jogo, pagina, resultado, ranking, player)
                st.rerun()

            config = jogo.configurar_input()

            if config.tipo != "none":
                render_answer_panel(
                    "Envie sua resposta nesta area",
                    "Use o campo logo abaixo para responder ao desafio atual. Se errar e a rodada continuar ativa, ajuste a resposta e envie novamente.",
                    config.label,
                    jogo.obter_contexto_resposta(desafio) or "",
                )
                with st.form(key=f"form_{pagina}"):
                    resposta = renderizar_input(config, pagina)

                    submitted = st.form_submit_button("Enviar resposta", use_container_width=True)

                    if submitted and resposta not in ("", None):
                        if "ultimo_resultado" in st.session_state:
                            del st.session_state.ultimo_resultado

                        resultado = jogo.verificar_resposta(str(resposta))
                        processar_resultado_padrao(jogo, pagina, resultado, ranking, player)
                        st.rerun()
            else:
                st.info("Conclua a etapa atual do jogo para habilitar a resposta.")

        jogo_perdido = exibir_feedback(jogo)

        if jogo_perdido:
            st.warning("Suas vidas acabaram nesta rodada.")
            if multiplayer_ativo(player):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Voltar para home", use_container_width=True):
                        player.resetar_vidas()
                        encerrar_jogo(jogo)
                        st.session_state.pagina = "🏠 Home"
                        st.rerun()
                with col2:
                    if st.button("Proximo jogador", key=f"passar_vez_{pagina}", use_container_width=True):
                        player.resetar_vidas()
                        encerrar_jogo(jogo)
                        avancar_turno_jogo(pagina, player)
                        st.rerun()
            else:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Jogar novamente", use_container_width=True):
                        player.resetar_vidas()
                        encerrar_jogo(jogo)
                        st.session_state.pagina = pagina
                        st.rerun()
                with col2:
                    if st.button("Voltar para home", use_container_width=True):
                        player.resetar_vidas()
                        encerrar_jogo(jogo)
                        st.session_state.pagina = "🏠 Home"
                        st.rerun()

        resultado_atual = st.session_state.get("ultimo_resultado")
        if not jogo_perdido and deve_avancar_turno_apos_resultado(player, resultado_atual):
            acao_label = "Proximo jogador" if resultado_atual.correto else "Passar a vez"
            if st.button(acao_label, key=f"proximo_jogador_{pagina}", use_container_width=True):
                if not resultado_atual.correto:
                    player.resetar_vidas()
                encerrar_jogo(jogo)
                avancar_turno_jogo(pagina, player)
                st.rerun()
