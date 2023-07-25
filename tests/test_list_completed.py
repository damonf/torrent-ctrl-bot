from unittest.mock import create_autospec

import pytest

from c2_telegram_bot.commands.list_completed import ListCompleted
from tests.helpers import shell_exec_stub

pytest_plugins = ("pytest_asyncio",)


class TestListCompleted:
    @pytest.mark.asyncio
    async def test_single_line(self, torrent_host, bot_context):
        mock_shell_exec = create_autospec(
            shell_exec_stub,
            return_value=(
                "     1   100%   131.0 MB  Done         0.0     0.0    0.5  Idle         Ubuntu 20.04 LTS (Focal Fossa) Desktop amd x64 2020 {Group}",
                None,
            ),
        )

        sut = ListCompleted(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -l"
        )

        bot_context.send_message.assert_called_with(
            "1 Ubuntu 20.04 LTS (Focal Fossa) Desktop amd x64 2020 {Group}\n"
        )

    @pytest.mark.asyncio
    async def test_multi_line(self, torrent_host, bot_context):
        mock_shell_exec = create_autospec(
            shell_exec_stub,
            return_value=(
                (
                    "    ID   Done       Have  ETA           Up    Down  Ratio  Status       Name\n"
                    "     1   100%   930.0 MB  Done         0.0     0.0    0.0  Idle         Manjaro Linux 17.1.10 x86-64 (Multi/ITA)\n"
                    "     2     0%       None  Unknown      0.0     0.0   None  Idle         Arch Linux 2021.11.01 (32 and 64bit) operating system\n"
                    "     3   100%     2.5 GB  Done         0.0     0.0    0.5  Idle         Ubuntu 20.04 LTS (Focal Fossa) Desktop amd x64 2020 {Group}\n"
                    "     4    n/a       None  Unknown      0.0     0.0   None  Idle         debian-11.2.0-amd64-DVD-1.iso\n"
                    '     5   100%   958.1 MB  Done         0.0     0.0    0.5  Idle         Linux Mint "Debian" - Linux Mint Xfce [201104] [32-Bit] [ISO\n'
                    "Sum:             4.66 GB               0.0     0.0\n"
                ),
                None,
            ),
        )

        sut = ListCompleted(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -l"
        )

        bot_context.send_message.assert_called_with(
            (
                "1 Manjaro Linux 17.1.10 x86-64 (Multi/ITA)\n"
                "3 Ubuntu 20.04 LTS (Focal Fossa) Desktop amd x64 2020 {Group}\n"
                '5 Linux Mint "Debian" - Linux Mint Xfce [201104] [32-Bit] [ISO\n'
            )
        )

    @pytest.mark.asyncio
    async def test_none_completed(self, torrent_host, bot_context):
        mock_shell_exec = create_autospec(
            shell_exec_stub,
            return_value=(
                (
                    "    ID   Done       Have  ETA           Up    Down  Ratio  Status       Name\n"
                    "     2     0%       None  Unknown      0.0     0.0   None  Idle         Arch Linux 2021.11.01 (32 and 64bit) operating system\n"
                    "     4    n/a       None  Unknown      0.0     0.0   None  Idle         debian-11.2.0-amd64-DVD-1.iso\n"
                    "Sum:             0.00 GB               0.0     0.0\n"
                ),
                None,
            ),
        )

        sut = ListCompleted(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -l"
        )

        bot_context.send_message.assert_called_with("No completed torrents")

    @pytest.mark.asyncio
    async def test_sends_error(self, torrent_host, bot_context):
        mock_shell_exec = create_autospec(
            shell_exec_stub, return_value=(None, "some error")
        )

        sut = ListCompleted(mock_shell_exec, torrent_host)

        await sut.handle(bot_context)

        mock_shell_exec.assert_called_with(
            "transmission-remote host -n transmission:password -l"
        )

        bot_context.send_message.assert_called_with("some error")
