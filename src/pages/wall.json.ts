import type { APIRoute } from 'astro';
import wall from '../data/wall.json';

export const GET: APIRoute = () =>
  new Response(JSON.stringify({ count: wall.length, posts: wall }, null, 2), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
