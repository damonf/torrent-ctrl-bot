from telegram.ext import CommandHandler

from c2_telegram_bot.command_handler_access import CommandHandlerAccess
from c2_telegram_bot.handler_builder import HandlerBuilder
from c2_telegram_bot.interfaces.command_handler_interface import CommandHandlerInterface


class CommandHandlerBuilder(HandlerBuilder):
    def build(self, command_handler: CommandHandlerInterface) -> CommandHandler:
        decorated = CommandHandlerAccess(command_handler)
        return CommandHandler(decorated.name, self.create_handler_callback(decorated))
