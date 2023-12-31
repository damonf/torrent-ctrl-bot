import re
from typing import Callable

from ..bot_context import BotContext
from ..torrent_host import TorrentHost


class ListTorrents:
    def __init__(
        self, shell_exec: Callable[[str], tuple[str, str]], torrent_host: TorrentHost
    ):
        self._name = "ls"
        self._description = "list torrents"
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
            f"transmission-remote {self._torrent_host.host} -n transmission:{self._torrent_host.password} -l"
        )

        detailed = len(context.args) == 1 and context.args[0] == "-d"

        if error:
            print(error)
        elif not detailed:
            lines = output.splitlines()
            torrents = []

            for line in lines:
                mc = re.match(r"^\s+(\S+)\s+(\S+)\s+(\s+\S+){6,7}\s+(.*)$", line)

                if mc:
                    torrents.append(
                        f"{mc.group(1)} {mc.group(2)} {mc.group(mc.lastindex)}\n"  # type: ignore
                    )

            output = "".join(torrents) or "No torrents"

        await context.send_message(output or error)
