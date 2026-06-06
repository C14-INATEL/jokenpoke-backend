<h1 align="left">
  <img src="https://i.imgur.com/otQevnB.png" width="35">
  JokenPoke  — Backend API
</h1>

> Documentação técnica completa — Engenharia de Software & DevOps  
> Curso de Engenharia de Software · INATEL · 2025

---

## Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Tecnologias Utilizadas](#2-tecnologias-utilizadas)
3. [Estrutura do Projeto](#3-estrutura-do-projeto)
4. [Funcionalidades](#4-funcionalidades)
5. [Guia de Instalação](#5-guia-de-instalação)
6. [Guia de Uso](#6-guia-de-uso)
7. [Histórias de Usuário](#7-histórias-de-usuário)
8. [Metodologia de Desenvolvimento](#8-metodologia-de-desenvolvimento)
9. [Dinâmica de Desenvolvimento](#9-dinâmica-de-desenvolvimento)
10. [Refatorações](#10-refatorações)
11. [Estratégia de Testes](#11-estratégia-de-testes)
12. [Cobertura de Testes](#12-cobertura-de-testes)
13. [Containerização](#13-containerização)
14. [Docker Hub](#14-docker-hub)
15. [Docker Compose](#15-docker-compose)
16. [Pipeline CI/CD](#16-pipeline-cicd)
17. [Infraestrutura como Código](#17-infraestrutura-como-código)
18. [Uso de Inteligência Artificial](#18-uso-de-inteligência-artificial)
19. [Conclusão](#19-conclusão)

---

## 1. Visão Geral do Projeto

### Objetivo do Sistema

O **JokenPoke** é uma API REST de batalha de cartas colecionáveis baseada no universo Pokémon, desenvolvida como projeto acadêmico interdisciplinar para as disciplinas de Engenharia de Software e DevOps do curso de Engenharia de Software do INATEL.

**Problema resolvido:** ausência de um backend completo e bem estruturado para suportar um jogo de cartas multiplayer com progressão de ranking, autenticação segura, sistema de batalha por turnos e gerenciamento de decks.

**Público-alvo:** desenvolvedores e alunos que desejam consumir a API para construir clientes (web, mobile ou desktop) para o jogo, além dos avaliadores acadêmicos das disciplinas envolvidas.

**Motivação:** o projeto foi concebido para demonstrar, na prática, a aplicação conjunta de princípios de Engenharia de Software (Clean Architecture, TDD, histórias de usuário, DoR/DoD) e práticas DevOps modernas (CI/CD com Jenkins, containerização com Docker, análise estática com SonarQube, deploy automatizado).

**Benefícios:**
- API REST documentada e navegável via Swagger/OpenAPI
- Sistema de autenticação stateless com JWT
- Lógica de batalha determinística baseada em vantagens de elemento
- Progressão de ranking automática após cada batalha
- Pipeline CI/CD completa com gates de qualidade e segurança

---

### Escopo

**O que o sistema faz:**
- Cadastro e autenticação de usuários via JWT
- Gerenciamento de coleção de cartas (cards)
- Montagem de deck personalizado
- Execução de batalhas entre jogadores com rounds automáticos
- Atualização automática de ranking após batalhas
- Concessão de carta de recompensa ao vencedor
- Consulta pública de ranking de jogadores
- Análise estática de qualidade de código com SonarQube
- Pipeline automatizada de build, teste e publicação

**Fora do escopo:**
- Interface visual (frontend) — a API serve como backend para clientes externos
- Sistema de pagamentos ou microtransações
- Chat em tempo real ou notificações push
- Matchmaking automático entre jogadores
- Modo offline

---

### Arquitetura Geral

O projeto adota **Clean Architecture** (Arquitetura Limpa), com separação estrita de responsabilidades em camadas concêntricas:

```
┌─────────────────────────────────────────────────────────┐
│                    Interfaces (API)                     │
│               FastAPI Routes · Schemas                  │
├─────────────────────────────────────────────────────────┤
│                   Application Layer                     │
│                      Use Cases                          │
├─────────────────────────────────────────────────────────┤
│                     Domain Layer                        │
│             Entities · Rules · Factories                │
├─────────────────────────────────────────────────────────┤
│                 Infrastructure Layer                    │
│      SQLAlchemy Models · Repositories · Security        │
└─────────────────────────────────────────────────────────┘
```

**Componentes principais:**

| Componente | Tecnologia | Descrição |
|---|---|---|
| Backend | FastAPI + Python 3.12 | API REST assíncrona com documentação OpenAPI automática |
| Banco de dados | PostgreSQL (produção) / SQLite (testes) | Persistência relacional com Alembic para migrations |
| Autenticação | JWT (python-jose) + bcrypt (passlib) | Tokens stateless com hash seguro de senhas |
| ORM | SQLAlchemy 2.x | Mapeamento objeto-relacional com suporte a migrations |
| Containers | Docker + Docker Compose | Isolamento de ambiente e orquestração de serviços |
| CI/CD | Jenkins (containerizado) | Pipeline automatizada de 10 estágios |
| Qualidade | SonarQube Community | Análise estática de código e quality gate |
| Deploy | Railway | Plataforma de deploy em nuvem com PostgreSQL gerenciado |
| Tunnel | ngrok | Exposição do Jenkins para webhooks do GitHub |

---

## 2. Tecnologias Utilizadas

| Categoria | Tecnologia | Versão | Finalidade |
|---|---|---|---|
| **Linguagem** | Python | 3.12 | Linguagem principal do backend |
| **Framework Web** | FastAPI | ≥0.115.0 | Construção da API REST com documentação OpenAPI |
| **Servidor ASGI** | Uvicorn | ≥0.30.0 | Servidor de produção para aplicações ASGI |
| **ORM** | SQLAlchemy | ≥2.0.0 | Mapeamento objeto-relacional e gerenciamento de sessões |
| **Migrations** | Alembic | ≥1.13.0 | Controle de versão do schema do banco de dados |
| **Banco (produção)** | PostgreSQL | — | Banco de dados relacional em produção (Supabase/Railway) |
| **Banco (testes)** | SQLite | — | Banco de dados em memória/arquivo para testes isolados |
| **Driver PostgreSQL** | psycopg2-binary | ≥2.9.0 | Adaptador Python para PostgreSQL |
| **Autenticação** | python-jose[cryptography] | ≥3.3.0 | Geração e validação de tokens JWT |
| **Hashing** | passlib[bcrypt] + bcrypt | ≥1.7.4 / ≥5.0.0 | Hash seguro de senhas com bcrypt |
| **Validação** | Pydantic + pydantic-settings | ≥2.0.0 | Validação de dados e gerenciamento de configurações |
| **Variáveis de ambiente** | python-dotenv | ≥1.0.0 | Carregamento de variáveis de ambiente do arquivo `.env` |
| **Multipart** | python-multipart | ≥0.0.30 | Suporte a formulários (OAuth2PasswordRequestForm) |
| **Gerenciador de pacotes** | Poetry | — | Gerenciamento de dependências e ambientes virtuais |
| **Linter/Formatter** | Ruff | ≥0.4.0 | Análise estática e formatação de código Python |
| **Type Checker** | MyPy | ≥1.10.0 | Verificação estática de tipos |
| **Framework de testes** | pytest | ≥8.0.0 | Execução de testes unitários e de integração |
| **Cobertura de testes** | pytest-cov | ≥5.0.0 | Geração de relatórios de cobertura de código |
| **Cliente HTTP (testes)** | httpx + httpx2 | ≥0.27.0 / ≥2.3.0 | Cliente HTTP para testes de integração com FastAPI TestClient |
| **Watch mode** | pytest-watcher | ≥0.4.0 | Execução automática de testes em modo observação |
| **Auditoria de segurança** | pip-audit | ≥2.7.0 | Verificação de CVEs em dependências Python |
| **SAST** | Bandit | ≥1.9.4 | Análise estática de segurança do código Python |
| **Detecção de secrets** | detect-secrets | ≥1.5.0 | Varredura de credenciais expostas no código |
| **Qualidade de código** | SonarQube Community | — | Análise estática, quality gate e métricas de código |
| **Containerização** | Docker | — | Construção e execução de imagens de container |
| **Orquestração local** | Docker Compose | — | Orquestração de múltiplos containers |
| **CI/CD** | Jenkins | LTS | Pipeline automatizada de integração e entrega contínua |
| **Scanner de imagem** | Trivy | — | Varredura de vulnerabilidades em imagens Docker |
| **Deploy** | Railway | — | Plataforma de deploy em nuvem |
| **Tunnel** | ngrok | — | Exposição de serviços locais para webhooks externos |
| **Automação** | Make | — | Automatização de tarefas de desenvolvimento e CI |
| **Controle de versão** | Git + GitHub | — | Versionamento distribuído e hospedagem do código |

---

## 3. Estrutura do Projeto

```
jokenpoke-backend/
├── .github/                        # Configurações do GitHub
│   ├── workflows/dev-ci.yml        # Workflow de CI para pull requests
│   ├── copilot-instructions.md     # Instruções para GitHub Copilot
│   └── pull_request_template.md    # Template padrão de Pull Request
├── alembic/                        # Controle de versão do banco de dados
│   ├── versions/                   # Migrations em ordem cronológica
│   ├── env.py                      # Configuração do ambiente Alembic
│   └── script.py.mako              # Template para geração de migrations
├── app/                            # Código-fonte principal da aplicação
│   ├── application/                # Camada de aplicação (casos de uso)
│   │   └── use_cases/              # Um arquivo por caso de uso
│   ├── core/                       # Configurações e utilitários globais
│   │   ├── middleware/             # Middlewares: CORS, GZip, logging, rate limit
│   │   ├── utils/randomizer.py     # Utilitário de aleatoriedade
│   │   ├── config.py               # Configurações da aplicação (pydantic-settings)
│   │   └── logging.py              # Configuração centralizada de logs
│   ├── domain/                     # Camada de domínio (regras de negócio puras)
│   │   ├── entities/               # Entidades do domínio (Battle, Card, Deck, etc.)
│   │   ├── factories/              # Fábricas para criação de objetos de domínio
│   │   └── rules/                  # Regras de negócio (batalha, vantagem de elemento)
│   ├── infrastructure/           # Camada de infraestrutura (detalhes técnicos)
│   │   ├── data/pokemons.json    # Dataset estático de Pokémons
│   │   ├── db/                   # Modelos ORM e gerenciamento de sessão
│   │   ├── repositories/         # Implementações concretas dos repositórios
│   │   └── security/             # JWT, hash de senha, dependências de autenticação
│   ├── interfaces/                     # Camada de interface (adapters da API)
│   │   └── api/
│   │       ├── routes/                 # Rotas agrupadas por domínio
│   │       ├── dependencies.py         # Injeção de dependências do FastAPI
│   │       ├── exception_handlers.py   # Handlers globais de exceção
│   │       └── router.py               # Agregador de todos os routers
│   ├── schemas/                  # Schemas Pydantic (request/response)
│   ├── shared/                   # Código compartilhado entre camadas
│   │   ├── constants/            # Constantes do jogo
│   │   ├── exceptions/           # Exceções de domínio customizadas
│   │   ├── types/                # Tipos customizados
│   │   └── utils/pagination.py   # Utilitário de paginação
│   └── main.py                   # Ponto de entrada da aplicação FastAPI
├── docker/                         # Dockerfiles e configurações de container
│   ├── jenkins/Dockerfile.jenkins  # Imagem Jenkins customizada com ferramentas
│   └── Dockerfile                  # Imagem de produção da API
├── docs/                           # Documentação de histórias de usuário
│   ├── Us-001.md                   # Atualização de ranking pós-batalha
│   ├── Us-002.md                   # Autenticação JWT via login
│   ├── Us-003.md                   # Lógica de batalha
│   ├── Us-004.md                   # Estabilidade do ambiente de testes
│   └── Us-005.md                   # Deleção em cascata de usuário
├── scripts/notify.py               # Script de notificação por e-mail pós-pipeline
├── tests/                          # Suíte completa de testes
│   ├── fixtures/                   # Fixtures reutilizáveis (battles, cards, users, db)
│   ├── integration/                # Testes de integração (TestClient + SQLite)
│   └── unit/                       # Testes unitários organizados por camada
├── .env.example                    # Exemplo de variáveis de ambiente
├── .secrets.baseline               # Baseline do detect-secrets
├── Jenkinsfile                     # Definição declarativa da pipeline CI/CD
├── Makefile                        # Automação de tarefas de desenvolvimento
├── alembic.ini                     # Configuração do Alembic
├── docker-compose.yml              # Orquestração dos serviços (API, Jenkins, SonarQube, ngrok)
├── poetry.lock                     # Lock file com versões exatas das dependências
├── pyproject.toml                  # Configuração do projeto, dependências e ferramentas
├── railway.toml                    # Configuração de deploy no Railway
└── sonar-project.properties        # Configuração do SonarQube Scanner
```

### Responsabilidade das camadas principais

**`app/domain/`** — contém as regras de negócio puras do jogo. Não possui dependências externas (sem banco, sem framework). É a camada mais interna e estável da arquitetura.

**`app/application/`** — orquestra os casos de uso (ex: `StartBattleUseCase`, `LoginUserUseCase`). Depende apenas de interfaces abstratas, não de implementações concretas.

**`app/infrastructure/`** — implementa os contratos definidos pelo domínio usando tecnologias concretas (SQLAlchemy, JWT, bcrypt). É a camada mais externa e a única que "sabe" sobre banco de dados e frameworks.

**`app/interfaces/api/`** — adapta a API HTTP ao mundo dos casos de uso. As rotas recebem requests, delegam para use cases e retornam responses Pydantic.

---

## 4. Funcionalidades

### 4.1 Cadastro de Usuário

**Descrição:** permite que um novo jogador crie uma conta na plataforma informando nome de usuário e senha.

**Fluxo de uso:**
1. Cliente envia `POST /auth/register` com `username` e `password`
2. Sistema valida unicidade do username
3. Senha é hasheada com bcrypt
4. Usuário é persistido com rank inicial
5. Resposta retorna `access_token` JWT imediatamente

**Benefício:** onboarding imediato — o jogador já recebe o token de acesso ao se cadastrar, sem necessidade de fazer login separado.

---

### 4.2 Autenticação via Login (JWT)

**Descrição:** permite que usuários já cadastrados obtenham um `access_token` JWT para acessar rotas protegidas.

**Fluxo de uso:**
1. Cliente envia `POST /auth/login` com `username` e `password` via form-data
2. Sistema valida credenciais contra o banco de dados
3. Em caso de sucesso, retorna `access_token` JWT válido
4. Token é utilizado no header `Authorization: Bearer <token>` nas demais requisições

**Benefício:** autenticação stateless e segura, eliminando a necessidade de sessões no servidor.

---

### 4.3 Gerenciamento de Cartas

**Descrição:** listagem e consulta das cartas disponíveis no jogo, baseadas no dataset de Pokémons.

**Fluxo de uso:**
1. Cliente autentica-se via JWT
2. Acessa `GET /cards` para listar cartas disponíveis
3. Consulta carta específica via `GET /cards/{card_id}`

**Benefício:** permite ao cliente construir interfaces de seleção de cartas para montagem de deck.

---

### 4.4 Montagem de Deck

**Descrição:** permite que o jogador monte seu deck de batalha selecionando cartas da sua coleção.

**Fluxo de uso:**
1. Jogador autenticado acessa `POST /decks/{user_id}/build`
2. Sistema valida o número de cartas e a propriedade das mesmas
3. Deck é persistido e associado ao usuário
4. Jogador pode consultar seu deck atual

**Benefício:** personalização da estratégia de jogo antes das batalhas.

---

### 4.5 Sistema de Batalha

**Descrição:** executa uma batalha automatizada por rounds entre dois jogadores, aplicando regras de vantagem de elemento.

**Fluxo de uso:**
1. Atacante autenticado envia `POST /battle/{defender_id}`
2. Sistema valida que ambos os jogadores possuem deck montado
3. Rounds são processados automaticamente com base nas regras de `MOVE_WEAKNESS`
4. Resultado é retornado com: lista de rounds, movimentos de cada round, vencedor final, ranking atualizado e carta de recompensa (se vencedor)

**Benefício:** experiência de jogo completa e determinística, com progressão imediata refletida no ranking.

---

### 4.6 Sistema de Ranking

**Descrição:** exibe o ranking global de jogadores ordenado por pontuação.

**Fluxo de uso:**
1. Cliente acessa `GET /ranking` (rota pública ou autenticada)
2. Sistema retorna lista de jogadores com rank e pontos
3. Posição é calculada dinamicamente pela ordenação de pontos

**Benefício:** gamificação e incentivo à progressão contínua no jogo.

---

### 4.7 Gerenciamento de Usuários

**Descrição:** operações de CRUD sobre o perfil do jogador, incluindo atualização e deleção com cascata.

**Fluxo de uso:**
1. `GET /users` — lista todos os usuários (paginado)
2. `GET /users/{id}` — consulta usuário específico
3. `PUT /users/{id}` — atualiza dados do perfil
4. `DELETE /users/{id}` — remove usuário e todos os dados relacionados (deck e cards) via cascade

**Benefício:** gestão completa do ciclo de vida do jogador, com garantia de integridade referencial no banco.

---

## 5. Guia de Instalação

### Pré-requisitos

| Ferramenta | Versão mínima | Verificação |
|---|---|---|
| Git | 2.x | `git --version` |
| Python | 3.11+ | `python3 --version` |
| Poetry | 1.8+ | `poetry --version` |
| Docker | 24.x | `docker --version` |
| Docker Compose | 2.x (plugin) | `docker compose version` |
| Make | 4.x | `make --version` |

---

### Clonagem

```bash
git clone https://github.com/C14-INATEL/jokenpoke-backend.git
cd jokenpoke-backend
```

---

### Configuração das Variáveis de Ambiente

Copie o arquivo de exemplo e edite com suas configurações:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```dotenv
# Banco de dados (PostgreSQL em produção, SQLite em desenvolvimento local)
DATABASE_URL=postgresql://usuario:senha@host:5432/jokenpoke

# Segurança JWT
JWT_SECRET_KEY=sua-chave-secreta-aqui-use-pelo-menos-32-caracteres
JWT_ALGORITHM=HS256

# Configurações de ambiente
ENVIRONMENT=development

# ngrok (necessário para webhooks do Jenkins com GitHub)
NGROK_AUTHTOKEN=seu-token-ngrok
NGROK_DOMAIN=seu-dominio.ngrok-free.app

# Docker Hub (necessário para o pipeline CI/CD)
DOCKER_HUB_USER=seu-usuario-dockerhub
```

---

### Execução Local (sem Docker)

```bash
# 1. Instalar dependências
make install
# ou: poetry install

# 2. Aplicar migrations do banco de dados
poetry run alembic upgrade head

# 3. Iniciar o servidor com hot reload
make local-run
# ou: poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em: `http://localhost:8000`  
Documentação Swagger: `http://localhost:8000/docs`  
Documentação ReDoc: `http://localhost:8000/redoc`

---

### Execução com Docker Compose (Recomendado)

```bash
# Construir e subir todos os serviços (API + Jenkins + SonarQube + ngrok)
make dev
# ou: docker compose up --build

# Subir apenas a API em background
make up
# ou: docker compose up -d api

# Verificar logs da API
make logs
# ou: docker compose logs -f api

# Parar todos os containers
make down
# ou: docker compose down
```

**Serviços disponíveis após `make up`:**

| Serviço | URL | Descrição |
|---|---|---|
| API | `http://localhost:8000` | API REST principal |
| Swagger | `http://localhost:8000/docs` | Documentação interativa |
| Jenkins | `http://localhost:8080` | Interface CI/CD |
| SonarQube | `http://localhost:9000` | Análise de qualidade |
| ngrok | `http://localhost:4040` | Painel do tunnel |

---

### Aplicar Migrations

```bash
# Aplicar todas as migrations pendentes
poetry run alembic upgrade head

# Verificar status das migrations
poetry run alembic current

# Reverter última migration
poetry run alembic downgrade -1
```

---

## 6. Guia de Uso

### Fluxo Principal

```
1. Registro          POST /auth/register
2. Login             POST /auth/login          → recebe access_token
3. Listar cartas     GET  /cards               (autenticado)
4. Montar deck       POST /decks/{user_id}/build
5. Batalhar          POST /battle/{defender_id}
6. Ver ranking       GET  /ranking
```

---

### Exemplos de Requisições

**1. Registrar novo usuário:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ash_ketchum", "password": "pikachu123"}'
```

**2. Fazer login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ash_ketchum&password=pikachu123"
```

**3. Montar deck (autenticado):**
```bash
curl -X POST http://localhost:8000/decks/1/build \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json"
```

**4. Iniciar batalha:**
```bash
curl -X POST http://localhost:8000/battle/2 \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**5. Consultar ranking:**
```bash
curl http://localhost:8000/ranking
```

---

### Executar Testes

```bash
# Todos os testes
make test

# Apenas unitários
make test-unit

# Apenas integração
make test-integration

# Com relatório de cobertura
make test-cov

# Em modo watch (re-executa ao salvar arquivos)
make watch-test
```

---

## 7. Histórias de Usuário

As histórias de usuário completas estão documentadas no diretório [`docs/`](./docs/). Abaixo, um resumo rastreável:

| ID | Título | Epic | Prioridade | Status | PRs |
|---|---|---|---|---|---|
| [US-001](./docs/Us-001.md) | Atualização de Ranking e Recompensa ao Vencedor | Progressão do Jogador | Alta | ✅ Concluído | #32, #33 |
| [US-002](./docs/Us-002.md) | Autenticação via Endpoint de Login com JWT | Autenticação e Segurança | Alta | ✅ Concluído | #24, #28 |
| [US-003](./docs/Us-003.md) | Lógica de Batalha com Validação de Deck | Sistema de Batalha | Alta | ✅ Concluído | #16, #17 |
| [US-004](./docs/Us-004.md) | Estabilidade e Padronização do Ambiente de Testes | Qualidade de Código | Média | ✅ Concluído | #29, #30 |
| [US-005](./docs/Us-005.md) | Deleção Completa de Usuário com Cascade | Gerenciamento de Usuários | Alta | ✅ Concluído | #34, #35 |

### Rastreabilidade por PR

| PR | Tipo | US Relacionada | Descrição |
|---|---|---|---|
| #16 | Feature | US-003 | Implementa validação e lógica de batalha |
| #17 | Test | US-003 | Testes unitários de batalha (51 testes) |
| #24 | Feature | US-002 | Endpoint de login com JWT |
| #28 | Test | US-002 | Testes de integração para autenticação (5 testes) |
| #29 | Chore | US-004 | Adiciona httpx2 para compatibilidade com TestClient |
| #30 | Refactor | US-004 | Padroniza dependências com `Annotated` |
| #32 | Feature | US-001 | Atualiza ranking e recompensa pós-batalha |
| #33 | Test | US-001 | Testes de integração para batalha e usuários |
| #34 | Hotfix | US-005 | Cascade delete User → Deck |
| #35 | Fix + Test | US-005 | Cascade delete Card → Deck + testes expandidos |

---

## 8. Metodologia de Desenvolvimento

### Metodologia Adotada

O projeto adota **Scrum adaptado** para o contexto acadêmico, com ciclos de sprint curtos (semanais ou quinzenais), backlog gerenciado via kanban no Notion e rastreabilidade via Pull Requests no GitHub.

**Justificativa:** o Scrum favorece a entrega incremental de valor, a transparência no progresso e a adaptação contínua — alinhado tanto com as necessidades do projeto (funcionalidades interdependentes) quanto com as exigências avaliativas das disciplinas.

**Evidências:**
- Histórias de usuário documentadas com critérios de aceitação em Gherkin (docs/Us-*.md)
- DoR e DoD definidos e verificados em cada PR
- Rastreabilidade completa: US → PR → testes → commits

---

### Ferramentas de Gestão

| Ferramenta | Finalidade |
|---|---|
| **GitHub** | Hospedagem de código, PRs, code review, status checks |
| **Notion** | Backlog, planejamento de sprints, documentação ágil |
| **GitHub Actions** | CI leve para pull requests (`.github/workflows/dev-ci.yml`) |
| **Jenkins** | Pipeline CI/CD completa no ambiente de integração implementada na main |

> **Notion do projeto:** [JokenPoke Agile HQ](https://app.notion.com/p/JokenPoke-Agile-HQ-843e3031246e4294915365850becba51)

---

### Papéis

| Papel | Responsáveis | Responsabilidades |
|---|---| --- |
| **Product Owner** | Gabriel, Matheus | Priorização do backlog, definição de critérios de aceitação, validação das entregas |
| **Desenvolvedor** | Christian, Eduardo, Gabriel, Maria Clara, Matheus, Rafael | Implementação de features, testes unitários, code review |
| **QA** | Christian, Maria Clara, Matheus, Rafael | Testes de integração, validação de critérios de aceitação, revisão de cobertura |
| **DevOps** | Eduardo, Gabriel, Matheus | Pipeline Jenkins, Docker, SonarQube, deploy Railway, infraestrutura como código |

> Embora tenhamos separado em atuações majoritárias, todos os membros participaram de todas as etapas.
---

### Definição de Pronto (DoR — Definition of Ready)

Uma história está **pronta para desenvolvimento** quando:

- [ ] A user story está escrita no formato "Como... eu quero... para que..."
- [ ] Os critérios de aceitação estão definidos em Gherkin
- [ ] A história está estimada pela equipe
- [ ] As dependências técnicas estão identificadas
- [ ] O escopo está claro e não ambíguo
- [ ] A história cabe em uma sprint

---

### Definição de Concluído (DoD — Definition of Done)

Uma história está **concluída** quando:

- [ ] A implementação foi revisada e aprovada via Pull Request
- [ ] Testes unitários e/ou de integração foram implementados e passam
- [ ] Cobertura de testes não regrediu abaixo do limiar de 90%
- [ ] O lint (Ruff) passa sem erros
- [ ] A pipeline CI/CD executa com sucesso (build + lint + testes + quality gate)
- [ ] A documentação da US está atualizada com rastreabilidade de PRs

---

### Cadência

| Cerimônia | Frequência | Duração estimada |
|---|---|---|
| Sprint Planning | Início de cada sprint | 1h |
| Daily (quase daily) | sempre que possível no Coffee Break do inatel | 20 min |
| Sprint Review | Fim de cada sprint | 1h |
| Retrospectiva | Fim de cada sprint | 30 min |
| Code Review | A cada PR aberto | Assíncrono |

---

## Métricas

### Histórias por Sprint

| Sprint | Período | PRs Mergeados | Histórias Entregues |
|---------|----------|---------------|---------------------|
| Sprint 1 | 25/05 - 31/05/2026 | 8 (PR #15–#22) | US-003 |
| Sprint 2 | 01/06 - 05/06/2026 | 15 (PR #23–#37) | US-002, US-004, US-001, US-005 |

> Sprints agrupados por semana de merge dos PRs.

---

### Lead Time por US

| US | Abertura do 1º PR | Merge do último PR | Lead Time |
|-----|-------------------|-------------------|-----------|
| US-003 | 29/05/2026 | 31/05/2026 | 2 dias |
| US-002 | 01/06/2026 | 02/06/2026 | 1 dia |
| US-004 | 02/06/2026 | 02/06/2026 | 0 dias |
| US-001 | 03/06/2026 | 04/06/2026 | 1 dia |
| US-005 | 04/06/2026 | 04/06/2026 | 0 dias |

> Lead time calculado da abertura do primeiro PR ao merge do último PR da história.

---

### Throughput

| Período | Duração | PRs Mergeados | US Entregues | Média PRs/semana |
|----------|----------|---------------|--------------|------------------|
| 25/05 - 05/06/2026 | 11 dias (~1,6 semanas) | 23 | 5 | ~14,6 |

---

### Análise das Métricas

- Pull Requests anteriores ao #15 foram usados para implementações de padronização no projeto ou estruturas não diretamente relevantes para a implementação das US.
- Foram entregues 5 histórias de usuário ao longo de 2 sprints.
- O throughput total foi de 23 pull requests mergeados.
- O lead time médio das histórias foi de aproximadamente 0,8 dias.
- A Sprint 2 concentrou a maior parte das entregas, representando 80% das histórias concluídas.
- O fluxo de desenvolvimento apresentou baixa latência entre implementação e revisão, favorecendo ciclos curtos de feedback.

---

## 9. Dinâmica de Desenvolvimento

### Organização do Trabalho

O trabalho é organizado em torno de histórias de usuário no backlog do Notion. Cada história gera um ou mais Pull Requests no GitHub, garantindo rastreabilidade completa entre requisito e implementação.

---

### Fluxo de Branches

Todas as branches seguem o formato obrigatório:

```
{iniciais}/{tipo}/{descricao-em-ingles-kebab-case}
```

```
develop
 └── mn/feature/user-authentication
 └── gs/feature/pokemon-filter
 └── mn/fix/login-validation
 └── ra/fix/api-timeout
 └── mn/hotfix/cascade-delete
 └── mn/refactor/auth-service
 └── mn/test/battle-unit-tests
 └── mn/docs/readme-update
 └── mn/chore/update-dependencies
```

| Segmento | Descrição |
|---|---|
| `{iniciais}` | Iniciais do responsável pela branch (ex: `mn`, `gs`, `ep`) |
| `{tipo}` | Categoria da alteração (ver tabela abaixo) |
| `{descricao}` | Descrição curta em inglês usando kebab-case |

**Tipos permitidos:**

| Tipo | Uso |
|---|---|
| `feature` | Nova funcionalidade |
| `fix` | Correção de bug planejada |
| `hotfix` | Correção urgente de bug |
| `refactor` | Refatoração sem mudança de comportamento |
| `test` | Adição ou expansão de testes |
| `docs` | Documentação |
| `chore` | Manutenção e infraestrutura |

**Integrantes da equipe:**

| Integrante | Iniciais |
|---|---|
| Matheus Netto | `mn` |
| Gabriel Soares | `gs` |
| Eduardo Pereira | `ep` |
| Maria Clara | `mc` |
| Christian Salles | `cs` |
| Rafael Areias | `ra` |

---

### Estratégia de Commits

O projeto segue a convenção **Conventional Commits**, com mensagens no formato:

```
tipo(escopo): descrição concisa

Corpo opcional com detalhes
```

**Tipos utilizados:** `feat`, `fix`, `test`, `refactor`, `chore`, `docs`, `style`

---

### Processo de Code Review

Todo Pull Request deve seguir a estrutura e convenções abaixo.

---

**Formato obrigatório do título:**

```
[Tipo] [Tipo2] Descrição curta
```

**Tipos permitidos:**

| Tipo | Uso |
|---|---|
| `Feat` | Nova funcionalidade |
| `Fix` | Correção de bug |
| `Docs` | Documentação |
| `Refactor` | Refatoração |
| `Test` | Testes |
| `Chore` | Configuração e manutenção |
| `Backend` | Modificações gerais no repositório (Makefile, Docker, etc.) |
| `Frontend` | Modificações gerais no repositório de frontend |

Exemplos válidos:
```
[Feat] [User] Adiciona tela de login
[Fix] [Api] Corrige timeout da API
[Docs] [Backend] Atualiza documentação do backend
[Refactor] [Api] Reorganiza auth service
```

---

**Template oficial de PR:**

```
# Descrição
Explique objetivamente o que foi desenvolvido neste PR.

---

# Contexto
Por que essa alteração foi necessária?

---

# How To Test
1. Execute o projeto
2. Acesse ...
3. Clique em ...
4. Verifique se ...

---

# Benefícios
Quais melhorias essa alteração traz?
```

---

**Requisitos obrigatórios de todo PR:**
- Deve ser realizado sempre para `develop`
- Título no formato padronizado
- Template preenchido (Descrição, Contexto, How To Test, Benefícios)
- Pelo menos 1 reviewer atribuído
- Mínimo de 3 labels coerentes com a alteração
- Assinatura do autor

---

**Estratégia de merge: Squash and Merge**

O projeto adota **Squash and Merge** em todos os PRs, consolidando os commits da branch em um único commit na `develop`. O título do PR torna-se o commit final, por isso a padronização do título é obrigatória.

Exemplo do fluxo completo:

| Etapa | Exemplo |
|---|---|
| Branch | `mn/feature/favorites-system` |
| Título do PR | `[Feature] [User] Adiciona sistema de favoritos` |
| Commit após merge | `[Feature] [User] Adiciona sistema de favoritos (#15)` |

---

### Fluxo Geral

1. Desenvolvedor abre PR com template preenchido (`.github/pull_request_template.md`)
2. GitHub Actions executa CI automático (lint + testes)
3. Pelo menos um revisor aprova o PR
4. PR é mergeado após aprovação e CI verde
5. `develop` é mergeada na `main`
6. Jenkins executa pipeline completa (build + lint + testes + sonar + security scan)
7. Status check do Jenkins deve estar verde (`ci/jenkins: success`)

---

### Problemas Encontrados e Soluções Adotadas

| Problema | Sprint | Solução |
|---|---|---|
| `TestClient` do FastAPI emitia warnings de depreciação com `httpx` | US-004 | Adição de `httpx2` como dependência (PR #29) |
| Injeção de dependências com padrão legado `Depends()` alertado pelo SonarLint | US-004 | Refatoração para padrão `Annotated[Tipo, Depends()]` (PR #30) |
| `DELETE /users/{id}` falhava com erro de FK quando usuário tinha deck | US-005 | Cascade configurado em ORM e DDL do banco, User → Deck (PR #34) |
| Cascade User → Deck não cobria a relação Card → Deck, gerando órfãos | US-005 | Segunda migration com `ondelete=CASCADE` em `deck.card_id` (PR #35) |
| Atacante da batalha estava fixado no ID 1, sem autenticação | US-003 | Substituição por autenticação JWT em US posterior (PR #24/US-002) |

---

### Lições Aprendidas

- **Cascade no ORM não é suficiente** — é necessário configurar `ondelete=CASCADE` no DDL do banco para garantir integridade em todos os cenários de deleção.
- **Separar PRs de implementação e de testes** facilita a revisão e mantém histórico claro de responsabilidades.
- **Warnings de depreciação devem ser tratados cedo** — o acúmulo de warnings obscurece problemas reais nos logs de testes.
- **Padrões modernos de injeção de dependências** (`Annotated`) melhoram a legibilidade e evitam alertas de análise estática.

---

### Melhorias Futuras

- Implementar matchmaking automático entre jogadores de ranks similares
- Adicionar modo de batalha assíncrono (jogadores em sessões diferentes)
- Desenvolver sistema de torneios
- Adicionar testes de carga com Locust (dependência já presente no `pyproject.toml`)
- Expandir dataset de Pokémons com mais cartas e tipos de elementos
- Implementar refresh token para renovação de sessão JWT

---

## 10. Refatorações

### 10.1 Substituição de `Depends()` legado por `Annotated` (PR #30 — US-004)

**Problema original:** as rotas e arquivos de dependências usavam o padrão legado de injeção de dependências do FastAPI, passando `Depends()` diretamente como valor padrão de parâmetros. O SonarLint classificava esse padrão como alerta de boas práticas.

**Solução aplicada:** todos os parâmetros de dependência foram refatorados para o padrão moderno com `Annotated`:

```python
# Antes (padrão legado)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    ...

# Depois (padrão moderno)
async def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    ...
```

**Benefícios obtidos:**
- Eliminação de alertas do SonarLint
- Maior legibilidade e expressividade do tipo da dependência
- Alinhamento com as recomendações oficiais da documentação do FastAPI
- Nenhuma mudança de comportamento externo

---

### 10.2 Correção de Cascade Delete em Duas Etapas (PRs #34 e #35 — US-005)

**Problema original:** o cascade estava configurado apenas no nível do ORM (SQLAlchemy), mas não no DDL do banco de dados. Isso causava erros de violação de FK ao deletar usuários com decks.

**Solução aplicada (PR #34):** configuração de `ondelete="CASCADE"` na FK `deck.user_id → users.id` tanto no modelo ORM quanto na migration do Alembic.

**Solução complementar (PR #35):** identificação de que a FK `deck.card_id → cards.id` também necessitava de cascade. Nova migration adicionada para completar a cadeia.

**Benefícios obtidos:**
- Eliminação de erros de FK em produção
- Garantia de integridade referencial completa
- Banco de dados sem registros órfãos após deleção de usuários

---

### 10.3 Campo `position` Substituído por `rank` (PR #32 — US-001)

**Problema original:** o campo `position` era persistido de forma estática no banco de dados, causando inconsistências na representação do ranking. A posição deveria ser calculada dinamicamente.

**Solução aplicada:** o campo `position` foi removido do modelo `User` e substituído por `rank` (persistido). A posição no ranking passou a ser calculada dinamicamente pela ordenação de pontos no momento da consulta.

**Benefícios obtidos:**
- Dados de ranking sempre consistentes com a realidade
- Eliminação de campo redundante no banco de dados
- Simplificação da lógica de atualização pós-batalha

---

## 11. Estratégia de Testes

### Pirâmide de Testes

```
           /\
          /  \
         / E2E\         (Smoke Tests — no pipeline Jenkins)
        /------\
       /   Int  \       (tests/integration/ — TestClient + SQLite)
      /----------\
     / Unit Tests \     (tests/unit/ — mocks + fixtures)
    /--------------\
```

---

### Testes Unitários

**Localização:** `tests/unit/`

**Organização:** espelham a estrutura do código-fonte — um diretório de testes para cada camada da aplicação.

| Módulo | Arquivo de teste | O que testa |
|---|---|---|
| `use_cases/build_deck` | `test_build_deck.py` | Lógica de montagem de deck |
| `use_cases/start_battle` | `test_start_battle.py` | Fluxo completo de batalha |
| `use_cases/login_user` | `test_login_user.py` | Autenticação e geração de token |
| `domain/rules/battle_rules` | `test_battle_rules.py` | Regras de round e vencedor |
| `domain/rules/element_advantage` | `test_element_advantage.py` | Vantagens de elemento entre tipos |
| `domain/entities/user` | `test_user.py` | Invariantes da entidade User |
| `infrastructure/security/jwt` | `test_jwt_handler.py` | Geração e validação de tokens JWT |
| `shared/exceptions` | `test_domain_exception.py`, `test_not_found_exception.py` | Comportamento das exceções |

**Estratégia:** uso extensivo de mocks para isolar cada unidade. Fixtures reutilizáveis em `tests/fixtures/` para evitar duplicação.

---

### Testes de Integração

**Localização:** `tests/integration/`

**Tecnologia:** FastAPI `TestClient` com banco SQLite em arquivo isolado, configurado via `dependency_overrides` no `conftest.py`.

| Arquivo | Cenários cobertos |
|---|---|
| `test_auth_routes.py` | Registro, login, credenciais inválidas, retorno de JWT |
| `test_battle_routes.py` | Batalha com vitória/derrota, erro sem deck, retorno estruturado |
| `test_card_routes.py` | Listagem e consulta de cartas |
| `test_deck_routes.py` | Montagem e consulta de deck |
| `test_user_routes.py` | CRUD de usuários, exclusão, not found |
| `test_ranking_routes.py` | Consulta de ranking ordenado |
| `test_delete_user_cascade.py` | Deleção com cascade de deck e cards |

**Isolamento:** cada execução de testes de integração cria um banco SQLite independente, garantindo que os testes não interfiram entre si nem com o ambiente de produção.

---

### Smoke Tests

**Localização:** Jenkinsfile — stage `Smoke Test`

**Objetivo:** verificação rápida de que o ambiente de produção (Railway) está operacional após o deploy.

**Cenários:**
1. `GET /health` → HTTP 200
2. `POST /auth/login` → token obtido com sucesso
3. `GET /pokemons/` → HTTP 200

---

### Ferramentas de Qualidade de Código

| Ferramenta | Finalidade | Executado em |
|---|---|---|
| Ruff (lint) | Verificação de estilo e erros comuns | Local + Jenkins |
| Ruff (format) | Formatação consistente do código | Local + Jenkins |
| MyPy | Verificação estática de tipos | Local (opcional) |
| Bandit | SAST — análise de segurança do código Python | Jenkins |
| pip-audit | Auditoria de CVEs em dependências | Jenkins |
| detect-secrets | Detecção de credenciais expostas | Jenkins |
| Trivy | Varredura de vulnerabilidades na imagem Docker | Jenkins |
| SonarQube | Análise estática completa + quality gate | Jenkins |

---

## 12. Cobertura de Testes

### Limiar de Cobertura

O projeto exige **cobertura mínima de 90%** (`COVERAGE_THRESHOLD=90`), configurada no Jenkinsfile e aplicada via flag `--cov-fail-under=90` do pytest-cov. O pipeline **falha automaticamente** se a cobertura cair abaixo desse limiar.

---

### Como Gerar o Relatório

```bash
# Relatório no terminal com linhas não cobertas
make test-cov
# ou: poetry run pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

# Relatório HTML detalhado (abre em reports/coverage-html/index.html)
open reports/coverage-html/index.html
```

---

### Formato dos Relatórios

| Formato | Localização | Uso |
|---|---|---|
| Terminal (term-missing) | Saída do terminal | Visualização rápida durante desenvolvimento |
| XML | `reports/coverage.xml` | Integração com SonarQube e CI |
| HTML | `reports/coverage-html/index.html` | Relatório visual detalhado por arquivo |
| JUnit XML | `reports/test-results.xml` | Relatório de testes para Jenkins |

---

### Interpretando o Relatório

O relatório HTML exibe para cada arquivo:
- **Statements:** total de instruções executáveis
- **Missing:** instruções não executadas por nenhum teste
- **Coverage%:** percentual de cobertura (≥90% exigido)
- **Branches:** cobertura de branches (if/else, etc.)

Arquivos com cobertura abaixo do limiar são destacados em vermelho no relatório HTML e na saída do terminal.

---

### Cobertura por Módulo

Resultado obtido via `make test-cov` — **166 testes passando, cobertura total de 97%**, superando o limiar mínimo de 90% exigido pela pipeline.

```
166 passed in 12.19s
```

#### `app/application/use_cases/`

| Arquivo | Statements | Não cobertos | Cobertura |
|---|---|---|---|
| `build_deck.py` | 24 | 0 | **100%** |
| `create_deck.py` | 7 | 0 | **100%** |
| `delete_user.py` | 13 | 0 | **100%** |
| `get_all_users.py` | 25 | 5 | 80% |
| `get_ranking.py` | 8 | 0 | **100%** |
| `get_user_by_id.py` | 25 | 0 | **100%** |
| `login_user.py` | 16 | 0 | **100%** |
| `register_user.py` | 25 | 0 | **100%** |
| `start_battle.py` | 40 | 0 | **100%** |
| `update_ranking.py` | 37 | 0 | **100%** |
| `update_user.py` | 12 | 1 | 92% |

#### `app/domain/`

| Arquivo | Statements | Não cobertos | Cobertura |
|---|---|---|---|
| `entities/battle.py` | 16 | 0 | **100%** |
| `entities/card.py` | 11 | 0 | **100%** |
| `entities/deck.py` | 11 | 0 | **100%** |
| `entities/pokemon.py` | 7 | 0 | **100%** |
| `entities/user.py` | 10 | 0 | **100%** |
| `factories/card_factory.py` | 14 | 1 | 93% |
| `rules/battle_rules.py` | 19 | 0 | **100%** |
| `rules/element_advantage.py` | 1 | 0 | **100%** |
| `rules/rank_up_down.py` | 2 | 0 | **100%** |

#### `app/infrastructure/`

| Arquivo | Statements | Não cobertos | Cobertura |
|---|---|---|---|
| `db/base.py` | 2 | 0 | **100%** |
| `db/models/card_model.py` | 9 | 0 | **100%** |
| `db/models/deck_model.py` | 9 | 0 | **100%** |
| `db/models/user_model.py` | 12 | 0 | **100%** |
| `db/session.py` | 10 | 4 | 60% |
| `repositories/card_repository.py` | 9 | 0 | **100%** |
| `repositories/deck_repository.py` | 28 | 0 | **100%** |
| `repositories/pokemon_repository.py` | 17 | 0 | **100%** |
| `repositories/ranking_repository.py` | 8 | 0 | **100%** |
| `repositories/user_repository.py` | 47 | 7 | 85% |
| `security/auth_dependencies.py` | 6 | 0 | **100%** |
| `security/jwt_handler.py` | 16 | 0 | **100%** |
| `security/password.py` | 7 | 0 | **100%** |

#### `app/interfaces/api/`

| Arquivo | Statements | Não cobertos | Cobertura |
|---|---|---|---|
| `dependencies.py` | 9 | 0 | **100%** |
| `exception_handlers.py` | 15 | 0 | **100%** |
| `router.py` | 9 | 0 | **100%** |
| `routes/auth_routes.py` | 16 | 0 | **100%** |
| `routes/battle_routes.py` | 39 | 1 | 97% |
| `routes/card_routes.py` | 10 | 0 | **100%** |
| `routes/deck_routes.py` | 10 | 0 | **100%** |
| `routes/ranking_routes.py` | 9 | 0 | **100%** |
| `routes/user_routes.py` | 19 | 0 | **100%** |

#### `app/schemas/` e demais

| Arquivo | Statements | Não cobertos | Cobertura |
|---|---|---|---|
| `schemas/auth_schema.py` | 13 | 0 | **100%** |
| `schemas/battle_schema.py` | 21 | 0 | **100%** |
| `schemas/deck_schema.py` | 8 | 0 | **100%** |
| `schemas/pokemon_schema.py` | 6 | 0 | **100%** |
| `schemas/ranking_schema.py` | 7 | 0 | **100%** |
| `shared/exceptions/domain_exception.py` | 4 | 0 | **100%** |
| `shared/exceptions/not_found_exception.py` | 4 | 0 | **100%** |
| `shared/exceptions/unauthorized_exception.py` | 4 | 0 | **100%** |
| `main.py` | 12 | 1 | 92% |

---

**Total: 718 statements · 20 não cobertos · 97% de cobertura**

Os únicos arquivos abaixo de 90% são `db/session.py` (60%) e `user_repository.py` (85%), ambos relacionados a código de inicialização de conexão com banco e cenários de erro que exigiriam falhas de banco para serem ativados nos testes — sem impacto na cobertura total, que permanece em 97%.

---

## 13. Containerização

### Imagem de Produção (`docker/Dockerfile`)

```dockerfile
FROM python:3.12-slim
```

**Análise do Dockerfile:**

| Instrução | Finalidade |
|---|---|
| `FROM python:3.12-slim` | Imagem base minimalista baseada em Debian Slim, reduzindo o tamanho final |
| `PYTHONDONTWRITEBYTECODE=1` | Evita geração de arquivos `.pyc`, economizando espaço |
| `PYTHONUNBUFFERED=1` | Garante que logs apareçam em tempo real (essencial para Docker) |
| `WORKDIR /app` | Define o diretório de trabalho dentro do container |
| `apt-get install build-essential libpq-dev curl` | Dependências do sistema: compilador C (para extensões Python), driver PostgreSQL nativo e cliente HTTP |
| `pip install poetry` | Instalação do gerenciador de pacotes |
| `POETRY_VIRTUALENVS_CREATE=false` | Instala dependências diretamente no Python do container (sem virtualenv isolado) |
| `COPY pyproject.toml poetry.lock` | Copia apenas os arquivos de dependências primeiro (cache de layers) |
| `poetry install --no-interaction --no-ansi` | Instala todas as dependências de forma não-interativa |
| `COPY . .` | Copia o código-fonte após instalar dependências (otimização de cache) |
| `EXPOSE 8000` | Documenta a porta utilizada pela aplicação |
| `CMD ["uvicorn", ...]` | Comando de inicialização do servidor ASGI |

**Estratégia de otimização de layers:** as dependências são instaladas antes de copiar o código-fonte. Isso garante que a layer de dependências seja reutilizada do cache enquanto o código não mudar — acelerando significativamente rebuilds durante desenvolvimento.

---

### Imagem Jenkins Customizada (`docker/jenkins/Dockerfile.jenkins`)

A imagem Jenkins estende a imagem oficial `jenkins/jenkins:lts` com:

| Adição | Finalidade |
|---|---|
| Docker CLI | Permite que o Jenkins construa e publique imagens Docker |
| Python 3 + pip + venv | Ambiente Python para execução da pipeline |
| SonarQube Scanner (v5.0.1) | Scanner para análise de código e envio para SonarQube |
| Trivy | Varredura de vulnerabilidades em imagens Docker |
| Plugins Jenkins | git, pipeline, docker-workflow, sonar, junit, htmlpublisher, email-ext, etc. |

**Integração Docker-in-Docker:** o volume `/var/run/docker.sock` é montado no container Jenkins, permitindo que ele controle o daemon Docker do host — padrão conhecido como DinD (Docker-in-Docker via socket).

---

## 14. Docker Hub

### Imagem Publicada


| Campo | Valor |
|---|---|
| **URL** | `https://hub.docker.com/r/bagrielzin/jokenpoke-jenkins` |

---

### Estratégia de Versionamento de Imagens

O pipeline publica a imagem Jenkins com **duas tags por build**:

| Tag | Formato | Exemplo | Uso |
|---|---|---|---|
| `latest` | Fixo | `jokenpoke-jenkins:latest` | Sempre aponta para o build mais recente |
| Número do build | `{BUILD_NUMBER}` | `jokenpoke-jenkins:42` | Imutável — permite rollback para build específico |

---

### Como Consumir a Imagem

```bash
# Puxar a imagem mais recente
docker pull bagrielzin/jokenpoke-jenkins:latest

# Executar a API diretamente da imagem publicada
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./app.db \
  -e JWT_SECRET_KEY=minha-chave-secreta \
  bagrielzin/jokenpoke-backend:latest

# No docker-compose.yml, a imagem Jenkins é consumida automaticamente:
# image: ${DOCKER_HUB_USER}/jokenpoke-jenkins:latest
```

---

## 15. Docker Compose

### Serviços

| Serviço | Imagem | Porta | Descrição |
|---|---|---|---|
| `api` | Build local (`docker/Dockerfile`) | `8000:8000` | API REST principal |
| `jenkins` | `bagrielzin/jokenpoke-jenkins:latest` | `8080:8080`, `50000:50000` | Servidor CI/CD |
| `sonarqube` | `sonarqube:community` | `9000:9000` | Análise estática de código |
| `ngrok` | `ngrok/ngrok:latest` | `4040:4040` | Tunnel para webhooks do GitHub → Jenkins |

---

### Diagrama da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                   Rede: jokenpoke-net (bridge)                  │
│                                                                 │
│  ┌──────────────┐    webhook    ┌──────────────┐                │
│  │    GitHub    │ ────────────▶ │    ngrok     │                │
│  │  (externo)   │               │    :4040     │                │
│  └──────────────┘               └──────┬───────┘                │
│                                        │ tunnel                 │
│  ┌──────────────┐    análise    ┌──────▼───────┐                │
│  │  SonarQube   │ ◀──────────── │    Jenkins   │                │
│  │  :9000       │               │    :8080     │                │
│  └──────────────┘               └──────┬───────┘                │
│                                        │ docker.sock            │
│  ┌──────────────┐                      │                        │
│  │     API      │               ┌──────▼───────┐                │
│  │  :8000       │               │  Docker Host │                │
│  │  (FastAPI)   │               │  (daemon)    │                │
│  └──────────────┘               └──────────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Volumes persistentes:
  jenkins_data         → /var/jenkins_home
  sonarqube_data       → /opt/sonarqube/data
  sonarqube_logs       → /opt/sonarqube/logs
  sonarqube_extensions → /opt/sonarqube/extensions
```

---

### Comunicação Entre Containers

| Origem | Destino | Protocolo | Porta interna |
|---|---|---|---|
| Jenkins | SonarQube | HTTP | 9000 |
| Jenkins | API (smoke test) | HTTP | 8000 |
| ngrok | Jenkins | HTTP | 8080 |
| GitHub Webhook | ngrok | HTTPS | 443 (externo) |

**Redes:** todos os serviços compartilham a rede `jokenpoke-net` do tipo `bridge`, permitindo comunicação via nome do serviço (ex: `http://sonarqube:9000`).

---

### Volumes

| Volume | Dados armazenados | Persistência |
|---|---|---|
| `jenkins_data` | Jobs, configurações, histórico de builds do Jenkins | Entre reinicializações |
| `sonarqube_data` | Projetos, métricas e análises do SonarQube | Entre reinicializações |
| `sonarqube_logs` | Logs do servidor SonarQube | Entre reinicializações |
| `sonarqube_extensions` | Plugins adicionais do SonarQube | Entre reinicializações |

---

## 16. Pipeline CI/CD

### Visão Geral

A pipeline é definida de forma declarativa no `Jenkinsfile` e executa em um agente Docker baseado na imagem customizada `jokenpoke-jenkins:latest`. Possui **10 estágios principais** e é acionada por push ao GitHub e por execução diária às 18h.

---

### Diagrama da Pipeline

```mermaid
flowchart TD
    A[🚀 Trigger\nGitHub Push / Cron 18h] --> B

    B[1️⃣ Build\nConfigura venv\nInstala dependências via Poetry] --> C

    C[2️⃣ Lint\nRuff check\nRuff format --check] --> D

    D[3️⃣ Unit Tests\nPytest - tests/\nJUnit XML\nCobertura XML+HTML\nFalha se < 90%] --> E

    E[4️⃣ Integration Tests\nPytest - tests/integration/\nCobertura acumulada] --> F

    F[5️⃣ SonarQube Analysis\nsonar-scanner\nEnvia métricas e cobertura] --> G

    G[6️⃣ Quality Gate\nAguarda resultado SonarQube\nAbort se reprovado] --> H

    H[7️⃣ Package\nEmpacota código em .tar.gz\nArtefato do build] --> I

    I[8️⃣ Docker Build & Push\nConstrói imagem Jenkins\nPublica no Docker Hub\ntags: latest + BUILD_NUMBER] --> J

    J[9️⃣ Security Scan\npip-audit - CVEs Python\ndetect-secrets - credenciais\nBandit - SAST\nTrivy - imagem Docker] --> K

    K[🔟 Smoke Test\nGET /health → 200\nPOST /auth/login → token\nGET /pokemons/ → 200] --> L

    L{Resultado}

    L -->|SUCCESS| M[✅ Post Success\nAtualiza status GitHub\nci/jenkins: success\nNotifica por e-mail]

    L -->|FAILURE| N[❌ Post Failure\nAtualiza status GitHub\nci/jenkins: failure\nNotifica por e-mail]

    L -->|UNSTABLE| O[⚠️ Post Unstable\nAtualiza status GitHub\nci/jenkins: failure\nNotifica por e-mail]

    M --> P[🧹 Always\nLimpa arquivos temporários\nExecuta notify.py]
    N --> P
    O --> P
```

---

### Detalhamento dos Estágios

#### Estágio 1 — Build

Configura o ambiente Python dentro do container de agente:
1. Cria virtualenv isolado (`.venv`)
2. Atualiza pip para a versão mais recente
3. Instala o Poetry
4. Configura Poetry para criar o virtualenv no projeto
5. Instala todas as dependências do `pyproject.toml`

#### Estágio 2 — Lint

Executa as verificações de qualidade de código com Ruff:
- `ruff check .` — verifica erros de lint (E, F, I, B, UP, SIM, C4, S)
- `ruff format --check .` — verifica se o código está formatado corretamente

**O estágio falha se houver qualquer violação de lint.**

#### Estágio 3 — Unit Tests

Executa a suíte completa de testes com coleta de cobertura:
- Saída JUnit XML: `reports/test-results.xml`
- Cobertura XML: `reports/coverage.xml` (para SonarQube)
- Cobertura HTML: `reports/coverage-html/` (publicado via htmlpublisher)
- **Falha automaticamente se cobertura < 90%**

**Artefatos publicados:** `test-results.xml`, `coverage.xml`, `coverage-html/**`

#### Estágio 4 — Integration Tests

Executa especificamente os testes de integração com acumulação de cobertura (`--cov-append`):
- Banco SQLite isolado via `dependency_overrides`
- Resultado em `reports/integration-results.xml`

#### Estágio 5 — SonarQube Analysis

Executa o `sonar-scanner` no contexto do servidor SonarQube via `withSonarQubeEnv`. Envia:
- Código-fonte (`app/`)
- Relatório de cobertura XML (`reports/coverage.xml`)
- Resultados de testes JUnit (`reports/test-results.xml`)

#### Estágio 6 — Quality Gate

Aguarda o resultado do Quality Gate do SonarQube (timeout de 5 minutos). **Se o quality gate reprovar, a pipeline é abortada** (`abortPipeline: true`).

#### Estágio 7 — Package

Empacota o código-fonte em um arquivo `.tar.gz` com número do build, excluindo artefatos de desenvolvimento (`.venv`, `dist`, `reports`, `.git`). Publicado como artefato do Jenkins.

#### Estágio 8 — Docker Build & Push (Imagem Jenkins)

Constrói a imagem Docker customizada do Jenkins com labels de rastreabilidade (`build.number`, `build.branch`, `build.commit`), publica no Docker Hub com duas tags (`latest` e `{BUILD_NUMBER}`) e limpa as imagens locais após o push.

#### Estágio 9 — Security Scan

Varredura completa de segurança:
- **pip-audit:** CVEs conhecidas em dependências Python
- **detect-secrets:** secrets e credenciais expostas no código (comparado com baseline)
- **Bandit:** análise estática de segurança (SAST) — severity médio ou superior
- **Trivy:** varredura da imagem Docker por vulnerabilidades HIGH e CRITICAL

#### Estágio 10 — Smoke Test

Verifica o ambiente de produção no Railway com três checks críticos:
1. Health check do servidor
2. Fluxo de autenticação (obtenção de token JWT)
3. Disponibilidade de rota pública

---

### Notificações e Integrações

**GitHub Status Checks:** a pipeline atualiza o status do commit no GitHub via API (`/repos/{owner}/{repo}/statuses/{sha}`), exibindo `ci/jenkins: success/failure` diretamente na branch de deploy do projeto (`main`).

**E-mail:** o script `scripts/notify.py` é executado ao final de cada build (sucesso ou falha), enviando notificação por e-mail via SMTP configurado nas credenciais do Jenkins.

**Opções da pipeline:**
- Timeout global: 30 minutos
- Histórico de builds: últimos 10 retidos
- Builds concorrentes desabilitados

---

## 17. Infraestrutura como Código

O projeto aplica o princípio de **Infrastructure as Code (IaC)** em múltiplas camadas:

### Dockerfile (`docker/Dockerfile`)

Define de forma declarativa e reproduzível o ambiente de execução da API. Qualquer desenvolvedor ou servidor CI pode construir o ambiente exato com `docker build`.

**Princípio DevOps aplicado:** *Build Once, Run Anywhere* — a imagem gerada é idêntica em desenvolvimento, CI e produção.

---

### Dockerfile.jenkins (`docker/jenkins/Dockerfile.jenkins`)

Define o ambiente do agente CI/CD, incluindo todas as ferramentas necessárias (Python, Docker CLI, SonarScanner, Trivy, plugins Jenkins). Elimina a necessidade de configuração manual do servidor Jenkins.

**Princípio DevOps aplicado:** *Immutable Infrastructure* — o servidor CI é reconstruído a partir da imagem versionada, não configurado manualmente.

---

### Docker Compose (`docker-compose.yml`)

Define e configura todo o stack de desenvolvimento local: API, Jenkins, SonarQube e ngrok. Um único comando (`make up`) provisiona o ambiente completo.

**Princípio DevOps aplicado:** *Dev/Prod Parity* — o ambiente local espelha o ambiente de CI, reduzindo o clássico problema "funciona na minha máquina".

---

### Jenkinsfile

Define a pipeline CI/CD como código versionado no repositório. Qualquer alteração na pipeline passa pelo mesmo processo de revisão que o código da aplicação.

**Princípio DevOps aplicado:** *Pipeline as Code* — a pipeline é um artefato de primeira classe do projeto, versionado, revisado e rastreável.

---

### Makefile

Abstrai comandos complexos em alvos simples e auto-documentados. Padroniza a interface de desenvolvimento para toda a equipe.

**Princípio DevOps aplicado:** *Automation First* — todas as tarefas repetitivas (test, lint, build, deploy) são automatizadas e acessíveis via `make <target>`.

---

### Alembic Migrations

O schema do banco de dados é versionado como código. Cada migration é um artefato auditável e reversível.

**Princípio DevOps aplicado:** *Database as Code* — mudanças no banco seguem o mesmo fluxo de revisão do código da aplicação.

---

### sonar-project.properties

Configuração do SonarQube Scanner como arquivo versionado no repositório, garantindo consistência na análise entre execuções locais e no CI.

---

## 18. Uso de Inteligência Artificial

### Ferramentas Utilizadas

| Ferramenta | Finalidade principal no projeto |
|---|---|
| **Claude** | Geração de documentação técnica, revisão/refinamento de código, debug de problemas complexos |
| **ChatGPT** | Pesquisa de padrões, revisão de arquitetura, debug de problemas complexos |
| **Gemini** | Pesquisas referentes a documentação de bibliotecas/ferramentas e instalações no projeto |
| **GitHub Copilot** | Autocompletar código, sugestões inline |

> Todas essas ferramentas foram usadas para tarefas de rotina pelos membros do grupo de acordo com as preferências de cada um.

---

### Casos de Uso

| Área | Atividade | Ferramenta |
|---|---|---|
| **Desenvolvimento** | Geração de schemas Pydantic, modelos ORM, rotas FastAPI | Copilot |
| **Refatoração** | Migração de `Depends()` legado para `Annotated` | Copilot + ChatGPT |
| **Debug** | Diagnóstico de erros de FK e cascade no SQLAlchemy | ChatGPT |
| **Testes** | Geração de fixtures e casos de teste unitários | Copilot |
| **DevOps** | Estrutura do Jenkinsfile, configuração do Docker Compose | ChatGPT |
| **Documentação** | Geração desta documentação técnica completa | Claude |
| **Segurança** | Revisão de configurações JWT e bcrypt | ChatGPT |
| **Arquitetura** | Validação das decisões de Clean Architecture | ChatGPT + Claude |

---

### Dinâmica de Utilização

A equipe adotou IA como ferramenta de **amplificação**, não de substituição. O fluxo padrão foi:
1. Desenvolvedor define o problema ou requisito
2. IA gera proposta inicial de código ou solução
3. Desenvolvedor revisa criticamente, adapta ao contexto do projeto
4. Código revisado passa pelo processo normal de PR e review
5. Decisão de aceitar, adaptar ou rejeitar é sempre humana

**Política:** código gerado por IA é sempre revisado por pelo menos um membro da equipe antes de ser mergeado.

---

### Registro de Prompts

| # | Prompt | Aceito? | Motivo |
|---|---|---|---|
| 01 | "Gere um Dockerfile para uma API FastAPI com Python 3.12 e Poetry, otimizado para produção com python:slim" | ✅ Sim | Estrutura correta e boas práticas de otimização de layers |
| 02 | "Crie um modelo SQLAlchemy para a entidade User com campos: id, username, password_hash, rank, points, created_at" | ✅ Adaptado | Estrutura correta, mas nomes de campos ajustados para o padrão do projeto |
| 03 | "Como configurar cascade delete no SQLAlchemy com Alembic para garantir que a FK também tenha ondelete no DDL?" | ✅ Sim | Solução precisa que resolveu o bug do US-005 |
| 04 | "Refatore esta rota FastAPI para usar o padrão moderno Annotated ao invés de Depends() direto nos parâmetros" | ✅ Sim | Corretamente aplicado, resolveu os alertas do SonarLint (US-004) |
| 05 | "Gere testes unitários para a função resolve_move em battle_rules.py cobrindo todos os casos de MOVE_WEAKNESS" | ✅ Adaptado | Boa cobertura inicial, mas alguns edge cases foram adicionados manualmente |
| 06 | "Crie um Jenkinsfile declarativo com estágios: build, lint, unit tests, integration tests, sonarqube, quality gate, docker build, security scan, smoke test" | ✅ Adaptado | Estrutura base correta; configurações específicas (credenciais, URLs) foram personalizadas |
| 07 | "Crie fixtures pytest reutilizáveis para testes de integração FastAPI usando SQLite e dependency_overrides" | ✅ Sim | Padrão adotado integralmente no conftest.py de integração |
| 08 | "Como configurar o SonarQube Scanner para um projeto Python com pytest-cov, enviando relatório XML de cobertura?" | ✅ Sim | Configuração aplicada no sonar-project.properties |
| 09 | "Gere exemplos de critérios de aceitação em Gherkin para uma funcionalidade de login com JWT" | ✅ Adaptado | Estrutura base boa, cenários ajustados para a realidade do projeto |
| 10 | "Escreva documentação técnica completa em Markdown para este projeto de API FastAPI com Clean Architecture e pipeline Jenkins" | ✅ Sim | Este documento foi gerado com base neste prompt + análise dos arquivos do projeto |

> **Nota sobre a fidelidade dos prompts:** os prompts acima são representações resumidas das interações reais com as ferramentas de IA. Os prompts originais eram consideravelmente mais ricos — incluíam arquivos anexados (código-fonte, exemplos de implementações já validadas no projeto, trechos de configuração), exemplos do padrão já adotado pela equipe e contexto acumulado de conversas anteriores. Parte do histórico de conversas foi perdida por deleção manual ao longo do desenvolvimento, impossibilitando a recuperação dos prompts exatos. O que está registrado aqui reflete a **intenção** de cada interação, não sua forma literal.

---

### O que NÃO foi feito por IA

As seguintes atividades foram realizadas **exclusivamente pela equipe**, sem assistência de IA:

- **Escolha da Stack tecnológica:** a grande maioria das decisões relacionadas a stack tecnológica foram decididas antes do início do desenvolvimento do projeto, com exceção de alguns ajustes motivados por incompatibilidades técnicas
- **Decisões de arquitetura:** a escolha de Clean Architecture, a separação em camadas (domain, application, infrastructure, interfaces) e as fronteiras entre elas foram definidas pelos desenvolvedores
- **Modelagem do domínio:** as entidades `Battle`, `Card`, `Deck`, `Pokemon`, `Ranking`, `User` e suas relações foram modeladas pela equipe
- **Regras de negócio do jogo:** a lógica de `MOVE_WEAKNESS`, `element_advantage`, critérios de vitória por round e progressão de ranking são de autoria da equipe
- **Definição das histórias de usuário:** os critérios de aceitação, a priorização e o DoD/DoR foram elaborados pelos membros do projeto
- **Padronização técnica do projeto:** os modelos de PR, implementação de branches e convenção de commits foram decididos pelos membros do projeto
- **Processo de code review:** todas as revisões de PRs foram realizadas por membros da equipe
- **Identificação e diagnóstico de bugs:** a descoberta do bug de cascade (US-005) e o debugging do comportamento do TestClient (US-004) partiram de observação humana
- **Estrutura de migrations:** a sequência de migrations do Alembic e suas dependências foram planejadas e escritas pela equipe
- **Configuração do ambiente Railway:** o deploy em produção e as variáveis de ambiente foram configurados manualmente
- **Decisões técnicas:** todas as decisões técnicas tomadas no projeto (mesmo as sugeridas por assistêntes de IA) foram decididas por pelo menos um membro do projeto

---

## 19. Conclusão

### Resultados Alcançados

O projeto JokenPoke entregou, ao longo de seu desenvolvimento, uma API REST completa e production-ready para um sistema de batalha de cartas colecionáveis, demonstrando maturidade técnica tanto em Engenharia de Software quanto em práticas DevOps:

**Engenharia de Software:**
- Clean Architecture implementada com separação clara de camadas
- 5 histórias de usuário entregues com critérios de aceitação verificáveis
- Cobertura de testes ≥ 90% como gate de qualidade automatizado
- Rastreabilidade completa: US → PR → testes → código

**DevOps:**
- Pipeline CI/CD de 10 estágios com Jenkins containerizado
- Análise de qualidade com SonarQube e quality gate
- Segurança integrada ao pipeline (pip-audit, Bandit, detect-secrets, Trivy)
- Infraestrutura 100% como código (Dockerfile, Compose, Jenkinsfile, Makefile)
- Deploy automatizado com smoke tests em produção (Railway)

---

### Benefícios do Projeto

- **Reproduzibilidade:** qualquer desenvolvedor pode replicar o ambiente completo com `make up`
- **Confiabilidade:** a pipeline bloqueia automaticamente código abaixo do limiar de qualidade
- **Rastreabilidade:** cada feature é rastreável de US → PR → commit → teste → deploy
- **Segurança:** múltiplas camadas de varredura de segurança integradas ao pipeline
- **Escalabilidade:** a arquitetura limpa facilita a adição de novas funcionalidades sem degradação

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

## Equipe

Projeto desenvolvido por alunos do curso de Engenharia de Software do **INATEL — Instituto Nacional de Telecomunicações**, para as disciplinas de **Engenharia de Software** e **DevOps**.

| Membro | GitHub |
|---|---|
| Christian Salles | [Christiansalles](https://github.com/Christiansalles) |
| Eduardo Pereira | [odraude222k](https://github.com/odraude222k) |
| Gabriel Soares | [Bagrielzin](https://github.com/Bagrielzin) |
| Maria Clara Ignácio | [mariaclaraig](https://github.com/mariaclaraig) |
| Matheus Netto | [MatheusNetto1](https://github.com/MatheusNetto1) |
| Rafael Areias | [RafaelAreias](https://github.com/RafaelAreias) |

> Repositório: [C14-INATEL/jokenpoke-backend](https://github.com/C14-INATEL/jokenpoke-backend)  
> Notion: [JokenPoke Agile HQ](https://app.notion.com/p/JokenPoke-Agile-HQ-843e3031246e4294915365850becba51)

---