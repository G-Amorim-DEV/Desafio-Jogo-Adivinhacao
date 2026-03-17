# Arcade Cognitivo

Aplicacao web desenvolvida com `Streamlit` para treino cognitivo, aprendizado introdutorio de programacao e experiencias locais multiplayer. O projeto combina jogos curtos, progressao por perfil, ranking, acessibilidade e exportacao/importacao de progresso para continuar a sessao depois.

## Visao Geral

O `Arcade Cognitivo` foi estruturado para reunir, em uma unica plataforma:

- jogos de raciocinio, memoria, linguagem e logica;
- perfis locais com `XP`, `vidas`, `nivel` e dificuldade configuravel;
- multiplayer local com regras de troca de turno;
- ranking global e por jogo;
- `Circuito Aleatorio` com rotacao automatica entre participantes;
- trilha educativa `Code Lab`;
- recursos de acessibilidade integrados;
- funcionalidade de salvar e restaurar progresso.

## Recursos Principais

- perfis persistidos em `JSON`;
- dificuldade `automatica` e `manual`;
- multiplayer local com dois modos:
  `Cada jogador responde um desafio`
  `Errou, passou a vez`
- exportacao de progresso por download;
- importacao de progresso por upload;
- ranking global e ranking por jogo;
- sistema de dicas com custo de XP;
- leitura automatica da tela;
- alto contraste, fonte ampliada e reducao de movimento;
- conteudo expansivel por arquivos em `data/`.

## Jogos Disponiveis

- `Adivinhacao`
- `Analogias`
- `Antonimos`
- `Categorias`
- `Code Lab`
- `Forca`
- `Matematica`
- `Memoria`
- `Palavra Intrusa`
- `Quiz`
- `Scramble`
- `Sequencia`
- `Sinonimos`
- `Verdadeiro ou Falso`

## Code Lab

O `Code Lab` e a trilha educativa do projeto para treino de leitura de codigo e fundamentos de programacao.

Cobertura atual:

- `Python`
- `JavaScript`
- `TypeScript`
- `Java`
- `C#`
- `SQL`
- `Go`
- `Rust`

Os desafios podem envolver:

- leitura de codigo;
- logica basica;
- sintaxe;
- estruturas condicionais;
- repeticao;
- funcoes;
- conceitos por linguagem.

## Como Executar

### Requisitos

- `Python 3`
- dependencias descritas em `requirements.txt`

### Instalacao

```bash
pip install -r requirements.txt
```

### Execucao local

```bash
streamlit run app.py
```

URL local padrao:

```text
http://localhost:8501
```

## Aplicacao Online

Versao publicada no Streamlit Community Cloud:

https://desafio-jogo-adivinhacao-bo25wk4blgetwgqvfw9q7v.streamlit.app/

## Guia de Uso

### Primeiro acesso

1. Crie um perfil local.
2. Abra o `Menu da Sessao`.
3. Ajuste a dificuldade.
4. Monte a sessao multiplayer, se desejar.
5. Escolha um jogo na `Home`.

### Dificuldade

- `automatico`: acompanha o nivel do jogador.
- `manual`: fixa em `facil`, `medio` ou `dificil`.

### Multiplayer

No `Menu da Sessao`, o usuario pode:

1. definir a quantidade de jogadores;
2. selecionar os perfis ativos;
3. ativar o multiplayer nos jogos individuais;
4. configurar a regra de troca de turno.

Regras disponiveis:

- `Cada jogador responde um desafio`
  A vez troca quando o desafio do jogador termina.
- `Errou, passou a vez`
  Qualquer erro passa a vez para o proximo jogador.

### Salvar de onde parou

No `Menu da Sessao`, existe uma area dedicada para progresso.

#### Exportar progresso

O botao `Baixar progresso` gera um arquivo `.json` com:

