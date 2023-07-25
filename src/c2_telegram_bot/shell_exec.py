import shlex
import subprocess
import traceback
from typing import Callable

ShellExec = Callable[[str, str], tuple[str, str]]


def shell_exec(command_string: str, env: str) -> tuple[str, str]:
    """run a shell command and return its output"""

    if env == "TEST":
        return "", command_string

    error = output = ""

    try:
        process = subprocess.Popen(
            # use shlex.split for commands with args
            shlex.split(command_string),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            # Need this, or it will return bytes.
            # https://stackoverflow.com/questions/4256107/running-bash-commands-in-python
            universal_newlines=True,
        )

        try:
            output, _ = process.communicate(timeout=15)

        except TimeoutError:
            # on a timeout the process will still be running, so kill it
            process.kill()
            error, _ = process.communicate()

    # pylint: disable=broad-exception-caught
    except BaseException:
        error = traceback.format_exc()

    return format(f"{output}"), format(f"{error}")
