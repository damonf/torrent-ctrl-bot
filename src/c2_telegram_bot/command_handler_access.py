from c2_telegram_bot.bot_context import BotContext
from c2_telegram_bot.environ_var import EnvironVar
from c2_telegram_bot.interfaces.command_handler_interface import CommandHandlerInterface


class CommandHandlerAccess:

    def __init__(self, command_handler: CommandHandlerInterface):
        self._cmd_hnd = command_handler
        self._user_id = EnvironVar('USER_ID').get()

    @property
    def name(self) -> str:
        return self._cmd_hnd.name

    @property
    def description(self) -> str:
        return self._cmd_hnd.description

    async def handle(self, context: BotContext):
        if str(context.user_id) == self._user_id:
            await self._cmd_hnd.handle(context)