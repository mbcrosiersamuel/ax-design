# Agent experience on the internet: research report

Date: 2026-09-20. Sources: Reddit (archive APIs) and X (API v2). Owner: agentexperience.design.

## 1. Summary

- The dataset has **824 sourced records**: 565 from Reddit and 259 from X. Each record has a permanent URL and an exact quote.
- Sentiment: 401 bad, 244 good, 179 mixed. Viewpoint: 546 agent users, 149 site owners, 68 agent builders, 61 observers.
- The records name 172 sites. **36 sites have three or more reports** and are in the first benchmark.
- **The primary pattern:** sites that give agents a structured path (MCP server, CLI, API) get good sentiment. Consumer sites with bot protection get bad sentiment. Stripe has a score of 62. Delta has 26. Walmart has 17.
- **The number one friction is the bot block** (207 records). CAPTCHA is second (69). Login walls are third (48). Payment friction is rare, because the agent usually stops before payment.
- **A block on the browser path is not the full story.** OpenTable blocks browser agents, but its Muse connector "works great". This is the best example for the site: close the scrape path and open an agent path.
- **Site owners have real causes to block:** bandwidth cost, false bot identities, lost advertisement income, and lost customer relationship. The site must show this viewpoint also.
- **Agents will not find the site and contribute by themselves.** They contribute when a person or a vendor connects them first (MCP tool, skill, API). See section 7.

## 2. Method and data

| Track | Source | Records | Sub-agent output |
|---|---|---|---|
| Consumer agents on consumer sites | Reddit | 183 | `data/reddit_consumer.jsonl` |
| Coding and work agents on SaaS and developer tools | Reddit | 193 | `data/reddit_developer.jsonl` |
| Agent-forward companies and site owners | Reddit | 204 | `data/reddit_agent_forward.jsonl` |
| Seed threads, Muse, Instinct, Grok Bot | X | 194 | `data/x_consumer.jsonl` |
| CAPTCHA, login, site owners, WebMCP, agentic checkout | X | 72 | `data/x_dev_owner.jsonl` |

The totals are larger than 824 because the merge removes records with the same id.

- **Schema:** `SCHEMA.md`. Each record has the site, agent, task, sentiment, friction tags, enabler tags, viewpoint, and confidence.
- **Merged files:** `data/all_records.jsonl`, `data/all_records.csv`, `data/benchmark.json`, `data/benchmark.csv`, `data/tags.json`. To build them again: `python3 research/build_benchmark.py`.
- **Classification:** a model read each candidate post. Keyword filters only found candidates. Approximately 75% to 90% of the X posts were noise and were removed.
- **Quality check:** all 259 X quotes are exact text from the raw posts. A random sample of 12 Reddit records was checked against the archive: 12 of 12 quotes and permalinks were correct.
- **X cost:** $7.41 of the $8.00 limit, for 1,360 unique posts. The ledger is in `raw/x/ledger.json`.
- **Reference data:** `raw/webmcp_directory.json` has the 822 sites of the WebMCP directory.

### Limits of the data

1. **X covers only seven days** (2026-09-14 to 2026-09-21). The X search endpoint does not go back more. Muse (Meta, released 2026-09-08), Instinct, and Grok Bot dominate the X data for this reason.
2. **Reddit access was by archive only.** Reddit returned HTTP 403 to this computer. PullPush stopped the sub-agents with HTTP 429 and the text "This website does not provide free scraping resources for agents". The sub-agents obeyed and used only Arctic Shift after that. Arctic Shift has no relevance ranking and had timeouts on large subreddits.
3. **231 records do not name a site.** They count for the friction patterns but not for the benchmark.
4. **Short replies have medium confidence.** A reply such as "@united" to the question "where do agents struggle?" shows that the person named the site. It does not confirm the failure mode.
5. **Weak coverage:** Instacart, Etsy, Booking.com, Expedia, Cathay Pacific (2 records), American Airlines, Resy, Costco, Clerk, Auth0, Resend, Twilio, Neon, Netlify, and the named WebMCP brands.
6. **Few first-hand reports** about magic links, passkeys, SSO-only login, and device-code flow. The data does not show that these are not problems. It shows that people do not write about them, or that agents stop before that step.
7. **Vendor promotion:** some posts come from vendors that sell a solution. Pure promotion was removed. Records with a first-hand test remain, with medium or low confidence.

