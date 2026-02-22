from typing import TypeAlias, TypedDict

from langchain_core.messages import BaseMessage


# Estrutura de mensagem: contém um BaseMessage do LangChain e um ID opcional
class Message(TypedDict):
    lc_message: BaseMessage
    id: str | None


ThreadId: TypeAlias = str


class ThreadStore:
    """
    Gerencia armazenamento e recuperação de mensagens de chat
    associadas a IDs de thread.
    Mensagens são armazenadas internamente como o TypedDict Message.
    """

    def __init__(self) -> None:
        """Inicializa um store vazio para threads."""
        self._thread_store: dict[ThreadId, list[Message]] = {}

    def get_messages(self, thread_id: ThreadId) -> list[BaseMessage]:
        """
        Recupera todas as mensagens de uma thread,
        extraindo o BaseMessage do LangChain.

        Args:
            thread_id: O ID da thread.

        Returns:
            Lista de BaseMessage compatível com o LangChain.
        """
        stored_messages = self._thread_store.get(thread_id, [])
        return [msg['lc_message'] for msg in stored_messages]

    def append_message(self, thread_id: ThreadId, message: Message) -> None:
        """
        Adiciona uma mensagem à thread especificada.
        Se a thread não existir, ela é criada.

        Args:
            thread_id: O ID da thread.
            message: O objeto Message a ser adicionado.
        """
        if thread_id not in self._thread_store:
            self._thread_store[thread_id] = []
        self._thread_store[thread_id].append(message)

    def append_messages(
        self, thread_id: ThreadId, messages: list[Message]
    ) -> None:
        """
        Adiciona múltiplas mensagens à thread especificada.
        Se a thread não existir, ela é criada.

        Args:
            thread_id: O ID da thread.
            messages: Lista de objetos Message a serem adicionados.
        """
        if thread_id not in self._thread_store:
            self._thread_store[thread_id] = []
        self._thread_store[thread_id].extend(messages)


thread_store = ThreadStore()
