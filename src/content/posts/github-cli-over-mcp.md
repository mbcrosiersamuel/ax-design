---
title: "Agents prefer the CLI"
companies:
  - name: "GitHub"
verdict: "good"
summary: "GitHub has an MCP server with more than 80 tools. Agents and their users keep choosing the gh CLI instead. The maintainers agree."
date: 2026-09-21
tags: ["cli", "mcp", "devtools"]
pattern: "mcp-quality"
sources:
  - "https://www.reddit.com/r/mcp/comments/1mj0fxs/i_spent_3_weeks_building_my_dream_mcp_setup_and/n7935ux/"
  - "https://www.reddit.com/r/mcp/comments/1mj0fxs/i_spent_3_weeks_building_my_dream_mcp_setup_and/n7yl2f9/"
---

> I stopped using the GitHub mcp and just use gh cli. I find that my agent is much better with the cli vs the mcp.
>
> [r/mcp](https://www.reddit.com/r/mcp/comments/1mj0fxs/i_spent_3_weeks_building_my_dream_mcp_setup_and/n7935ux/), score 11

The GitHub MCP maintainer replied in the same thread: "most agents are pretty great at gh cli commands." ([r/mcp](https://www.reddit.com/r/mcp/comments/1mj0fxs/i_spent_3_weeks_building_my_dream_mcp_setup_and/n7yl2f9/))

## Why the CLI wins

- **Cost.** Eighty tool definitions sit in the context on every turn. `gh` costs nothing until it is called.
- **Training.** Agents have read millions of `gh pr create` commands. They have read the MCP tool list only in the current session.
- **Composition.** `gh api ... | jq` does things no fixed tool list can. The shell is the agent's native interface.
- **Login.** `gh auth login` works in a terminal. The device code flow needs no browser redirect.

## Why this is good AX

GitHub did not have to choose. It ships both. The lesson for other vendors is the order: a good CLI first, then a small MCP server for the cases where a typed tool call is better than a shell command. Reports in the dataset name the same problem at Atlassian (17,000 tokens of tool definitions) and Notion.

See [MCP servers that agents avoid](/patterns/mcp-quality).
