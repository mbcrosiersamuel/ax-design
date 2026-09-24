---
title: "Bot block with no agent path"
kind: anti
summary: "The site returns 403, 503, or a challenge page to the agent. The agent stops, and the user goes to a competitor."
wallTag: "Bot block"
order: 1
---

## What people report

> Delta seems to do a great job of blocking every agent I've tried.
>
> [@owendesign on X](https://x.com/owendesign/status/2101409822625173815)

> I just tried Best Buy today with no luck. Apparently Best Buy has a bot detection which Muse cannot bypass or click around.
>
> [@cj_streetpoet on X](https://x.com/cj_streetpoet/status/2101830169119863201)

> Thumbtack and Yelp block instinct. Would love to find yellow page services that welcome agents.
>
> [@suvirjain on X](https://x.com/suvirjain/status/2101707913660453130)

## Do this instead

- Separate training crawlers from live user agents. Permit signed agents (Web Bot Auth) and known user agents such as `ChatGPT-User` and `Claude-User`.
- If you block the browser path, give an agent path: an API, an MCP server, or a connector. [OpenTable](/gallery/opentable-connector) does this.
- Test your own site with a real agent each month. A default block is easy to miss.
