from typing import Protocol

from c2_telegram_bot.bot_context import BotContext


class HandlerInterface(Protocol):
    async def handle(self, context: BotContext) -> None:
        ...
