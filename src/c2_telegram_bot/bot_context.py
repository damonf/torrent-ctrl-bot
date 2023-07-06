from telegram import Update
from telegram.ext import ContextTypes


class BotContext:
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._update = update
        self._context = context

    async def send_message(self, message: str):
        chat_id = getattr(self._update.effective_chat, "id", None)

        if chat_id is not None:
            await self._context.bot.send_message(chat_id=chat_id, text=message)

    @property
    def message_text(self):
        return self._update.message.text

    @property
    def args(self):
        return self._context.args