- perfis locais;
- ranking;
- configuracoes da sessao;
- configuracoes de acessibilidade;
- configuracoes do multiplayer;
- estado do circuito;
- parte do estado dos jogos para retomada.

#### Importar progresso

1. Abra o `Menu da Sessao`.
2. Selecione um arquivo exportado anteriormente.
3. Clique em `Restaurar progresso`.

### Recomendacoes para backup

- exporte o progresso ao final de sessoes importantes;
- mantenha mais de um arquivo se quiser pontos diferentes de restauracao;
- importe apenas arquivos gerados pelo proprio app;
- em troca de maquina ou navegador, restaure o progresso antes de continuar jogando.

## Acessibilidade

Recursos disponiveis:

- alto contraste;
- fonte ampliada;
- reducao de efeitos visuais;
- leitura automatica da tela;
- controle de velocidade da narracao;
- leitura manual da tela atual.

Tambem houve reorganizacao da interface para manter o enunciado proximo da area de resposta, melhorando legibilidade e usabilidade.

## Estrutura do Projeto

```text
app.py
core/
  engine/
  models/
  player_manager.py
  ranking_manager.py
games/
  adivinhacao/
  analogias/
  antonimos/
  categorias/
  code_lab/
  forca/
  intruso/
  matematica/
  memoria/
  quiz/
  scramble/
  sequencia/
  sinonimos/
  verdadeiro_falso/
services/
  loaders/
  persistence/
ui/
  components.py
  layout.py
  theme.py
data/
tests/
utils/
```

## Arquitetura

### `app.py`

Responsavel pelo fluxo principal da aplicacao, navegacao entre paginas, gerenciamento da sessao, acessibilidade, multiplayer, feedback de rodada e salvamento/restauracao do progresso.

### `core/`

Contem os gerenciadores centrais e o motor base da aplicacao.

### `games/`

Cada modulo define:

- geracao do desafio;
- renderizacao;
- configuracao de input;
- verificacao da resposta;
- dica.

### `services/persistence/`

Responsavel por salvar e carregar perfis e ranking em arquivos `JSON`.

### `ui/`

Contem componentes reutilizaveis, layout e tema visual.

### `data/`

Armazena o conteudo dos desafios em arquivos `JSON`.

## QA e Robustez

Durante a revisao de qualidade, o projeto recebeu melhorias em pontos importantes:

- carregamento de dados sem depender do diretorio atual;
- tratamento mais seguro para arquivos JSON ausentes ou invalidos;
- correcao da troca de turno no multiplayer;
- ajuste do fluxo de pergunta e resposta para acessibilidade;
- protecao contra repeticao indevida de letras na `Forca`;
- persistencia mais consistente do estado de alguns jogos;
- normalizacao mais segura dos perfis locais;
- ampliacao da cobertura de regressao.

## Solucao de Problemas

### O app nao inicia

Confirme a instalacao das dependencias e execute novamente:

```bash
streamlit run app.py
```

### Os testes nao rodam

Os testes dependem de `streamlit`. Instale as dependencias antes de executar:

```bash
pip install -r requirements.txt
```

### Quero retomar meu progresso

Abra o `Menu da Sessao`, selecione um arquivo `.json` exportado anteriormente e clique em `Restaurar progresso`.

### O multiplayer parece incorreto

Confira no `Menu da Sessao`:

- quais perfis estao ativos;
- quantos jogadores participam da sessao;
- qual regra de troca esta selecionada.

## Testes

Existe cobertura em `tests/test_game_logic.py`.

Para executar:

```bash
python3 -m unittest -v tests.test_game_logic
```

Observacao:
os testes dependem da biblioteca `streamlit`. Se ela nao estiver instalada no ambiente, a importacao dos testes falhara antes da execucao.

## Deploy

O projeto pode ser executado localmente e tambem publicado no `Streamlit Community Cloud`, desde que as dependencias estejam instaladas corretamente.

## Autor

Desenvolvido por **Guilherme**.