## 3. Benchmark: internet sentiment for each site

**This is a sentiment score, not a lab test.** It shows what people report, with more weight for high-confidence and high-engagement reports.

- Record weight = confidence (high 1.0, medium 0.6, low 0.3) × engagement (1 + log10(1 + likes or score), maximum 3).
- Score = 50 + 50 × (weighted good minus bad) × n / (n + 3). The range is 0 to 100, and 50 is neutral.
- The n / (n + 3) term moves sites with few reports toward 50.
- Opinion records ("please block this person") do not count for a site.

| Score | Site | Reports | Good / mixed / bad | Primary friction | Primary enablers |
|---|---|---|---|---|---|
| 79 | linear.app | 4 | 4 / 0 / 0 | none | MCP server, API, webhooks |
| 71 | shopify.dev (developer tools) | 9 | 5 / 3 / 1 | stale docs | MCP server, API, Markdown docs |
| 62 | stripe.com | 22 | 10 / 5 / 7 | unclear errors, no agent spend limits | MCP server, CLI, Link payments |
| 61 | target.com | 3 | 1 / 2 / 0 | bot block, CAPTCHA | human handoff |
| 61 | webflow.com | 3 | 1 / 2 / 0 | slow, MCP scope too small | MCP server |
| 60 | n8n.io | 18 | 8 / 5 / 5 | unclear errors, MCP token bloat | MCP server, API |
| 59 | github.com | 17 | 6 / 9 / 2 | MCP token bloat | CLI (`gh`), MCP server |
| 59 | vercel.com | 10 | 6 / 1 / 3 | manual API key, MCP wrong data | MCP server, CLI |
| 58 | atlassian.com | 7 | 2 / 5 / 0 | MCP token bloat, session expiry | MCP server |
| 54 | aws.amazon.com | 7 | 4 / 0 / 3 | destructive-action risk, coarse permissions | CLI |
| 50 | ubereats.com | 4 | 2 / 0 / 2 | CAPTCHA, verification code | login link to the user's email |
| 50 | x402.org | 3 | 0 / 3 / 0 | no spend limits, unreliable paid endpoints | agent payments |
| 49 | shopify.com (merchant side) | 74 | 23 / 26 / 25 | no merchant opt-out, unclear attribution | agent payments, MCP server |
| 47 | supabase.com | 38 | 13 / 10 / 15 | destructive-action risk, unclear errors | MCP server, CLI, Markdown docs |
| 46 | opentable.com | 7 | 4 / 0 / 3 | bot block on the website | Muse connector, skill |
| 45 | notion.so | 3 | 0 / 2 / 1 | OAuth browser flow, MCP coverage | MCP server |
| 42 | amazon.com | 50 | 14 / 7 / 29 | bot block, unclear error page | user's own browser session |
| 40 | cloudflare.com | 56 | 16 / 13 / 27 | bot block, unclear errors | Markdown docs, MCP server |
| 40 | facebook.com | 4 | 1 / 2 / 1 | account ban, terms of service | user's own browser session |
| 39 | gmail.com | 4 | 1 / 1 / 2 | account ban, human verification | CLI |
| 37 | linkedin.com | 13 | 4 / 1 / 8 | bot block, account ban | user's own browser session |
| 37 | ebay.com | 6 | 1 / 2 / 3 | bot block, session expiry | none |
| 37 | bestbuy.com | 3 | 1 / 0 / 2 | bot block (HTTP 503) | none |
| 33 | xfinity.com | 4 | 0 / 1 / 3 | bot block, also after human takeover | none |
| 32 | canva.com | 3 | 0 / 1 / 2 | bot block, CAPTCHA | none |
| 31 | appstoreconnect.apple.com | 8 | 2 / 1 / 5 | dashboard-only, manual API key | API |
| 28 | uber.com | 4 | 0 / 1 / 3 | session expiry, login wall | none |
| 26 | delta.com | 10 | 3 / 0 / 7 | bot block, CAPTCHA | local browser |
| 25 | united.com | 3 | 0 / 0 / 3 | bot block | none |
| 25 | accounts.google.com | 3 | 0 / 0 / 3 | login wall, OAuth browser flow | none |
| 24 | x.com | 7 | 0 / 1 / 6 | bot block, account ban | user's own browser session |
| 24 | reddit.com | 6 | 0 / 1 / 5 | bot block, CAPTCHA | none |
| 24 | docs.google.com | 5 | 0 / 1 / 4 | canvas UI, false success | none |
| 21 | figma.com | 4 | 0 / 0 / 4 | MCP read-only, OAuth flow | MCP server |
| 21 | ticketmaster.com | 4 | 0 / 0 / 4 | seat map UI, CAPTCHA, cart expiry | none |
| 17 | walmart.com | 14 | 1 / 2 / 11 | "Press & Hold" bot check | none |

