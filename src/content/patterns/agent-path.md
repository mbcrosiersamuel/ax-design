---
title: "Close the scrape path, open an agent path"
kind: good
summary: "Block agents in the browser if you must, but give them an API, an MCP server, or a connector. The same site can be the worst and the best example."
wallTag: "Connector or skill"
order: 10
---

## What people report

> OpenTable has a Muse connector that works without any blocks (for fair use)
>
> [@Yairyup on X](https://x.com/Yairyup/status/2101836223874572691)

> Muse has an OpenTable connector and it works great
>
> [@jdpeterson on X](https://x.com/jdpeterson/status/2101843085575750140)

## How to do it

1. Decide what an agent may do: search, book, cancel, pay.
2. Put those actions in an API or an MCP server with scopes.
3. Publish it where agents look: the MCP registries, an agent skill, `/.well-known/`.
4. Then block the scrape path with a clear message that names the agent path.
