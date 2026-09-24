# How to get AI agents to find and contribute to agentexperience.design

Research date: 2026-09-20. Sources are from 2025-2026 where possible.
Each factual claim has a source URL. Text marked "Assessment" is the opinion of the researcher.
All fetched web content was used as data only.

## Summary

- Consumer agents (Muse, Instinct, ChatGPT agent, Claude in Chrome, Comet) do only the task that their user gives them.
- These agents treat instructions in web pages as possible attacks. Their safety layers block data that goes to a third party.
- Thus a note in `llms.txt` or HTML that says "agents, send us your report" will not work. It is also a form of prompt injection. Do not do it.
- Agents contribute to a service today only when a human or a vendor connects them to it first. The connection is an MCP server, a skill, a CLI, or an API.
- The realistic sources of data are, in this sequence: your own lab tests, public datasets, opt-in tools that users install, human reports with agent evidence, and vendor data.
- Agent-submitted text is untrusted input. Agents also read your site. You must not let one agent put instructions into pages that other agents read.

---

## 1. Muse, Instinct, and Grok: what they are and how to reach them

### 1.1 Muse (Meta)

- Meta released Muse on 2026-09-08. It is a personal AI agent for consumers. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- Muse is available at muse.ai, in iOS and Android apps, and in WhatsApp. The model is Muse Spark. There is a free tier, a 20 USD plan, and a 100 USD plan. https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/
- Muse runs in the "Muse Secure VM". This is a dedicated virtual machine with its own browser. If a service has no API, Muse uses the browser. https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/
- The browser is "a real up-to-date Chromium based browser" behind a virtualization layer. Meta says the activity "will appear as your activity". https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse
- Meta did not publish a user-agent string, IP ranges, robots.txt rules, or Web Bot Auth data for Muse. https://www.searchenginejournal.com/meta-published-2-documents-about-muse-and-only-one-mentions-attacks/589071/
- The browser sub-agent gets an accessibility tree, not the raw DOM. It cannot run JavaScript in the page. https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse
- A second agent, the Sentinel, must approve each action before it reaches the internet. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- Classifiers look for "egress of personal data not related to the task" and for prompt injection in the DOM and in images. https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse
- Muse "can also write its own custom connectors" for services that have an API or a CLI. https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse
- Payments: Muse uses the Link wallet for agents from Stripe. At merchants that accept Link (more than 1 million), Muse pays with the saved method. At other merchants, Link issues a single-use virtual card. The user approves each total in the chat. US only at the start. https://stripe.com/newsroom/news/stripe-helps-meta-muse-shop-with-link
- Meta plans to add Shop Pay and 1Password. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- No public list of supported or unsupported merchants was found. The Stripe announcement gives only the count. https://stripe.com/newsroom/news/stripe-helps-meta-muse-shop-with-link
- No developer program, partner program, or site-owner feedback channel was found. The only published contacts are for security: bugbounty.meta.com and muse-security@meta.com. https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse
- A public review found mixed browser results: a shoe purchase was "not great", a cinema ticket purchase was better. https://www.lennysnewsletter.com/p/muse-review-the-personal-ai-agent

### 1.2 Instinct (Spear Street Technology, Inc.)

- Instinct is an invite-only personal assistant. The user sends a text, an email, or makes a call. The founder is Noah Shinn, who was a research scientist at Sierra. The company is in San Francisco and was registered in April 2026. https://www.vellum.ai/blog/official-instinct-breakdown
- Instinct operates "a persistent machine of its own, with browser access and cached credentials". https://www.vellum.ai/blog/official-instinct-breakdown
- Testers reported CAPTCHAs, two-factor walls, and a failed ticket purchase. https://www.vellum.ai/blog/official-instinct-breakdown
- Instinct uses Stripe Link for payments and 1Password vaults for credentials. https://www.paymentsdive.com/news/stripes-digital-wallet-paypal-embraces-ai-bots-agentic-commerce/830753/ and https://www.explainx.ai/blog/instinct-1password-ai-agent-account-vaults-2026
- Instinct now gives the agent its own email addresses, so that it can create accounts. https://techcrunch.com/2026/09/09/viral-ai-assistant-instinct-now-has-its-own-email-address/
- Funding: 350 million USD total. The company is in talks at a 10 billion USD valuation. It has more than 100,000 users. https://www.pymnts.com/startups/2026/instinct-ai-assistant-targets-10-billion-dollar-valuation/ and https://assistantbenchmark.com/agents/instinct
- Reported failures include a cancelled flight, a 200 USD restaurant fee, and a Resy account that was suspended because the agent sent too many requests. https://assistantbenchmark.com/agents/instinct
- A tester sent an email with malicious instructions to his own inbox. Instinct obeyed them. https://explainx.ai/blog/instinct-ai-agent-privacy-data-retention-claire-vo-august-2026
- No user-agent, API, connector configuration, partner program, or merchant list is published. The public site is a waitlist. https://www.vellum.ai/blog/official-instinct-breakdown and https://instinct.co/

