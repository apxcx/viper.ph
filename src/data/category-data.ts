import type { Article } from './articles';
import { posts, postCard } from './posts';

export type CategoryPage = {
  label: string;
  slug: string;
  topStories: Article[];
  moreStories: Article[];
};

export const CATEGORY_ARCHIVE_PAGE_SIZE = 10;

const categories = [
  { label: 'PH Tech', slug: 'ph-tech', matches: ['PH Tech', 'Tech News'] },
  { label: 'Telcos and Internet', slug: 'telcos-and-internet', matches: ['Telcos and Internet'] },
  { label: 'Fintech and Banking Tech', slug: 'fintech-banking-tech', matches: ['Fintech and Banking Tech'] },
  { label: 'Gadgets', slug: 'gadgets', matches: ['Gadgets', 'Products'] },
  { label: 'E-commerce', slug: 'e-commerce', matches: ['E-commerce', 'E-Commerce'] },
  { label: 'Apps and Software', slug: 'apps-and-software', matches: ['Apps and Software'] },
  { label: 'AI', slug: 'ai', matches: ['AI'] },
  { label: 'International Tech', slug: 'international-tech', matches: ['International Tech'] },
  { label: 'Tech Events', slug: 'tech-events', matches: ['Tech Events'] },
  { label: 'Electric Vehicles', slug: 'electric-vehicles', matches: ['Electric Vehicles'] },
  { label: 'Tech News', slug: 'tech-news', matches: ['Tech News'] },
  { label: 'Products', slug: 'products', matches: ['Products'] },
  { label: 'E-Commerce', slug: 'e-commerce-legacy', matches: ['E-Commerce'] },
  { label: 'Auto', slug: 'auto', matches: ['Auto'] },
];

export const categoryPages: CategoryPage[] = categories.map(({ matches, ...category }) => {
  const articles = posts.filter((post) => matches.some((label) => post.categories.includes(label))).map(postCard);
  return { ...category, topStories: articles.slice(0, 3), moreStories: articles.slice(3) };
});

export const categoryPageMap: Record<string, CategoryPage> = Object.fromEntries(
  categoryPages.map((page) => [page.slug, page]),
);
