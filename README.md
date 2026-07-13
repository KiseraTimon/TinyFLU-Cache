# TinyLFU Cache Lab

A from-scratch Python/Flask replication of the core claim in:

> Gil Einziger, Roy Friedman, and Ben Manes. **"TinyLFU: A Highly Efficient
> Cache Admission Policy."** ACM Transactions on Storage, 2017 (originally
> PDP 2014). [arXiv:1512.00727](https://arxiv.org/abs/1512.00727)

**The paper's claim:** adding a cheap, frequency-based
*admission* policy on top of a normal eviction policy (like LRU) meaningfully
improves cache hit ratios under skewed access distributions — especially
when the cache is small relative to the working set.

This project builds a plain LRU cache and an LRU+TinyLFU cache from
scratch, runs both against synthetic Zipfian-distributed traffic (a standard
stand-in for real, skewed web/cache access patterns), and exposes the
simulator as a Flask API so you can reproduce and explore the paper's
hit-ratio results yourself.

## Replication results

A sample run (`cache_size=100`, `trace_length=50000`,
`num_items=5000`, `zipf_alpha=1.1`) gives:

| Policy   | Hit ratio | Rejections |
|----------|-----------|------------|
| LRU      | 0.559     | —          |
| TinyLFU  | 0.653     | 15,885     |

**~17% relative improvement in hit ratio**, consistent with the paper's
finding that admission filtering helps most under skewed traffic. Sweeping
across cache sizes also reproduces the paper's qualitative shape: TinyLFU's
advantage is largest for small caches and shrinks as the cache grows toward
the size of the working set.

This is an educational, from-scratch reimplementation — not the paper's
original C++/Java benchmarking code, and it uses synthetic Zipfian traces
rather than the paper's real YouTube/Wikipedia traces. Treat the numbers as
"same qualitative shape," not "identical figures."

## How TinyLFU works

1. **Doorkeeper** — a Bloom filter that cheaply tracks "have I seen this key
   before?" An item must be seen twice before it's worth tracking precisely.
2. **Count-Min Sketch** — a compact, approximate frequency counter for items
   that passed the doorkeeper. Counters are capped (behaving like 4-bit
   counters, as in the paper) and periodically halved ("aging") so the
   sketch reflects *recent* frequency, not all-time frequency.
3. **Admission decision** — on a cache miss with a full cache, TinyLFU
   compares the estimated frequency of the new item against the item LRU
   would evict. The new item is only admitted if it's estimated to be
   accessed more often than the eviction victim.

## Project structure

```
tinylfu-cache/
├── pyproject.toml              # uv-managed dependencies
├── main.py                     # application entrypoint (runs Flask API)
├── .env.example                # environment variables example
├── README.md
├── src/
│   ├── __init__.py             # flask app factory
│   ├── simulate.py             # simulation runner / metrics
│   ├── routes/
│   │   └── views.py            # aflask pi routes
│   ├── cache/
│   │   ├── bloom.py            # Bloom filter (doorkeeper)
│   │   ├── count_min_sketch.py # approximate frequency counter
│   │   ├── tinylfu.py          # doorkeeper + sketch -> admission filter
│   │   ├── lru_cache.py        # baseline LRU cache
│   │   └── tinylfu_cache.py    # LRU eviction + TinyLFU admission
│   └── workload/
│       └── zipf.py             # synthetic Zipf trace generator
├── tests/                      # pytest suite (11 tests)
├── config/                     # configuration files
└── utilities/                  # utility scripts
```

## Setup (uv)

```bash
uv sync                 # installs Flask, numpy, pytest into .venv
uv run pytest -v        # run the test suite
```

## Running the API

```bash
uv run flask --app main:application run
```

### `GET /health`
Sanity check.

### `POST /simulate`
Run a single policy against a generated trace.

```bash
curl -X POST http://127.0.0.1:5000/simulate \
  -H "Content-Type: application/json" \
  -d '{"policy": "tinylfu", "cache_size": 100, "trace_length": 50000, "num_items": 5000, "zipf_alpha": 1.1, "seed": 42}'
```

### `POST /compare`
Run **all** policies on the *same* generated trace, for a fair head-to-head.

```bash
curl -X POST http://127.0.0.1:5000/compare \
  -H "Content-Type: application/json" \
  -d '{"cache_size": 100, "trace_length": 50000, "num_items": 5000, "zipf_alpha": 1.1, "seed": 42}'
```

Returns hit ratios for both policies plus `tinylfu_improvement_pct`.

### `POST /sweep`
Reproduce the paper's "hit ratio vs. cache size" style curves.

```bash
curl -X POST http://127.0.0.1:5000/sweep \
  -H "Content-Type: application/json" \
  -d '{"cache_sizes": [20,50,100,200,400], "trace_length": 30000, "num_items": 3000, "zipf_alpha": 1.0, "seed": 1}'
```

### Request parameters (all endpoints)

| Field          | Meaning                                                        | Default |
|----------------|-----------------------------------------------------------------|---------|
| `cache_size`   | number of items the cache can hold                              | 100     |
| `trace_length` | number of accesses in the synthetic trace                       | 20000   |
| `num_items`    | size of the universe of distinct keys                            | 1000    |
| `zipf_alpha`   | skew of the Zipf distribution (higher = more skewed/"hotter")    | 1.0     |
| `seed`         | RNG seed, for reproducible traces                                | none    |

## Why this is a fair replication target

- It's an algorithms/systems paper: no GPUs, no massive datasets — just
  data structures and simulation logic, well suited to a Flask/Python stack.
- The paper's central claim is a single measurable quantity (hit ratio)
  under a controllable variable (workload skew, cache size), which maps
  cleanly onto an experiment you can actually run and check.
- TinyLFU isn't just academic — it's the real admission policy behind
  [Caffeine](https://github.com/ben-manes/caffeine), a widely used Java
  caching library (one of this paper's co-authors, Ben Manes, maintains it).

## Known simplifications vs. the original paper

- Counters are implemented as capped Python ints rather than true packed
  4-bit values — functionally equivalent, not bit-identical in memory layout.
- The doorkeeper/sketch promotion logic is a simplified version of the
  paper's exact reset/aging schedule.
- Workload is synthetic Zipf traffic, not the paper's real traces.

These simplifications preserve the paper's *qualitative* result (TinyLFU
improves hit ratio under skew, with diminishing benefit as cache size
grows) while keeping the implementation approachable.

## License

MIT — see `LICENSE`
