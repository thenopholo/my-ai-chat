Atue como um "Project Rule Builder" para este repositório que é um fork/implementação baseada na plataforma **Thesys C1**.

Objetivo: criar/atualizar um conjunto de Project Rules (.mdc) em pt-BR dentro de `.cursor/rules/`, baseadas:

1) no estado REAL do projeto (pastas, dependências, padrões já usados)

2) na documentação oficial do Thesys C1 e padrões de integração:

   - Thesys C1 Basics: https://docs.thesys.dev/guides/basics
   - Integração com Backend: https://docs.thesys.dev/guides/implementing-api
   - Rendering UI: https://docs.thesys.dev/guides/rendering-ui
   - Streaming: https://docs.thesys.dev/guides/streaming
   - Guiding UI Generations: https://docs.thesys.dev/guides/guiding-outputs
   - Tool Calling: https://docs.thesys.dev/guides/integrate-data/tool-calling
   - LangChain Integration: https://docs.thesys.dev/guides/frameworks/langchain
   - Full Documentation Index: https://docs.thesys.dev/llms.txt
   - Exemplo oficial: https://github.com/thesysdev/examples/tree/main/langchain-with-c1-python
   - Se não conseguir acessar os links, derive as regras a partir do código existente, `pyproject.toml`, `package.json` e dos SDKs instalados.


## DEVE/NÃO DEVE

- Caso tenha alguma dúvida ou algo que não esteja claro, **VOCÊ DEVE** perguntar ao usuário para esclarecer antes de continuar.
- Caso tenha alguma dúvida ou algo que não esteja claro, **VOCÊ NÃO DEVE** continuar sem esclarecer.


## O que é o Thesys C1

Thesys C1 é uma plataforma de **Generative UI** que permite construir aplicações de chat com IA que geram interfaces dinâmicas. Os conceitos centrais são:

- **C1 API**: endpoint OpenAI-compatible (`https://api.thesys.dev/v1/embed`) que gera respostas contendo DSL de UI nativa.
- **Backend SDKs**: `thesys-genui-sdk` e `crayonai-stream` para Python — fornecem decorators e helpers para streaming de respostas.
- **Frontend SDKs**: `@thesysai/genui-sdk` e `@crayonai/react-ui` para React — renderizam as respostas da API como componentes interativos.
- **Integração com LangChain**: usar `ChatOpenAI` com `base_url` da Thesys como LLM provider dentro de chains/agents do LangChain.


## Contexto do Projeto Atual

### Backend (Python 3.13 + FastAPI + LangChain)

Arquivos atuais: `backend/main.py`, `backend/llm_runner.py`, `backend/thread_store.py`.

**Padrão de integração backend atual:**

```python
# main.py — Endpoint com decorator C1
from thesys_genui_sdk.fast_api import with_c1_response

@app.post('/chat')
@with_c1_response()
async def chat_endpoint(request: ChatRequest):
    await generate_stream(request)
```

```python
# llm_runner.py — LLM via LangChain + Thesys API
from langchain_openai import ChatOpenAI
from thesys_genui_sdk.context import get_assistant_message, write_content

llm = ChatOpenAI(
    api_key=os.getenv('THESYS_API_KEY'),
    base_url='https://api.thesys.dev/v1/embed',
    model='c1/anthropic/claude-sonnet-4/v-20250815',
    streaming=True,
)

async def generate_stream(chat_request: ChatRequest) -> None:
    # Streaming via LangChain .astream()
    async for chunk in llm.astream(conversation_history):
        if isinstance(chunk.content, str) and chunk.content:
            await write_content(chunk.content)  # Envia chunk para o frontend

    # Obtém a mensagem final montada pelo SDK
    assistant_response = get_assistant_message()
```

```python
# thread_store.py — Mensagens LangChain
from langchain_core.messages import BaseMessage

class Message(TypedDict):
    lc_message: BaseMessage  # HumanMessage, AIMessage, SystemMessage
    id: str | None
```

**Dependências backend:**
- `fastapi`, `uvicorn`, `pydantic`
- `thesys-genui-sdk`, `crayonai-stream`
- `langchain`, `langchain-core`, `langchain-openai`
- `python-dotenv`, `ruff`

### Frontend (React 19 + Vite + TypeScript)

Arquivo atual: `ui/src/App.tsx`.

**Padrão de integração frontend atual:**

```tsx
// App.tsx — Componente de chat C1
import "@crayonai/react-ui/styles/index.css";
import { C1Chat } from "@thesysai/genui-sdk";

export default function App() {
  return <C1Chat apiUrl="/api/chat" />;
}
```

