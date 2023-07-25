import logging
from functools import partial

from telegram.ext import ApplicationBuilder

from c2_telegram_bot.command_handler_builder import CommandHandlerBuilder
from c2_telegram_bot.commands.fast import Fast
from c2_telegram_bot.commands.list_completed import ListCompleted
from c2_telegram_bot.commands.remove_torrents import RemoveTorrents
from c2_telegram_bot.commands.slow import Slow
from c2_telegram_bot.environ_var import EnvironVar
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
    application = ApplicationBuilder().token(EnvironVar("TOKEN").get()).build()

    shell_exec_env = partial(shell_exec, env=EnvironVar("ENV").get())

    torrent_host = TorrentHost(
        EnvironVar("TORRENT_HOST").get(), EnvironVar("TORRENT_PWD").get()
    )

    command_handlers = [
        ListTorrents(shell_exec_env, torrent_host),
        ListCompleted(shell_exec_env, torrent_host),
        RemoveTorrents(shell_exec_env, torrent_host),
        Fast(shell_exec_env, torrent_host),
        Slow(shell_exec_env, torrent_host),
    ]

    command_help = CommandHelp(command_handlers)
    command_handlers.append(command_help)

    for hnd in command_handlers:
        application.add_handler(CommandHandlerBuilder().build(hnd))

    message_handlers = [
        MagnetLink(shell_exec_env, torrent_host),
        Echo(),
    ]
    for hnd in message_handlers:
        application.add_handler(MessageHandlerBuilder().build(hnd))

    application.run_polling()


if __name__ == "__main__":
    main()
