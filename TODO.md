# Viper — Journal implementation

- [x] Build a simple dark-mode blog landing page titled “Viper — Journal” using Astro and Tailwind CSS.
  - The page presents a clear journal header and introductory branding.
  - The visual treatment is cohesive, dark, editorial, restrained, and responsive.
  - The page is usable on both mobile and desktop screens.
- [x] Include three dummy article previews with titles, excerpts, categories, dates, reading times, and clear reading actions.
- [x] Provide accessible navigation, a mobile menu toggle, a newsletter callout, and meaningful footer links without claiming a real submission backend.
- [x] Serve a synchronized `/manus-routes.json` route manifest and include crawler-visible page content and metadata.
- [x] Verify diagnostics, production build, route manifest, and responsive preview rendering.
- [x] Push the completed project to the requested `apxcx/viper.ph` GitHub repository through the authenticated GitHub connection.
- [x] Rework the homepage to mirror the live Viper.ph structure: logo-led header, top-three news hero, and a two-column latest-news section.
  - The headline tagline is “The pulse of what’s next.”
  - The palette uses the live Viper navy, cream, and rust accent treatment.
- [x] Add a horizontal first-name and email newsletter form directly below the header.
  - Form submissions post to the server-side `/api/subscribe` route without exposing MailerLite credentials in the browser.
- [ ] Add `MAILERLITE_API_TOKEN` and `MAILERLITE_GROUP_ID` to the Cloudflare Worker environment so production subscriptions are delivered to MailerLite.
