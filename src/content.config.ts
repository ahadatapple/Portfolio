import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    order: z.number().int(),
    // One sentence, shown under the title and on the home page card.
    result: z.string(),
    // The single number shown in the first-screen project row.
    rowLine: z.string(),
    summary: z.string(),
    role: z.string(),
    org: z.string(),
    dates: z.string(),
    stack: z.array(z.string()).min(1),
    status: z.string().optional(),
    links: z
      .array(z.object({ label: z.string(), href: z.url() }))
      .default([]),
    description: z.string().max(160),
  }),
});

export const collections = { projects };
