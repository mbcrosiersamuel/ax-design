---
title: "Agent-Friendly Formats"
companies:
  - name: "Mintlify"
    logo: "/images/logos/mintlify.svg"
verdict: "good"
summary: "Mintlify builds documentation that's inherently agent- and AI-friendly, with auto-updating LLMs.txt files that make content discoverable and usable by LLMs and copy-to-ChatGPT buttons."
date: 2025-11-02
tags: ["documentation", "llms.txt", "markdown"]
sources:
  - "https://mintlify.com"
  - "https://llmstxt.org/"
---

## Excellence in Agent Experience

One great example of thoughtful agent experience design comes from Mintlify, a documentation provider that’s naturally incentivized to be early here. 

Many of Mintlify's clients, who use them for documentation, are developer tools and AI software companies. These companies, in turn, have end consumers who were early adopters of AI tools (e.g. software engineers), so Mintlify has invested meaningfully in exploring ways to improve the agent experience of their documentation on behalf of their clients.

## Agents ❤️ Structured Data

AI Agents love structured data. Formats like Markdown and HTML are easy for them to process and consume at high accuracy, since they are plain text and similar to the documents that AI models are trained on.

In contrast, sites that have a lot of Javascript, progressively unfolding features, or require lots of clicks present challenges for AI agents, even ones that have access to a browser use tool. 

One of the biggest investments that Mintlify has made in their documetation is incorporating structured data via LLMs.txt

### LLMs.Txt

While there are a number of emerging and competing standards for how to share information succinctly with AI agents (e.g. ), LLMs.txt is an emerging leader. 

The concept is simple: appending `/LLMs.txt` to your website's root URL / homepage should give you a lightweight, LLM-friendly links to each of the site's sub-pages with a brief summary of what they contain. This page should also update automatically as your site evolves.

Here's Mintlify's LLMs.txt file for their own docs: [https://www.mintlify.com/docs/llms.txt](https://www.mintlify.com/docs/llms.txt)

Mintlify also supports a less popular variant, **LLMs-Full**. This is an extended version, located at /`llms-full.txt` that also includes the contents of each page, so basically captures your entire site in one long markdown file.

Here's Mintlify's: [https://www.mintlify.com/docs/llms-full.txt](https://www.mintlify.com/docs/llms-full.txt)

Depending on the length of your documentation, this may be too much context for any one LLM at once, but it’s useful as a more comprehensive reference.

### The AX Impact

These small touches make it easier for LLMs to find, interpret, and use your content, and Mintlify supports them out of the box - both for their own site, and for their customers' sites, which is pretty cool.

![Screenshot of Mintlify's documentation showing the out-of-hte-box support for LLMs.txt](public/images/mintlify/llms-txt.png)

## An Aside: Copy Page Button

Another nice feature Mintlify is their 'Copy Page' / Markdown export functionality. This allows users to easily copy a markdown version of the page, or export that markdown directly into an AI tool of their choice:

![Mintlify buttons on the documentation showing options to copy paste as markdown for LLMs, open in ChatGPT, open in Claude, connect to Cursor, or connect to VSCode](public/images/mintlify/copy-page.png)

This is a UX benefit, not an AX one: it's designed for humans using AI tools, rather than AI-tool-first, but it's very nice for the transitional phase we're in today. 

A number of other sites that don't use Mintlify (such as Posthog, shown below) have also started to offer this. I suspect it will move beyond documentation to a wide range of websites soon:

![Posthog documentation page showing options to copy as markdown, view as markdown, open in ChatGPT, or open in Claude](public/images/mintlify/posthog-copy-page.png)

## Broader than Documentation

It's also worth noting that llms.txt isn't just for documentation sites. The official [LLMstxt site ](https://llmstxt.org/domains.html) includes a helpful example (reproduced below) from a Barbecue Restaurant to show how you might also include menus, helping LLMs offer users up to date info about your product offerings:

```
| Item              | Price         |
| --------------    | -----------   |
| Brisket           | 34            |
| Pork Spare Ribs   | 30            |
| Pulled Pork       | 28            |

## Drinks

| Item              | Price         |
| --------------    | -----------   |
| Iced Tea          | 3             |
| Mexican Coke      | 3             |

## Sides

| Item              | Price         |
| --------------    | -----------   |
| Potato Salad      | 4             |
| Slaw              | 4             |
```

## Best Practices Demonstrated

To summarize, Mintlify's out-of-the-box support for `llms.txt` reflects a few AX best practices:

- Building documentation in structured, LLM-friendly formats like markdown
- Keeping machine-readable content automatically updated  
- Treating docs as both human- and agent-facing interfaces  