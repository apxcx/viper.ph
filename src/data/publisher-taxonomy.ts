export const PUBLISHER_CATEGORIES = [
  { label: 'PH Tech', slug: 'ph-tech' },
  { label: 'Telcos and Internet', slug: 'telcos-and-internet' },
  { label: 'Fintech and Banking Tech', slug: 'fintech-banking-tech' },
  { label: 'Gadgets', slug: 'gadgets' },
  { label: 'E-commerce', slug: 'e-commerce' },
  { label: 'Apps and Software', slug: 'apps-and-software' },
  { label: 'AI', slug: 'ai' },
  { label: 'International Tech', slug: 'international-tech' },
  { label: 'Tech Events', slug: 'tech-events' },
  { label: 'Electric Vehicles', slug: 'electric-vehicles' },
] as const;

export const LEGACY_CATEGORY_ALIASES = [
  { label: 'Tech News', canonical: 'PH Tech', slug: 'tech-news' },
  { label: 'Products', canonical: 'Gadgets', slug: 'products' },
  { label: 'E-Commerce', canonical: 'E-commerce', slug: 'e-commerce' },
  { label: 'Auto', canonical: 'Electric Vehicles', slug: 'auto' },
] as const;

export type PublisherCategory = (typeof PUBLISHER_CATEGORIES)[number]['label'];
export const PUBLISHER_CATEGORY_LABELS = PUBLISHER_CATEGORIES.map((category) => category.label);
