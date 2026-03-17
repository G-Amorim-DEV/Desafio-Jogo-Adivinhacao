import streamlit as st

from core.game_manager import GameManager
from core.player_manager import PlayerManager
from core.jogador import Jogador
from core.ranking_manager import RankingManager
from ui.layout import sidebar
from ui.theme import aplicar_tema
from ui.components import game_card

# -------------------------
# Tema e configuração
# -------------------------
aplicar_tema()

# Inicializa gerenciadores
manager = GameManager()
player = PlayerManager()
jogador = Jogador(player.dados()["nome"])
ranking = RankingManager()
jogos = manager.listar_jogos()

# -------------------------
# Configuração do nome do jogador
# -------------------------
if not player.dados().get("nome") or st.session_state.get("mudar_nome"):
    st.title("🧠 Plataforma Cognitiva")
    if st.session_state.get("mudar_nome"):
        st.subheader("Mudar Nome")
        st.write("Digite seu novo nome:")
    else:
        st.subheader("Bem-vindo!")
        st.write("Por favor, digite seu nome para começar:")
    
    nome_atual = player.dados().get("nome", "")
    nome = st.text_input("Seu nome", value=nome_atual, key="nome_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirmar") and nome.strip():
            player.set_nome(nome)
            st.success(f"Nome atualizado para {nome}!")
            if "mudar_nome" in st.session_state:
                del st.session_state.mudar_nome
            st.rerun()
    with col2:
        if st.session_state.get("mudar_nome") and st.button("Cancelar"):
            del st.session_state.mudar_nome
            st.rerun()
    
    st.stop()  # Para a execução até ter nome

# -------------------------
# Sidebar e navegação
# -------------------------
sidebar(jogos)  # Renderiza a sidebar
pagina = st.session_state.get("pagina", "🏠 Home")

st.title("🧠 Plataforma Cognitiva")

# -------------------------
# HOME
# -------------------------
if pagina == "🏠 Home":
    st.subheader("Escolha um jogo")
    for jogo in jogos:
        if game_card(jogo):
            st.session_state.pagina = jogo
            st.rerun()
    
    st.divider()
    if st.button("🏆 Ver Ranking"):
        st.session_state.pagina = "🏆 Ranking"
        st.rerun()

# -------------------------
# RANKING
# -------------------------
elif pagina == "🏆 Ranking":
    st.subheader("🏆 Ranking de Jogadores")
    
    filtro = st.selectbox(
        "Filtrar por:",
        ["Global"] + ranking.get_jogos(),
        key="filtro_ranking"
    )
    
    if filtro == "Global":
        rank = ranking.get_ranking_global()
        titulo = "Ranking Global (XP Total)"
    else:
        rank = ranking.get_ranking_jogo(filtro)
        titulo = f"Ranking - {filtro}"
    
    st.write(f"### {titulo}")
    
    if rank:
        for i, (nome, score) in enumerate(rank[:10], 1):  # Top 10
            medalha = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "🏅")
            st.write(f"{medalha} **{i}º** {nome}: {score} pontos")
    else:
        st.write("Nenhum score registrado ainda.")
    
    if st.button("🏠 Voltar ao Home"):
        st.session_state.pagina = "🏠 Home"
        st.rerun()

