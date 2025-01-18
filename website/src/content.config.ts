import { glob } from 'astro/loaders';
import { defineCollection, z } from 'astro:content';
import type { Loader, LoaderContext } from 'astro/loaders';

const blog = defineCollection({
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	schema: z.object({
		title: z.string(),
		description: z.string(),
		// Transform string to Date object
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		heroImage: z.string().optional(),
	}),
});


const notes = defineCollection({
	loader: glob({ base: '../notes', pattern: '**/*.md' }),
	schema: z.object({
		title: z.string(),
		description: z.string().optional().nullable(),
		added: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		created_date: z.coerce.date().optional(),
		draft: z.boolean().default(true),
		tags: z.array(z.string()).optional(),
		image: z.string().optional().nullable(),
	}),
});

console.log('collections', { blog, notes });
export const collections = { blog, notes };
