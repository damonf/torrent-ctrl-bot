import asyncio


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


def shell_exec_stub(cmd: str) -> tuple[str, str]:
    pass
