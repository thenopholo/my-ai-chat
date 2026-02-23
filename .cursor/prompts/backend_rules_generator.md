Atue como um "Project Rule Builder" para o backend deste repositório Python 3.13 + FastAPI + LangChain/LangGraph.

Objetivo: criar/atualizar um conjunto de Project Rules (.mdc) em pt-BR dentro de `.cursor/rules/`, baseadas:

1) no estado REAL do projeto (pastas, dependências, padrões já usados)

2) nas convenções oficiais e boas práticas do ecossistema Python:

   A) Oficiais Python:
   - Python Docs: https://docs.python.org/3/
   - PEP 8 (Style Guide): https://peps.python.org/pep-0008/
   - PEP 20 (Zen of Python): https://peps.python.org/pep-0020/
   - PEP 257 (Docstrings): https://peps.python.org/pep-0257/

   B) Boas práticas e guias:
   - The Hitchhiker's Guide to Python: https://docs.python-guide.org/
   - Real Python: https://realpython.com/
   - Google Python Style Guide: https://google.github.io/styleguide/pyguide.html

   C) Arquitetura e organização:
   - Cosmic Python (Architecture Patterns): https://www.cosmicpython.com/
   - FastAPI Best Practices: https://github.com/zhanymkanov/fastapi-best-practices
   - Cookiecutter: https://cookiecutter.readthedocs.io/
   - Cookiecutter Django: https://github.com/cookiecutter/cookiecutter-django

   E) FastAPI:
   - Docs oficiais: https://fastapi.tiangolo.com/
   - Best Practices: https://github.com/zhanymkanov/fastapi-best-practices
   - Full-Stack Template: https://github.com/tiangolo/full-stack-fastapi-template

   F) LangChain e LangGraph:
   - LangChain Docs: https://python.langchain.com/docs/
   - LangGraph Docs: https://langchain-ai.github.io/langgraph/
   - LangChain Repo: https://github.com/langchain-ai/langchain
   - LangGraph Repo: https://github.com/langchain-ai/langgraph
   - LangChain Templates: https://github.com/langchain-ai/langchain/tree/master/templates

   G) Repositórios de referência:
   - https://github.com/tiangolo/full-stack-fastapi-template
   - https://github.com/HackSoftware/Django-Styleguide-Example
   - https://github.com/encode/django-rest-framework
   - https://github.com/cosmicpython/code
   - https://github.com/langchain-ai/langgraph/tree/main/examples
   - https://github.com/donnemartin/system-design-primer

   H) Ferramentas modernas:
   - Ruff (linter + formatter): https://docs.astral.sh/ruff/
   - mypy (type checker): https://mypy.readthedocs.io/
   - pytest: https://docs.pytest.org/
   - uv (package manager): https://docs.astral.sh/uv/

   - Se não conseguir acessar os links, derive as regras a partir do `pyproject.toml`, `pyrightconfig.json`, `uv.lock` e do código existente.


## DEVE/NÃO DEVE

- Caso tenha alguma dúvida ou algo que não esteja claro, **VOCÊ DEVE** perguntar ao usuário para esclarecer antes de continuar.
- Caso tenha alguma dúvida ou algo que não esteja claro, **VOCÊ NÃO DEVE** continuar sem esclarecer.


## Contexto do projeto

Este é o backend de um **chat com IA** (AI Chat). Stack atual:
- **Python 3.13** com **uv** como gerenciador de pacotes/ambientes
- **FastAPI 0.110** + **Uvicorn 0.27** como framework web e servidor ASGI
- **Pydantic 2.11** para validação e serialização de dados
- **OpenAI SDK 1.66** para comunicação com LLMs (via Thesys API)
- **python-dotenv** para variáveis de ambiente
- **crayonai-stream** e **thesys-genui-sdk** para streaming e integração com GenUI
- **Pyright** configurado via `pyrightconfig.json` (type checker)
- Estrutura atual: flat (`main.py`, `llm_runner.py`, `thread_store.py`)
- **Planos futuros**: migração para **LangChain** e **LangGraph** para orquestração de agentes/chains de IA


### Entrada opcional

- É possível fornecer um arquivo complementar com informações/contexto para orientar a geração das rules.
- Formatos aceitos: `.md`, `.mdc`, `.txt`, `.json`, `.yaml`.
- Tratamento:
  - Leia o arquivo integralmente e extraia diretrizes úteis (decisões arquiteturais, exceções locais, convenções do time, restrições de segurança, etc.).
  - Em caso de conflito entre o arquivo auxiliar e o estado real do repositório, priorize o repositório e registre a divergência nos TODOs do resumo final.
  - Não copie o conteúdo na íntegra; incorpore como regras objetivas alinhadas ao código e às lints.
  - No resumo final, indique o nome do arquivo usado como "Fonte auxiliar".


### O que analisar no repo