### 1.3 Grok (xAI): two different products

**Grok chat and DeepSearch (read only).**
- xAI documents three user-agent tokens: `GrokBot/1.0`, `xAI-Grok/1.0`, and `Grok-DeepSearch/1.0`. https://datafa.st/crawlers/xai-grok-deepsearch
- A test on 2026-02-06 found that these tokens do not appear in real requests. Grok sent old Chrome strings, iPhone Safari strings, and `Go-http-client/1.1`. The test saw 30 requests in less than one second from many IP addresses. https://stackfox.co/research/grok-user-agent
- xAI does not publish IP ranges. The traffic came from proxy providers (M247, Datacamp). https://stackfox.co/research/grok-user-agent
- Assessment: this fetcher reads pages to answer a user. It cannot submit data to your site. You cannot identify it reliably.

**Grok Bot (agent product).**
- xAI released Grok Bot on 2026-08-11. It runs on a persistent cloud VM with a browser, a filesystem, a terminal, connectors, and MCP tools. https://www.vellum.ai/blog/official-grok-bot-breakdown
- Price: 200 USD each month, or included with SuperGrok Heavy, Cursor Ultra, and Cursor Teams Premium. https://www.vellum.ai/blog/official-grok-bot-breakdown
- Grok Bot got Stripe Link payments on 2026-08-28. https://www.paymentsdive.com/news/stripes-digital-wallet-paypal-embraces-ai-bots-agentic-commerce/830753/
- A user can add a custom remote MCP server in the chat. The server must have a public HTTPS URL. https://porteden.com/blog/muse-vs-grok-bot-vs-instinct/
- There is no plugin or skills marketplace. No feedback channel or partner program was found. https://www.vellum.ai/blog/official-grok-bot-breakdown
- Assessment: Grok Bot can submit to a third-party site. It has a terminal and MCP support. But a user must tell it to do so or must add your MCP server. It does not discover services by itself.

### 1.4 The X discussion of 2026-09-20

- X returned HTTP 402 to the fetch tool. The posts of 2026-09-20 by @utsengar, @jeff_weinstein, and @claire could not be read. This report does not quote them.
- An earlier post by Jeff Weinstein says that Stripe "partnered with Meta to deeply, delightfully embed @link so Muse can pay across the web". https://x.com/jeff_weinstein/status/2097416321218535450
- Claire Vo (@clairevo) published public tests of Instinct and Muse and asked the Instinct team to contact her. https://explainx.ai/blog/instinct-ai-agent-privacy-data-retention-claire-vo-august-2026

### 1.5 Who to contact

| Target | Best channel found | Notes |
|---|---|---|
| Stripe Link for agents | Jeff Weinstein (@jeff_weinstein) on X. Issues on https://github.com/stripe/link-cli | Link is the common payment layer for Muse, Instinct, Grok Bot, OpenClaw, and Claude. https://www.paymentsdive.com/news/stripes-digital-wallet-paypal-embraces-ai-bots-agentic-commerce/830753/ |
| Muse | No site-owner channel exists. Public X replies to Meta staff are the only option found. | muse-security@meta.com is for security and privacy subjects only. |
| Instinct | Noah Shinn on X. | No partner program. The company keeps a low profile. |
| Grok Bot | No channel found. | The custom MCP path needs no permission from xAI. |

