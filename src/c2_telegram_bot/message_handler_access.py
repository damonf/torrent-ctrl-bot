from c2_telegram_bot.bot_context import BotContext
from c2_telegram_bot.environ_var import EnvironVar
from c2_telegram_bot.interfaces.message_handler_interface import MessageHandlerInterface


class MessageHandlerAccess:

    def __init__(self, message_handler: MessageHandlerInterface):
        self._msg_hnd = message_handler
        self._user_id = EnvironVar('USER_ID').get()

    @property
    def filter(self):
        return self._msg_hnd.filter

    async def handle(self, context: BotContext):
        if str(context.user_id) == self._user_id:
            await self._msg_hnd.handle(context)