"""A simple bit-array Bloom filter, used by TinyLFU as the 'doorkeeper'.

The doorkeeper's job (per the TinyLFU paper) is cheap deduplication:
-   an item must be seen at least twice before it earns a slot in the
    (more expensive) frequency sketch.

This keeps one-hit-wonders from polluting the sketch.
"""
from __future__ import annotations
import hashlib


class BloomFilter:
    # construvtor
    def __init__(self, size: int, num_hashes: int = 4):
        if size <= 0:
            raise ValueError("size must be positive")

        self.size = size
        self.num_hashes = num_hashes
        self._bits = bytearray((size + 7) // 8)

    def _positions(self, item: str):
        # Double hashing: derive num_hashes indices from two base hashes.
        h1 = int.from_bytes(hashlib.md5(item.encode()).digest()[:8], "little")
        h2 = int.from_bytes(hashlib.sha1(item.encode()).digest()[:8], "little")

        for i in range(self.num_hashes):
            yield (h1 + i * h2) % self.size

    def add(self, item: str) -> None:
        for pos in self._positions(item):
            self._bits[pos // 8] |= 1 << (pos % 8)

    def contains(self, item: str) -> bool:
        return all(self._bits[pos // 8] & (1 << (pos % 8)) for pos in self._positions(item))

    def clear(self) -> None:
        self._bits = bytearray((self.size + 7) // 8)
