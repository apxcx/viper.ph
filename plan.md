# Viper.ph — premium editorial refinement

Refine the existing Astro/Tailwind homepage, without changing its Cloudflare Worker, R2, or MailerLite integration. Retain the exact H1 “The Daily Pulse of Philippine Tech”, background `#14171c`, button/highlight accent `#0000ff`, solid blue article-title panels, and the absence of article excerpts.

## Design direction

Dark editorial: a calm, precise technology publication rather than an agency template. Use Manrope for a confident grotesk display and DM Sans for readable interface text, with restrained Playfair Display italics in the masthead. Warm off-white typography and layered neutral charcoal balance the vivid blue; reserve blue for title panels, primary controls, and small signal marks. Preserve the asymmetric lead-story composition and two-column latest-news feed, but use deliberate stacked right-hand cards rather than sparse horizontal rows. Reduce secondary blue boxes, keep rules fine, give metadata and content consistent spacing, and apply subtle image-hover motion with reduced-motion support.

Use the existing approved logo and each story's matching homepage image. News and footer links should point to their published destinations, not invented placeholder routes.

## Footer content

Use only published homepage data from https://viper.ph/ (retrieved 25 October 2026): Viper's published description, `hi@viper.ph`, SM North / North Avenue / Epifanio de los Santos Ave / Quezon City 1105 Metro Manila, eight category destinations, social profiles, copyright, Events, Partnerships, Privacy Policy, and Terms and Conditions. The social X profile was also visible in the previous homepage browser extraction. No additional page scraping is required.

## Article-page example

Create one review-only article route for the migrated Xiaomi POP Run story, preserving its original slug, four source paragraphs, published timestamp, category, author, Rank Math title/description, canonical and social metadata. Build the detail layout with a premium title/byline header, featured image, readable article body, the shared “Useful context. Less noise.” sidebar, and a related-story card section after the article. Change only this story's homepage and category hero links to its local route; do not generate routes for the other articles until the example is approved. Keep the preview image on the existing local `/media/xiaomi-pop-run.jpg` asset, while retaining the imported R2 object key in the Markdown frontmatter.

## Project structure

- `src/pages/index.astro`: homepage composition and existing newsletter form.
- `src/components/Header.astro`: logo, navigation, and responsive controls.
- `src/components/ArticleCard.astro`: shared image/title/metadata news card; no excerpts.
- `src/layouts/ArticleLayout.astro` and `src/pages/xiaomi-pop-run-redmi-note-17-battery-event.md`: one article-detail design example built from migrated Markdown.
- `src/components/BriefingSidebar.astro`: shared “Useful context. Less noise.” sidebar for category, homepage and article layouts.
- `src/components/Footer.astro`: reusable contact, category, social, address, and legal footer.
- `src/data/articles.ts`: captured homepage story metadata and published destinations.
- `src/styles/global.css`: semantic palette, typography, layouts, and responsive/motion rules.
- `public/media`: locally stored, matching source imagery and logo, served through static assets.
- `src/pages/api/subscribe.ts`, `wrangler.jsonc`: preserve the existing integration and deployment contracts.

The homepage is a snapshot, not an automatically refreshed live feed. Keep the MailerLite production-credential outcome open until configured and verified separately.
