from typing import Any, Callable, Coroutine

from telegram import Update
from telegram.ext import CallbackContext, ContextTypes, ExtBot

from c2_telegram_bot.bot_context import BotContext
from c2_telegram_bot.interfaces.message_handler_interface import HandlerInterface

HCB = Callable[
    [Update, CallbackContext[ExtBot[None], dict, dict, dict]], Coroutine[Any, Any, None]
]


class HandlerBuilder:

    @staticmethod
    def create_handler_callback(cmd_hnd: HandlerInterface) -> HCB:
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await cmd_hnd.handle(BotContext(update, context))

        return handler
