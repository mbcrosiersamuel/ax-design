import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = await getCollection('posts');
  const sortedPosts = posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());

  return rss({
    title: 'ax.design - Agent Experience Patterns',
    description: 'Agent Experience design patterns and best practices for the agentic web',
    site: context.site!,
    items: sortedPosts.map((post) => ({
      title: post.data.title,
      description: post.data.summary,
      pubDate: post.data.date,
      link: `/gallery/${post.slug}/`,
      categories: post.data.tags,
      customData: `
        <company>${post.data.company}</company>
        <verdict>${post.data.verdict}</verdict>
      `,
    })),
    customData: `<language>en-us</language>`,
  });
}
