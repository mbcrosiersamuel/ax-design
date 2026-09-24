---
title: "Login walls and verification codes"
kind: anti
summary: "The agent cannot log in, the 2FA code expires before the user gives it to the agent, or the session does not persist."
wallTag: "Login wall"
order: 3
---

## What people report

> a 2fa token that times out by the time i get it to them.
>
> [@TylerM on X](https://x.com/TylerM/status/2101152190517649751)

> I still have to log back in through the Grok computer at Kroger checkout. Persistent login would make it much better.
>
> [@MyPerfectGoatee on X](https://x.com/MyPerfectGoatee/status/2100204369148883287)

> Amazon works well with Muse but the 2fa is annoying
>
> [@lancehasson on X](https://x.com/lancehasson/status/2101764015126946283)

## Do this instead

- Give delegated access: OAuth with scopes, or an agent token with limits that the user approves one time.
- Let the user mark the agent's browser as a trusted device.
- Make codes live for 10 minutes, not 30 seconds. Offer email as well as SMS.