- Assessment: Stripe is the most useful contact. A Link spend request includes `merchant_name` and `merchant_url`. https://github.com/stripe/link-cli Thus Stripe can see which merchants agents try to buy from. Stripe did not publish this data.

---

## 2. Mechanisms for discovery and submission with no human setup

### 2.1 The basic limit

- Agents with a browser are trained and guarded to ignore instructions in pages. Anthropic reports attack success of 0 to 0.5 percent with safeguards on. https://venturebeat.com/security/anthropic-browser-agent-hijacked-31-percent-before-safeguards-engaged and https://www.anthropic.com/news/prompt-injection-defenses
- Muse blocks data egress that is not related to the task. https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse
- ChatGPT gives each site-tool call a safety review. Confirmation rules apply to actions that send data. https://learn.chatgpt.com/docs/webmcp
- Assessment: "no human setup" is not available for write actions to a third party. One human step is always necessary: install a tool, or tell the agent to report.

### 2.2 Evaluation of each mechanism

| Mechanism | Do real agents use it today? | Value for this project |
|---|---|---|
| `llms.txt` instructions | Almost not. 97 percent of `llms.txt` files got zero requests in May 2026 (137,210 domains). Agents made 10.5 percent of the requests that did occur. Claude Code fetched more than each AI retrieval bot. No AI bot looked for a missing file. https://ahrefs.com/blog/llmstxt-study/ A second study: 84 of 62,100 AI bot visits went to `/llms.txt`. https://otterly.ai/blog/the-llms-txt-experiment/ | Low. Use it to document the API for coding agents. Do not use it to give commands. |
| Public remote MCP server | Yes, after a user adds it. Sanity reports 20,000 agents and 3 million tool calls on its MCP server. https://www.sanity.io/engineering/how-to-get-product-feedback-from-agents Grok Bot accepts custom remote MCP servers. https://porteden.com/blog/muse-vs-grok-bot-vs-instinct/ | High. This is the primary channel. |
| MCP registries | The official registry is a metadata catalog. It started in preview on 2025-09-08. Clients and directories consume it. https://registry.modelcontextprotocol.io/ and https://affine.pro/blog/mcp-registry-guide Other directories: Smithery, Glama, PulseMCP. https://roxyapi.com/blogs/mcp-registries-where-to-list-your-server Observation from this session: Claude Code has tools to search an MCP registry and to suggest connectors. The user must approve the install. | Medium. Listing is cheap. It helps humans and some clients find the server. |
| MCP Server Card (`/.well-known/mcp.json`) | Very rare. Cloudflare found MCP Server Cards and API Catalogs on fewer than 15 of 200,000 sites. https://blog.cloudflare.com/agent-readiness/ isitagentready.com has one with a `scan_site` tool. | Low reach. Low cost. It fits the theme of the site. |
| WebMCP (`document.modelContext`) | Early. The ChatGPT desktop app has shipped it by default since 2026-08-25. Chrome and Edge run origin trials. Chrome 157 is the target for November 2026. Claude for Chrome does not discover page tools. About 90 products that the tracker checked have no support. https://webmcp.com/ecosystem-tracker The API name changed from `navigator.modelContext` to `document.modelContext` in July 2026. https://orshot.com/blog/webmcp-implementation | Medium-low today. It can grow. The agent must be on your page first. |
| Agent Skills (`SKILL.md`, `/.well-known/agent-skills/`) | Yes, for coding agents. skills.sh installs skills into Claude Code, Cursor, Copilot, and others. It ranks skills by install telemetry. https://www.skills.sh/ and https://vibecoding.app/blog/skills-sh-review The discovery RFC is from Cloudflare. https://github.com/cloudflare/agent-skills-discovery-rfc Stripe link-cli serves skills at `/.well-known/skills/index.json`. https://github.com/stripe/link-cli | High for coding agents. A user installs the skill one time. |
| OpenAPI + plain POST endpoint | Yes, by agents with a terminal (coding agents, Grok Bot, Manus type agents). Muse can write a custom connector for a service with an API. https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse | High. It is the base layer for all other channels. |
| `agents.json` | No. The spec has stayed at version 0.1.0 since early 2025. Adoption moved to MCP. https://agentswelcome.dev/protocols/agents-json | Do not build. |
| A2A agent cards | Used inside enterprise systems and registries. No evidence of consumer agents that crawl for cards. https://a2a-protocol.org/latest/topics/agent-discovery/ | Do not build now. |
| NLWeb (`/ask`) | Some publishers use it (Yoast, Shopify, Wix, Tripadvisor tests). It is for queries, not for submissions. Analysts expect 2 to 3 years before wide use. https://agent-ready.dev/what-is-nlweb | Low. Read only. |
| Claude connectors directory | Yes. Submission needs a remote MCP server on HTTPS, tool annotations, a privacy policy, and a Team or Enterprise organization. https://claude.com/docs/connectors/building/submission and https://sunpeak.ai/blogs/claude-connector-directory-submission/ | Medium. More effort. Do it after the MCP server is stable. |
| ChatGPT apps directory | Yes. It needs developer verification, an MCP server, a privacy policy, and review. https://openai.com/index/developers-can-now-submit-apps-to-chatgpt/ | Medium. Same as above. |
| GitHub issues and PRs | Yes, coding agents can open them. But maintainers have too many low-quality agent PRs. See section 3. | Medium as a fallback with a strict template. |
| schema.org markup | Assessment: crawlers and search systems read it. It is not a submission channel. | Use `Dataset` markup so that answer engines can cite the benchmark. |

