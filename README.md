# Arcade Cognitivo

Aplicacao web em `Streamlit` com jogos cognitivos, trilha educativa de programacao, perfis locais, ranking, multiplayer por turnos, acessibilidade e recurso de exportar/importar progresso para continuar depois.

## O que o projeto entrega

O `Arcade Cognitivo` combina:

- jogos curtos de raciocinio, linguagem, memoria e logica;
- perfis locais com `XP`, `vidas`, `nivel` e dificuldade;
- multiplayer local com regras de troca de turno;
- ranking global e ranking por jogo;
- `Circuito Aleatorio` com rotacao automatica entre participantes;
- `Code Lab` para treino de leitura de codigo;
- acessibilidade integrada;
- arquivo de progresso para salvar e retomar a sessao.

## Recursos Principais

- perfis persistidos em `JSON`;
- dificuldade `automatica` e `manual`;
- multiplayer com dois modos:
  `Cada jogador responde um desafio`
  `Errou, passou a vez`
- exportacao de progresso via download;
- importacao de progresso via upload;
- ranking global e por jogo;
- dicas com custo de XP;
- leitura automatica da tela;
- alto contraste, fonte ampliada e reducao de movimento;
- conteudo extensivel por arquivos em `data/`.

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

## Como Executar

### Requisitos

- `Python 3`
- dependencias do `requirements.txt`

### Instalacao

```bash
pip install -r requirements.txt
```

### Execucao local

```bash
streamlit run app.py
```

O Streamlit normalmente abre em:

```text
http://localhost:8501
```

## Como Usar

### Primeiro acesso

1. Crie um perfil local.
2. Abra o `Menu da Sessao`.
3. Ajuste a dificuldade.
4. Monte a sessao multiplayer, se quiser jogar com mais pessoas.
5. Escolha um jogo na `Home`.

### Dificuldade

- `automatico`: acompanha o nivel do jogador.
- `manual`: fixa em `facil`, `medio` ou `dificil`.

### Multiplayer

No `Menu da Sessao`, voce pode:

1. definir quantos jogadores participam;
2. escolher os perfis ativos;
3. ativar o multiplayer nos jogos individuais;
4. escolher a regra de troca de turno.

Regras disponiveis:

- `Cada jogador responde um desafio`
  A vez troca quando o desafio do jogador termina.
- `Errou, passou a vez`
  Qualquer erro passa a vez para o proximo jogador.

### Salvar de onde parou

O app agora possui uma area de progresso no `Menu da Sessao`.

#### Exportar progresso

Use o botao `Baixar progresso atual` para gerar um arquivo `.json` com:

- perfis locais;
- ranking;
- configuracoes da sessao;
- configuracoes de acessibilidade;
- configuracoes do multiplayer;
- estado do circuito;
- parte relevante do estado dos jogos para retomar depois.

#### Importar progresso

1. Abra o `Menu da Sessao`.
2. Selecione um arquivo exportado anteriormente.
3. Clique em `Restaurar progresso`.

Isso permite continuar a experiencia em outro momento ou em outro ambiente com o mesmo progresso salvo.

## Acessibilidade

Recursos disponiveis:

- alto contraste;
- fonte ampliada;
- reducao de efeitos visuais;
- leitura automatica da tela;
- controle de velocidade da narracao;
- leitura manual da tela atual.

Tambem foi reorganizada a interface para manter o enunciado proximo da area de resposta, melhorando usabilidade e leitura.

## Code Lab

`Code Lab` e a trilha educativa do projeto para iniciantes em programacao.

Ela oferece desafios de:

- leitura de codigo;
- logica basica;
- sintaxe;
- estruturas condicionais;
- repeticao;
- funcoes;
- conceitos por linguagem.

Linguagens atuais:

- `Python`
- `JavaScript`
- `TypeScript`
- `Java`
- `C#`
- `SQL`
- `Go`
- `Rust`

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

Orquestra as paginas, o fluxo da sessao, acessibilidade, multiplayer, feedback de rodada e a exportacao/importacao do progresso.

### `core/`

Contem os gerenciadores de dominio e o motor base dos jogos.

### `games/`

Cada modulo define:

- geracao do desafio;
- renderizacao;
- configuracao do input;
- verificacao da resposta;
- dica.

### `services/persistence/`

Responsavel por salvar e carregar perfis e ranking em `JSON`.

### `ui/`

Componentes visuais e tema aplicado sobre a interface do Streamlit.

### `data/`

Conteudo dos desafios em arquivos `JSON`.

## QA e Robustez

Durante a varredura de QA, o projeto foi ajustado em varios pontos importantes:

- carregamento de dados sem depender do diretorio atual;
- tratamento mais seguro para arquivos JSON ausentes ou invalidos;
- correcao da troca de turno no multiplayer;
- ajuste do fluxo de pergunta e resposta para acessibilidade;
- protecao contra letra repetida na `Forca`;
- persistencia mais consistente do estado de alguns jogos para retomada;
- normalizacao mais segura dos perfis locais;
- testes de regressao ampliados.

## Testes

Existe cobertura em `tests/test_game_logic.py`.

Para rodar:

```bash
python3 -m unittest -v tests.test_game_logic
```

Observacao:
os testes dependem da biblioteca `streamlit`. Se ela nao estiver instalada no ambiente, a importacao dos testes falhara antes da execucao.

## Deploy

O projeto pode ser executado localmente e tambem publicado no `Streamlit Community Cloud`, desde que as dependencias estejam instaladas corretamente.

## Licenca

Adicione aqui a licenca oficial do projeto, se desejar.
