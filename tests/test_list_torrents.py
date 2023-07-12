from unittest.mock import create_autospec
import pytest

from c2_telegram_bot.commands.list_torrents import ListTorrents
from tests.helpers import shell_exec_stub

pytest_plugins = ("pytest_asyncio",)


class TestListTorrent:

    @pytest.mark.asyncio
    async def test_sends_list(self, torrent_host, bot_context):
        mock_shell_exec = create_autospec(shell_exec_stub, return_value=('torrent list', None))

        list_torrents = ListTorrents(mock_shell_exec, torrent_host)

        await list_torrents.handle(bot_context)

        mock_shell_exec.assert_called_with(
           'transmission-remote host -n transmission:password -l'
        )

        bot_context.send_message.assert_called_with(
            'torrent list'
        )

    @pytest.mark.asyncio
    async def test_sends_error(self, torrent_host, bot_context):
        mock_shell_exec = create_autospec(shell_exec_stub, return_value=(None, 'some error'))

        list_torrents = ListTorrents(mock_shell_exec, torrent_host)

        await list_torrents.handle(bot_context)

        mock_shell_exec.assert_called_with(
           'transmission-remote host -n transmission:password -l'
        )

        bot_context.send_message.assert_called_with(
            'some error'
        )