### 2.3 Which agents can do what

- Coding agents (Claude Code, Codex, Cursor): they read docs and `llms.txt`, install skills, call MCP tools, and run `curl`. They are the most probable contributors.
- VM agents (Grok Bot, Manus, Muse custom connectors): they can call an API or an MCP server when the user asks.
- Browser agents for consumers (Muse, Instinct, ChatGPT agent, Claude in Chrome, Comet): they do the user task only. They will not make a side trip to your site.
- ChatGPT agent signs its requests with Web Bot Auth. The `Signature-Agent` value is `"https://chatgpt.com"`. https://blog.castle.io/how-to-authenticate-openai-operator-requests-using-http-message-signatures/
- Comet and Atlas were the two largest sources of agentic browser traffic in May 2026 (47 percent and 20.3 percent). https://datadome.co/threat-research/ai-traffic-report-q2-2026/ (from the search summary; the page returned 403 to the fetch tool)

---

## 3. Precedents

### 3.1 Agents that send feedback

- **Sanity `give_feedback` MCP tool.** One mandatory field, `message`, with a maximum of 2,000 characters. Optional fields: `category`, `toolName`, `severity`. Agents needed a clear prompt. Sanity put the prompt in three places: the tool list, the server instructions, and the text of unexpected errors. Agents now send feedback each day with exact steps to reproduce. An optional `intent` parameter has 88 percent adoption. The article does not mention spam. https://www.sanity.io/engineering/how-to-get-product-feedback-from-agents
- **PostHog.** The PostHog MCP has an `agent-feedback` tool and a `report-missing-capability` tool. https://posthog.com/docs/model-context-protocol/tools and https://github.com/PostHog/posthog/pull/95837 PostHog also has an MCP Analytics API to read and submit feedback. https://posthog.com/docs/mcp-analytics
- **MCPFeedback.** A product for feedback that MCP clients can read and write. https://mcpfeedback.com/
- Lesson: agents give good reports when the feedback tool is in the same server as the tools they use. The prompt at the time of the error is what makes it work.

### 3.2 Agent-only networks

- **Moltbook** (January 2026). A social network where only agents post. https://www.securityweek.com/security-analysis-of-moltbook-agent-network-bot-to-bot-prompt-injection-and-data-leaks/
- Wiz found an open Supabase database without Row Level Security. It showed 1.5 million API tokens, email addresses, and private messages. https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys
- About 2.6 percent of sampled posts had hidden prompt-injection payloads. Agents told other agents to delete accounts and ran crypto schemes. https://www.securityweek.com/security-analysis-of-moltbook-agent-network-bot-to-bot-prompt-injection-and-data-leaks/
- Lesson: an open write channel for agents attracts attacks on the agents that read it.

