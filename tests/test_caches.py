from src.cache.lru_cache import LRUCache
from src.cache.tinylfu_cache import TinyLFUCache


def test_lru_basic_hit_miss():
    cache = LRUCache(capacity=2)
    assert cache.access("a") is False  # miss
    assert cache.access("a") is True   # hit
    cache.access("b")
    cache.access("c")  # evicts "a" (least recently used)
    assert cache.access("a") is False  # miss, was evicted


def test_lru_capacity_validation():
    try:
        LRUCache(capacity=0)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_tinylfu_basic_hit_miss():
    cache = TinyLFUCache(capacity=2)
    assert cache.access("a") is False
    assert cache.access("a") is True
    assert cache.hit_ratio == 0.5


def test_tinylfu_protects_hot_item_from_cold_churn():
    """This is the paper's core claim in miniature: a frequently-accessed
    item should survive a flood of one-hit-wonder accesses that would
    otherwise evict it under plain LRU."""
    cache = TinyLFUCache(capacity=2, sketch_width=256, sketch_depth=4)

    # Warm up "hot" so TinyLFU has frequency history for it.
    for _ in range(20):
        cache.access("hot")
    cache.access("warm")

    # Flood with one-hit-wonders that would evict "hot" under plain LRU.
    for i in range(50):
        cache.access(f"churn-{i}")

    assert cache.access("hot") is True  # still resident
