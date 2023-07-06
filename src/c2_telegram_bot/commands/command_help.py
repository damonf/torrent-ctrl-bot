from ..bot_context import BotContext
from ..interfaces.command_handler_interface import CommandHandlerInterface


class CommandHelp:
    def __init__(self, commands: list[CommandHandlerInterface]):
        self._name = "help"
        self._description = "show help"
        self._help_text = ""

        for name, desc in ((c.name, c.description) for c in commands):
            self._help_text += f"/{name}    {desc}\n"

        self._help_text += f"/{self._name}    {self._description}\n"

    @property
    def name(self):
        return self._name

    async def handle(self, context: BotContext):
        await context.send_message(self._help_text)
