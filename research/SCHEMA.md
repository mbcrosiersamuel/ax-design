# AX research: record schema

Each research agent writes one JSONL file to `research/data/`. One line is one record.
One record is one first-hand report (or a strong second-hand report) of an AI agent that did a task on a website, app, or service.

## Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | `<platform>:<native id>`, for example `reddit:t3_abc123`, `reddit:t1_xyz`, `x:2101695125151977803` |
| `platform` | string | `reddit` or `x` or `web` |
| `url` | string | Permanent link to the post or comment. Mandatory. |
| `author` | string | Username or handle |
| `created` | string | ISO date (`YYYY-MM-DD`) |
| `community` | string | Subreddit, or empty for X |
| `engagement` | number | Reddit score, or X likes |
| `quote` | string | Exact words from the source, 40 words maximum. Do not paraphrase in this field. |
| `summary` | string | One sentence: what the agent tried to do and what occurred |
| `site` | string | The website or service that the agent used, as a bare domain if known (`aa.com`, `stripe.com`). `unknown` if not named. |
| `site_category` | string | `airline`, `travel`, `retail`, `grocery`, `payments`, `bank`, `government`, `health`, `saas`, `devtool`, `social`, `food-delivery`, `ticketing`, `other` |
| `agent` | string | The agent product: `chatgpt-agent`, `operator`, `claude-in-chrome`, `claude-code`, `claude-cowork`, `comet`, `atlas`, `codex`, `cursor`, `manus`, `browser-use`, `openclaw`, `custom`, `unknown`, ... |
| `task` | string | Short task name: `book-flight`, `checkout`, `sign-up`, `log-in`, `read-docs`, `create-api-key`, `fill-form`, `scrape`, ... |
| `sentiment` | string | `good`, `bad`, or `mixed` (the experience of the agent on the site) |
| `friction` | array of strings | Zero or more tags from the list below. Empty for a good experience with no friction. |
| `enablers` | array of strings | Zero or more tags from the list below. What made it work. |
| `perspective` | string | `agent-user` (person whose agent did the task), `site-owner` (person who operates the site), `agent-builder`, `observer` |
| `confidence` | string | `high` (first-hand, names the site), `medium`, `low` |

## Friction tags (add a new tag only if none of these apply, and put `new:` before it)

`bot-block` (WAF, Cloudflare, Akamai, 403, "unusual traffic"), `captcha`, `auth-magic-link`, `auth-email-otp`, `auth-sms-otp`, `auth-2fa-app`, `auth-passkey`, `auth-sso-only`, `login-wall`, `session-expiry`, `payment-3ds`, `payment-card-entry`, `payment-declined`, `no-api`, `dashboard-only` (action is possible only in a web UI), `api-key-manual`, `dynamic-ui` (canvas, shadow DOM, custom widgets, date pickers), `popups-modals`, `cookie-banner`, `slow-or-timeout`, `rate-limit`, `tos-prohibits-agents`, `account-ban`, `docs-not-machine-readable`, `docs-stale`, `error-messages-unclear`, `human-verification` (ID, phone call), `app-only` (no web flow), `pricing-hidden`, `agent-refuses` (the agent's own safety rule stops the task), `hallucinated-success`

## Enabler tags

`mcp-server`, `public-api`, `cli`, `llms-txt`, `markdown-docs`, `agent-payments` (Stripe Link, agentic commerce protocol, virtual cards), `oauth-device-flow`, `api-key-self-serve`, `simple-html`, `guest-checkout`, `clear-errors`, `agent-allowed-policy`, `skill-or-plugin`, `sandbox-mode`, `webhooks`

## Rules

1. Include a record only if the source URL is real and you fetched it. Do not invent records.
2. Keep records about real agent-on-website experience. Remove general AI opinions, model benchmarks, and product announcements with no experience report.
3. Reports from a site owner about agent or bot traffic are in scope (`perspective: site-owner`).
4. Remove duplicates by `id`.
5. Time window: 2025-01-01 to today (2026-09-20).
