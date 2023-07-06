import logging
import os
import sys
from functools import partial

from telegram.ext import ApplicationBuilder

from c2_telegram_bot.command_handler_builder import CommandHandlerBuilder
from c2_telegram_bot.message_handler_builder import MessageHandlerBuilder

from .commands.command_help import CommandHelp
from .commands.list_torrents import ListTorrents
from .messages.echo import Echo
from .messages.magnet_link import MagnetLink
from .shell_exec import shell_exec
from .torrent_host import TorrentHost

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    def environ_get(name: str) -> str:
        var = os.environ.get(name)
        if var is None:
            print(f"{name} not set", file=sys.stderr)
            exit(1)
        return var

    application = ApplicationBuilder().token(environ_get("TOKEN")).build()

    shell_exec_env = partial(shell_exec, env=environ_get("ENV"))

    torrent_host = TorrentHost(environ_get("TORRENT_HOST"), environ_get("TORRENT_PWD"))

    command_handlers = [
        ListTorrents(shell_exec_env, torrent_host),
    ]

    command_help = CommandHelp(command_handlers)
    command_handlers.append(command_help)

    for hnd in command_handlers:
        application.add_handler(CommandHandlerBuilder().build(hnd))

    application.add_handler(
        MessageHandlerBuilder().build(MagnetLink(shell_exec_env, torrent_host))
    )
    application.add_handler(MessageHandlerBuilder().build(Echo()))

    application.run_polling()


if __name__ == "__main__":
    main()
