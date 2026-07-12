"""TinyLFU admission filter.

Combines a doorkeeper Bloom filter with a Count-Min Sketch to give an
approximate, memory-light estimate of 'how often has this item been
accessed recently', which is used to decide whether a newly-accessed item
deserves to evict the cache's current eviction victim.
"""

from __future__ import annotations

from .bloom import BloomFilter
from .count_min_sketch import CountMinSketch


class TinyLFU:
    # constructor
    def __init__(self, capacity: int, sketch_width: int = 1024, sketch_depth: int = 4):
        self.doorkeeper = BloomFilter(size=max(sketch_width, 64), num_hashes=4)
        self.sketch = CountMinSketch(
            width=sketch_width, depth=sketch_depth, sample_size=capacity * 10
        )


    def record_access(self, item: str) -> None:
        """Called on every access (hit or miss) to update frequency history."""
        if self.doorkeeper.contains(item):
            self.sketch.increment(item)
        else:
            self.doorkeeper.add(item)


    def estimate(self, item: str) -> int:
        base = self.sketch.estimate(item)

        """
        An item that's only cleared the doorkeeper (not yet in the sketch)
        # still counts as 'seen once'.
        """

        return base + 1 if self.doorkeeper.contains(item) and base == 0 else base


    def admit(self, candidate: str, victim: str) -> bool:
        """Should `candidate` be admitted at the expense of `victim`?"""
        return self.estimate(candidate) > self.estimate(victim)
