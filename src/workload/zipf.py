"""Synthetic Zipf-distributed access trace generator.

The TinyLFU paper's central claim is that admission policies help most
under *skewed* access distributions. Zipf distributions are the standard
stand-in for real-world web/cache traffic (a small number of items get
most of the requests — think trending articles, hot product pages, etc).
"""
from __future__ import annotations

import numpy as np


def generate_zipf_trace(
    length: int,
    num_items: int,
    alpha: float = 1.0,
    seed: int | None = None,
) -> list[str]:
    """Generate a trace of `length` key accesses over `num_items` distinct
    keys, drawn from a Zipf distribution with skew parameter `alpha`.

    Higher alpha = more skewed (more concentrated on a few "hot" keys).
    alpha close to 0 approaches a uniform distribution.
    """
    rng = np.random.default_rng(seed)

    # Rank-based Zipf weights over a fixed universe of `num_items` keys.
    ranks = np.arange(1, num_items + 1)
    weights = 1.0 / np.power(ranks, alpha)
    weights /= weights.sum()

    indices = rng.choice(num_items, size=length, p=weights)
    return [f"item-{i}" for i in indices]
