import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = await getCollection('posts');
  const sortedPosts = posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());

  const feed = {
    version: 'https://jsonfeed.org/version/1.1',
    title: 'ax.design - Agent Experience Patterns',
    home_page_url: context.site!.toString(),
    feed_url: `${context.site}feed.json`,
    description: 'Agent Experience design patterns and best practices for the agentic web',
    language: 'en',
    items: sortedPosts.map((post) => ({
      id: `${context.site}gallery/${post.slug}/`,
      url: `${context.site}gallery/${post.slug}/`,
      title: post.data.title,
      summary: post.data.summary,
      content_text: post.data.summary,
      date_published: post.data.date.toISOString(),
      tags: post.data.tags,
      _company: post.data.company,
      _verdict: post.data.verdict,
      _sources: post.data.sources,
      ...(post.data.heroImage && { image: `${context.site}${post.data.heroImage}` }),
    })),
  };

  return new Response(JSON.stringify(feed, null, 2), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
    },
  });
}
