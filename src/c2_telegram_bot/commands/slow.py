from typing import Callable

from ..bot_context import BotContext
from ..torrent_host import TorrentHost


class Slow:
    def __init__(
        self, shell_exec: Callable[[str], tuple[str, str]], torrent_host: TorrentHost
    ):
        self._name = "sl"
        self._description = "enable speed limit"
        self._shell_exec = shell_exec
        self._torrent_host = torrent_host

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    async def handle(self, context: BotContext):
        output, error = self._shell_exec(
            f"transmission-remote {self._torrent_host.host} -n transmission:{self._torrent_host.password} -as"
        )

        if error:
            print(error)

        await context.send_message(output or error)
