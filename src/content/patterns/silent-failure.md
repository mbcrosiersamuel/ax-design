---
title: "Silent failure"
kind: anti
summary: "The site blocks the action but shows no error, or shows a general error page. The agent cannot tell the user what occurred."
wallTag: "Unclear error"
order: 2
---

## What people report

> Their bot protection silently blocks the login with no error shown
>
> [@SystemArch_AI on X](https://x.com/SystemArch_AI/status/2101363787467219099), about Costco

> Cloudflare was returning a 403 HTML block page, and the client was trying to parse it as JSON.
>
> [r/CloudFlare](https://www.reddit.com/r/CloudFlare/comments/1wcgl58/is_claudeuser_being_categorised_as_ai_crawler/)

> Muse enters information, Muse clicks "submit", "submit" stays enabled, Muse clicks it again (and again), site gives error, site says to contact the office by phone
>
> [@kevinyien on X](https://x.com/kevinyien/status/2101717033398235618), about Texas government sites

## Do this instead

- Return a real status code and a machine-readable cause (`application/problem+json` is enough).
- Say what to do next: "Log in as a person", "Use the API at ...", "Try again after 30 seconds".
- Disable a submit button after the first click. Show one clear result page.
