import os


class EnvironVar:

    def __init__(self, name: str):
        self._name = name

    def get(self) -> str:
        var = os.environ.get(self._name)
        if var is None:
            raise ValueError(f"Environment variable '{self._name}' not set")
        return var