**Dependências frontend:**
- `@thesysai/genui-sdk`, `@crayonai/react-ui`
- `react`, `react-dom`, `react-markdown`, `lucide-react`
- Proxy Vite: `/api` → `http://127.0.0.1:8000`

### Padrão LangChain com C1 (documentação oficial)

Conforme a documentação em https://docs.thesys.dev/guides/frameworks/langchain:

```python
# Padrão de agente LangChain com C1
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# C1 como LLM provider
model = ChatOpenAI(
    base_url="https://api.thesys.dev/v1/embed",
    model="c1/anthropic/claude-sonnet-4/v-20250815",
    api_key=os.environ.get("THESYS_API_KEY"),
)

# Tools para o agente
@tool
def execute_sql_query(query: str) -> str:
    """Execute a SQL query on the database."""
    # implementação...

# Prompt com SystemMessage + HumanMessage + scratchpad
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant..."),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Agente e executor
tools = [execute_sql_query]
agent = create_openai_tools_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

```tsx
// Frontend com C1Component para UIs mais customizadas
import { ThemeProvider, C1Component } from "@thesysai/genui-sdk";

<ThemeProvider>
  <C1Component
    c1Response={c1Response}
    isStreaming={isLoading}
    updateMessage={(message) => setC1Response(message)}
    onAction={({ llmFriendlyMessage }) => {
      makeApiCall(llmFriendlyMessage, c1Response);
    }}
  />
</ThemeProvider>
```


### O que analisar no repo

- `backend/main.py` (FastAPI app, endpoints, uso de `@with_c1_response()`).
- `backend/llm_runner.py` (integração LangChain + Thesys, streaming com `write_content`, `get_assistant_message`).
- `backend/thread_store.py` (gerenciamento de threads com `BaseMessage` do LangChain).
- `backend/pyproject.toml` (dependências, config do Ruff).
- `pyrightconfig.json` (type checking).
- `ui/src/App.tsx` (componente raiz com `C1Chat`).
- `ui/package.json` (dependências frontend, SDKs Thesys).
- `ui/vite.config.ts` (proxy para backend).
- Presença de tools, agents, chains no backend.
- Presença de componentes customizados de chat no frontend.
- Presença de system prompts e templates de prompt.


### Entrada opcional

- É possível fornecer um arquivo complementar com informações/contexto para orientar a geração das rules.
- Formatos aceitos: `.md`, `.mdc`, `.txt`, `.json`, `.yaml`.
- Tratamento:
  - Leia o arquivo integralmente e extraia diretrizes úteis.
  - Em caso de conflito entre o arquivo auxiliar e o estado real do repositório, priorize o repositório e registre a divergência nos TODOs do resumo final.
  - Não copie o conteúdo na íntegra; incorpore como regras objetivas.
  - No resumo final, indique o nome do arquivo usado como "Fonte auxiliar".


### Saída esperada (arquivos e conteúdo)

Crie/atualize **exatamente** estes arquivos, com front-matter e conteúdo conciso em bullets:


1) `.cursor/rules/thesys-c1-overview.mdc` (Always)

- `description`: Visão geral da plataforma Thesys C1 e do projeto.
- O que é C1: plataforma de Generative UI; API OpenAI-compatible (`https://api.thesys.dev/v1/embed`).
- Arquitetura: Backend (FastAPI + LangChain + C1 SDK) → Frontend (React + GenUI SDK).
- Fluxo principal: usuário envia mensagem → backend processa com LangChain/C1 → streaming de resposta com UI dinâmica → frontend renderiza com `C1Chat`/`C1Component`.
- Variável de ambiente obrigatória: `THESYS_API_KEY` (nunca hardcodar).
- Modelos disponíveis: `c1/anthropic/claude-sonnet-4/v-*`, `c1/openai/gpt-4o/v-*`, etc.
- Documentação de referência: links oficiais.
- Seções: Objetivo, Visão Geral, Fluxo de Dados, Variáveis de Ambiente, Referências.


