---
title: "Docs as files, over SSH"
companies:
  - name: "Supabase"
    logo: "/images/logos/supabase.svg"
verdict: "good"
summary: "Supabase serves its documentation as a filesystem of Markdown over SSH. The agent reads docs the same way it reads code: ls, cat, grep."
date: 2026-09-21
tags: ["docs", "markdown", "cli"]
pattern: "dashboard-only"
sources:
  - "https://www.reddit.com/r/Supabase/comments/1s9ni4o/we_shipped_an_ssh_server_for_supabase_docs/"
  - "https://www.reddit.com/r/mcp/comments/1m75ww6/just_used_supabase_mcp_didnt_even_open_the/"
---

> Every page is a markdown file. Your agent navigates them the same way it navigates your code.
>
> Supabase staff, [r/Supabase](https://www.reddit.com/r/Supabase/comments/1s9ni4o/we_shipped_an_ssh_server_for_supabase_docs/)

## Why this is good AX

Coding agents already have a perfect interface for text: the shell. `ls` lists the sections, `cat` reads a page, `grep` finds the one line about connection pooling. There is no HTML to strip, no JavaScript to render, no search box to operate, and no 28,000-token tool result.

That last point matters. In the same dataset, Supabase's own MCP `search_docs` tool got complaints for the size of its results. The SSH server is the opposite design: the agent pulls only the file it needs.

## The pattern

1. Write docs in Markdown. Most teams already do.
2. Serve the source, not the rendered page. A Git repository, an SSH server, or a plain `.md` URL for each page all work.
3. Give the agent a map: an index file at the root, with one line per page.

`llms.txt` was meant to be that map. Server logs show that crawlers almost never read it, but coding agents do.

## Related

Supabase's MCP server and CLI get the same praise for setup: "All without ever opening the Supabase dashboard" ([r/mcp](https://www.reddit.com/r/mcp/comments/1m75ww6/just_used_supabase_mcp_didnt_even_open_the/)). Docs, setup, and data all have a path that does not need a browser.
