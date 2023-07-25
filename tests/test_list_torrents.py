from unittest.mock import create_autospec

import pytest

from c2_telegram_bot.commands.list_torrents import ListTorrents
from tests.helpers import shell_exec_stub

pytest_plugins = ("pytest_asyncio",)


class TestListTorrent:
    @pytest.mark.asyncio
    async def test_sends_list(self, torrent_host, bot_context):
        bot_context.args = []
        mock_shell_exec = create_autospec(
            shell_exec_stub,
            return_value=(
                (
                    "    ID   Done       Have  ETA           Up    Down  Ratio  Status       Name\n"
                    "     1   100%   930.0 MB  Done         0.0     0.0    0.0  Idle         Manjaro Linux 17.1.10 x86-64 (Multi/ITA)\n"
                    "     2    n/a       None  Unknown      0.0     0.0   None  Idle         debian-11.2.0-amd64-DVD-1.iso\n"
                    '     3    55%   958.1 MB  Done         0.0     0.0    0.5  Idle         Linux Mint "Debian" - Linux Mint Xfce [201104] [32-Bit] [ISO\n'
                    "Sum:             1.88 GB               0.0     0.0\n"
                ),
                None,
            ),
        )

        sut = ListTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -l"
        )

        bot_context.send_message.assert_called_with(
            "ID Done Name\n"
            "1 100% Manjaro Linux 17.1.10 x86-64 (Multi/ITA)\n"
            "2 n/a debian-11.2.0-amd64-DVD-1.iso\n"
            '3 55% Linux Mint "Debian" - Linux Mint Xfce [201104] [32-Bit] [ISO\n'
        )

    @pytest.mark.asyncio
    async def test_sends_detailed_list(self, torrent_host, bot_context):
        bot_context.args = ["-d"]
        mock_shell_exec = create_autospec(
            shell_exec_stub,
            return_value=(
                (
                    "    ID   Done       Have  ETA           Up    Down  Ratio  Status       Name\n"
                    "     1   100%   930.0 MB  Done         0.0     0.0    0.0  Idle         Manjaro Linux 17.1.10 x86-64 (Multi/ITA)\n"
                    "     2    n/a       None  Unknown      0.0     0.0   None  Idle         debian-11.2.0-amd64-DVD-1.iso\n"
                    '     3    55%   958.1 MB  Done         0.0     0.0    0.5  Idle         Linux Mint "Debian" - Linux Mint Xfce [201104] [32-Bit] [ISO\n'
                    "Sum:             1.88 GB               0.0     0.0\n"
                ),
                None,
            ),
        )

        sut = ListTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -l"
        )

        bot_context.send_message.assert_called_with(
            "    ID   Done       Have  ETA           Up    Down  Ratio  Status       Name\n"
            "     1   100%   930.0 MB  Done         0.0     0.0    0.0  Idle         Manjaro Linux 17.1.10 x86-64 (Multi/ITA)\n"
            "     2    n/a       None  Unknown      0.0     0.0   None  Idle         debian-11.2.0-amd64-DVD-1.iso\n"
            '     3    55%   958.1 MB  Done         0.0     0.0    0.5  Idle         Linux Mint "Debian" - Linux Mint Xfce [201104] [32-Bit] [ISO\n'
            "Sum:             1.88 GB               0.0     0.0\n"
        )

    @pytest.mark.asyncio
    async def test_sends_error(self, torrent_host, bot_context):
        bot_context.args = []
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=(None, "some error")
        )

        sut = ListTorrents(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -l"
        )

        bot_context.send_message.assert_called_with("some error")
