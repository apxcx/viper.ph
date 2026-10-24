export type Article = {
  index: string;
  category: string;
  date: string;
  readTime: string;
  title: string;
  excerpt: string;
  accent: string;
  texture: string;
};

export const articles: Article[] = [
  {
    index: '01',
    category: 'Point of view',
    date: 'October 18, 2026',
    readTime: '6 min read',
    title: 'The quiet power of a considered digital presence',
    excerpt:
      'Why the most memorable brands are learning to edit harder, move slower, and leave room for people to look closer.',
    accent: 'from-[#4c2014] via-[#1e1210] to-[#101010]',
    texture: 'article-art--one',
  },
  {
    index: '02',
    category: 'Field notes',
    date: 'September 29, 2026',
    readTime: '4 min read',
    title: 'Designing for the space between signal and noise',
    excerpt:
      'A field note on restraint, rhythm, and building interfaces that feel as assured as the products behind them.',
    accent: 'from-[#1d2626] via-[#111b1b] to-[#101010]',
    texture: 'article-art--two',
  },
  {
    index: '03',
    category: 'Practice',
    date: 'August 11, 2026',
    readTime: '8 min read',
    title: 'A slower route to sharper creative decisions',
    excerpt:
      'Inside the rituals that make a small studio useful: fewer meetings, better questions, and a point of view worth protecting.',
    accent: 'from-[#302515] via-[#171510] to-[#101010]',
    texture: 'article-art--three',
  },
];
