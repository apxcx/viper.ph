# Viper.ph — premium editorial refinement

Refine the existing Astro/Tailwind homepage, without changing its Cloudflare Worker, R2, or MailerLite integration. Retain the exact H1 “The Daily Pulse of Philippine Tech”, background `#14171c`, button/highlight accent `#0000ff`, solid blue article-title panels, and the absence of article excerpts.

## Design direction

Dark editorial: a calm, precise technology publication rather than an agency template. Use Manrope for a confident grotesk display and DM Sans for readable interface text, with restrained Playfair Display italics in the masthead. Warm off-white typography and layered neutral charcoal balance the vivid blue; reserve blue for title panels, primary controls, and small signal marks. Preserve the asymmetric lead-story composition and two-column latest-news feed, but use deliberate stacked right-hand cards rather than sparse horizontal rows. Reduce secondary blue boxes, keep rules fine, give metadata and content consistent spacing, and apply subtle image-hover motion with reduced-motion support.

Use the existing approved logo and each story's matching homepage image. News and footer links should point to their published destinations, not invented placeholder routes.

## Footer content

Use only published homepage data from https://viper.ph/ (retrieved 25 October 2026): Viper's published description, `hi@viper.ph`, SM North / North Avenue / Epifanio de los Santos Ave / Quezon City 1105 Metro Manila, eight category destinations, social profiles, copyright, Events, Partnerships, Privacy Policy, and Terms and Conditions. The social X profile was also visible in the previous homepage browser extraction. No additional page scraping is required.

## Article pages

The Xiaomi POP Run page is the approved example. Extend its `ArticleLayout.astro` to all 216 published articles from the three verified migration batches (10 + 48 + 158 unique slugs). Store the original Markdown files under `src/content/articles/` and generate root-level static detail routes from their frontmatter via `src/pages/[slug].astro`. Preserve the source slugs, body text, publication and modified timestamps, author, category/tags, canonical URL and SEO/OG fields. The migration export's first Markdown H1 repeats the frontmatter title; move only that heading into the shared article header so each output has one H1, leaving the rest of each body unchanged. Each page uses the approved article title/byline header, original featured image, article body, shared sidebar, and three related posts chosen from the same category when possible.

Serve each featured image from its existing `featured_image_key` in the Cloudflare R2 `media` bucket using a same-origin `/api/media/...` Worker endpoint backed by the existing `MEDIA` binding. Do not duplicate the image binaries into the repository. Route homepage/category/related-story links to generated local article paths, retain the original source URL in migrated metadata, declare all 216 root article paths in `public/manus-routes.json`, and keep unknown slugs as real 404s.

The archives use the same imported post index, including all eight original categories, so breadcrumb/footer taxonomy links resolve locally. Preview-only middleware reads the verified local image mirrors using a Git-ignored map; production reads only the existing R2 binding. Ten oldest source snapshots captured a Cloudflare challenge instead of SEO metadata; retain those raw frontmatter values for provenance but render the article title and a source-text description fallback rather than challenge-page titles.

## Project structure

- `src/pages/index.astro`: homepage composition and existing newsletter form.
- `src/components/Header.astro`: logo, navigation, and responsive controls.
- `src/components/ArticleCard.astro`: shared image/title/metadata news card; no excerpts.
- `src/layouts/ArticleLayout.astro`: reusable article-detail layout with per-article SEO/Open Graph metadata, R2 image, shared sidebar, and related stories.
- `src/content/articles/*.md` and `src/pages/[slug].astro`: migrated source Markdown and generated static article routes.
- `src/pages/api/media/[...key].ts`: same-origin reader for featured images from the configured Cloudflare `MEDIA` R2 bucket.
- `src/components/BriefingSidebar.astro`: shared “Useful context. Less noise.” sidebar for category, homepage and article layouts.
- `src/components/Footer.astro`: reusable contact, category, social, address, and legal footer.
- `src/data/articles.ts`: captured homepage story metadata and published destinations.
- `src/styles/global.css`: semantic palette, typography, layouts, and responsive/motion rules.
- `public/media`: locally stored, matching source imagery and logo, served through static assets.
- `src/pages/api/subscribe.ts`, `wrangler.jsonc`: preserve the existing integration and deployment contracts.

The homepage is a snapshot, not an automatically refreshed live feed. Keep the MailerLite production-credential outcome open until configured and verified separately.
