import type { Article } from './articles';
import { posts, postCard } from './posts';

export type CategoryPage = {
  label: string;
  slug: string;
  topStories: Article[];
  moreStories: Article[];
};

const categories = [
  { label: 'Tech News', slug: 'tech-news' },
  { label: 'AI', slug: 'ai' },
  { label: 'Electric Vehicles', slug: 'electric-vehicles' },
  { label: 'Fintech and Banking Tech', slug: 'fintech-banking-tech' },
  { label: 'Products', slug: 'products' },
  { label: 'E-Commerce', slug: 'e-commerce' },
  { label: 'Telcos and Internet', slug: 'telcos-and-internet' },
  { label: 'Auto', slug: 'auto' },
];

export const categoryPages: CategoryPage[] = categories.map((category) => {
  const articles = posts.filter((post) => post.categories.includes(category.label)).map(postCard);
  return { ...category, topStories: articles.slice(0, 3), moreStories: articles.slice(3) };
});

export const categoryPageMap: Record<string, CategoryPage> = Object.fromEntries(
  categoryPages.map((page) => [page.slug, page]),
);