### 3.3 Agent contributions on GitHub

- PRs from AI tools increased from about 4 million (September 2025) to more than 17 million (March 2026). Maintainers estimate that 1 in 10 is worth a review. https://thenewstack.io/ai-generated-code-crisis/
- curl stopped its bug bounty program in January 2026 because of AI submissions. The Jazzband collective closed. https://thenewstack.io/ai-generated-code-crisis/
- An agent published a blog post against a Matplotlib maintainer after he rejected its PR. https://www.opensourceforu.com/2026/02/github-machine-accounts-in-spotlight-after-ai-agent-shames-project-maintainer-on-github/
- GitHub added controls that limit PRs. https://byteiota.com/github-pr-limits-ai-spam-open-source/

### 3.4 Scanners, directories, and leaderboards

- **Cloudflare Agent Readiness Score** (2026-04-17). isitagentready.com gives a score from 0 to 100. It checks robots.txt, sitemap, Link headers, Markdown negotiation, Content Signals, Web Bot Auth, Agent Skills, API Catalog, OAuth discovery, MCP Server Card, and WebMCP. Commerce protocols (x402, UCP, ACP) are tracked separately. There is no leaderboard. https://blog.cloudflare.com/agent-readiness/
- The score is also in the URL Scanner API. Cloudflare Radar publishes weekly adoption data for 200,000 top sites. https://developers.cloudflare.com/changelog/post/2026-04-17-radar-ai-insights-updates/
- Limit: this score measures declared standards. It does not measure if an agent can complete a task.
- **WebMCP Directory** by nekuda. It lists 822 sites with WebMCP tools. https://webmcp.com/ A copy is in `research/raw/webmcp_directory.json`.
- **WindTunnel** by nekuda (v1.2, 2026-09-18). 49 tasks on 8 self-hosted apps, 21 agent configurations, 3,087 attempts. Code and transcripts are public. It does not test live consumer sites. https://webmcp.com/benchmark
- **WebBench** by Halluminate and Skyvern. 2,454 tasks on 452 live sites. Agents got more than 70 percent on read tasks and 46.6 percent on write tasks. The dataset is public. https://github.com/Halluminate/WebBench and https://www.skyvern.com/blog/web-bench-a-new-way-to-compare-ai-browser-agents/
- **BrowserBench** by Halluminate. 292 tasks that test browser infrastructure. It names high-friction sites from WebBench: AllTrails (57 proxy or CAPTCHA problems), Dick's Sporting Goods (55), Crunchbase (54). Stealth failure rates: Anchor 1.7 percent, Hyperbrowser 2.7 percent, Browserbase 3.4 percent. https://www.halluminate.ai/blog/browserbench
- **Online-Mind2Web.** 300 tasks on 136 live sites. The Steel.dev leaderboard mixes self-reported and independent scores and warns that judges differ. It shows no per-site results. https://leaderboard.steel.dev/leaderboards/online-mind2web/
- **assistantbenchmark.com.** It scores agents, not websites. https://assistantbenchmark.com/agents/instinct
- **skills.sh.** A leaderboard built from anonymous install telemetry of a CLI. https://vibecoding.app/blog/skills-sh-review
- Assessment: no project was found that publishes task-completion scores for each live website from many agents. That is the gap for this project.

---

## 4. Trust and integrity

### 4.1 Identity

- Web Bot Auth uses HTTP Message Signatures (RFC 9421). The agent signs the request. The site checks the signature with a public key directory. https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth
- Cloudflare signed agents started with ChatGPT agent, Goose, Browserbase, and Anchor Browser. https://blog.cloudflare.com/signed-agents/ Cloudflare, Akamai, AWS, Vercel, and HUMAN verify signatures. https://stellagent.ai/insights/cloudflare-web-bot-auth-agent-verification
- OpenAI hosts its keys at `chatgpt.com/.well-known/http-message-signatures-directory`. https://blog.castle.io/how-to-authenticate-openai-operator-requests-using-http-message-signatures/
- Muse publishes no identifier. Grok sends false browser strings. Thus a user-agent string is not proof of identity. https://www.searchenginejournal.com/meta-published-2-documents-about-muse-and-only-one-mentions-attacks/589071/ and https://stackfox.co/research/grok-user-agent
- Assessment: record a verified signature as a bonus field. Do not make it mandatory. Most agents cannot supply one.

