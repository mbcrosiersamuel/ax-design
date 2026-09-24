#!/usr/bin/env python3
"""Run the X collection: counts first, then the searches that are worth the credit.

Usage:  python3 research/x/run_x.py [--dry] [--budget 8] [--seed <post id> ...]

1. For each query in queries.tsv, one "counts" request ($0.005) shows how many posts
   matched in the last 7 days.
2. Seed threads (conversation_id:<id>) are fetched in full, newest first.
3. Keyword queries are fetched with sort=relevancy, capped at MAX_PER_QUERY posts each,
   until the budget is used. Queries with a very large count are noise (a word like
   "muse" or "instinct" in ordinary use); they get the cap, not the full count.
4. Raw posts land in research/raw/x/<name>.jsonl. Classification is a separate step
   (see README.md).
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
COLLECT = os.path.join(HERE, "x_collect.py")
MAX_PER_QUERY = 100
SEED_MAX = 200

args = sys.argv[1:]
dry = "--dry" in args
budget = args[args.index("--budget") + 1] if "--budget" in args else None
seeds = [args[i + 1] for i, a in enumerate(args) if a == "--seed"]

queries = []
for line in open(os.path.join(HERE, "queries.tsv")):
    if line.startswith("#") or not line.strip():
        continue
    name, q = line.rstrip("\n").split("\t", 1)
    if q.startswith("conversation_id:") and not seeds:
        continue  # old seed threads; pass --seed for new ones
    queries.append((name, q))
for s in seeds:
    queries.insert(0, (f"seed_{s}", f"conversation_id:{s}"))

env = dict(os.environ)
if budget:
    env["X_BUDGET_USD"] = budget


def run(*a):
    cmd = [sys.executable, COLLECT, *a]
    print("$", " ".join(cmd[2:])[:120])
    if not dry:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        print((r.stdout + r.stderr).strip()[-160:])


for name, q in queries:
    run("counts", q)
for name, q in queries:
    is_seed = q.startswith("conversation_id:")
    run("search", q, "--max", str(SEED_MAX if is_seed else MAX_PER_QUERY), "--sort", "recency" if is_seed else "relevancy", "--name", name)
run("ledger")
