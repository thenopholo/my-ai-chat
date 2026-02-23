### **Contexto**

Você é um desenvolvedor sênior Python, especialista em **LangChain**, **LangGraph** e **FastAPI**, trabalhando num projeto de chat com IA.

O projeto é um fork do **C1 Thesys** (https://docs.thesys.dev/guides/setup) que atualmente usa o **OpenAI SDK** diretamente para se comunicar com LLMs via Thesys API. A meta é migrar a camada de LLM para **LangChain** (`langchain-openai`) apontando diretamente para a **API da OpenAI**, mantendo o restante do projeto 100% funcional.

**Stack atual do backend:**
- Python 3.13 com **uv** como gerenciador de pacotes
- FastAPI 0.110 + Uvicorn 0.27
- Pydantic 2.11
- OpenAI SDK 1.66 (comunicação direta com `https://api.thesys.dev/v1/embed`)
- `thesys-genui-sdk` e `crayonai-stream` para streaming e integração GenUI
- `python-dotenv` para variáveis de ambiente
- Estrutura flat: `main.py`, `llm_runner.py`, `thread_store.py`

**Stack do frontend (não deve ser alterado):**
- React 19 + TypeScript + Vite
- `@thesysai/genui-sdk` (`C1Chat` component) — comunica via `POST /api/chat`
- Proxy Vite redireciona `/api` → `http://127.0.0.1:8000`

---

### **Objetivo**

Migrar o backend de **OpenAI SDK direto** para **LangChain** (`langchain-openai`), substituindo:

1. **Client OpenAI** (`openai.OpenAI`) → **`ChatOpenAI`** do `langchain-openai`.
2. **API Key**: `THESYS_API_KEY` → `OPENAI_API_KEY` (variável de ambiente no `.env`).
3. **Base URL**: remover `https://api.thesys.dev/v1/embed` — usar o endpoint padrão da OpenAI.
4. **Modelo**: substituir `c1/anthropic/claude-sonnet-4/v-20250815` por um modelo OpenAI válido (ex.: `gpt-4o-mini` ou `gpt-4o`, configurável via variável de ambiente `OPENAI_MODEL`).
5. **Streaming**: adaptar o loop de streaming para usar `.astream()` do LangChain, mantendo a integração com `write_content()` e `get_assistant_message()` do `thesys_genui_sdk`.
6. **Histórico**: converter o histórico de mensagens do formato `ChatCompletionMessageParam` (OpenAI SDK) para `BaseMessage` (LangChain: `HumanMessage`, `AIMessage`, `SystemMessage`).

O projeto deve continuar **100% funcional** após a migração — o frontend (`C1Chat`) não deve sofrer alterações.

---

### **Instruções específicas**

#### Arquivos a modificar

1. **`backend/llm_runner.py`** — arquivo principal da migração:
   - Remover import do `openai` SDK (`from openai import OpenAI`, tipos `ChatCompletion*`).
   - Adicionar imports do LangChain: `ChatOpenAI` de `langchain_openai`, `HumanMessage`/`AIMessage` de `langchain_core.messages`.
   - Substituir instanciação do client `OpenAI(api_key=..., base_url=...)` por `ChatOpenAI(api_key=..., model=..., streaming=True)`.
   - Na função `generate_stream()`:
     - Converter `conversation_history` de `list[ChatCompletionMessageParam]` para `list[BaseMessage]` do LangChain.
     - Substituir o loop `client.chat.completions.create(stream=True)` por `.astream()` do `ChatOpenAI`.
     - Manter `await write_content(chunk.content)` para cada chunk de streaming.
     - Manter `get_assistant_message()` para obter a mensagem final do assistente.
     - Armazenar a mensagem do assistente no `thread_store` convertendo de volta para o formato compatível.
   - Atualizar os `TypedDict` e models (`Prompt`, `ChatRequest`) conforme necessário.
   - Carregar variáveis de ambiente com **`python-dotenv`** (`load_dotenv()`) antes de acessar qualquer env var — este é o padrão do projeto para carregamento de `.env`.
   - Garantir que `OPENAI_API_KEY` é lida de `os.getenv('OPENAI_API_KEY')`.
   - Adicionar variável `OPENAI_MODEL` para configurar o modelo via `.env` (default: `gpt-4o-mini`).

2. **`backend/thread_store.py`** — adaptar tipos de mensagem:
   - Avaliar se `Message(TypedDict)` precisa mudar de `openai_message: ChatCompletionMessageParam` para `BaseMessage` do LangChain.
   - Se necessário, adaptar `get_messages()` para retornar `list[BaseMessage]`.
   - Manter backward compatibility para não quebrar contratos internos.

3. **`backend/main.py`** — verificar se precisa de ajustes:
   - O decorator `@with_c1_response()` e o endpoint `POST /chat` devem continuar funcionando.
   - Importações de `ChatRequest` e `generate_stream` de `llm_runner` devem continuar válidas.

4. **`backend/pyproject.toml`** — atualizar dependências:
   - Adicionar: `langchain-openai`, `langchain-core`, `langchain`.
   - Avaliar se `openai` SDK ainda é necessário como dependência transitiva (o `langchain-openai` já depende dele).
   - Manter: `thesys-genui-sdk`, `crayonai-stream`, `fastapi`, `pydantic`, `python-dotenv`.

5. **`backend/.env`** (ou `.env.example`) — atualizar variáveis:
   - Remover/substituir `THESYS_API_KEY` por `OPENAI_API_KEY`.
   - Adicionar `OPENAI_MODEL=gpt-4o-mini` (ou modelo desejado).
   - As variáveis são carregadas via `python-dotenv` (`load_dotenv()`) no início do módulo, conforme padrão já existente em `llm_runner.py`.

#### Frontend — validação (sem alterações esperadas)

- O frontend usa `<C1Chat apiUrl="/api/chat" />` — não referencia API keys nem modelos.
- O proxy Vite (`/api` → backend) é transparente.
- O contrato HTTP (`POST /chat` com body `ChatRequest`, resposta via SSE/streaming do `thesys_genui_sdk`) não muda.
- **Confirmar**: nenhum arquivo frontend precisa ser alterado.

#### Regras e padrões do projeto a seguir

- **Padrões Python**: PEP 8, PEP 257, type hints em todas as funções, single quotes, line-length 79 (Ruff).
- **Async**: usar `async def` e `await` para chamadas ao LLM; usar `.astream()` do LangChain (não o client sync).
- **Variáveis de ambiente**: usar **`python-dotenv`** com `load_dotenv()` para carregar o `.env` — é o padrão adotado no projeto. Nunca hardcodar API keys; `.env` no `.gitignore`.
- **Pydantic v2**: `model_config = ConfigDict(...)` em vez de `class Config:`.
- **LangChain patterns**: usar LCEL quando aplicável; `ChatOpenAI` com parâmetros explícitos; configuração centralizada de modelos; timeouts configurados.
- **Gerenciamento de deps**: usar `uv add` para adicionar pacotes; commitar `uv.lock`.
- **Nomenclatura**: `snake_case` para funções/variáveis, `PascalCase` para classes, `UPPER_SNAKE_CASE` para constantes.

---

### **Formato da resposta**

1. **Plano técnico**: antes de codar, explique passo a passo o que será feito e por quê.
2. **Implementação**: aplique as mudanças em cada arquivo, na ordem indicada.
3. **Dependências**: liste os comandos `uv add` / `uv remove` necessários.
4. **Validação**: descreva como testar que a migração funcionou (checklist manual).
5. **Impacto no frontend**: confirme explicitamente se há ou não alterações necessárias.

---

### **Persona / Tom**

Aja como um **desenvolvedor sênior Python** que domina LangChain e FastAPI.
Mantenha o tom técnico, claro e direto. Explique decisões de design quando relevantes.
Código em **pt-BR** (docstrings, comentários) alinhado ao padrão do projeto.

---

### **Critérios de Aceite**

1. O backend usa `ChatOpenAI` do `langchain-openai` em vez do client `openai.OpenAI` direto.
2. A variável de ambiente `OPENAI_API_KEY` é usada (não mais `THESYS_API_KEY`).
3. O modelo LLM é configurável via variável de ambiente `OPENAI_MODEL` (default: `gpt-4o-mini`).
4. O streaming continua funcionando via `write_content()` do `thesys_genui_sdk` — cada chunk é enviado em tempo real.
5. O histórico de conversação (`thread_store`) é preservado entre mensagens, convertido para/de `BaseMessage` do LangChain.
6. O endpoint `POST /chat` mantém o mesmo contrato (request/response) — o frontend `C1Chat` funciona sem alterações.
7. O decorator `@with_c1_response()` continua aplicado no endpoint.
8. `pyproject.toml` atualizado com `langchain-openai`, `langchain-core`, `langchain`.
9. Type hints presentes em todas as funções e métodos modificados.
10. Código passa no `ruff check` e `ruff format` sem erros.
11. Nenhum arquivo do frontend (`ui/`) foi alterado.
12. `.env` atualizado com `OPENAI_API_KEY` e `OPENAI_MODEL`.
13. O `uv.lock` é atualizado após as mudanças de dependência.

---

### **Referências**

- Código atual: `backend/llm_runner.py`, `backend/main.py`, `backend/thread_store.py`
- LangChain Docs: https://python.langchain.com/docs/
- LangChain OpenAI integration: https://python.langchain.com/docs/integrations/chat/openai/
- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- Thesys C1 Setup: https://docs.thesys.dev/guides/setup
- Cursor Rules do projeto: `.cursor/rules/backend-langchain-langgraph.mdc`, `.cursor/rules/backend-async-patterns.mdc`, `.cursor/rules/backend-clean-architecture.mdc`
