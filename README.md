# Arcade Cognitivo

Plataforma web de jogos cognitivos, desafios educacionais e trilhas introdutórias de programação construída com `Streamlit`. O projeto combina jogos rápidos de raciocínio, memória e linguagem com um modo educacional chamado `Code Lab`, além de perfis locais, multiplayer por turnos, ranking, circuito aleatório e recursos de acessibilidade.

## Acesso Online

Aplicação publicada no Streamlit Community Cloud:

https://desafio-jogo-adivinhacao-bo25wk4blgetwgqvfw9q7v.streamlit.app/

## Sumário

- [Visão Geral](#visão-geral)
- [Principais Recursos](#principais-recursos)
- [Jogos Disponíveis](#jogos-disponíveis)
- [Manual do Usuário](#manual-do-usuário)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Tecnologias e Bibliotecas](#tecnologias-e-bibliotecas)
- [Estrutura de Dados](#estrutura-de-dados)
- [Como Executar Localmente](#como-executar-localmente)
- [Testes e Validação](#testes-e-validação)
- [Acessibilidade](#acessibilidade)
- [Deploy](#deploy)
- [Roadmap](#roadmap)

## Visão Geral

O `Arcade Cognitivo` foi projetado para ser uma plataforma extensível de desafios interativos. A ideia central é unir:

- jogos cognitivos curtos e reutilizáveis;
- progressão de jogador com `XP`, `vidas` e `nível`;
- conteúdo orientado a dados em arquivos `JSON`;
- experiência local multiplayer;
- trilhas educacionais para iniciantes em programação;
- interface com foco em usabilidade e acessibilidade.

O projeto atende tanto usuários que querem jogar casualmente quanto pessoas que desejam aprender lógica, interpretação e fundamentos de programação de forma lúdica.

## Principais Recursos

- catálogo com múltiplos jogos cognitivos;
- perfis locais de usuários;
- multiplayer por sessão com rotação entre perfis;
- `Circuito Aleatório`, que mistura o catálogo inteiro em uma maratona;
- ranking global e ranking por jogo;
- dificuldade automática ou manual;
- sistema de vidas, XP e progressão;
- sistema de dicas com custo controlado;
- manual de uso integrado ao app;
- recursos de acessibilidade na interface;
- leitura de tela via síntese de voz do navegador;
- trilha `Code Lab` com desafios de programação;
- conteúdo expansível por arquivos `JSON`;
- validação automatizada com testes.

## Jogos Disponíveis

### Jogos cognitivos

- `Adivinhação`
- `Analogias`
- `Antônimos`
- `Categorias`
- `Forca`
- `Matemática`
- `Memória`
- `Palavra Intrusa`
- `Quiz`
- `Scramble`
- `Sequência`
- `Sinônimos`
- `Verdadeiro ou Falso`

### Trilha educacional

- `Code Lab`

## Code Lab

O `Code Lab` foi criado para ajudar programadores iniciantes a aprenderem por meio de microdesafios. A trilha usa questões curtas com foco em leitura de código, lógica, sintaxe, estruturas básicas e entendimento de conceitos fundamentais.

Linguagens atualmente incluídas:

- `Python`
- `JavaScript`
- `TypeScript`
- `Java`
- `C#`
- `SQL`
- `Go`
- `Rust`

Os desafios podem incluir:

- leitura de código;
- lógica básica;
- variáveis e tipos;
- estruturas condicionais;
- estruturas de repetição;
- coleções e arrays;
- funções e métodos;
- conceitos específicos por linguagem.

## Manual do Usuário

### Primeiro acesso

1. Abra o app localmente ou pela versão publicada.
2. Crie um perfil com o nome do jogador.
3. Escolha a dificuldade:
   `automatico` ajusta conforme o progresso;
   `manual` trava entre `facil`, `medio` e `dificil`.
4. Se quiser jogar com outras pessoas, configure a sessão multiplayer na sidebar.

### Como jogar

1. Entre na `Home`.
2. Escolha um card de jogo ou inicie o `Circuito Aleatório`.
3. Leia a introdução do desafio e as instruções.
4. Envie sua resposta pelo campo apropriado.
5. Use dicas quando necessário.
6. Acompanhe vidas, XP e ranking.

### Multiplayer local

1. Crie múltiplos perfis.
2. Defina quantos jogadores participarão da sessão.
3. Selecione os perfis ativos.
4. Use o `Circuito Aleatório` para alternar automaticamente entre eles.

### Ranking

- O ranking pode ser visualizado no modo global.
- Também é possível filtrar por jogo específico.
- A plataforma registra pontuações para comparação entre perfis locais.

### Acessibilidade

Na sidebar, o usuário pode ativar:

- `alto contraste`;
- `fonte ampliada`;
- `reduzir efeitos visuais`;
- `leitura automática da tela`;
- velocidade de leitura;
- botão para ler a tela atual.

## Arquitetura do Projeto

```text
app.py
core/
  engine/
  models/
  game_ui.py
  player_manager.py
  ranking_manager.py
services/
  loaders/
  persistence/
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
ui/
  components.py
  layout.py
  theme.py
data/
tests/
utils/
```

### Responsabilidades por camada

- `app.py`
  fluxo principal da aplicação, roteamento de páginas, renderização das telas e integração dos gerenciadores.

- `core/engine`
  contratos base, descoberta dinâmica dos jogos, fábrica e gerenciamento de ciclo de vida.

- `core/models`
  modelos de domínio usados na aplicação.

- `core/player_manager.py`
  gestão de perfis, experiência, vidas, dificuldade e perfis ativos.

- `core/ranking_manager.py`
  armazenamento e leitura do ranking.

- `services/loaders`
  carregamento de conteúdo estruturado dos jogos.

- `services/persistence`
  persistência local em arquivos `JSON`.

- `games/`
  implementação da lógica específica de cada jogo.

- `ui/`
  componentes reutilizáveis, layout lateral e tema visual.

- `data/`
  bases de dados em `JSON` com perguntas, palavras, sequências, analogias e trilhas do `Code Lab`.

- `tests/`
  testes automatizados de lógica e regressão.

## Tecnologias e Bibliotecas

### Linguagem

- `Python 3`

### Framework principal

- `Streamlit`

### UI e experiência

- `HTML` e `CSS` customizados aplicados sobre componentes do Streamlit
- `Streamlit Components`

### Persistência

- `JSON` para ranking, perfis locais e conteúdo dos jogos

### Visualização

- `Matplotlib` para apoio visual na forca

### Testes

- `unittest`

### Controle de versão e publicação

- `Git`
- `GitHub`
- `Streamlit Community Cloud`

### Bibliotecas do projeto

Dependências listadas em `requirements.txt`:

- `streamlit`
- `streamlit-extras`
- `watchdog`
- `pydantic`
- `python-dotenv`
- `requests`
- `python-dateutil`
- `typing_extensions`
- `numpy`
- `pandas`
- `matplotlib`
- `faker`

### Bibliotecas da standard library utilizadas

- `abc`
- `dataclasses`
- `datetime`
- `importlib`
- `json`
- `logging`
- `pathlib`
- `pkgutil`
- `random`
- `tempfile`
- `typing`
- `unittest`
- `uuid`

## Estrutura de Dados

O projeto foi pensado para crescer via conteúdo orientado a dados. A maior parte dos desafios é alimentada por arquivos `JSON`.

### Exemplos de bases atuais

- `data/quiz.json`
- `data/vf.json`
- `data/sequencias.json`
- `data/palavras_forca.json`
- `data/memoria_palavras.json`
- `data/analogias.json`
- `data/intrusos.json`
- `data/categorias.json`
- `data/sinonimos.json`
- `data/antonimos.json`
- `data/code_lab/python.json`
- `data/code_lab/javascript.json`
- `data/code_lab/typescript.json`
- `data/code_lab/java.json`
- `data/code_lab/csharp.json`
- `data/code_lab/sql.json`
- `data/code_lab/go.json`
- `data/code_lab/rust.json`

Esse formato facilita:

- manutenção do conteúdo;
- expansão para novos jogos;
- criação de novas linguagens no `Code Lab`;
- revisão de desafios sem alterar a lógica central.

## Como Executar Localmente

### Pré-requisitos

- `Python 3.10+` recomendado
- ambiente virtual opcional, mas recomendado

### Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Execução

```bash
streamlit run app.py
```

Depois, abra a URL local exibida no terminal, normalmente:

```text
http://localhost:8501
```

## Testes e Validação

### Rodar os testes automatizados

```bash
python -m unittest discover -s tests -v
```

### Validar sintaxe dos arquivos principais

```bash
python -m py_compile app.py ui/theme.py ui/components.py
```

### Observações

- os testes cobrem partes importantes da lógica e regressões conhecidas;
- a validação visual final deve ser feita no navegador com `streamlit run app.py`;
- componentes do Streamlit podem exibir avisos quando executados fora do modo padrão do framework durante testes unitários.

## Acessibilidade

O projeto inclui recursos para melhorar a experiência de pessoas com diferentes necessidades de uso:

- contraste mais forte;
- aumento de fonte;
- redução de efeitos visuais;
- foco visível;
- leitura automatizada da tela atual;
- apoio ao uso com leitores de tela do navegador;
- feedback textual claro de erros, acertos e progresso.

Observação importante:
para uma validação completa de acessibilidade, o ideal é testar com ferramentas reais como `NVDA`, `VoiceOver` e navegação apenas por teclado.

## Deploy

O projeto roda em:

- ambiente local com `Streamlit`;
- `Streamlit Community Cloud`.

Aplicação publicada:

https://desafio-jogo-adivinhacao-bo25wk4blgetwgqvfw9q7v.streamlit.app/

## Roadmap

Possíveis melhorias futuras:

- ampliar o `Code Lab` com novos formatos de desafio;
- adicionar estatísticas detalhadas por perfil;
- criar conquistas e medalhas;
- melhorar tutorial interativo dentro do app;
- adicionar modo campeonato por rodadas;
- incluir novas bases educacionais e novos jogos;
- fortalecer validação com testes de interface.

## Status do Projeto

Projeto funcional, em evolução contínua, com foco em:

- experiência do usuário;
- acessibilidade;
- arquitetura mais profissional;
- expansão do conteúdo;
- estabilidade da lógica principal.
