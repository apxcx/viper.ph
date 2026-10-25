# Viper.ph Astro publisher

The Astro project is the authoritative Viper.ph publisher. It does not call WordPress, use WordPress application passwords, update Rank Math, upload WordPress media, or depend on a WordPress schedule. The existing `MEDIA` binding remains the only application image store: Cloudflare R2 bucket `media`, exposed to the site through the read-only same-origin `/api/media/...` endpoint.

## Editorial contract

For each daily run, research the top three distinct technology stories from the previous 24 hours. Prefer Philippine mainstream, government, business, and official company sources; include a strong Philippine-focused story when available. Before drafting, compare the proposed title, slug, focus keyword, and source URLs against `src/data/post-index.json` and the current Markdown collection. Do not republish a materially identical story. The quick comparison helper is `python3 scripts/check-astro-duplicates.py --title "Proposed headline" --focus-keyword "keyword"`; review its highest-scoring matches before writing.

New articles belong in `src/content/articles/<slug>.md` and use `publisher_status: ready` before publication. The authoritative categories are:

- PH Tech
- Telcos and Internet
- Fintech and Banking Tech
- Gadgets
- E-commerce
- Apps and Software
- AI
- International Tech
- Tech Events
- Electric Vehicles

Legacy migrated labels and source metadata remain in the existing files for provenance. They are not used as a runtime publishing dependency.

A ready article must include:

- a lowercase hyphenated slug;
- a headline under 60 characters;
- `focus_keyword`;
- an `seo_title` ending in ` | Viper` and no longer than 60 characters;
- an `seo_description` between 145 and 155 characters;
- an ISO-8601 Manila date with `+08:00` and `publication_slot: "06:00"`, `"08:00"`, or `"10:00"`;
- at least one HTTPS source object in `sources`;
- exactly four paragraphs of 80–110 words each, with exactly one relevant image immediately after each paragraph;
- four `images` records with rights-cleared status, source URL, credit, license, dimensions, and the same public URLs used in the body;
- a featured R2 image using the deterministic `articles/YYYY/MM/<slug>/featured.ext` key.

The public image URLs use the existing Worker endpoint and never expose R2 credentials:

```text
https://viper.ph/api/media/articles/YYYY/MM/<slug>/featured.ext
https://viper.ph/api/media/articles/YYYY/MM/<slug>/image-1.ext
https://viper.ph/api/media/articles/YYYY/MM/<slug>/image-2.ext
https://viper.ph/api/media/articles/YYYY/MM/<slug>/image-3.ext
https://viper.ph/api/media/articles/YYYY/MM/<slug>/image-4.ext
```

## Deterministic recovery and idempotency

`src/data/publisher-manifest.json` is generated without timestamps. Each entry has a `slot_key` and `idempotency_key` such as `2026-10-26/06:00`, plus slug, title, status, category, source count, image count, and body hash. The manifest has a `days` lookup for recovery and duplicate checks. `scripts/publish-astro-article.py` refuses a duplicate slot or a slug moved to another slot; retrying the exact same file is a no-op.

For an image folder containing `featured.jpg` and `image-1.jpg` through `image-4.jpg`, upload deterministic objects before installing the Markdown:

```bash
pnpm exec wrangler r2 object put media/articles/2026/10/<slug>/featured.jpg --file ./images/featured.jpg --remote --content-type image/jpeg
pnpm exec wrangler r2 object put media/articles/2026/10/<slug>/image-1.jpg --file ./images/image-1.jpg --remote --content-type image/jpeg
pnpm exec wrangler r2 object put media/articles/2026/10/<slug>/image-2.jpg --file ./images/image-2.jpg --remote --content-type image/jpeg
pnpm exec wrangler r2 object put media/articles/2026/10/<slug>/image-3.jpg --file ./images/image-3.jpg --remote --content-type image/jpeg
pnpm exec wrangler r2 object put media/articles/2026/10/<slug>/image-4.jpg --file ./images/image-4.jpg --remote --content-type image/jpeg
```

The deterministic R2 key is safe to retry: the same key is the same article asset. The public Markdown URL remains the same after a retry.

## Commands

Set up the local publisher tooling once:

```bash
python3 -m pip install --user -r scripts/requirements.txt
```

Regenerate the index and day/slot manifest after adding or replacing content:

```bash
pnpm publisher:index
pnpm publisher:manifest
pnpm publisher:routes
```

Validate every ready article, source link, R2 URL, rights-cleared image record, paragraph word count, image order, and approximately 16:9 dimensions. `--network` fetches every ready image and verifies the returned bytes and dimensions:

```bash
pnpm publisher:check
```

Install a ready Markdown file idempotently by slug and slot. The command also rebuilds the index and manifest and performs network image validation:

```bash
pnpm publisher:publish -- /absolute/path/to/article.md
# Same slug, intentionally revised body:
pnpm publisher:publish -- --replace /absolute/path/to/article.md
```

Before a GitHub push, run the full content preparation and application checks:

```bash
pnpm publisher:prepare
pnpm check
pnpm build
pnpm exec wrangler deploy --dry-run

git add src/content/articles src/data/post-index.json src/data/publisher-manifest.json public/manus-routes.json public/sitemap.xml public/robots.txt
git commit -m "Publish Viper Astro articles"
git fetch origin main && git merge --ff-only origin/main && git push origin HEAD:main
```

The existing GitHub remote is the Manus canonical remote for `apxcx/viper.ph`; the repository's existing Cloudflare Worker workflow remains unchanged. Daily scheduling is intentionally disabled until this migration is verified.
