import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const prerender = true;

export const GET: APIRoute = async ({ site }) => {
  const posts = await getCollection('posts');
  const baseUrl = site?.toString() || 'https://agentexperience.design';

  // Sort posts by date, newest first
  const sortedPosts = posts.sort((a, b) =>
    b.data.date.getTime() - a.data.date.getTime()
  );

  // Separate good and bad examples
  const goodExamples = sortedPosts.filter(p => p.data.verdict === 'good');
  const badExamples = sortedPosts.filter(p => p.data.verdict === 'bad');

  const content = `# agentexperience.design

> A curated collection of real-world Agent Experience (AX) design patterns, showcasing examples of both excellent and poor agent-friendly design to help developers build better experiences for AI agents and automated systems.

Agent Experience (AX) refers to how well your website or application works for AI agents, bots, and other automated systems. Good AX design incorporates structured content in plain text, machine-readable formats, and ensures agents can access the content, context, and actions they need to act as delegates for humans.

## Site Pages

- [Home](${baseUrl}): Introduction to Agent Experience design
- [Gallery](${baseUrl}/gallery): Browse all examples organized by Good AX and Bad AX
- [About](${baseUrl}/about): Information about the project and AX principles

## Machine-Readable Formats

- [RSS Feed](${baseUrl}/feed.xml): RSS 2.0 feed of all examples
- [JSON Feed](${baseUrl}/feed.json): JSON Feed format for easy parsing
- [Sitemap](${baseUrl}/sitemap.xml): Complete sitemap for crawling

## Good AX Examples

${goodExamples.map(post =>
  `- [${post.data.title}](${baseUrl}/gallery/${post.slug}): ${post.data.summary}`
).join('\n')}

## Bad AX Examples

${badExamples.map(post =>
  `- [${post.data.title}](${baseUrl}/gallery/${post.slug}): ${post.data.summary}`
).join('\n')}

---

Last updated: ${new Date().toISOString().split('T')[0]}
Total examples: ${posts.length} (${goodExamples.length} good, ${badExamples.length} bad)
`;

  return new Response(content, {
    status: 200,
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
};