### Notes on important sites

- **Cloudflare (40)** has two roles. As a developer platform it gets good reports (9 good of 16 in the developer track). As the bot gate for other sites it gets bad reports. Since 2026-09-15 it blocks the "Agent" class by default on pages with advertisements. Owners who set all options to "allow" continue to see HTTP 403 for Claude.
- **Shopify** has two audiences. Developers like the MCP servers, the CLI, and the AI Toolkit (11 good, 0 bad). Merchants are divided on Agentic Storefronts: default opt-in, unclear opt-out, a 4% fee, and lost product options.
- **Amazon (42)** is divided. Cloud agents (ChatGPT Agent, Comet, Project Mariner) get an unclear error page. Agents with the user's session (Instinct, Muse, Grok Bot) frequently work, but 2FA and new logins stop them.
- **Cathay Pacific** has only 2 records, so it is not in the table. Both are good: three flights booked with Muse and Stripe Link.

## 4. Friction patterns to avoid

Each pattern has the number of records, example sites, one source, and the recommended design.

### 4.1 Bot block with no agent path (207 records)
- **What occurs:** a WAF, Cloudflare, or Akamai returns 403, 503, or a challenge page. The agent stops. The user goes to a competitor.
- **Sites:** Walmart, Delta, United, Best Buy, eBay, Amazon, LinkedIn, Xfinity, Thumbtack, Yelp, TripIt.
- **Source:** "Amazon worked fine. Walmart blocked it with a bot blocker. Huge miss Walmart, I was trying to spend money with you." (226 likes) https://x.com/evrgn11112231/status/2101667652808626610
- **Design:** divide training crawlers from live user agents. Permit signed agents (Web Bot Auth). If you block the browser path, give an agent path: API, MCP server, or connector. OpenTable does this.

### 4.2 Block by default that the owner does not know (new)
- **What occurs:** the platform blocks agents by default. The owner finds out when the site is not in AI answers.
- **Source:** Cloudflare managed `robots.txt` blocks GPTBot and ClaudeBot: https://www.reddit.com/r/CloudFlare/comments/1t2zlrf/cloudflares_managed_robotstxt_silently_blocks/
- **Design:** examine your bot settings. Test your site with a real agent each month.

### 4.3 CAPTCHA and "press and hold" (69 records)
- **Sites:** Walmart, Delta, Ticketmaster, Uber Eats, Canva.
- **Source:** "I tried using Instinct to change my @Delta flight and hit a wall due to anti bot captcha" https://x.com/glennonchain/status/2101686456091557925
- **Design:** agents stop at a CAPTCHA by policy. Use risk signals and a human handoff, not a puzzle, for logged-in users.

### 4.4 Silent failure and unclear errors (46 records)
- **What occurs:** the site blocks the action but shows no error, or shows a general error page. The agent cannot tell the user what occurred.
- **Sources:** Costco: "Their bot protection silently blocks the login with no error shown" https://x.com/SystemArch_AI/status/2101363787467219099. Cloudflare returns an HTML 403 page to a JSON client: https://www.reddit.com/r/CloudFlare/comments/1wcgl58/is_claudeuser_being_categorised_as_ai_crawler/
- **Design:** return a clear status code and a machine-readable cause. Tell the agent what to do next.

