import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async ({ site }) => {
  const base = (site?.toString() || 'https://agentexperience.design').replace(/\/$/, '');
  const patterns = (await getCollection('patterns')).sort((a, b) => a.data.order - b.data.order);
  const posts = (await getCollection('posts')).sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
  const body = {
    patterns: patterns.map((p) => ({
      slug: p.slug,
      url: `${base}/patterns/${p.slug}`,
      title: p.data.title,
      kind: p.data.kind === 'anti' ? 'stops agents' : 'lets them through',
      summary: p.data.summary,
      wallTag: p.data.wallTag,
      body: p.body,
    })),
    examples: posts.map((p) => ({
      slug: p.slug,
      url: `${base}/gallery/${p.slug}`,
      title: p.data.title,
      companies: p.data.companies.map((c) => c.name),
      summary: p.data.summary,
      date: p.data.date.toISOString().slice(0, 10),
      pattern: p.data.pattern ?? null,
    })),
  };
  return new Response(JSON.stringify(body, null, 2), {
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=3600' },
  });
};
