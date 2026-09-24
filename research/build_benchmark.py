#!/usr/bin/env python3
"""Merge all curated records and make the sentiment benchmark.

Input:  research/data/*.jsonl  (schema: research/SCHEMA.md)
Output: research/data/all_records.jsonl, all_records.csv,
        benchmark.json, benchmark.csv, tags.json

Score method (internet sentiment, not a lab test):
  weight of a record = confidence weight (high 1.0, medium 0.6, low 0.3)
                       x engagement weight (1 + log10(1 + engagement)), max 3
  value of a record  = good +1, mixed 0, bad -1
  raw   = sum(weight x value) / sum(weight)            -> range -1 to +1
  score = 50 + 50 x raw x n / (n + 3)                  -> range 0 to 100
The n / (n + 3) term moves sites with few reports toward 50 (neutral).
A site is in the benchmark only if it has 3 or more reports.
"""
import csv, glob, json, math, os, re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
GENERATED = {"all_records.jsonl"}
MIN_REPORTS = 3

ALIASES = {
    "american airlines": "aa.com", "americanair": "aa.com", "americanairlines.com": "aa.com",
    "delta": "delta.com", "united": "united.com", "southwest": "southwest.com",
    "cathay pacific": "cathaypacific.com", "opentable": "opentable.com", "amazon": "amazon.com",
    "walmart": "walmart.com", "target": "target.com", "best buy": "bestbuy.com", "bestbuy": "bestbuy.com",
    "ebay": "ebay.com", "stripe": "stripe.com", "link.com": "stripe.com", "stripe link": "stripe.com",
    "supabase": "supabase.com", "vercel": "vercel.com", "cloudflare": "cloudflare.com",
    "github": "github.com", "shopify": "shopify.com", "ticketmaster": "ticketmaster.com",
    "linkedin": "linkedin.com", "instacart": "instacart.com", "doordash": "doordash.com",
    "airbnb": "airbnb.com", "booking": "booking.com", "expedia": "expedia.com", "marriott": "marriott.com",
    "usps": "usps.com", "yelp": "yelp.com", "thumbtack": "thumbtack.com", "tripit": "tripit.com",
    "reddit": "reddit.com", "google": "google.com", "x": "x.com", "twitter": "x.com", "twitter.com": "x.com",
}


def norm_site(s):
    s = (s or "unknown").strip().lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s).split("/")[0]
    return ALIASES.get(s, s)


def load():
    seen, rows = set(), []
    for path in sorted(glob.glob(os.path.join(DATA, "*.jsonl"))):
        if os.path.basename(path) in GENERATED:
            continue
        for n, line in enumerate(open(path), 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                print(f"bad JSON: {os.path.basename(path)}:{n}")
                continue
            if not r.get("url") or not r.get("id") or r["id"] in seen:
                continue
            seen.add(r["id"])
            r["site"] = norm_site(r.get("site"))
            r["agent"] = {"grok": "grok-bot"}.get((r.get("agent") or "unknown").lower(), (r.get("agent") or "unknown").lower())
            r["sentiment"] = (r.get("sentiment") or "mixed").lower()
            r["friction"] = [t for t in (r.get("friction") or []) if t]
            r["enablers"] = [t for t in (r.get("enablers") or []) if t]
            r["_source_file"] = os.path.basename(path)
            rows.append(r)
    return rows


def weight(r):
    c = {"high": 1.0, "medium": 0.6, "low": 0.3}.get((r.get("confidence") or "medium").lower(), 0.6)
    try:
        e = max(0, float(r.get("engagement") or 0))
    except (TypeError, ValueError):
        e = 0
    return c * min(3.0, 1 + math.log10(1 + e))


def main():
    rows = load()
    with open(os.path.join(DATA, "all_records.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    cols = ["id", "platform", "url", "author", "created", "community", "engagement", "site", "site_category",
            "agent", "task", "sentiment", "friction", "enablers", "perspective", "confidence", "summary", "quote"]
    with open(os.path.join(DATA, "all_records.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow(["|".join(r[c]) if isinstance(r.get(c), list) else r.get(c, "") for c in cols])

    by_site = defaultdict(list)
    for r in rows:
        # opinion records say nothing about how the site treats an agent
        if r["site"] not in ("unknown", "", "n/a", "various", "multiple") and r.get("task") != "opinion-on-blocking":
            by_site[r["site"]].append(r)
    bench = []
    for site, rs in by_site.items():
        n = len(rs)
        if n < MIN_REPORTS:
            continue
        val = {"good": 1, "bad": -1}
        tw = sum(weight(r) for r in rs)
        raw = sum(weight(r) * val.get(r["sentiment"], 0) for r in rs) / tw if tw else 0
        sc = Counter(r["sentiment"] for r in rs)
        top = sorted(rs, key=lambda r: -weight(r))
        bench.append({
            "site": site,
            "category": Counter(r.get("site_category") or "other" for r in rs).most_common(1)[0][0],
            "reports": n, "good": sc["good"], "mixed": sc["mixed"], "bad": sc["bad"],
            "score": round(50 + 50 * raw * n / (n + 3)),
            "platforms": dict(Counter(r.get("platform") for r in rs)),
            "top_friction": [t for t, _ in Counter(t for r in rs for t in r["friction"]).most_common(4)],
            "top_enablers": [t for t, _ in Counter(t for r in rs for t in r["enablers"]).most_common(4)],
            "agents": [a for a, _ in Counter(r.get("agent") or "unknown" for r in rs).most_common(4)],
            "sources": [r["url"] for r in top[:5]],
        })
    bench.sort(key=lambda b: (-b["reports"], b["site"]))
    json.dump(bench, open(os.path.join(DATA, "benchmark.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(DATA, "benchmark.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["site", "category", "score", "reports", "good", "mixed", "bad", "top_friction", "top_enablers", "agents", "sources"])
        for b in bench:
            w.writerow([b["site"], b["category"], b["score"], b["reports"], b["good"], b["mixed"], b["bad"],
                        "|".join(b["top_friction"]), "|".join(b["top_enablers"]), "|".join(b["agents"]), " ".join(b["sources"])])

    def tagstats(field):
        out = {}
        for t, n in Counter(t for r in rows for t in r[field]).most_common():
            rs = [r for r in rows if t in r[field]]
            out[t] = {"records": n,
                      "sites": [s for s, _ in Counter(r["site"] for r in rs if r["site"] != "unknown").most_common(8)],
                      "examples": [r["url"] for r in sorted(rs, key=lambda r: -weight(r))[:5]]}
        return out
    json.dump({"friction": tagstats("friction"), "enablers": tagstats("enablers")},
              open(os.path.join(DATA, "tags.json"), "w"), indent=1, ensure_ascii=False)

    print(f"records {len(rows)} | by file {dict(Counter(r['_source_file'] for r in rows))}")
    print(f"sentiment {dict(Counter(r['sentiment'] for r in rows))}")
    print(f"sites with >= {MIN_REPORTS} reports: {len(bench)}")
    for b in bench[:40]:
        print(f"  {b['score']:3d}  {b['site']:<28} n={b['reports']:<3} g/m/b={b['good']}/{b['mixed']}/{b['bad']}  {','.join(b['top_friction'][:3])}")


if __name__ == "__main__":
    main()
