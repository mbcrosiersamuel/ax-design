#!/usr/bin/env python3
"""X API v2 collector with a hard cost limit.

Usage:
  x_collect.py counts "<query>"                 # $0.005 per request
  x_collect.py search "<query>" [--max N] [--all] [--sort recency|relevancy] [--name slug]
  x_collect.py ledger

Pricing (docs.x.com, 2026-09-20): $0.005 per post returned. No user expansions are
requested because a user read costs $0.010.
Credentials are read from ~/.config/ax-research/x_credentials.env and are never printed.
"""
import base64, hashlib, hmac, json, os, re, secrets, sys, time, urllib.parse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "..", "raw", "x", "ledger.json")
CRED_FILE = os.path.expanduser("~/.config/ax-research/x_credentials.env")
BUDGET_USD = float(os.environ.get("X_BUDGET_USD", "8"))
POST_COST = 0.005
COUNT_COST = 0.005
FIELDS = "created_at,public_metrics,conversation_id,author_id,in_reply_to_user_id,referenced_tweets,lang,note_tweet,entities"


def ledger():
    if os.path.exists(LEDGER):
        return json.load(open(LEDGER))
    return {"spent_usd": 0.0, "posts": 0, "count_requests": 0, "calls": []}


def save_ledger(l):
    json.dump(l, open(LEDGER, "w"), indent=1)


def creds():
    c = {}
    for line in open(CRED_FILE):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            c[k.strip()] = v.strip().strip('"').strip("'")
    return c


def pct(x):
    return urllib.parse.quote(str(x), safe="-._~")


def auth_header(base_url, params):
    c = creds()
    if c.get("X_BEARER_TOKEN"):
        return "Bearer " + c["X_BEARER_TOKEN"]
    need = ["X_API_KEY", "X_API_KEY_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]
    missing = [k for k in need if not c.get(k)]
    if missing:
        raise SystemExit("credentials missing: " + ", ".join(missing))
    o = {"oauth_consumer_key": c["X_API_KEY"], "oauth_nonce": secrets.token_hex(16),
         "oauth_signature_method": "HMAC-SHA1", "oauth_timestamp": str(int(time.time())),
         "oauth_token": c["X_ACCESS_TOKEN"], "oauth_version": "1.0"}
    allp = sorted((pct(k), pct(v)) for k, v in {**params, **o}.items())
    base = "&".join(["GET", pct(base_url), pct("&".join(f"{k}={v}" for k, v in allp))])
    key = pct(c["X_API_KEY_SECRET"]) + "&" + pct(c["X_ACCESS_TOKEN_SECRET"])
    o["oauth_signature"] = base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()
    return "OAuth " + ", ".join(f'{pct(k)}="{pct(v)}"' for k, v in sorted(o.items()))


def get(path, params):
    base_url = "https://api.x.com/2/" + path
    url = base_url + "?" + "&".join(f"{pct(k)}={pct(v)}" for k, v in params.items())
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"Authorization": auth_header(base_url, params), "User-Agent": "ax-research/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")[:500]
            if e.code == 429:
                reset = int(e.headers.get("x-rate-limit-reset", time.time() + 60))
                wait = max(5, min(reset - int(time.time()) + 2, 900))
                print(f"429, wait {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            if e.code >= 500:
                time.sleep(5 * (attempt + 1))
                continue
            raise SystemExit(f"HTTP {e.code}: {body}")
    raise SystemExit("too many retries")


def slug(q):
    return re.sub(r"[^a-z0-9]+", "_", q.lower()).strip("_")[:60]


def cmd_counts(q):
    l = ledger()
    if l["spent_usd"] + COUNT_COST > BUDGET_USD:
        raise SystemExit("budget limit")
    d = get("tweets/counts/recent", {"query": q, "granularity": "day"})
    l["spent_usd"] = round(l["spent_usd"] + COUNT_COST, 4)
    l["count_requests"] += 1
    l["calls"].append({"type": "counts", "q": q, "total": d.get("meta", {}).get("total_tweet_count")})
    save_ledger(l)
    print(d.get("meta", {}).get("total_tweet_count"), "posts in 7 days |", q)


def cmd_search(q, maxn, use_all, sort, name):
    l = ledger()
    out = os.path.join(HERE, "..", "raw", "x", (name or slug(q)) + ".jsonl")
    seen = set()
    if os.path.exists(out):
        for line in open(out):
            seen.add(json.loads(line)["id"])
    got, token = 0, None
    path = "tweets/search/all" if use_all else "tweets/search/recent"
    while got < maxn:
        page = max(10, min(100, maxn - got))
        if l["spent_usd"] + page * POST_COST > BUDGET_USD:
            print("STOP: budget limit would be exceeded", file=sys.stderr)
            break
        p = {"query": q, "max_results": page, "tweet.fields": FIELDS, "sort_order": sort}
        if use_all:
            p["start_time"] = "2025-01-01T00:00:00Z"
        if token:
            p["next_token"] = token
        d = get(path, p)
        data = d.get("data", [])
        l["spent_usd"] = round(l["spent_usd"] + len(data) * POST_COST, 4)
        l["posts"] += len(data)
        l["calls"].append({"type": "search", "q": q, "n": len(data), "all": use_all})
        save_ledger(l)
        with open(out, "a") as f:
            for t in data:
                if t["id"] not in seen:
                    seen.add(t["id"])
                    t["_query"] = q
                    f.write(json.dumps(t) + "\n")
        got += len(data)
        token = d.get("meta", {}).get("next_token")
        if not token or not data:
            break
        time.sleep(1.2)
    print(f"{got} posts -> {out} | spent ${l['spent_usd']:.3f} of ${BUDGET_USD}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "ledger":
        l = ledger()
        print(f"spent ${l['spent_usd']:.3f} | posts {l['posts']} | count requests {l['count_requests']}")
    elif a[0] == "counts":
        cmd_counts(a[1])
    elif a[0] == "search":
        q = a[1]
        maxn = int(a[a.index("--max") + 1]) if "--max" in a else 100
        sort = a[a.index("--sort") + 1] if "--sort" in a else "relevancy"
        name = a[a.index("--name") + 1] if "--name" in a else None
        cmd_search(q, maxn, "--all" in a, sort, name)
