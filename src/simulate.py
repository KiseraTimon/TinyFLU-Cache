"""Runs a trace through a cache policy and reports hit-ratio metrics.

This piece reproduces the paper's core figures:
hit ratio vs. cache size, for LRU vs. LRU+TinyLFU, under a skewed workload.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from src.cache import LRUCache, TinyLFUCache
from src.workload import generate_zipf_trace


POLICIES = {"lru": LRUCache, "tinylfu": TinyLFUCache}


@dataclass
class SimulationResult:
    policy: str
    cache_size: int
    trace_length: int
    hits: int
    misses: int
    hit_ratio: float
    rejections: int = 0
    elapsed_seconds: float = 0.0
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "policy": self.policy,
            "cache_size": self.cache_size,
            "trace_length": self.trace_length,
            "hits": self.hits,
            "misses": self.misses,
            "hit_ratio": round(self.hit_ratio, 4),
            "rejections": self.rejections,
            "elapsed_seconds": round(self.elapsed_seconds, 4),
        }


def run_simulation(policy: str, cache_size: int, trace: list[str]) -> SimulationResult:
    if policy not in POLICIES:
        raise ValueError(f"unknown policy '{policy}', choose from {list(POLICIES)}")

    cache = POLICIES[policy](cache_size)
    start = time.perf_counter()

    for key in trace:
        cache.access(key)
    elapsed = time.perf_counter() - start

    return SimulationResult(
        policy=policy,
        cache_size=cache_size,
        trace_length=len(trace),
        hits=cache.hits,
        misses=cache.misses,
        hit_ratio=cache.hit_ratio,
        rejections=getattr(cache, "rejections", 0),
        elapsed_seconds=elapsed,
    )


def build_trace(
    trace_length: int, num_items: int, zipf_alpha: float, seed: int | None = None
) -> list[str]:
    return generate_zipf_trace(trace_length, num_items, alpha=zipf_alpha, seed=seed)


def compare_policies(
    cache_size: int, trace_length: int, num_items: int, zipf_alpha: float, seed: int | None = None
) -> dict:
    """Run every registered policy on the *same* trace for a fair comparison."""
    trace = build_trace(trace_length, num_items, zipf_alpha, seed)
    results = {
        name: run_simulation(name, cache_size, trace).to_dict() for name in POLICIES
    }
    lru_ratio = results["lru"]["hit_ratio"]
    tinylfu_ratio = results["tinylfu"]["hit_ratio"]
    improvement = (
        round((tinylfu_ratio - lru_ratio) / lru_ratio * 100, 2) if lru_ratio > 0 else None
    )
    return {
        "config": {
            "cache_size": cache_size,
            "trace_length": trace_length,
            "num_items": num_items,
            "zipf_alpha": zipf_alpha,
            "seed": seed,
        },
        "results": results,
        "tinylfu_improvement_pct": improvement,
    }


def sweep_cache_sizes(
    cache_sizes: list[int], trace_length: int, num_items: int, zipf_alpha: float, seed: int | None = None
) -> list[dict]:
    """Reproduce the paper's 'hit ratio vs cache size' style curve."""
    trace = build_trace(trace_length, num_items, zipf_alpha, seed)
    sweep = []
    for size in cache_sizes:
        row = {"cache_size": size}
        for name in POLICIES:
            row[name] = run_simulation(name, size, trace).hit_ratio
        sweep.append(row)
    return sweep
