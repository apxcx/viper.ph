export type Article = {
  category: string;
  date: string;
  time: string;
  title: string;
  excerpt: string;
  image: string;
  href: string;
};

export const leadStories: Article[] = [
  {
    category: 'Tech News',
    date: '25 October 2026',
    time: '8:00 am',
    title: 'Xiaomi POP Run Puts Redmi Battery to Test',
    excerpt:
      'Xiaomi Philippines turned a community run into a closer look at the battery life and everyday performance behind its latest Redmi experience.',
    image: '/media/xiaomi-pop-run.jpg',
    href: '#story-xiaomi',
  },
  {
    category: 'Electric Vehicles',
    date: '25 October 2026',
    time: '6:00 am',
    title: 'Deepal S07 EV Launches in Philippines',
    excerpt: 'The new electric SUV brings a sharper design and a more considered approach to the local EV conversation.',
    image: '/media/deepal-s07.jpg',
    href: '#story-deepal',
  },
  {
    category: 'AI',
    date: '24 October 2026',
    time: '10:00 am',
    title: 'AI Finds More Bugs, Shrinking Patch Time',
    excerpt: 'New developer tools are changing how teams find, understand, and fix software problems before they reach users.',
    image: '/media/ai-bugs.webp',
    href: '#story-ai',
  },
];

export const latestStories: Article[] = [
  {
    category: 'Tech News',
    date: '24 October 2026',
    time: '8:00 am',
    title: 'Converge Studios Unveils AI Health Tools',
    excerpt: 'A new set of tools puts practical AI closer to the people who need it most.',
    image: '/media/ai-bugs.webp',
    href: '#story-converge',
  },
  {
    category: 'Space & Science',
    date: '24 October 2026',
    time: '6:00 am',
    title: 'Philippine Spaceport Plan Gains Rocket Test',
    excerpt: 'The country’s space ambitions move one step closer to a launch-ready future.',
    image: '/media/deepal-s07.jpg',
    href: '#story-spaceport',
  },
  {
    category: 'Electric Vehicles',
    date: '23 October 2026',
    time: '10:00 am',
    title: 'BYD Brings EV Experience to Philippine Summit',
    excerpt: 'Charging, ownership, and a more accessible electric future take the spotlight in Manila.',
    image: '/media/xiaomi-pop-run.jpg',
    href: '#story-byd',
  },
  {
    category: 'Security',
    date: '23 October 2026',
    time: '8:00 am',
    title: 'PHP Flaws Put Government Websites Offline',
    excerpt: 'The latest outage is another reminder that resilient digital infrastructure is never optional.',
    image: '/media/ai-bugs.webp',
    href: '#story-security',
  },
];
