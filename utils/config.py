from collections.abc import Mapping
from typing import Any

class BaseNamespace(Mapping[str, Any]):
    def __init__(self, data: dict):
        self._data = data

    def __iter__(self):
        yield from self._data.keys()

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __getattr__(self, key: str) -> Any:
        try:
            return super().__getattribute__(key)  # type: ignore
        except AttributeError:
            return self._data[key]

class Bot(BaseNamespace):
    def __init__(self, data):
        super().__init__(data)
        self.args = BaseNamespace(data["args"])
        self.allowed_mentions = BaseNamespace(data["allowed_mentions"])

class Config(BaseNamespace):
    def __init__(self, data):
        super().__init__(data)
        self.bot = Bot(data["bot"])
        self.database = BaseNamespace(data["database"])
        self.environment = BaseNamespace(data["environment"])
        self.prefixes = BaseNamespace(data["prefixes"])
        self.redis = BaseNamespace(data["redis"])
        self.logging = BaseNamespace(data["logging"])