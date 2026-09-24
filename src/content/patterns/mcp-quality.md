---
title: "MCP servers that agents avoid"
kind: anti
summary: "The MCP server exists, but it is too large, too small, needs a browser to log in, or returns data from the wrong project."
wallTag: "Mcp token bloat"
order: 6
---

## What people report

> nothing tells you which store a tool call actually hit. We've had a global config quietly win over the project one and pull from the wrong shop. No error, just wrong numbers.
>
> [u/datagekko on Reddit](https://www.reddit.com/r/shopify/comments/1wjidu6/how_to_connect_multiple_stores_to_claude_code_via/paq4g7r/)

> it will confidently wire a node that does not have the field it thinks it has. About one in three of my generated workflows needed manual repair.
>
> [r/n8n](https://www.reddit.com/r/n8n/comments/1wcrnvw/does_anyone_use_n8nmcp_to_enable_ai_to/p948mv3/)

> For authoring it's slower than me and the bill is real, a session in February to add four nodes cost $11.
>
> [r/n8n](https://www.reddit.com/r/n8n/comments/1wcrnvw/does_anyone_use_n8nmcp_to_enable_ai_to/pag9gyh/)

## Do this instead

- Few tools, small responses. Ten good tools beat eighty thin ones.
- Full write coverage with scopes, and a read-only mode.
- A login that works in a terminal: device code flow or a pasted token.
- Put the project or store name in every response.