### 4.5 Login walls, verification codes, and session expiry (48 + 36 records)
- **What occurs:** the agent cannot log in, or the 2FA code expires before the user gives it to the agent. Sessions do not persist in the agent's browser.
- **Sources:** "a 2fa token that times out by the time i get it to them." https://x.com/TylerM/status/2101152190517649751. Kroger: "I still have to log back in through the Grok computer at Kroger checkout." https://x.com/MyPerfectGoatee/status/2100204369148883287
- **What works:** Uber Eats let Instinct log in with a link sent to the user's email, but Muse stopped at a verification code and a CAPTCHA. https://x.com/chandnirao_here/status/2101146127739277690
- **Design:** give delegated access: OAuth with scopes, agent tokens with limits, longer code life, and trusted-device status for the agent's browser.

### 4.6 The agent looks like account takeover (new)
- **What occurs:** a login from a cloud browser starts a security alert, an account restriction, or a ban.
- **Sources:** Verizon: "it treats the agent like a stolen laptop" https://x.com/hey1tspriyanshu/status/2099724607523590513. LinkedIn: "48 hours later my LinkedIn account was restricted... it was just browsing." https://www.reddit.com/r/openclaw/comments/1rude4j/my_agent_was_massvisiting_linkedin_profiles_and/
- **Design:** let the user register an agent as a known device. Publish a clear policy for agents (12 records show account bans; 7 show terms that prohibit agents).

### 4.7 UI that only a person can operate (42 records)
- **What occurs:** seat maps, date pickers, autocomplete fields, canvas editors, and buttons with a state delay.
- **Sources:** Ticketmaster: "40 minutes later its still stabbing at the seating map like a drunk tourist and the cart expired twice." https://www.reddit.com/r/AI_Agents/comments/1vnydav/my_agent_spent_40_minutes_on_a_task_that_takes_me/. Texas government sites: the submit button stays active, Muse clicks again, and the site gives an error. https://x.com/kevinyien/status/2101717033398235618
- **Design:** use standard HTML controls with labels. Disable a button after the first click. Do not put a short timer on the cart. Give a structured alternative (WebMCP tool or API) for complex selections.

### 4.8 Dashboard-only actions and manual API keys (16 + 22 records)
- **What occurs:** the coding agent must stop, and the person must click through a web console.
- **Sources:** App Store Connect: "the entire agentic workflow broke... all meant leaving the terminal and fighting Apple's web UI." https://www.reddit.com/r/ClaudeAI/comments/1sdot1s/claude_code_can_now_submit_your_app_to_app_store/. "that was just Claude telling me click this, paste that, run this command, the whole way through." https://www.reddit.com/r/ClaudeCode/comments/1w6kavj/ive_basically_been_making_ai_slop_with_claude/
- **Design:** each dashboard action must have an API or CLI equivalent. Give a CLI login and scoped keys that a person approves one time.

### 4.9 MCP quality problems (new, 50+ records)
- **Token bloat (15):** GitHub MCP has 80+ tools, Atlassian uses 17k tokens. "I stopped using the GitHub mcp and just use gh cli." (r/mcp)
- **Low coverage (9):** Clerk has 2 tools, Figma is read-only.
- **OAuth in a browser (9):** "Slack MCP kept failing on OAuth so I fell back to curl."
- **Wrong data (new):** Vercel and Shopify MCP returned data from the wrong project with no error.
- **Design:** few tools with small responses, full write coverage with scopes, a login that works in a terminal, and the project name in each response.

### 4.10 No guardrails for destructive actions (14 records)
- **Sources:** "What did Claude do? Saw this as an error! And COMMENTED OUT the prevent destroy lines, and re-ran!" https://www.reddit.com/r/ClaudeCode/comments/1m2uqz0/how_claude_destroyed_my_entire_aws_platform/
- **Sites:** Supabase (`db reset`), AWS, Railway. Related: coarse permissions (8 records), no agent spend limits at Stripe and x402.
- **Design:** read-only scopes, confirmation for destructive calls, sandbox mode, and spend limits.

