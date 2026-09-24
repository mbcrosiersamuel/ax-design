#!/usr/bin/env python3
"""Make src/data/wall.json (the quote wall) from research/data/all_records.jsonl.

Selection: consumer (B2C) sites only, site is named, confidence is not low.
Run research/build_benchmark.py first.
"""
import json, os, re, time, urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "data", "all_records.jsonl")
OUT = os.path.join(HERE, "..", "src", "data", "wall.json")

B2B_CATEGORIES = {"devtool", "saas"}
# Infrastructure, protocols, and agent vendors are not consumer destinations.
EXCLUDE_SITES = {"cloudflare.com", "x402.org", "shopify.dev", "agenticcommerce.dev", "muse.ai", "manus.im",
                 "openrouter.ai", "visa.com", "mastercard.com"}
MIN_SITE_RECORDS = 1

AGENTS = {
    "muse": "Muse (Meta)", "instinct": "Instinct", "grok-bot": "Grok Bot", "chatgpt-agent": "ChatGPT Agent",
    "operator": "Operator (OpenAI)", "chatgpt": "ChatGPT", "chatgpt-instant-checkout": "ChatGPT",
    "comet": "Comet (Perplexity)", "perplexity": "Comet (Perplexity)", "atlas": "ChatGPT Atlas",
    "claude-in-chrome": "Claude in Chrome", "claude-cowork": "Claude Cowork", "claude": "Claude",
    "claude-code": "Claude Code", "openclaw": "OpenClaw", "alexa-plus": "Alexa+", "gemini": "Gemini",
    "manus": "Manus", "custom": "Custom agent", "codex": "Codex", "cursor": "Cursor",
}

TAG_LABELS = {
    "bot-block": "Bot block", "captcha": "CAPTCHA", "login-wall": "Login wall", "dynamic-ui": "UI made only for people",
    "slow-or-timeout": "Slow or timeout", "agent-refuses": "Agent refuses the task", "account-ban": "Account ban",
    "hallucinated-success": "False success report", "session-expiry": "Session expiry", "rate-limit": "Rate limit",
    "error-messages-unclear": "Unclear error", "no-api": "No API", "tos-prohibits-agents": "Terms prohibit agents",
    "auth-sms-otp": "SMS code", "auth-email-otp": "Email code", "auth-2fa-app": "2FA app", "auth-magic-link": "Magic link",
    "auth-otp-unspecified": "Verification code", "auth-verification-code": "Verification code",
    "payment-declined": "Payment declined", "payment-card-entry": "Card entry", "payment-3ds": "3-D Secure",
    "human-verification": "Human verification", "popups-modals": "Popups", "pricing-hidden": "Hidden price",
    "app-only": "App only", "no-merchant-opt-out": "No merchant opt-out",
    "agent-traffic-attribution-unclear": "Lost attribution", "product-detail-lost-in-agent-channel": "Product detail lost",
    "low-conversion-in-agent-channel": "Low conversion", "low-in-chat-conversion": "Low conversion",
    "channel-fees": "Channel fees", "higher-support-load": "More support load", "currency-unsupported": "Currency not supported",
    "new-device-security-alert": "Security alert on agent login", "phone-only": "Phone only",
    "agent-payments": "Agent payments (Stripe Link)", "mcp-server": "MCP server", "public-api": "Public API", "cli": "CLI",
    "skill-or-plugin": "Connector or skill", "agent-allowed-policy": "Policy permits agents",
    "user-browser-session": "Runs in the user's browser", "local-browser": "Runs in the user's browser",
    "human-handoff": "Human handoff", "human-handoff-login": "Human handoff", "guest-checkout": "Guest checkout",
    "webmcp": "WebMCP", "llms-txt": "llms.txt", "markdown-docs": "Markdown docs", "simple-html": "Simple HTML",
    "login-link-to-user-email": "Login link by email", "email-link-account-connect": "Login link by email",
    "voice-call": "Voice call", "clear-errors": "Clear errors",
}


