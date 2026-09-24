import { defineCollection, z } from 'astro:content';

const companySchema = z.object({
  name: z.string(),
  logo: z.string().optional(), // Path to logo image, e.g., "/images/logos/stripe.svg"
});

const postsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    companies: z.array(companySchema).min(1).max(3), // Support 1-3 companies with logos
    verdict: z.enum(['good', 'bad']),
    summary: z.string(),
    date: z.date(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    sources: z.array(z.string()).default([]),
    pattern: z.string().optional(), // slug of the related pattern page
  }),
});

// A pattern is one thing that stops agents (kind: anti) or one thing that lets them through (kind: good).
const patternsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    kind: z.enum(['anti', 'good']),
    summary: z.string(), // one sentence: what occurs
    wallTag: z.string(), // the label used on /wall; the count and link come from there
    order: z.number().default(99),
  }),
});

export const collections = {
  posts: postsCollection,
  patterns: patternsCollection,
};
