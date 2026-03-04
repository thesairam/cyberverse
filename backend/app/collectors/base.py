from abc import ABC, abstractmethod
from typing import Any


class BaseCollector(ABC):
    """All collectors must implement collect() and return a list of raw dicts."""

    @abstractmethod
    async def collect(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def _safe_str(self, val, max_len: int = 2048) -> str:
        if val is None:
            return ""
        return str(val)[:max_len]
