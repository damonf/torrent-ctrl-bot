from typing import Callable

from ..bot_context import BotContext
from ..torrent_host import TorrentHost
from .filter_magnet import FilterMagnet


class MagnetLink:
    def __init__(
        self, shell_exec: Callable[[str], tuple[str, str]], torrent_host: TorrentHost
    ):
        self._filter = FilterMagnet()
        self._shell_exec = shell_exec
        self._torrent_host = torrent_host

    @property
    def filter(self):
        return self._filter

    async def handle(self, context: BotContext):
        magnet_link = context.message_text

        output, error = self._shell_exec(
            f'transmission-remote {self._torrent_host.host} -n transmission:{self._torrent_host.password} -a "{magnet_link}"'
        )

        if error:
            print(error)

        await context.send_message(output or error)
