import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    date: z.string(),
    modified: z.string().optional(),
    author: z.string().optional(),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    seo_title: z.string().optional(),
    seo_description: z.string().optional(),
    seo_robots: z.string().optional(),
    og_title: z.string().optional(),
    og_description: z.string().optional(),
    canonical_url: z.string().optional(),
    featured_image_key: z.string(),
    featured_image_alt: z.string().optional(),
    featured_image_width: z.number().optional(),
    featured_image_height: z.number().optional(),
  }).passthrough(),
});

export const collections = { articles };