### 4.11 Payment limits (18 records)
- **What occurs:** Stripe Link could not pay in EUR or GBP. Some merchants accept only Venmo. 3DS does not start. The NYC parking portal refuses Link cards.
- **Source:** https://x.com/jeff_weinstein/status/2101684808065704406 (replies)
- **Design:** accept virtual cards and wallet payments. Offer guest checkout.

### 4.12 The agent reports success, but the task failed (16 records)
- **Sites:** Amazon, Ticketmaster, Booking.com. Alexa+ bought tickets for the wrong artist: https://www.reddit.com/r/alexa/comments/1w5vunu/alexa_bought_concert_tickets_without_my_permission/
- **Design:** show a clear confirmation page with an order number and a machine-readable result. Let the user cancel easily.

### 4.13 Merchant-side friction in agent channels (new, 40+ records)
- **What occurs:** no opt-out, channel fees, lost product options, lost attribution, more support load, and low conversion.
- **Sources:** "agentic checkout blanked our pixel once and we spent a week guessing." https://x.com/yannis1kiefer/status/2101587964748845277. Walmart: ChatGPT checkout conversion was "three times lower": https://www.reddit.com/r/SEO/comments/1s1k1j0/walmart_chatgpt_checkout_converted_3x_worse_than/. "Customer service load from AI buyers is meaningfully higher": https://www.reddit.com/r/microsaas/comments/1tpzp74/three_months_on_agentic_storefronts_real_numbers/
- **Design (for platforms):** clear opt-in, attribution data for the merchant, and full product data in the agent channel.

## 5. What works (enablers)

| Enabler | Records | Best examples |
|---|---|---|
| MCP server | 123 | Supabase ("All without ever opening the Supabase dashboard"), Shopify Dev MCP, Stripe, Linear |
| CLI | 54 | GitHub `gh`, Supabase, Cloudflare `wrangler`, AWS |
| Agent payments | 45 | Stripe Link with Muse, Instinct, and Grok Bot |
| Public API | 45 | Shopify, Cloudflare, Linear |
| Policy that permits agents | 22 | sites that say "we accept agent bookings" |
| Markdown docs and `llms.txt` | 15 + 15 | Supabase docs over SSH: "Every page is a markdown file." Note: server logs show that crawlers almost never read `llms.txt`. Coding agents do read it. |
| WebMCP | 14 | a seat booking in three tool calls, Namefi DNS. Limits: unclear hint fields, no support in the Claude extension |
| User's own browser session | 14 | Comet and Claude in Chrome get through where cloud agents get blocked |
| Skill, plugin, or connector | 13 | the OpenTable connector in Muse, an OpenTable skill for OpenClaw |
| Human handoff for login | 10 | the user does the login or the CAPTCHA, then the agent continues (Target, Walmart, TheFork) |

