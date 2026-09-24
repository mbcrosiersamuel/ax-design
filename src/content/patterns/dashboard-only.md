---
title: "Dashboard-only actions"
kind: anti
summary: "The coding agent must stop, and the person must click through a web console to create a key, submit a build, or change a setting."
wallTag: "Dashboard only"
order: 5
---

## What people report

> used supabase and vercel, but honestly that was just Claude telling me click this, paste that, run this command, the whole way through.
>
> [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1w6kavj/ive_basically_been_making_ai_slop_with_claude/)

> What really helped - giving Claude access to all the tools it wanted and letting it do most of the work. gh, cloudflair wrangler, Supabase cli, and full access to the new projects
>
> [r/Supabase](https://www.reddit.com/r/Supabase/comments/1wkid2y/four_hours_to_move_my_project_from_lovable_to/)

> The sites are served through Cloudflare, but the domains do not appear in my personal Cloudflare dashboard.
>
> [r/CloudFlare](https://www.reddit.com/r/CloudFlare/comments/1wd2bpf/how_do_i_opt_out_of_ai_crawler_blocking_for/)

## Do this instead

- Each dashboard action gets an API or CLI equivalent. If a person can click it, an agent can call it.
- Give a CLI login (`vercel login`, `gh auth login`) and scoped keys that a person approves one time.
- Show the person the exact command, not a page of screenshots.
