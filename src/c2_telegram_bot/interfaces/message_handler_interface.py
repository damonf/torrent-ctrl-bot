from abc import abstractmethod
from typing import Protocol

from c2_telegram_bot.interfaces.handler_interface import HandlerInterface


class MessageHandlerInterface(HandlerInterface, Protocol):
    @property
    @abstractmethod
    def filter(self):
        ...
