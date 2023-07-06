from telegram.ext import MessageHandler

from c2_telegram_bot.handler_builder import HandlerBuilder
from c2_telegram_bot.interfaces.message_handler_interface import MessageHandlerInterface


class MessageHandlerBuilder(HandlerBuilder):
    def build(self, message_handler: MessageHandlerInterface) -> MessageHandler:
        return MessageHandler(
            message_handler.filter, self.create_handler_callback(message_handler)
        )
