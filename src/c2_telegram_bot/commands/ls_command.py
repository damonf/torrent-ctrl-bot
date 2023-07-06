from ..bot_context import BotContext


class LsCommand:
    def __init__(self, shell):
        self._name = "ls"
        self._shell_exec = shell

    @property
    def name(self):
        return self._name

    async def handle(self, context: BotContext):
        output, error = self._shell_exec(f"ls {' '.join(context.args)}")

        if error:
            print(error)

        await context.send_message(output or error)
