from pydantic import BaseModel
from typing import (
    TypedDict,
    Literal,
)
import os
from openai import OpenAI
from dotenv import load_dotenv  # type: ignore

from thread_store import Message, thread_store
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
)
from thesys_genui_sdk.context import get_assistant_message, write_content  # type: ignore[import-untyped]

_ = load_dotenv()

# define the client
client = OpenAI(
    api_key=os.getenv('THESYS_API_KEY'),
    base_url='https://api.thesys.dev/v1/embed',
)


# define the prompt type in request
class Prompt(TypedDict):
    role: Literal['user']
    content: str
    id: str


# define the request type
class ChatRequest(BaseModel):
    prompt: Prompt
    threadId: str
    responseId: str

    class Config:
        extra: str = 'allow'  # Allow extra fields


async def generate_stream(chat_request: ChatRequest):
    conversation_history: list[ChatCompletionMessageParam] = (
        thread_store.get_messages(chat_request.threadId)
    )

    user_message: ChatCompletionUserMessageParam = {
        'role': 'user',
        'content': chat_request.prompt['content'],
    }
    conversation_history.append(user_message)
    thread_store.append_message(
        chat_request.threadId,
        Message(openai_message=user_message, id=chat_request.prompt['id']),
    )

    assistant_message_for_history: (
        ChatCompletionAssistantMessageParam | None
    ) = None

    stream = client.chat.completions.create(
        messages=conversation_history,
        model='c1/anthropic/claude-sonnet-4/v-20250815',
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        finish_reason = chunk.choices[0].finish_reason

        if delta and delta.content:
            await write_content(delta.content)

        if finish_reason:
            msg = get_assistant_message()
            assistant_message_for_history = (
                ChatCompletionAssistantMessageParam(
                    role='assistant',
                    content=msg['content'],
                )
            )

    if assistant_message_for_history:
        conversation_history.append(assistant_message_for_history)

        # Store the assistant message with the responseId
        thread_store.append_message(
            chat_request.threadId,
            Message(
                openai_message=assistant_message_for_history,
                id=chat_request.responseId,  # Assign responseId to the final assistant message
            ),
        )