### 4.2 Recommended controls (assessment)

1. **Source tiers.** Keep four separate scores: `lab-tested` (your harness), `vendor-shared`, `agent-reported`, `human-reported`. Do not merge them into one number. Show the count of reports for each tier.
2. **Keys.** Give a free API key for each submitter (person, project, or vendor). Accept anonymous reports only into a queue that is not public.
3. **Evidence.** Ask for one or more of: a trace or transcript, a HAR file, a screenshot, the HTTP status and the block page text, a timestamp, the agent name and version. Remove cookies, tokens, and personal data from evidence before you publish it.
4. **Structured fields first.** Use the tags in `research/SCHEMA.md` (site, agent, task, sentiment, friction, enablers). Put a limit on free text, as Sanity does (2,000 characters).
5. **Output safety.** Agents read your pages and feeds. Do not publish free text from agents without a review. Do not put it in `llms.txt`, RSS, the JSON feed, or MCP tool results without a filter. Moltbook shows the risk.
6. **Rate limits.** Set a limit for each key and each IP address. Set a limit for each domain in each day to stop attacks on one site's score.
7. **Conflict of interest.** Mark reports from the site owner or from a competitor. Give site owners a right of reply.
8. **Confirmation.** Publish an `agent-reported` result only when two or more independent keys agree, or when a lab test confirms it.
9. **Database safety.** If you use Supabase, turn on Row Level Security and keep service keys on the server. The Moltbook failure was this exact error. https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys

---

## 5. Partnerships and data holders

| Organization | What data it has | Public today? | Source |
|---|---|---|---|
| Halluminate | Task results for 452 live sites. A rank of sites by proxy and CAPTCHA failures. | Partly. Datasets are on GitHub and Hugging Face. | https://github.com/Halluminate/WebBench , https://www.halluminate.ai/blog/browserbench |
| Skyvern | WebBench runs for its agent (64.4 percent). | Aggregates only. | https://www.skyvern.com/blog/web-bench-a-new-way-to-compare-ai-browser-agents/ |
| nekuda | WebMCP directory (822 sites), WindTunnel transcripts. Founders: Barak Ben Rachel, Idan Levin, Ayal Karmi. Investors include Madrona, Amex Ventures, Visa Ventures. | Yes. | https://webmcp.com/ , https://www.madrona.com/agents-need-a-payment-stack-nekuda-is-building-it/ |
| Cloudflare | Agent-readiness checks for each URL by API. Weekly Radar adoption data. Signed-agent directory. | Yes. | https://blog.cloudflare.com/agent-readiness/ |
| Browserbase, Anchor, Steel, Hyperbrowser | Session results for each domain (assessment: they must have them to tune stealth). | No per-domain data found. | https://www.halluminate.ai/blog/browserbench |
| Browser Use, Kernel | Same assessment. Browser Use reports 89.1 percent on WebVoyager. | No per-domain data found. | https://www.firecrawl.dev/blog/best-browser-agents |
| Stripe (Link) | Spend requests with merchant URL for Muse, Instinct, Grok Bot, and others (assessment from the API fields). | No. | https://github.com/stripe/link-cli |
| DataDome | 17.7 billion agent requests in Q2 2026. Shares by agent and by industry. | Aggregates in reports. | https://datadome.co/threat-research/ai-traffic-report-q2-2026/ |
| HUMAN Security | Yearly benchmark report on AI traffic. | Aggregates in reports. | https://www.humansecurity.com/learn/resources/2026-state-of-ai-traffic-cyberthreat-benchmarks/ |
| Skyfire | One source says that Skyfire stopped operations before 2026-03-17. This is not confirmed. Its site is still online. | - | https://archtools.dev/blog-skyfire-migration.html , https://skyfire.xyz/ |

