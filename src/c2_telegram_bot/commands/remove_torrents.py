import re
from typing import Callable

from ..bot_context import BotContext
from ..torrent_host import TorrentHost


class RemoveTorrents:
    def __init__(
        self, shell_exec: Callable[[str], tuple[str, str]], torrent_host: TorrentHost
    ):
        self._name = "rm"
        self._description = "remove torrents"
        self._shell_exec = shell_exec
        self._torrent_host = torrent_host

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    async def handle(self, context: BotContext):
        async def bad_args():
            await context.send_message(
                "Bad args\nspecify torrent ids to remove, e.g. 2,4,6-8 or all"
            )

        if len(context.args) != 1:
            await bad_args()
            return

        torrent_ids = context.args[0]

        if not torrent_ids == "all" and not re.match(
            r"^((\d+)|(\d+-\d+))((,\d+)|(,\d+-\d+))*$", torrent_ids
        ):
            await bad_args()
            return

        output, error = self._shell_exec(
            f"transmission-remote {self._torrent_host.host} -n transmission:{self._torrent_host.password} -t {torrent_ids} -r"
        )

        if error:
            print(error)

        await context.send_message(output or error)
