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
    publisher_status: z.enum(['draft', 'ready', 'published', 'legacy-migrated']).optional(),
    focus_keyword: z.string().optional(),
    publication_slot: z.enum(['06:00', '08:00', '10:00']).optional(),
    featured_image_key: z.string(),
    featured_image_url: z.string().url().optional(),
    featured_image_alt: z.string().optional(),
    featured_image_license: z.string().optional(),
    featured_image_credit: z.string().optional(),
    featured_image_width: z.number().optional(),
    featured_image_height: z.number().optional(),
    sources: z.array(z.object({
      title: z.string().optional(),
      url: z.string().url(),
      publisher: z.string().optional(),
    })).optional(),
    images: z.array(z.object({
      url: z.string().url(),
      alt: z.string(),
      source_url: z.string().url(),
      credit: z.string(),
      license: z.string(),
      rights_cleared: z.boolean(),
      width: z.number().int(),
      height: z.number().int(),
    })).optional(),
  }).passthrough(),
});

export const collections = { articles };
