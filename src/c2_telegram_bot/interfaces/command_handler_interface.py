from abc import abstractmethod
from typing import Protocol

from c2_telegram_bot.interfaces.handler_interface import HandlerInterface


class CommandHandlerInterface(HandlerInterface, Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...
