"""Count-Min Sketch: the approximate frequency-counting structure at the
heart of TinyLFU.

Faithful to the paper's design goals (not the exact bit-packing):
-   Counters are capped at 15 (i.e. behave like 4-bit counters).
-   Every `sample_size` increments, all counters are halved ("aging"), so the
    sketch tracks *recent* frequency rather than all-time frequency.
"""
from __future__ import annotations
import hashlib


class CountMinSketch:
    MAX_COUNT = 15  # matches the paper's 4-bit counter design


    # constructor
    def __init__(self, width: int = 1024, depth: int = 4, sample_size: int | None = None):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]

        # Reset/halve after this many increments, per TinyLFU's aging scheme.
        self.sample_size = sample_size or width * depth
        self._additions = 0


    def _positions(self, item: str):
        for row in range(self.depth):
            digest = hashlib.md5(f"{row}:{item}".encode()).digest()
            yield row, int.from_bytes(digest[:8], "little") % self.width


    def increment(self, item: str) -> None:
        for row, col in self._positions(item):
            if self.table[row][col] < self.MAX_COUNT:
                self.table[row][col] += 1
        self._additions += 1
        if self._additions >= self.sample_size:
            self._age()


    def estimate(self, item: str) -> int:
        return min(self.table[row][col] for row, col in self._positions(item))


    def _age(self) -> None:
        """Halve every counter — keeps the sketch responsive to recency."""
        for row in self.table:
            for i in range(len(row)):
                row[i] //= 2
        self._additions = 0

    def reset(self) -> None:
        self.table = [[0] * self.width for _ in range(self.depth)]
        self._additions = 0