# -------------------------
# JOGOS
# -------------------------
else:
    # Verifica se o jogo mudou
    if "jogo_atual" not in st.session_state or st.session_state.jogo_atual != pagina:
        # Limpa o jogo anterior
        if "jogo_ativo" in st.session_state:
            del st.session_state.jogo_ativo
        st.session_state.jogo_atual = pagina
    
    # Inicializa jogo ativo se não existir
    if "jogo_ativo" not in st.session_state:
        # ✅ PASSA O JOGADOR na criação do jogo
        st.session_state.jogo_ativo = manager.criar_jogo(pagina, jogador)
        # Limpar resultado anterior quando novo jogo começa
        if "ultimo_resultado" in st.session_state:
            del st.session_state.ultimo_resultado

    jogo = st.session_state.jogo_ativo
    desafio = jogo.gerar_desafio()

    # Renderiza o desafio (cada jogo implementa renderizar)
    jogo.renderizar(desafio)

    # Exibir feedback persistente se existir
    if "ultimo_resultado" in st.session_state:
        resultado = st.session_state.ultimo_resultado
        if resultado.correto:
            st.success(f"✅ {resultado.mensagem} (+{resultado.pontos} XP)")
        else:
            st.error(f"❌ {resultado.mensagem}")
            # Mostrar dica quando erra
            dica = jogo.obter_dica()
            if dica:
                st.info(f"💡 Dica: {dica}")

    # Verificar se o jogo já foi perdido (para mostrar botão fora do form)
    jogo_perdido = False
    if "ultimo_resultado" in st.session_state:
        resultado = st.session_state.ultimo_resultado
        if not resultado.correto and resultado.finalizado:
            jogo_perdido = True

    # Form para input e botão (apenas se jogo não foi perdido)
    if not jogo_perdido:
        with st.form(key=f"form_{pagina}"):
            # Input do usuário
            resposta = ""
            if "temp_letra" in st.session_state:
                resposta = st.session_state.temp_letra
                del st.session_state.temp_letra
            else:
                resposta = st.text_input("Digite sua resposta").strip()

            # Botão de enviar dentro do form
            submitted = st.form_submit_button("Enviar")
            
            if submitted and resposta:
                # Limpar resultado anterior antes de processar novo
                if "ultimo_resultado" in st.session_state:
                    del st.session_state.ultimo_resultado
                    
                resultado = jogo.verificar_resposta(resposta)

                # Armazenar resultado para exibição persistente
                st.session_state.ultimo_resultado = resultado

                # Feedback visual
                if resultado.correto:
                    st.success(f"✅ {resultado.mensagem} (+{resultado.pontos} XP)")
                    player.adicionar_xp(resultado.pontos)
                    # Adicionar ao ranking se jogo finalizado
                    if resultado.finalizado:
                        ranking.adicionar_score(player.dados()["nome"], pagina, resultado.pontos)
                else:
                    st.error(f"❌ {resultado.mensagem}")
                    # Mostrar dica quando erra
                    dica = jogo.obter_dica()
                    if dica:
                        st.info(f"💡 Dica: {dica}")

                # Finalização do jogo
                if resultado.finalizado:
                    if resultado.correto:
                        # Animação de parabéns
                        st.markdown("""
                        <style>
                        @keyframes congratulations {
                            0% { 
                                opacity: 0; 
                                transform: scale(0.5) rotate(-10deg); 
                                color: #FFD700;
                            }
                            50% { 
                                opacity: 1; 
                                transform: scale(1.2) rotate(5deg); 
                                color: #FF6B35;
                            }
                            100% { 
                                opacity: 1; 
                                transform: scale(1) rotate(0deg); 
                                color: #4CAF50;
                            }
                        }
                        @keyframes trophyBounce {
                            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                            40% { transform: translateY(-10px); }
                            60% { transform: translateY(-5px); }
                        }
                        .congratulations {
                            text-align: center;
                            font-size: 3em;
                            font-weight: bold;
                            animation: congratulations 2s ease-in-out;
                            margin: 20px 0;
                            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
                        }
                        .trophy-emoji {
                            animation: trophyBounce 2s infinite;
                            display: inline-block;
                            font-size: 1.5em;
                        }
                        </style>
                        <div class="congratulations">
                            🏆 <span class="trophy-emoji">🎉</span> PARABÉNS! VOCÊ GANHOU! <span class="trophy-emoji">🎉</span> 🏆
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.balloons()
                        st.success("🏆 Jogo concluído!")
                        # Limpar resultado quando jogo finaliza
                        if "ultimo_resultado" in st.session_state:
                            del st.session_state.ultimo_resultado
                        del st.session_state.jogo_ativo
                        st.rerun()

                # Força atualização da página
                st.rerun()

    # Botão para voltar ao menu (fora do form, só aparece quando perdeu)
    if jogo_perdido:
        st.warning("💔 Que pena! Você perdeu este jogo.")
        if st.button("🔄 Tentar outro jogo", key="voltar_menu"):
            # Limpar resultado e jogo
            if "ultimo_resultado" in st.session_state:
                del st.session_state.ultimo_resultado
            del st.session_state.jogo_ativo
            st.session_state.pagina = "🏠 Home"
            st.rerun()