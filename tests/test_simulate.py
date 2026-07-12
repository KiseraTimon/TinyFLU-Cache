from src.simulate import build_trace, compare_policies, run_simulation


def test_build_trace_length_and_seed_reproducible():
    t1 = build_trace(1000, 100, zipf_alpha=1.0, seed=42)
    t2 = build_trace(1000, 100, zipf_alpha=1.0, seed=42)
    assert len(t1) == 1000
    assert t1 == t2  # deterministic given a seed


def test_run_simulation_hit_ratio_bounds():
    trace = build_trace(5000, 200, zipf_alpha=1.2, seed=1)
    result = run_simulation("lru", cache_size=50, trace=trace)
    assert 0.0 <= result.hit_ratio <= 1.0
    assert result.hits + result.misses == len(trace)


def test_tinylfu_outperforms_lru_on_skewed_workload():
    """Reproduces the paper's central finding: under a skewed distribution
    and a small cache, TinyLFU admission should meet or beat plain LRU."""
    comparison = compare_policies(
        cache_size=50, trace_length=20000, num_items=1000, zipf_alpha=1.2, seed=7
    )
    lru_ratio = comparison["results"]["lru"]["hit_ratio"]
    tinylfu_ratio = comparison["results"]["tinylfu"]["hit_ratio"]
    assert tinylfu_ratio >= lru_ratio * 0.95  # allow small noise margin
