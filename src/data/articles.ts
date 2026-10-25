export type Article = {
  category: string;
  categorySlug?: string;
  date: string;
  time: string;
  publishedAt?: string;
  title: string;
  excerpt: string;
  image: string;
  href: string;
  migrated?: boolean;
  featuredImageKey?: string;
};

export const leadStories: Article[] = [
  {
    category: 'PH Tech',
    date: '26 October 2026',
    time: '6:00 am',
    title: 'PhilSA Warns After Long March 8A Launch',
    excerpt:
      'A Philippine Space Agency advisory identifies debris zones and urges ships, aircraft, and coastal communities to stay alert.',
    image: '/api/media/articles/2026/10/philsa-warns-long-march-8a-debris/featured.jpg',
    href: '/philsa-warns-long-march-8a-debris/',
  },
  {
    category: 'Electric Vehicles',
    date: '25 October 2026',
    time: '6:00 am',
    title: 'Deepal S07 EV Launches in Philippines',
    excerpt: 'The new electric SUV brings a sharper design and a more considered approach to the local EV conversation.',
    image: '/media/deepal-s07.jpg',
    href: 'https://viper.ph/deepal-s07-ev-launches-philippines/',
  },
  {
    category: 'AI',
    date: '24 October 2026',
    time: '10:00 am',
    title: 'AI Finds More Bugs, Shrinking Patch Time',
    excerpt: 'New developer tools are changing how teams find, understand, and fix software problems before they reach users.',
    image: '/media/ai-bugs.webp',
    href: 'https://viper.ph/ai-finds-more-software-bugs-shrinking-patch-time/',
  },
];

export const latestStories: Article[] = [
  {
    category: 'Tech News',
    date: '24 October 2026',
    time: '8:00 am',
    title: 'Converge Studios Unveils AI Health Tools',
    excerpt: 'A new set of tools puts practical AI closer to the people who need it most.',
    image: '/media/converge-health.jpg',
    href: 'https://viper.ph/converge-studios-ai-health-tools/',
  },
  {
    category: 'Space & Science',
    date: '24 October 2026',
    time: '6:00 am',
    title: 'Philippine Spaceport Plan Gains Rocket Test',
    excerpt: 'The country’s space ambitions move one step closer to a launch-ready future.',
    image: '/media/philippine-spaceport.jpg',
    href: 'https://viper.ph/philippine-spaceport-plan-rocket-test/',
  },
  {
    category: 'Electric Vehicles',
    date: '23 October 2026',
    time: '10:00 am',
    title: 'BYD Brings EV Experience to Philippine Summit',
    excerpt: 'Charging, ownership, and a more accessible electric future take the spotlight in Manila.',
    image: '/media/byd-ev-summit.webp',
    href: 'https://viper.ph/byd-acmobility-philippine-ev-summit-2026/',
  },
  {
    category: 'Security',
    date: '23 October 2026',
    time: '8:00 am',
    title: 'PHP Flaws Put Government Websites Offline',
    excerpt: 'The latest outage is another reminder that resilient digital infrastructure is never optional.',
    image: '/media/php-security.webp',
    href: 'https://viper.ph/php-flaws-put-government-websites-offline/',
  },
];
