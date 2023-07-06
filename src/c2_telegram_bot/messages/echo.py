from telegram.ext import filters

from ..bot_context import BotContext


class Echo:
    def __init__(self):
        self._filter = filters.TEXT

    @property
    def filter(self):
        return self._filter

    async def handle(self, context: BotContext):
        await context.send_message(context.message_text)
