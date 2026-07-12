from src.cache.count_min_sketch import CountMinSketch


def test_sketch_increments_and_estimates():
    cms = CountMinSketch(width=256, depth=4, sample_size=1_000_000)
    for _ in range(5):
        cms.increment("hot")
    assert cms.estimate("hot") >= 5
    assert cms.estimate("cold") == 0


def test_sketch_ages_after_sample_size():
    cms = CountMinSketch(width=64, depth=2, sample_size=10)
    for _ in range(10):
        cms.increment("x")  # 10th increment triggers aging: 10 -> halved to 5
    assert cms.estimate("x") == 5
    cms.increment("x")  # one more increment on top of the aged count
    assert cms.estimate("x") == 6
    # crucially: far less than the un-aged total of 11, proving aging fired
    assert cms.estimate("x") < 11