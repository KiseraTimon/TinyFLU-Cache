"""LRU eviction + TinyLFU admission.

On a miss with a full cache, instead of always admitting the new item,
we ask TinyLFU whether the new item is accessed more often recently than
the LRU eviction candidate. If not, we reject the new item outright
(this is the core idea from Einziger, Friedman & Manes, 2014/2017).
"""

from __future__ import annotations
from collections import OrderedDict

from .tinylfu import TinyLFU


class TinyLFUCache:
    name = "tinylfu"

    # constructor
    def __init__(self, capacity: int, sketch_width: int = 1024, sketch_depth: int = 4):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._store: OrderedDict[str, bool] = OrderedDict()
        self.filter = TinyLFU(capacity, sketch_width=sketch_width, sketch_depth=sketch_depth)
        self.hits = 0
        self.misses = 0
        self.rejections = 0  # misses that were NOT admitted into the cache


    def access(self, key: str) -> bool:
        self.filter.record_access(key)

        if key in self._store:
            self._store.move_to_end(key)
            self.hits += 1
            return True

        self.misses += 1
        if len(self._store) < self.capacity:
            self._store[key] = True
            return False

        victim, _ = next(iter(self._store.items()))  # LRU candidate
        if self.filter.admit(candidate=key, victim=victim):
            self._store.popitem(last=False)
            self._store[key] = True
        else:
            self.rejections += 1
        return False


    @property
    def hit_ratio(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
