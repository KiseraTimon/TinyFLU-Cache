"""Plain LRU cache — the baseline we compare TinyLFU against."""

from __future__ import annotations
from collections import OrderedDict


class LRUCache:
    name = "lru"


    # constructor
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._store: OrderedDict[str, bool] = OrderedDict()
        self.hits = 0
        self.misses = 0


    def access(self, key: str) -> bool:
        """Access `key`; returns True on hit, False on miss."""
        if key in self._store:
            self._store.move_to_end(key)
            self.hits += 1
            return True

        self.misses += 1
        if len(self._store) >= self.capacity:
            self._store.popitem(last=False)  # evict LRU item
        self._store[key] = True
        return False


    @property
    def hit_ratio(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