2) `.cursor/rules/thesys-c1-backend-sdk.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- SDK backend: `thesys-genui-sdk` e `crayonai-stream`.
- `@with_c1_response()`: decorator FastAPI que habilita o protocolo de resposta C1 no endpoint; deve ser aplicado **antes** do endpoint processar a lógica de streaming.
- `write_content(content: str)`: função async que envia chunks de texto ao frontend durante streaming; deve ser chamada para cada fragmento recebido do LLM.
- `get_assistant_message()`: retorna a mensagem final montada pelo SDK (dict com `content`); chamar **após** todo o streaming ser concluído.
- Padrão: decorar endpoint → chamar `write_content` para cada chunk → chamar `get_assistant_message` ao final → salvar no histórico.
- Não misturar `StreamingResponse` manual com `@with_c1_response()` — o decorator gerencia o protocolo.
- Seções: Objetivo, Componentes do SDK, Padrão de Uso, Exemplos, Anti-padrões, Checklist.


3) `.cursor/rules/thesys-c1-langchain-integration.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- **ChatOpenAI como LLM provider C1**: sempre configurar `base_url='https://api.thesys.dev/v1/embed'` e `api_key` via env var; `streaming=True` para chat.
- **Modelos**: usar prefixo `c1/` nos nomes de modelo (ex.: `c1/anthropic/claude-sonnet-4/v-20250815`); centralizar nome do modelo em variável ou settings.
- **Streaming com LangChain**: usar `.astream()` para streaming async; iterar sobre chunks e chamar `write_content()` para cada chunk com conteúdo.
- **Mensagens LangChain**: usar `HumanMessage`, `AIMessage`, `SystemMessage` do `langchain_core.messages`; armazenar no `ThreadStore` como `BaseMessage`.
- **Agents e Tools**: usar `@tool` decorator para definir tools; `create_openai_tools_agent` + `AgentExecutor` para agentes com tool calling; prompts com `ChatPromptTemplate.from_messages()` incluindo `("placeholder", "{agent_scratchpad}")`.
- **langserve** (opcional): usar `add_routes()` para expor chains como endpoints REST automaticamente.
- Seções: Objetivo, Configuração do LLM, Streaming, Mensagens e Histórico, Agents e Tools, Exemplos, Anti-padrões, Checklist.


4) `.cursor/rules/thesys-c1-frontend-sdk.mdc` (Auto-attach)

- `globs`: `"ui/src/**"`.
- SDK frontend: `@thesysai/genui-sdk` e `@crayonai/react-ui`.
- **C1Chat**: componente all-in-one para chat completo; aceita `apiUrl` (apontando para proxy do backend); gerencia UI, mensagens, streaming, threads internamente.
- **C1Component + ThemeProvider**: para UIs mais customizadas; `C1Component` renderiza uma resposta C1 individual; `isStreaming` para indicar loading; `updateMessage` para atualizar resposta; `onAction` para interceptar ações do usuário na UI gerada.
- **Estilos obrigatórios**: importar `@crayonai/react-ui/styles/index.css` no entry point.
- **Proxy**: toda comunicação via proxy Vite (`/api/*` → backend); nunca acessar backend diretamente.
- **Customização**: customizar aparência via props do componente ou CSS override; para funcionalidades além do SDK, criar componentes wrapper.
- Seções: Objetivo, Componentes, C1Chat vs C1Component, Estilos, Proxy, Anti-padrões, Checklist.


5) `.cursor/rules/thesys-c1-streaming-protocol.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py","ui/src/**"`.
- Protocolo de streaming C1: o backend envia chunks via `write_content()` → o SDK monta a resposta → o frontend renderiza em tempo real.
- **Backend**: `@with_c1_response()` gerencia o protocolo; **nunca** enviar JSON bruto ou SSE manual quando usando este decorator; `write_content()` aceita strings (chunks de texto); chamar `get_assistant_message()` ao final para obter resposta montada.
- **Frontend**: `C1Chat` gerencia streaming automaticamente; `C1Component` com `isStreaming={true}` mostra estado de loading e atualiza progressivamente.
- **Timeouts**: configurar timeouts no LLM (`ChatOpenAI` timeout param); tratar erros de streaming graciosamente.
- **Thread management**: cada request inclui `threadId` e `responseId`; manter histórico de mensagens por thread; `ThreadStore` para persistência em memória (evoluir para persistência real).
- Seções: Objetivo, Fluxo Completo, Backend Protocol, Frontend Protocol, Error Handling, Anti-padrões, Checklist.


