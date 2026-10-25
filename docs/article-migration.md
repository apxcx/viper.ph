# Article migration and rendering

The site renders **216 migrated published articles** at their original root slugs through `src/pages/[slug].astro`, using the approved `ArticleLayout.astro`. The eight original categories share the imported inventory. Each category root has a three-story hero; the remaining list shows up to 10 posts per page. Later pages use `/category/<slug>/page/<number>/`, keep the hero/sidebar, and include numbered plus previous/next links. Each paginated URL has its own canonical link. The route manifest contains 245 pages: 216 posts, 8 category roots, 16 additional category pages, the homepage, and 4 utility/legal pages.

`public/sitemap.xml` lists all 245 public routes at the canonical `https://viper.ph` origin. `public/robots.txt` allows public crawling, disallows `/api/`, and points crawlers to `https://viper.ph/sitemap.xml`. Submit `https://viper.ph/sitemap.xml` in Google Search Console after this checkpoint is deployed to the `viper.ph` domain.

## Preserved source data

`src/content/articles/*.md` retains the original migration frontmatter and article text. Only the leading export H1 is moved into the layout's title header to avoid duplicate H1s. The source publication/modified dates, author, category/tag assignments, canonical URLs, and available SEO/Open Graph values remain in frontmatter. Ten oldest exports captured a Cloudflare challenge title rather than SEO data; those raw values are retained, but public pages use a proper title and source-text description fallback.

Inline content images were excluded in the migration batches. Each original featured-image reference remains available through its `featured_image_key`.

## Image delivery

Production article, archive, homepage, and related-card images use `/api/media/<featured_image_key>`. The read-only Worker endpoint uses the existing `MEDIA` binding to the Cloudflare R2 `media` bucket. It restricts reads to imported public featured-image keys, sets image MIME and ETag headers, and supports HEAD and conditional GET. No Cloudflare API token is shipped to the browser or required by the production binding.

Preview uses `scripts/r2-preview.mjs` to serve already-verified local image mirrors. Its machine-local `.r2-preview-map.json` is Git-ignored; source image binaries are not duplicated in the repository. This development mirror does not prove a live production R2 request. The existing objects were checksum-verified in the migration batches; an additional remote Wrangler read during this rollout timed out without modifying the bucket.

## Reimporting source batches

From the project root, pass the paths to the three verified migration folders:

```sh
python3 scripts/import-migrated-articles.py /path/to/batch-01 /path/to/ai-ev-fintech /path/to/final-remaining
```

The importer checks unique slugs, writes normalized Markdown, refreshes `src/data/post-index.json`, creates the local Preview image map, and regenerates article, category, and page-numbered archive manifest entries. It does not upload or delete R2 objects.

## Checks

```sh
pnpm check
pnpm build
python3 scripts/verify-article-rollout.py
node --experimental-strip-types scripts/verify-media-endpoint.mjs
pnpm exec wrangler deploy --dry-run
```

The Python verification requires Beautiful Soup (`beautifulsoup4`). Node 22.13+ supports the isolated endpoint test's TypeScript stripping flag. The endpoint test uses mock R2 objects; it never makes a remote bucket request or sends newsletter/contact submissions.