- `backend/pyproject.toml` (dependências → detectar frameworks web, ORMs, libs de IA, ferramentas de dev).
- `backend/uv.lock` (lockfile do uv → versões exatas).
- `pyrightconfig.json` (type checking: paths, venv, regras de report).
- Presença/ausência de:
  - `ruff.toml` / `[tool.ruff]` no `pyproject.toml` (linter/formatter).
  - `mypy.ini` / `[tool.mypy]` no `pyproject.toml` (type checker alternativo).
  - `pytest.ini` / `[tool.pytest]` no `pyproject.toml` / `conftest.py` (testes).
  - `.env` / `.env.example` (variáveis de ambiente).
  - `Makefile`, `Taskfile.yml`, `justfile` (automação).
- Estrutura de diretórios do backend:
  - Atual: flat (`backend/*.py`)
  - Recomendada: modular (`backend/app/`, `backend/app/api/`, `backend/app/core/`, `backend/app/models/`, `backend/app/services/`, `backend/app/agents/`, `backend/tests/`)
- Uso de LangChain/LangGraph: chains, agents, graphs, tools, prompts, memory.
- Presença de `Dockerfile`, `docker-compose.yml` (containers).
- Arquivo auxiliar (opcional), quando fornecido (ver "Entrada opcional").


### Saída esperada (arquivos e conteúdo)

Crie/atualize **exatamente** estes arquivos, com front-matter e conteúdo conciso em bullets:


1) `.cursor/rules/backend-python-standards.mdc` (Always)

- `description`: Padrões de código Python do projeto backend.
- Regras: PEP 8 (estilo), PEP 20 (Zen), PEP 257 (docstrings); Ruff como linter/formatter (se configurado, senão recomendar); naming conventions (`snake_case` para funções/variáveis, `PascalCase` para classes, `UPPER_SNAKE_CASE` para constantes); type hints em todas as funções (PEP 484/526); uso de `dataclasses`, `TypedDict`, `TypeAlias`; f-strings; async/await; comprehensions com moderação; imports organizados (stdlib → third-party → local); sem `print()` em prod (usar logging).
- Alinhe ao `pyrightconfig.json` e ao Google Python Style Guide.
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


2) `.cursor/rules/backend-project-structure.mdc` (Auto-attach)

- `globs`: `"backend/**"`.
- Estrutura atual (flat) e evolução recomendada para estrutura modular:
  - `backend/app/` → pacote principal
  - `backend/app/api/` → routers/endpoints FastAPI
  - `backend/app/core/` → configurações, settings, dependências
  - `backend/app/models/` → Pydantic models, schemas, DTOs
  - `backend/app/services/` → lógica de negócio
  - `backend/app/agents/` → chains, graphs, tools LangChain/LangGraph
  - `backend/app/prompts/` → templates de prompts para LLMs
  - `backend/tests/` → testes unitários e de integração
- Convenções de nomes de arquivos e módulos.
- Uso do uv para gerenciar dependências e ambientes virtuais.
- Seções: Objetivo, Estrutura de diretórios, Regras de imports, Anti-padrões, Checklist.


3) `.cursor/rules/backend-fastapi-patterns.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- Regras FastAPI: routers com prefixos claros; dependency injection com `Depends()`; Pydantic models para request/response; status codes explícitos; error handling com `HTTPException` e exception handlers; middleware (CORS, logging, auth); streaming responses (SSE para chat); async vs sync endpoints; settings com `pydantic-settings` ou `python-dotenv`; versionamento de API; documentação automática (OpenAPI/Swagger).
- Alinhe ao FastAPI Best Practices e Full-Stack Template.
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


4) `.cursor/rules/backend-clean-architecture.mdc` (Auto-attach)

- `globs`: `"backend/**"`.
- Camadas: API (routers/endpoints) → Services (lógica de negócio) → Repositories (acesso a dados); direções de dependência (Dependency Inversion Principle); interfaces/protocolos para abstração; DTOs vs domain entities; injeção de dependência via FastAPI `Depends()`.
- Referência ao Cosmic Python (Architecture Patterns with Python).
- Seções: Objetivo, Camadas e responsabilidades, Direções de dependência, Anti-padrões, Checklist.


5) `.cursor/rules/backend-langchain-langgraph.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- Regras para LangChain: uso correto de chains (LCEL - LangChain Expression Language), prompts (ChatPromptTemplate, SystemMessage, HumanMessage), modelos (ChatOpenAI, etc.), output parsers, retrievers, tools, memory/history.
- Regras para LangGraph: definição de grafos (StateGraph), nós (nodes), arestas (edges), estado tipado, conditional edges, checkpointing, subgraphs; padrões de agentes (ReAct, Plan-and-Execute, multi-agent).
- Organização: separar chains/graphs em módulos próprios (`agents/`); prompts em arquivos separados; configuração de modelos centralizada; callbacks para observabilidade.
- Referência aos docs oficiais e exemplos do repo LangGraph.
- Seções: Objetivo, Regras LangChain, Regras LangGraph, Patterns recomendados, Anti-padrões, Checklist.


