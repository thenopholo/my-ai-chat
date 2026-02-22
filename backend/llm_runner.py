import os
import traceback
from typing import (
    Literal,
    TypedDict,
)

from dotenv import load_dotenv  # type: ignore
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict
from thesys_genui_sdk.context import (  # type: ignore[import-untyped]
    get_assistant_message,
    write_content,
)

from thread_store import Message, thread_store

_ = load_dotenv()

C1_MODEL: str = os.getenv(
    'C1_MODEL', 'c1/anthropic/claude-sonnet-4/v-20250815'
)

# ChatOpenAI apontando para a API Thesys (C1 DSL nativo)
llm = ChatOpenAI(
    api_key=os.getenv('THESYS_API_KEY'),  # type: ignore[arg-type]
    base_url='https://api.thesys.dev/v1/embed',
    model=C1_MODEL,
    streaming=True,
)


# Define o tipo de prompt no request
class Prompt(TypedDict):
    role: Literal['user']
    content: str
    id: str


# Define o tipo do request
class ChatRequest(BaseModel):
    model_config = ConfigDict(extra='allow')

    prompt: Prompt
    threadId: str
    responseId: str


async def generate_stream(chat_request: ChatRequest) -> None:
    """Gera resposta via streaming usando LangChain ChatOpenAI."""
    try:
        conversation_history = thread_store.get_messages(chat_request.threadId)

        user_message = HumanMessage(content=chat_request.prompt['content'])
        conversation_history.append(user_message)
        thread_store.append_message(
            chat_request.threadId,
            Message(
                lc_message=user_message,
                id=chat_request.prompt['id'],
            ),
        )

        print(f'[LLM] Iniciando streaming - modelo: {C1_MODEL}')

        async for chunk in llm.astream(conversation_history):
            if isinstance(chunk.content, str) and chunk.content:
                await write_content(chunk.content)

        assistant_response = get_assistant_message()
        assistant_message = AIMessage(content=assistant_response['content'])

        conversation_history.append(assistant_message)
        thread_store.append_message(
            chat_request.threadId,
            Message(
                lc_message=assistant_message,
                id=chat_request.responseId,
            ),
        )
        print('[LLM] Streaming concluído com sucesso')
    except Exception:
        print('[LLM] ERRO em generate_stream:')
        traceback.print_exc()
