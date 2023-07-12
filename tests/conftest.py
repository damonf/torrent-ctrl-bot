import pytest

from tests.helpers import async_return


@pytest.fixture()
def torrent_host(mocker):
    torrent_host = mocker.Mock()
    torrent_host.host = 'host'
    torrent_host.password = 'password'
    return torrent_host


@pytest.fixture()
def bot_context(mocker):
    bot_context = mocker.Mock()
    bot_context.send_message.return_value = async_return(None)
    return bot_context
