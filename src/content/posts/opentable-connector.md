---
title: "A connector instead of a block"
companies:
  - name: "OpenTable"
verdict: "good"
summary: "OpenTable's website blocks browser agents. Its Muse connector books tables without a block. Two doors on one building."
date: 2026-09-21
tags: ["connector", "bot-block", "booking"]
pattern: "agent-path"
sources:
  - "https://x.com/_CallMeMacy/status/2101757585611444724"
  - "https://x.com/Yairyup/status/2101836223874572691"
  - "https://x.com/jdpeterson/status/2101843085575750140"
  - "https://x.com/milliemyang/status/2100323121979129959"
  - "https://www.reddit.com/r/openclaw/comments/1rxhdaf/solved_my_personal_pain_of_booking_restaurant_for/"
---

On 20 September 2026, the most-liked complaint about agents on the web named OpenTable:

> Yo @Delta and @OpenTable please stop blocking my agents 🙏🙏🙏🙏 this is the future.
>
> [@_CallMeMacy](https://x.com/_CallMeMacy/status/2101757585611444724), 575 likes

The replies gave the other half of the story:

> OpenTable has a Muse connector that works without any blocks (for fair use)
>
> [@Yairyup](https://x.com/Yairyup/status/2101836223874572691)

> Muse has an OpenTable connector and it works great
>
> [@jdpeterson](https://x.com/jdpeterson/status/2101843085575750140)

## Why this is good AX

OpenTable did not choose between "block all agents" and "let scrapers hammer the booking page". It blocked the browser path and opened a structured one. The connector knows what an agent may do (search, book, cancel) and at what rate. The website does not have to guess.

The cost of not doing this shows in the same week: one user's OpenTable account was blocked because their agent "scanned a couple of hundred times" ([@milliemyang](https://x.com/milliemyang/status/2100323121979129959)). A connector with a rate limit turns that ban into a polite "slow down".

## What it looks like from the agent side

An OpenClaw user wrote a booking skill against their own logged-in OpenTable account and booked three restaurants in one day ([r/openclaw](https://www.reddit.com/r/openclaw/comments/1rxhdaf/solved_my_personal_pain_of_booking_restaurant_for/)). The demand is there. The connector is the safe way to meet it.

## The gap

The connector exists only inside Muse. Instinct, Grok Bot, and Claude users still hit the block. The next step is one public API or MCP server that every agent can use.
