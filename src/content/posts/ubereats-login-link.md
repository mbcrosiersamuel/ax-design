---
title: "A login link lets the agent in"
companies:
  - name: "Uber Eats"
verdict: "good"
summary: "Uber Eats logs the agent in with a link sent to the user's email. An agent with an inbox gets through. An agent that must ask the user for a code does not."
date: 2026-09-21
tags: ["login", "email", "delegated-access"]
pattern: "delegated-login"
sources:
  - "https://x.com/chandnirao_here/status/2101146127739277690"
  - "https://x.com/chandnirao_here/status/2101146288008147374"
---

One person gave the same task to two agents: order dinner on Uber Eats.

> Instinct: easy authentication to ue (link to email), quick search for items, cart addition, hands the final cart back to me to verify.
>
> [@chandnirao_here](https://x.com/chandnirao_here/status/2101146127739277690)

Muse, which does not read the user's email, was asked for a verification code, then met a CAPTCHA, and gave the task back.

## Why this is good AX

The login link by email is an old pattern, and it is agent-friendly by accident. It needs no password, no authenticator app, and no code that expires before the person can paste it. An agent that has an inbox (Instinct gives each agent its own email address) completes the loop by itself.

The same site with the same login is a wall for an agent without an inbox. That is the second lesson: the site did not become agent-friendly. One agent's design matched one site's login.

## What a site can add

- Keep the email link. Make it live for 15 minutes, not 60 seconds.
- Let the user mark the agent's browser as a trusted device, so the second order does not need a link at all.
- Do not put a CAPTCHA behind a valid login link. The link already proves possession of the inbox.

See also [Login walls and verification codes](/patterns/login-and-codes).
