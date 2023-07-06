import asyncio

import pytest

from c2_telegram_bot.commands.command_help import CommandHelp

pytest_plugins = ("pytest_asyncio",)


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


@pytest.mark.asyncio
async def test_sample(mocker):
    bot_context = mocker.Mock()
    bot_context.send_message.return_value = async_return(None)

    cmd1 = mocker.Mock()
    cmd1.name = "cmd1"
    cmd1.description = "desc1"

    cmd2 = mocker.Mock()
    cmd2.name = "cmd2"
    cmd2.description = "desc2"

    command_help = CommandHelp([cmd1, cmd2])

    await command_help.handle(bot_context)

    bot_context.send_message.assert_called_with(
        "/cmd1    desc1\n/cmd2    desc2\n/help    show help\n"
    )