def tag(t):
    t = t.replace("new:", "")
    return TAG_LABELS.get(t, t.replace("-", " ").capitalize())


def agents(a):
    out = []
    for part in (a or "unknown").split("+"):
        label = AGENTS.get(part.strip())
        if label and label not in out:
            out.append(label)
    return out


def reddit_embed_path(url):
    m = re.match(r"https://www\.reddit\.com(/r/[^/]+/comments/[^/]+/[^/]*/?)([a-z0-9]+)?/?$", url)
    return url if m else None


rows = [json.loads(l) for l in open(SRC)]
keep = []
for r in rows:
    if r["site"] in ("unknown", "") or "." not in r["site"] or r["site"] in EXCLUDE_SITES:
        continue
    if (r.get("site_category") or "other") in B2B_CATEGORIES:
        continue
    if (r.get("confidence") or "").lower() == "low" or r.get("task") == "opinion-on-blocking":
        continue
    keep.append(r)

site_n = Counter(r["site"] for r in keep)
items = []
for r in keep:
    if site_n[r["site"]] < MIN_SITE_RECORDS:
        continue
    pid = r["id"].split(":", 1)[1].split("#")[0]
    items.append({
        "id": r["id"], "platform": r["platform"], "url": r["url"], "postId": pid if r["platform"] == "x" else None,
        "author": r.get("author") or "", "community": r.get("community") or "", "created": r.get("created") or "",
        "engagement": int(float(r.get("engagement") or 0)), "sites": [r["site"]], "agents": agents(r.get("agent")),
        "outcome": {"good": "worked", "bad": "stuck"}.get(r["sentiment"], "mixed"),
        "siteOutcomes": {r["site"]: {"good": "worked", "bad": "stuck"}.get(r["sentiment"], "mixed")},
        "antiPatterns": sorted({tag(t) for t in r["friction"]}), "patterns": sorted({tag(t) for t in r["enablers"]}),
        "quote": r["quote"], "summary": r.get("summary") or "",
    })

# One embed for each post: a post that names several sites gives several records.
merged = {}
for i in items:
    m = merged.get(i["url"])
    if not m:
        merged[i["url"]] = i
        continue
    for k in ("sites", "agents", "antiPatterns", "patterns"):
        m[k] = sorted(set(m[k]) | set(i[k]))
    m["siteOutcomes"].update(i["siteOutcomes"])
    if m["outcome"] != i["outcome"]:
        m["outcome"] = "mixed"
    if len(i["quote"]) > len(m["quote"]):
        m["quote"] = i["quote"]
items = list(merged.values())
items.sort(key=lambda i: (-i["engagement"], i["id"]))

# X posts can vanish (deleted post or account). The embed widget never resolves for these,
# so mark them here and the page keeps the quote instead. Results are cached by post id.
CACHE = os.path.join(HERE, "raw", "x", "availability.json")
avail = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
for i in items:
    if i["platform"] != "x":
        continue
    pid = i["postId"]
    if pid not in avail:
        try:
            req = urllib.request.Request(f"https://cdn.syndication.twimg.com/tweet-result?id={pid}&token=a", headers={"User-Agent": "Mozilla/5.0"})
            body = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
            avail[pid] = bool(body) and json.loads(body).get("__typename") != "TweetTombstone"
        except Exception:
            avail[pid] = True  # unknown: let the page try
        time.sleep(0.4)
    if not avail[pid]:
        i["unavailable"] = True
json.dump(avail, open(CACHE, "w"), indent=0)
print("unavailable x posts:", sum(1 for i in items if i.get("unavailable")))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(items, open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(items), "items |", Counter(i["platform"] for i in items), "|", Counter(i["outcome"] for i in items))
print("sites", len({x for i in items for x in i["sites"]}), Counter(x for i in items for x in i["sites"]).most_common(14))
print("agents", Counter(a for i in items for a in i["agents"]).most_common())
print("anti", Counter(t for i in items for t in i["antiPatterns"]).most_common(16))
print("patterns", Counter(t for i in items for t in i["patterns"]).most_common(12))
