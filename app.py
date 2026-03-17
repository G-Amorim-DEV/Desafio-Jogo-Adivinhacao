import streamlit as st
from random import shuffle

from core.engine.manager import GameManager
from core.player_manager import PlayerManager
from core.ranking_manager import RankingManager
from ui.components import (
    render_accessibility_reader,
    game_card,
    metric_card,
    render_championship_row,
    render_game_intro,
    render_page_hero,
    render_side_panel,
    render_spotlight_panel,
)
from ui.layout import sidebar
from ui.theme import aplicar_tema

CIRCUIT_PAGE = "🎲 Circuito Aleatorio"


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
    if pagina == CIRCUIT_PAGE:
        return base + "Tela de circuito aleatorio com rotacao entre os participantes da sessao."
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
        with st.form(key=f"form_circuito_{jogo_nome}"):
            resposta = renderizar_input(config, f"circuito_{jogo_nome}")
            submitted = st.form_submit_button("Enviar resposta", use_container_width=True)
            if submitted and resposta not in ("", None):
                resultado = jogo.verificar_resposta(str(resposta))
                processar_resultado_circuito(player_manager, ranking, jogo, jogo_nome, resultado)
                st.rerun()
    else:
        st.info("Conclua a etapa atual do jogo para enviar a resposta desta rodada.")


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
        placeholder=config.placeholder,
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

elif pagina == CIRCUIT_PAGE:
    render_page_hero(
        "Circuito Aleatorio",
        "Uma maratona que mistura todo o catalogo e alterna automaticamente entre os participantes da sessao.",
        "Modo Maratona",
    )
    render_circuit_page(manager, player, ranking, jogos)

else:
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
        render_side_panel(
            "Placar da Partida",
            [
                ("Jogador", player.dados()["nome"]),
                ("Jogo", pagina),
                ("XP total", str(player.dados()["xp"])),
                ("Nivel", str(player.nivel())),
                ("Vidas", f"{player.vidas()} / 5"),
                ("Dicas restantes", str(max(0, controle_partida["max_dicas"] - controle_partida["dicas_usadas"]))),
                ("Custo da dica", f"-{controle_partida['custo_dica_xp']} XP"),
            ],
            "O placar fica sempre visivel enquanto voce responde, para dar contexto sem poluir a area principal.",
        )
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
            metric_card("Progresso do perfil", f"Nivel {player.nivel()}")

        jogo.renderizar(desafio)
        jogo_perdido = exibir_feedback(jogo)

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

        if jogo_perdido:
            st.warning("Suas vidas acabaram nesta rodada.")
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
