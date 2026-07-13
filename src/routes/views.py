"""Flask API around the cache simulator.

Endpoints:
  GET  /health
  POST /simulate         -> run one policy on a generated trace
  POST /compare          -> run all policies on the SAME trace
  POST /sweep            -> hit ratio vs cache size (reproduces the paper's curves)
"""

from src.routes import routes
from flask import jsonify, request

from src.simulate import (
    build_trace,
    compare_policies,
    run_simulation,
    sweep_cache_sizes,
    POLICIES
)

# homepage route
@routes.route("/")
def homepage():
    return "Home Page is OK"


# health-check route
@routes.route("/health")
def health():
    return jsonify(status='ok')


# simulation runner route
@routes.route("/simulate", methods=['POST'])
def simulate():
    body = request.get_json(force=True) or {}
    policy = body.get("policy", "lru")
    cache_size = int(body.get("cache_size", 100))
    trace_length = int(body.get("trace_length", 20000))
    num_items = int(body.get("num_items", 1000))
    zipf_alpha = float(body.get("zipf_alpha", 1.0))
    seed = body.get("seed")


    if policy not in POLICIES:
        return jsonify(error = f"unknown policy '{policy}', choose from {list(POLICIES)}"), 400

    trace = build_trace(
        trace_length=trace_length,
        num_items=num_items,
        zipf_alpha=zipf_alpha,
        seed=seed
    )

    result = run_simulation(
        policy=policy,
        cache_size=cache_size,
        trace=trace
    )

    return jsonify(result.to_dict())


# compare route
@routes.route("/compare", methods=['POST'])
def compare():
    body = request.get_json(force=True) or {}
    cache_size = int(body.get("cache_size", 100))
    trace_length = int(body.get("trace_length", 20000))
    num_items = int(body.get("num_items", 1000))
    zipf_alpha = float(body.get("zipf_alpha", 1.0))
    seed = body.get("seed")


    return jsonify(
        compare_policies(
            cache_size,
            trace_length,
            num_items,
            zipf_alpha,
            seed
        )
    )


# sweep route
@routes.route("/sweep", methods=['POST'])
def sweep():
    body = request.get_json(force=True) or {}
    cache_sizes = body.get("cache_sizes", [10, 25, 50, 100, 200, 400])
    trace_length = int(body.get("trace_length", 20000))
    num_items = int(body.get("num_items", 1000))
    zipf_alpha = float(body.get("zipf_alpha", 1.0))
    seed = body.get("seed")


    data = sweep_cache_sizes(
        cache_sizes,
        trace_length,
        num_items,
        zipf_alpha,
        seed
    )

    return jsonify(config=dict(trace_length=trace_length, num_items=num_items, zipf_alpha=zipf_alpha), sweep=data)