6) `.cursor/rules/backend-error-handling.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- Regras: nunca silenciar exceções (`except: pass`); usar exceções tipadas e custom exceptions; logging estruturado com contexto; `try/except` granular (não blocos enormes); FastAPI exception handlers para respostas consistentes; retry com backoff para chamadas a LLMs/APIs externas; graceful degradation; erros de streaming (SSE).
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


7) `.cursor/rules/backend-async-patterns.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- Regras: async/await consistente (não misturar sync/async sem motivo); `asyncio` para concorrência; uso de `httpx` ou `aiohttp` para HTTP async; streaming com `StreamingResponse` e `async generators`; task groups para paralelismo; timeouts em chamadas externas; context propagation; event loop awareness.
- Seções: Objetivo, Regras, Patterns recomendados, Anti-padrões, Checklist.


8) `.cursor/rules/backend-pydantic-models.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- Regras Pydantic v2: `BaseModel` para schemas de request/response; `model_validator` e `field_validator` para validação; `TypedDict` para estruturas internas leves; `Config` com `extra = "forbid"` ou `"allow"` consciente; serialização (`model_dump()`, `model_dump_json()`); Field com `description` para OpenAPI; separation of concerns (input models, output models, domain models).
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


9) `.cursor/rules/backend-testing.mdc` (Auto-attach)

- `globs`: `"backend/tests/**","backend/**/*_test.py","backend/**/test_*.py"`.
- Framework: pytest (recomendar se ausente); tipos: unit, integration, e2e; uso de `httpx.AsyncClient` para testar endpoints FastAPI; fixtures e conftest; mocking de LLMs e APIs externas (langchain `FakeLLM`, `unittest.mock`); testes de chains/graphs LangChain/LangGraph; cobertura (`pytest-cov`); marcadores (`@pytest.mark`).
- Estrutura: `backend/tests/` espelhando `backend/app/`.
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


10) `.cursor/rules/backend-dependency-management.mdc` (Auto-attach)

- `globs`: `"backend/pyproject.toml","backend/uv.lock"`.
- Regras: usar **uv** como gerenciador (`uv add`, `uv remove`, `uv sync`, `uv run`); `pyproject.toml` como fonte única de dependências; lockfile (`uv.lock`) commitado no repo; separação de deps de prod vs dev (`[project.optional-dependencies]` ou `[tool.uv.dev-dependencies]`); pinagem de versões; ambiente virtual local (`.venv`); scripts no `pyproject.toml` ou `Makefile`.
- Seções: Objetivo, Regras, Comandos úteis, Checklist.


11) `.cursor/rules/backend-security.mdc` (Always)

- `description`: Regras de segurança para o backend Python.
- Regras: variáveis de ambiente via `.env` (nunca hardcoded); `.env` no `.gitignore`; validação de input com Pydantic; CORS configurado (origins explícitas); rate limiting; sem logs de dados sensíveis (API keys, tokens, PII); secrets management; headers de segurança; proteção contra injection (SQL, prompt injection para LLMs).
- Seções: Objetivo, Regras, Anti-padrões, Checklist.


12) `.cursor/rules/commits-and-language.mdc` (Always)

- Commits semânticos em **pt-BR** (feat/fix/chore/docs/refactor/test): título curto + corpo explicando o quê/por quê; referência a issues/PRs; padrão para PRs (título/descrição/labels).
- Seções: Objetivo, Padrões, Exemplos curtos, Checklist.


### Opcionais (criar somente se o repo indicar necessidade)

- `.cursor/rules/backend-database.mdc` (Auto-attach se detectar SQLAlchemy, SQLModel, Tortoise, Prisma, etc.).
- `.cursor/rules/backend-observability.mdc` (Auto-attach se detectar OpenTelemetry, Prometheus, structlog, loguru).
- `.cursor/rules/backend-docker.mdc` (Auto-attach se houver `Dockerfile`, `docker-compose.yml`).
- `.cursor/rules/backend-ci-cd.mdc` (Auto-attach se houver `.github/workflows/`, `.gitlab-ci.yml`, etc.).
- `.cursor/rules/backend-llm-prompt-engineering.mdc` (Auto-attach se houver templates de prompts ou diretório `prompts/` com system/user messages para LLMs).


### Requisitos de formatação

- Idioma: pt-BR, direto e assertivo.
- Cada arquivo começa com front-matter YAML: `description`, e **ou** `alwaysApply: true` **ou** `globs: [...]` (para Auto-attach).
- Texto em bullets, seções curtas: Objetivo, Regras, Anti-padrões, Checklist (e "Exemplos curtos" quando útil).
- Não copiar documentação inteira; **alinhe e referencie** (ex.: "seguir PEP 8 para estilo", "seguir padrão LCEL do LangChain").
- Limite: regras objetivas (evitar longos parágrafos).


### Passos finais

- Liste no final um "Resumo do que foi detectado" (framework web, ORM, libs de IA, DI, type checker, linter, gerenciador de pacotes, estrutura de pastas).
- Valide os `globs` com base na árvore real do repo e mostre-os no resumo.
- Se algo estiver ambíguo, proponha defaults sensatos e registre TODOs.
- Se um arquivo auxiliar foi utilizado, inclua no resumo: `Fonte auxiliar: <caminho/arquivo>` e destaque quaisquer decisões derivadas dele.
