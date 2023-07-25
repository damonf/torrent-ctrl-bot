from unittest.mock import create_autospec

import pytest

from c2_telegram_bot.commands.remove_torrents import RemoveTorrents
from tests.helpers import shell_exec_stub

pytest_plugins = ("pytest_asyncio",)


class TestRemoveTorrent:
    @pytest.mark.asyncio
    async def test_remove_all(self, torrent_host, bot_context):
        bot_context.args = ["all"]
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=("removed", None)
        )

        sut = RemoveTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -t all -r"
        )

        bot_context.send_message.assert_called_with("removed")

    @pytest.mark.asyncio
    async def test_remove_one(self, torrent_host, bot_context):
        bot_context.args = ["1"]
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=("removed", None)
        )

        sut = RemoveTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -t 1 -r"
        )

        bot_context.send_message.assert_called_with("removed")

    @pytest.mark.asyncio
    async def test_remove_list(self, torrent_host, bot_context):
        bot_context.args = ["1,2,3"]
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=("removed", None)
        )

        sut = RemoveTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -t 1,2,3 -r"
        )

        bot_context.send_message.assert_called_with("removed")

    @pytest.mark.asyncio
    async def test_remove_range(self, torrent_host, bot_context):
        bot_context.args = ["1-3"]
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=("removed", None)
        )

        sut = RemoveTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -t 1-3 -r"
        )

        bot_context.send_message.assert_called_with("removed")

    @pytest.mark.asyncio
    async def test_remove_range_and_list(self, torrent_host, bot_context):
        bot_context.args = ["2,4,6-8"]
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=("removed", None)
        )

        sut = RemoveTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -t 2,4,6-8 -r"
        )

        bot_context.send_message.assert_called_with("removed")

    @pytest.mark.asyncio
    async def test_prints_help_for_wrong_arg_count(self, torrent_host, bot_context):
        bot_context.args = ["1", "2", "3"]
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=("removed", None)
        )

        sut = RemoveTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_not_called()

        bot_context.send_message.assert_called_with(
            "Bad args\nspecify torrent ids to remove, e.g. 2,4,6-8 or all"
        )

    @pytest.mark.asyncio
    async def test_prints_help_for_bad_arg(self, torrent_host, bot_context):
        bot_context.args = ["1 2 3"]
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=("removed", None)
        )

        sut = RemoveTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_not_called()

        bot_context.send_message.assert_called_with(
            "Bad args\nspecify torrent ids to remove, e.g. 2,4,6-8 or all"
        )

    @pytest.mark.asyncio
    async def test_sends_error(self, torrent_host, bot_context):
        bot_context.args = ["1"]
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=(None, "some error")
        )

        sut = RemoveTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -t 1 -r"
        )

        bot_context.send_message.assert_called_with("some error")
