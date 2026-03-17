import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import streamlit as st

from core.engine.loader import GameLoader
from core.player_manager import PlayerManager
from games.adivinhacao import Game as AdivinhacaoGame
from games.analogias import Game as AnalogiasGame
from games.antonimos import Game as AntonimosGame
from games.categorias import Game as CategoriasGame
from games.code_lab import Game as CodeLabGame
from games.forca import Game as ForcaGame
from games.intruso import Game as IntrusoGame
from games.memoria import Game as MemoriaGame
from games.quiz import Game as QuizGame
from games.scramble import Game as ScrambleGame
from games.sequencia import Game as SequenciaGame
from games.sinonimos import Game as SinonimosGame


class GameLogicTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def criar_player_manager(self, xp=0, vidas=5):
        player_path = Path(self.temp_dir.name) / "player.json"
        player_path.write_text(
            json.dumps(
                {
                    "xp": xp,
                    "jogos_jogados": 0,
                    "nome": "Teste",
                    "vidas": vidas,
                }
            ),
            encoding="utf-8",
        )

        patcher = patch("services.persistence.player_repository.data_path", return_value=player_path)
        patcher.start()
        self.addCleanup(patcher.stop)
        return PlayerManager()

    def test_game_loader_cria_todos_os_jogos_com_player_manager(self):
        player = self.criar_player_manager()
        loader = GameLoader()

        esperados = {
            "Adivinhação",
            "Analogias",
            "Antônimos",
            "Categorias",
            "Code Lab",
            "Forca",
            "Matemática",
            "Memória",
            "Palavra Intrusa",
            "Quiz",
            "Scramble",
            "Sequencia",
            "Sinônimos",
            "Verdadeiro ou Falso",
        }
        self.assertTrue(esperados.issubset(set(loader.jogos.keys())))

        for nome, jogo_cls in loader.jogos.items():
            st.session_state.clear()
            jogo = jogo_cls(player)
            desafio = jogo.gerar_desafio()
            self.assertIsNotNone(desafio, msg=f"{nome} não gerou desafio")

    def test_adivinhacao_acertar_adiciona_xp_uma_vez(self):
        player = self.criar_player_manager()
        jogo = AdivinhacaoGame(player)
        st.session_state.adivinhacao["numero"] = 42
        st.session_state.adivinhacao["tentativas"] = 5

        resultado = jogo.verificar_resposta("42")

        self.assertTrue(resultado.correto)
        self.assertEqual(resultado.pontos, 10)
        self.assertEqual(player.dados()["xp"], 10)

    def test_player_dificuldade_manual_e_automatica(self):
        player = self.criar_player_manager(xp=0)

        self.assertEqual(player.dificuldade(), "facil")

        player.configurar_dificuldade("manual", "dificil")
        self.assertEqual(player.dificuldade(), "dificil")

        player.configurar_dificuldade("automatico", "medio")
        self.assertEqual(player.dificuldade(), "facil")

    def test_multiplayer_local_cria_e_alterna_perfis(self):
        player = self.criar_player_manager()

        primeiro = player.dados()["id"]
        novo = player.criar_jogador("Amigo")

        self.assertEqual(player.dados()["nome"], "Amigo")
        self.assertEqual(len(player.listar_jogadores()), 2)

        player.definir_jogador_ativo(primeiro)
        self.assertNotEqual(player.dados()["id"], novo["id"])

    def test_multiplayer_local_exclui_perfil_e_mantem_ativo_valido(self):
        player = self.criar_player_manager()
        primeiro = player.dados()["id"]
        segundo = player.criar_jogador("Amigo")["id"]

        self.assertTrue(player.excluir_jogador(segundo))
        self.assertEqual(len(player.listar_jogadores()), 1)
        self.assertEqual(player.dados()["id"], primeiro)

        self.assertTrue(player.excluir_jogador(primeiro))
        self.assertFalse(player.tem_jogadores())
        self.assertEqual(player.dados(), {})

    def test_quiz_aceita_player_manager_e_pontua(self):
        player = self.criar_player_manager()
        jogo = QuizGame(player)
        pergunta = jogo.perguntas[0]
        st.session_state.quiz["pergunta_atual"] = pergunta

        resultado = jogo.verificar_resposta(pergunta["resposta"])

        self.assertTrue(resultado.correto)
        self.assertEqual(player.dados()["xp"], pergunta["pontos"])
        self.assertIsNone(st.session_state.quiz["pergunta_atual"])

    def test_quiz_erro_permite_tentar_novamente_sem_revelar_resposta(self):
        player = self.criar_player_manager(vidas=5)
        jogo = QuizGame(player)
        pergunta = jogo.perguntas[0]
        resposta_errada = next(opcao for opcao in pergunta["opcoes"] if opcao != pergunta["resposta"])
        st.session_state.quiz["pergunta_atual"] = pergunta

        resultado = jogo.verificar_resposta(resposta_errada)

        self.assertFalse(resultado.correto)
        self.assertFalse(resultado.finalizado)
        self.assertNotIn(pergunta["resposta"], resultado.mensagem)
        self.assertEqual(st.session_state.quiz["pergunta_atual"], pergunta)

    def test_memoria_erro_mantem_ordem_para_feedback(self):
        player = self.criar_player_manager()
        jogo = MemoriaGame(player)
        st.session_state.memoria.update(
            {
                "ordem": ["gato", "mesa", "cachorro"],
                "categoria": "Palavras Gerais",
                "dificuldade": "facil",
                "fase": "esconder",
                "acertos_seguidos": 0,
            }
        )

        resultado = jogo.verificar_resposta("gato mesa sapo")

        self.assertFalse(resultado.correto)
        self.assertIn("gato mesa cachorro", resultado.mensagem)
        self.assertEqual(st.session_state.memoria["ordem"], ["gato", "mesa", "cachorro"])

    def test_scramble_erro_nao_apaga_palavra_atual(self):
        player = self.criar_player_manager()
        jogo = ScrambleGame(player)
        st.session_state.scramble.update(
            {
                "original": "python",
                "embaralhada": "nothyp",
                "acertos_seguidos": 0,
            }
        )

        resultado = jogo.verificar_resposta("typhon")

        self.assertFalse(resultado.correto)
        self.assertEqual(st.session_state.scramble["original"], "python")
        self.assertIn("letras na posicao certa", resultado.mensagem)

    def test_sequencia_erro_mantem_item_para_dica(self):
        player = self.criar_player_manager()
        jogo = SequenciaGame(player)
        item = {
            "sequencia": [2, 4, 6, 8],
            "resposta": 10,
            "dica": "+2",
            "explicacao": "soma constante",
            "pontos": 5,
        }
        st.session_state.sequencia["item_atual"] = item

        resultado = jogo.verificar_resposta("11")

        self.assertFalse(resultado.correto)
        self.assertEqual(st.session_state.sequencia["item_atual"], item)
        self.assertEqual(jogo.obter_dica(), "+2")

    def test_forca_registra_letra_errada_como_usada(self):
        player = self.criar_player_manager()
        jogo = ForcaGame(player)
        st.session_state.forca = {
            "palavra": "PYTHON",
            "letras": [],
            "tentativas": 6,
        }

        resultado = jogo.verificar_resposta("Z")

        self.assertFalse(resultado.correto)
        self.assertIn("Z", st.session_state.forca["letras"])
        self.assertEqual(st.session_state.forca["tentativas"], 5)

    def test_novos_jogos_carregam_desafios(self):
        player = self.criar_player_manager()

        jogo_analogias = AnalogiasGame(player)
        desafio_analogias = jogo_analogias.gerar_desafio()
        self.assertIn("pergunta", desafio_analogias)
        self.assertTrue(desafio_analogias["opcoes"])

        st.session_state.clear()
        jogo_intruso = IntrusoGame(player)
        desafio_intruso = jogo_intruso.gerar_desafio()
        self.assertEqual(len(desafio_intruso["opcoes"]), 4)
        self.assertTrue(desafio_intruso["resposta"])

        st.session_state.clear()
        jogo_categorias = CategoriasGame(player)
        self.assertTrue(jogo_categorias.gerar_desafio()["categoria"])

        st.session_state.clear()
        jogo_sinonimos = SinonimosGame(player)
        self.assertTrue(jogo_sinonimos.gerar_desafio()["termo"])

        st.session_state.clear()
        jogo_antonimos = AntonimosGame(player)
        self.assertTrue(jogo_antonimos.gerar_desafio()["termo"])

        st.session_state.clear()
        jogo_code_lab = CodeLabGame(player)
        desafio_code_lab = jogo_code_lab.gerar_desafio()
        self.assertIn("linguagem", desafio_code_lab)
        self.assertIn("conceito", desafio_code_lab)
        self.assertTrue(desafio_code_lab["opcoes"])

    def test_code_lab_filtra_por_linguagem_e_verifica_resposta(self):
        player = self.criar_player_manager(xp=20)
        jogo = CodeLabGame(player)

        st.session_state.code_lab["linguagem"] = "python"
        st.session_state.code_lab["conceito"] = "todos"
        desafio = jogo.gerar_desafio()

        self.assertEqual(desafio["linguagem"], "python")

        resultado = jogo.verificar_resposta(desafio["resposta"])

        self.assertTrue(resultado.correto)
        self.assertGreater(player.dados()["xp"], 20)
        self.assertIsNone(st.session_state.code_lab["item_atual"])


if __name__ == "__main__":
    unittest.main()
