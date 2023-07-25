import re
from typing import Callable

from ..bot_context import BotContext
from ..torrent_host import TorrentHost


class ListCompleted:
    def __init__(
        self, shell_exec: Callable[[str], tuple[str, str]], torrent_host: TorrentHost
    ):
        self._name = "lc"
        self._description = "list completed torrents"
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

        if error:
            print(error)
        else:
            lines = output.splitlines()
            completed = []

            for line in lines:
                if "100%" in line and "Done" in line:
                    mc = re.match(r"^\s+(\S+)(\s+\S+){8}\s+(.*)$", line)

                    if mc:
                        completed.append(mc.group(1) + " " + mc.group(3) + "\n")

            output = "".join(completed) or "No completed torrents"

        await context.send_message(output or error)
