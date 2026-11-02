import index from './post-index.json';
import type { Article } from './articles';

export interface ArticleFrontmatter {
  title: string;
  slug: string;
  date: string;
  modified?: string;
  author?: string;
  categories?: string[];
  tags?: string[];
  seo_title?: string;
  seo_description?: string;
  seo_robots?: string;
  og_title?: string;
  og_description?: string;
  canonical_url?: string;
  featured_image_key: string;
  featured_image_alt?: string;
  featured_image_width?: number;
  featured_image_height?: number;
}

export type PostSummary = (typeof index)[number];
export const posts = index;
export const postsBySlug = new Map(posts.map((post) => [post.slug, post]));

function featuredImageUrl(slug: string, image: string): string {
  return ['cirtek-semiconductor-unit-sale-sancode', 'gcash-ipo-share-price-after-listing', 'ai-election-content-philippine-guardrails', 'philippine-ev-summit-15-brands-2026', 'gbf-class-builder-stem-learning-philippines', 'philippine-business-ai-adoption-2027', 'pagasa-22-radar-weather-network', 'philippine-offshore-wind-hub', 'vivo-v80-philippine-preorders', 'quantum-cybersecurity-philippines', 'dost-el-nino-risk-tool-philippines', 'alon-filipino-indie-game-platform', 'ai-giants-shared-scraping-opt-out', 'binance-hack-crypto-security-reset', 'ntc-telcos-undas-mobile-network-readiness', 'chrg-japan-backed-solar-ev-charging-philippines', 'ai-data-centers-community-energy-pressure'].includes(slug)
    ? `${image}?v=${slug === 'vivo-v80-philippine-preorders' ? '202610312' : slug === 'quantum-cybersecurity-philippines' ? '202610313' : slug === 'dost-el-nino-risk-tool-philippines' ? '202610314' : slug === 'alon-filipino-indie-game-platform' ? '202611012' : slug === 'ai-giants-shared-scraping-opt-out' ? '202611013' : slug === 'binance-hack-crypto-security-reset' ? '202611014' : slug === 'ntc-telcos-undas-mobile-network-readiness' ? '202611025' : slug === 'chrg-japan-backed-solar-ev-charging-philippines' ? '202611026' : slug === 'ai-data-centers-community-energy-pressure' ? '202611023' : '20261031'}`
    : image;
}

export function manilaDate(value: string): Date {
  return new Date(/(?:Z|[+-]\d{2}:\d{2})$/.test(value) ? value : `${value}+08:00`);
}

export function postCard(post: PostSummary): Article {
  const published = manilaDate(post.date);
  return {
    category: post.categories[0] ?? 'Tech News',
    date: new Intl.DateTimeFormat('en-PH', {
      day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Asia/Manila',
    }).format(published),
    time: new Intl.DateTimeFormat('en-PH', {
      hour: 'numeric', minute: '2-digit', hour12: true, timeZone: 'Asia/Manila',
    }).format(published),
    publishedAt: published.toISOString(),
    title: post.title,
    excerpt: post.description,
    image: featuredImageUrl(post.slug, post.image),
    href: `/${post.slug}/`,
    migrated: true,
    featuredImageKey: post.imageKey,
  };
}

export function relatedPosts(slug: string): Article[] {
  const current = postsBySlug.get(slug);
  const candidates = posts.filter((post) => post.slug !== slug);
  const sameCategory = candidates.filter((post) =>
    post.categories.some((category) => current?.categories.includes(category)),
  );
  const matched = new Set(sameCategory.map((post) => post.slug));
  return [...sameCategory, ...candidates.filter((post) => !matched.has(post.slug))]
    .slice(0, 3).map(postCard);
}

export function migratedStory(article: Article): Article {
  const slug = new URL(article.href, 'https://viper.ph').pathname.replace(/^\/|\/$/g, '');
  const post = postsBySlug.get(slug);
  return post ? postCard(post) : article;
}
