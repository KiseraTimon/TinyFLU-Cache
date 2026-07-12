from src.cache.bloom import BloomFilter


def test_bloom_add_contains():
    bf = BloomFilter(size=1000, num_hashes=4)
    assert not bf.contains("a")
    bf.add("a")
    assert bf.contains("a")


def test_bloom_clear():
    bf = BloomFilter(size=1000, num_hashes=4)
    bf.add("a")
    bf.clear()
    assert not bf.contains("a")