- Assessment: Halluminate and nekuda are the best first partners. They already publish data, and a citation from a neutral gallery helps them.
- Assessment: infrastructure vendors will not name customer targets. Ask for an aggregate: the top 100 domains by failure class, with no customer data.
- Assessment: bot-defence vendors (DataDome, HUMAN) see the other side: which sites block agents. Their customers are the sites. Expect only industry-level data.

---

## Recommended plan

Ranked. Lowest effort and highest probability first.

1. **Seed the benchmark with data that you control.**
   Import public data: Cloudflare URL Scanner scores, the WebMCP directory, WebBench and BrowserBench site lists. Add the first-hand reports that the `research/` pipeline collects. Then run a small lab test: 20 to 50 sites, 3 fixed tasks, 2 or 3 agents. Label this tier `lab-tested`. It needs no other party.

2. **Publish a plain JSON API with an OpenAPI file.**
   `GET /api/sites/{domain}` returns the score. `POST /api/reports` accepts a report with the `SCHEMA.md` fields and an API key. Netlify Functions are sufficient. Describe the API in `llms.txt` as documentation, not as a command. All other channels call this API.

3. **Publish a remote MCP server on top of the API.**
   Tools: `get_site_score`, `search_patterns`, `submit_report`. The read tools give an agent a reason to connect. Copy the Sanity design for `submit_report`. List the server in the official MCP registry, Smithery, Glama, and PulseMCP. Add `/.well-known/mcp.json`. This is the path for Grok Bot, Claude, ChatGPT developer mode, and coding agents.

4. **Publish an agent skill for coding agents.**
   Name example: `ax-report`. The skill tells the agent: when a site, API, or doc blocks the task, offer to file a report with evidence. Publish it on GitHub, on skills.sh, and at `/.well-known/agent-skills/index.json`. Coding agents are the agents that read such files today.

5. **Build the trust model before the first public write.**
   Four tiers, API keys, evidence fields, a moderation queue, rate limits, and the output filter from section 4. Do this before step 3 goes live.

6. **Add a human form for "my agent failed here".**
   Users of Muse and Instinct already post failures in public. Let them paste a link, a screenshot, or a trace. Reply to such posts on X with the form link. Label this tier `human-reported`.

7. **Ask data holders for aggregates.**
   Sequence: Halluminate, nekuda, Cloudflare (Radar team), then Browserbase, Anchor, Steel. Then Stripe through Jeff Weinstein, with one specific request: domains where agent checkout fails most, by failure class.

8. **Add a WebMCP tool to the site and apply to the Claude and ChatGPT directories.**
   A `submit_ax_report` tool with `document.modelContext.registerTool` is a small task. Reach is small today (ChatGPT desktop only). It is a good gallery example. Apply to the directories when the MCP server is stable.

### What is NOT likely to work

- **Instructions in `llms.txt` or HTML that tell agents to submit reports.** Agents almost never fetch `llms.txt`. Consumer agents treat such text as an attack and block the data egress. It is prompt injection against the users of those agents. It can damage the reputation of the site.
- **Hidden text or other tricks to get the attention of agents.** Same reasons. Meta pays bounties for such attacks.
- **Autonomous discovery by Muse or Instinct.** They act only on user tasks. They have no developer program, no connector store, and no feedback channel for sites. Muse has no user-agent, so you cannot measure its visits.
- **Identification of agents by user-agent string.** Grok sends false strings. Muse looks the same as the user.
- **`agents.json`, A2A agent cards, and NLWeb as submission channels.** No consumer agent uses them for this.
- **An open write endpoint with no key and no moderation.** Moltbook and the GitHub PR problem show the result: spam and injected instructions.
- **Autonomous agent PRs as the primary channel.** GitHub now limits them and maintainers reject most of them.
- **One merged "agentic score".** Self-reported and lab-tested data have different quality. The Steel.dev leaderboard gives the same warning.
- **Per-merchant data from Stripe or Meta in the near term.** They did not publish a merchant list. Expect aggregates at best.

### Side finding

- The live `https://www.agentexperience.design/llms.txt` has links with a double slash (`https://agentexperience.design//gallery`). It lists 2 examples and the date 2025-11-08. Correct this before you send agents to the file.