6) `.cursor/rules/thesys-c1-tool-calling.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- Tool calling com C1: o LLM C1 suporta tool calling via protocolo OpenAI-compatible.
- **Definição de tools**: usar `@tool` decorator do LangChain; docstrings claras e descritivas (o LLM usa para decidir quando usar a tool); tipagem de parâmetros e retorno.
- **AgentExecutor**: combinar tools + prompt + model em `AgentExecutor`; tratar erros de tools graciosamente; logs verbosos em dev (`verbose=True`), desligados em prod.
- **Padrão de prompt para tools**: incluir `("placeholder", "{agent_scratchpad}")` no template para o agente registrar raciocínio; system prompt descrevendo capacidades e contexto.
- **SQL tools** (se aplicável): sanitizar queries; read-only quando possível; limitar resultados; tratar erros de conexão.
- Seções: Objetivo, Definição de Tools, Agent Pattern, Prompt Pattern, Segurança, Anti-padrões, Checklist.


7) `.cursor/rules/thesys-c1-guiding-outputs.mdc` (Auto-attach)

- `globs`: `"backend/**/*.py"`.
- Guiding UI generations: usar system prompts para controlar a estrutura e conteúdo da UI gerada pelo C1.
- **System prompts**: definir personalidade, formato de resposta, restrições; armazenar em módulos separados (`prompts/`).
- **Contexto**: incluir contexto relevante no prompt (dados do usuário, histórico, resultados de tools).
- **UI hints**: o C1 pode gerar componentes ricos (tabelas, gráficos, cards, formulários) baseados nas instruções do system prompt.
- Separação clara: system prompt (controlado pelo desenvolvedor) vs user input (nunca confiar sem validação).
- Seções: Objetivo, System Prompts, Contexto, UI Hints, Segurança, Checklist.


8) `.cursor/rules/thesys-c1-project-architecture.mdc` (Auto-attach)

- `globs`: `"backend/**","ui/src/**"`.
- Arquitetura full-stack: Backend (FastAPI + LangChain + C1 SDK) ↔ Proxy Vite ↔ Frontend (React + GenUI SDK).
- **Fluxo de request**: Frontend (`C1Chat` ou fetch) → Proxy Vite (`/api/*`) → Backend (`@with_c1_response()` endpoint) → LangChain (ChatOpenAI → C1 API) → Streaming response → Frontend renderiza.
- **Separação de responsabilidades**: Backend faz toda a lógica de IA (chains, agents, tools, prompts); Frontend renderiza UI gerada e gerencia interação do usuário.
- **Thread management**: `threadId` identifica a conversa; `responseId` identifica a resposta individual; `ThreadStore` mantém histórico; mensagens como `BaseMessage` do LangChain.
- **Evolução**: migrar ThreadStore para persistência real (DB); adicionar agents/tools; implementar autenticação; adicionar múltiplas conversas.
- Seções: Objetivo, Diagrama de Arquitetura, Fluxo de Dados, Separação de Responsabilidades, Evolução, Checklist.


### Opcionais (criar somente se o repo indicar necessidade)

- `.cursor/rules/thesys-c1-custom-components.mdc` (Auto-attach se houver componentes React customizados além do `C1Chat` padrão, usando `C1Component` + `ThemeProvider`).
- `.cursor/rules/thesys-c1-langserve.mdc` (Auto-attach se detectar uso de `langserve` para expor chains como endpoints REST).
- `.cursor/rules/thesys-c1-langgraph-agents.mdc` (Auto-attach se houver uso de `StateGraph` do LangGraph para orquestração de agentes multi-step).
- `.cursor/rules/thesys-c1-rag.mdc` (Auto-attach se houver implementação de RAG — Retrieval Augmented Generation — com retrievers, vector stores, embeddings).
- `.cursor/rules/thesys-c1-multi-model.mdc` (Auto-attach se o projeto usar múltiplos modelos C1 para diferentes tarefas).


### Requisitos de formatação

- Idioma: pt-BR, direto e assertivo.
- Cada arquivo começa com front-matter YAML: `description`, e **ou** `alwaysApply: true` **ou** `globs: [...]` (para Auto-attach).
- Texto em bullets, seções curtas: Objetivo, Regras, Anti-padrões, Checklist (e "Exemplos curtos" quando útil).
- Incluir **exemplos de código** concretos baseados no projeto real (não exemplos genéricos).
- Referenciar arquivos do projeto com `[arquivo.py](mdc:backend/arquivo.py)` ou `[App.tsx](mdc:ui/src/App.tsx)`.
- Não copiar documentação inteira; **alinhe e referencie** (ex.: "conforme documentação Thesys C1 Streaming Guide").
- Limite: regras objetivas (evitar longos parágrafos).


### Passos finais

- Liste no final um "Resumo do que foi detectado":
  - SDKs Thesys instalados e versões.
  - Padrão de integração backend (decorator, streaming, mensagens).
  - Padrão de integração frontend (C1Chat vs C1Component).
  - LangChain: uso de ChatOpenAI, agents, tools, chains.
  - Thread management (ThreadStore, BaseMessage).
  - Proxy Vite e comunicação frontend-backend.
- Valide os `globs` com base na árvore real do repo e mostre-os no resumo.
- Se algo estiver ambíguo, proponha defaults sensatos e registre TODOs.
- Se um arquivo auxiliar foi utilizado, inclua no resumo: `Fonte auxiliar: <caminho/arquivo>` e destaque quaisquer decisões derivadas dele.
