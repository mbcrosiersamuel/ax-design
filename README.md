# ax.design - Agent Experience Design Patterns

A curated collection of Agent Experience (AX) design patterns showcasing best practices and anti-patterns for the agentic web.

**Live Site:** https://agentexperience.design

## About

ax.design demonstrates real-world examples of both excellent and poor agent-friendly design, helping developers build better experiences for AI agents, bots, and automated systems.

## Features

- **Curated Examples**: Real-world patterns categorized as Good AX and Bad AX
- **Agent-Friendly**: Built with AX best practices
  - RSS and JSON feeds (`/feed.xml`, `/feed.json`)
  - Machine-readable formats
  - Agent guidance file (`/llms.txt`)
  - Sitemap and robots.txt
- **Modern Stack**: Built with Astro, TypeScript, and modern web standards
- **Responsive Design**: Mobile-first, accessible, and fast
- **Component-Based**: Modular, reusable components with a consistent design system

## Tech Stack

- **Framework**: [Astro](https://astro.build) 4.x
- **Language**: TypeScript (strict mode)
- **Deployment**: Netlify
- **Styling**: CSS with design tokens
- **Fonts**: Space Grotesk, Inter, JetBrains Mono

## Project Structure

```
/
├── public/
│   ├── llms.txt           # Agent guidance file
│   ├── robots.txt         # Crawler directives
│   └── favicon.svg        # Site favicon
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Button.astro
│   │   ├── Card.astro
│   │   ├── Header.astro
│   │   ├── Modal.astro
│   │   └── SubscribeForm.astro
│   ├── content/
│   │   ├── config.ts      # Content collection schema
│   │   └── posts/         # Markdown posts
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── pages/
│   │   ├── index.astro    # Homepage
│   │   ├── about.astro    # About page
│   │   ├── gallery/
│   │   │   ├── index.astro     # Gallery overview
│   │   │   └── [slug].astro    # Post detail pages
│   │   ├── feed.xml.ts    # RSS feed
│   │   └── feed.json.ts   # JSON feed
│   └── styles/
│       ├── tokens.css     # Design tokens
│       └── global.css     # Global styles
├── astro.config.mjs
├── tsconfig.json
└── package.json
```

## Getting Started

### Prerequisites

- Node.js 20+
- npm or pnpm

### Installation

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Adding Content

### Creating a New Post

1. Create a new Markdown file in `src/content/posts/`
2. Add frontmatter with required fields:

```yaml
---
title: "Your Post Title"
company: "Company Name"
verdict: "good"  # or "bad"
summary: "Brief summary of the example"
date: 2025-10-23
tags: ["api", "schema.org"]
sources:
  - "https://example.com/source"
---
```

3. Write your content in Markdown
4. The post will automatically appear in the gallery

## Design System

The project uses a comprehensive design system with CSS custom properties:

- **Colors**: Neutral palette with semantic color tokens
- **Typography**: Three-tier font system (display, body, mono)
- **Spacing**: Consistent 4px-based scale
- **Components**: Reusable, modular components with variants

## Deployment

The site is configured for Netlify deployment:

1. Push to GitHub
2. Connect repository to Netlify
3. Build settings are in `netlify.toml`
4. Automatic deployments on push

### Environment Variables

No environment variables required for basic deployment. For the subscribe form to work, ensure Netlify Forms is enabled in your Netlify settings.

## Agent-Friendly Features

This site practices what it preaches:

- **llms.txt**: Agent guidance at `/llms.txt`
- **Feeds**: RSS (`/feed.xml`) and JSON Feed (`/feed.json`)
- **Sitemap**: Auto-generated at `/sitemap.xml`
- **Structured Data**: Semantic HTML throughout
- **Copy as Markdown**: Every post can be copied as Markdown
- **Responsive**: Works on all device sizes

## Contributing

Interested in contributing examples? Here's how:

1. Fork the repository
2. Create a new post in `src/content/posts/`
3. Follow the frontmatter schema
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Created and maintained by **M.P. Samuel**

Inspired by [Mathias Biilmann](https://twitter.com/biilmann)'s writing on Agent Experience.

---

Built with [Astro](https://astro.build) and deployed on [Netlify](https://netlify.com)
