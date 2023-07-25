from telegram.ext import MessageHandler

from c2_telegram_bot.handler_builder import HandlerBuilder
from c2_telegram_bot.interfaces.message_handler_interface import MessageHandlerInterface
from c2_telegram_bot.message_handler_access import MessageHandlerAccess


class MessageHandlerBuilder(HandlerBuilder):
    def build(self, message_handler: MessageHandlerInterface) -> MessageHandler:
        decorated = MessageHandlerAccess(message_handler)
        return MessageHandler(decorated.filter, self.create_handler_callback(decorated))