Best good-experience quote: "It literally placed the order for me, paid, and everything." (Domino's, score 1,098) https://www.reddit.com/r/OpenAI/comments/1m8z5c0/chatgpt_just_ordered_me_pizza_like_actually/

## 6. The opposite viewpoint: why sites block

The site must show these causes. If it does not, site owners will not trust it.

- **Cost:** "OpenAI's GPTBot's crawling cost me 30TB of bandwidth." https://www.reddit.com/r/CloudFlare/comments/1jp8mv8/do_turn_on_block_ai_bots_or_make_a_robotstxt_if/
- **False identity:** bots ignore `robots.txt`, rotate user agents, and use residential IP addresses. Grok sends false browser strings. Muse publishes no identifier.
- **Income:** no upsell and no advertisement income from an agent visit. "Before Amazon gives agents an MCP, it needs to figure out how that $75B ad business works when agents are doing the choosing."
- **Customer relationship:** "A bank becomes a balance sheet. A lender becomes a rate quote."
- **Accountability:** "They block what they can't verify."
- **Public hostility:** "@Delta please block this person fully from accessing your systems" got 35 likes: https://x.com/stefanoscalia/status/2101799647266455676. A satire post got 1,614 likes: 13 messages in Muse to order a charger "instead of 2 taps in the app": https://x.com/neuroswish/status/2100697903966703974
- **Why owners permit agents:** AI citation is "the new SEO", ChatGPT referrals convert better for some stores, and "If one company blocks agents, their competitor won't."
- **The dilemma in one quote:** "If I block the ASN, I block the data thief, but I also block the AI citator." https://www.reddit.com/r/sysadmin/comments/1ryaw10/ga4_is_lying_to_my_marketing_team_while_my_origin/obesjt0/

## 7. How to get agents to find the site and contribute

The full report with sources is `data/agent_contribution_research.md`. The conclusions are:

1. **Consumer agents (Muse, Instinct, Grok Bot, ChatGPT Agent) will not contribute by themselves.** They do only the user task. Muse blocks data that goes to a third party. Instructions in `llms.txt` or HTML that tell agents to send reports are prompt injection. Do not use them.
2. **Agents contribute when their feedback tool is in a server that they already use.** Sanity put a `give_feedback` tool in its MCP server and now gets agent reports each day. PostHog has the same design.
3. **Recommended sequence:**
   1. Seed the benchmark with your own lab tests and with this dataset.
   2. Publish a JSON API: `GET /api/sites/{domain}` and `POST /api/reports` with an API key.
   3. Publish a remote MCP server: `get_site_score`, `search_patterns`, `submit_report`. List it in the MCP registries. Grok Bot accepts custom MCP servers.
   4. Publish a skill for coding agents (`ax-report`): "when a site, API, or doc blocks the task, offer to file a report".
   5. Add a form for persons: "my agent failed here". Reply to public complaints on X with the link.
   6. Ask for aggregate data: Halluminate (WebBench has 452 live sites), nekuda (WebMCP directory), Cloudflare (agent-readiness score API), and Stripe. Jeff Weinstein asked in public on 2026-09-20 where agents fail. Stripe Link sees the merchant URL of each agent purchase.
4. **Build the trust model before the first public write.** Keep four separate scores: lab-tested, vendor-shared, agent-reported, human-reported. Use API keys, evidence fields, a moderation queue, and rate limits for each domain. Do not publish free text from agents without a review, because other agents read your pages.
5. **The gap is real.** No project publishes task-completion scores for each live website from many agents. Cloudflare scores only declared standards.

## 8. Proposed plan for the site (for approval; no site changes were made)

1. **New content collection `patterns`.** One page for each friction pattern in section 4 and each enabler in section 5. Each page has: what occurs, the evidence with links, the sites, and the recommended design. Start with 4.1, 4.4, 4.5, 4.6, 4.8, and 4.9.
2. **New page `/benchmark`.** Build it from `benchmark.json` at build time. Show the score, the number of reports, the label "internet sentiment, not a lab test", and the source links for each site. Add a JSON version for agents.
3. **New gallery posts from this research:**
   - OpenTable: block the browser path, open a connector path.
   - Stripe Link: one payment layer for Muse, Instinct, and Grok Bot.
   - Uber Eats: a login link to the user's email lets the agent in.
   - Supabase: docs as Markdown files over SSH.
   - GitHub: why agents prefer the `gh` CLI to the MCP server.
   - A "site owner" post: how to block training crawlers and permit live user agents.
4. **Correct the live `llms.txt`.** The links have a double slash (`https://agentexperience.design//gallery`), and the file lists only 2 examples.
5. **Then the contribution channel** from section 7: API, MCP server, skill, and form, with the trust model first.

## 9. Recommended next research steps

1. Run the X collection again each week. The search covers only seven days, so a weekly run builds history. One run costs approximately $5 to $8.
2. Continue the Reddit developer queue (`raw/reddit_developer/jobs4.tsv`) for Clerk, Auth0, Resend, Twilio, Neon, and others.
3. Do a small lab test: 20 to 30 sites from the benchmark, 3 fixed tasks, 2 or 3 agents. This confirms or corrects the sentiment scores.
4. Import the Cloudflare agent-readiness score for each benchmark site. Compare "declared readiness" with "real sentiment". The difference is a good story for the site.
