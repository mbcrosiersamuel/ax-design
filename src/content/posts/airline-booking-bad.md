---
title: "Hidden fees and captcha walls"
companies:
  - name: "Legacy Airlines Inc"
verdict: "bad"
summary: "Multi-step booking flows with inconsistent pricing, aggressive captchas, and no structured data make agent booking nearly impossible."
date: 2025-10-18
tags: ["booking", "anti-pattern", "captcha"]
sources:
  - "https://example.com/airlines"
---

## What Goes Wrong

Many legacy airline booking systems present a masterclass in agent-hostile design. The combination of aggressive bot detection, inconsistent pricing, and zero machine-readable alternatives creates a frustrating experience for both humans and agents.

### Problems

1. **Aggressive Captchas**: Every search triggers multiple captcha challenges
2. **Dynamic Pricing**: Prices change between search and checkout with no API access
3. **Session Timeouts**: Short timeout windows force rushed decisions
4. **No Structured Data**: Flight information buried in HTML tables with inconsistent markup
5. **JavaScript-Required**: No fallback for non-JS environments

### The Agent Experience

An agent attempting to book a flight encounters:

- Captcha after captcha, making automated booking impossible
- Flight prices that differ from search to booking page
- Hidden fees that only appear at final checkout
- No JSON endpoints or RSS feeds to track prices
- Seat selection interfaces that require mouse interaction

### Missing Opportunities

```html
<!-- What we get -->
<div class="flight">Flight 123 to LAX - Check price</div>

<!-- What we need -->
<div itemscope itemtype="https://schema.org/Flight">
  <meta itemprop="flightNumber" content="123" />
  <meta itemprop="destination" content="LAX" />
  <data itemprop="price" value="299.00">$299</data>
</div>
```

## How to Fix This

- Provide JSON endpoints for flight search and pricing
- Use schema.org Flight markup for structured data
- Implement rate limiting instead of blanket captchas
- Offer RSS feeds for price tracking
- Create agent-friendly booking APIs
