#!/usr/bin/env python3
"""Refresh public route, sitemap, and robots declarations from the Astro article index."""
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
INDEX = PROJECT / 'src/data/post-index.json'
ROUTES = PROJECT / 'public/manus-routes.json'
posts = json.loads(INDEX.read_text(encoding='utf-8'))
manifest = json.loads(ROUTES.read_text(encoding='utf-8'))
category_definitions = [
    ('PH Tech', 'ph-tech', ['PH Tech', 'Tech News']),
    ('Telcos and Internet', 'telcos-and-internet', ['Telcos and Internet']),
    ('Fintech and Banking Tech', 'fintech-banking-tech', ['Fintech and Banking Tech']),
    ('Gadgets', 'gadgets', ['Gadgets', 'Products']),
    ('E-commerce', 'e-commerce', ['E-commerce', 'E-Commerce']),
    ('Apps and Software', 'apps-and-software', ['Apps and Software']),
    ('AI', 'ai', ['AI']),
    ('International Tech', 'international-tech', ['International Tech']),
    ('Tech Events', 'tech-events', ['Tech Events']),
    ('Electric Vehicles', 'electric-vehicles', ['Electric Vehicles']),
    ('Tech News', 'tech-news', ['Tech News']),
    ('Products', 'products', ['Products']),
    ('E-Commerce', 'e-commerce-legacy', ['E-Commerce']),
    ('Auto', 'auto', ['Auto']),
]
slugs = {post['slug'] for post in posts}
category_roots = {f'/category/{slug}/' for _, slug, _ in category_definitions}
base_routes = []
for route in manifest['routes']:
    path = route['path']
    if path in category_roots or any(path.startswith(root + 'page/') for root in category_roots):
        continue
    if path.strip('/') in slugs:
        continue
    base_routes.append(route)
manifest['routes'] = base_routes
for label, slug, matches in category_definitions:
    root = f'/category/{slug}/'
    manifest['routes'].append({'path': root, 'title': f'{label} | Viper.ph'})
    count = sum(any(match in post['categories'] for match in matches) for post in posts)
    total_pages = max(1, (max(0, count - 3) + 9) // 10)
    manifest['routes'].extend(
        {'path': f'{root}page/{number}/', 'title': f'{label} — Page {number} | Viper.ph'}
        for number in range(2, total_pages + 1)
    )
manifest['routes'].extend({'path': f"/{post['slug']}/", 'title': f"{post['title']} | Viper.ph"} for post in posts)
if len(manifest['routes']) > 1000:
    raise SystemExit('Route manifest exceeds platform limit')
ROUTES.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
sitemap = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for route in manifest['routes']:
    if not route['path'].startswith('/api/'):
        sitemap.append(f"  <url><loc>https://viper.ph{route['path']}</loc></url>")
sitemap.append('</urlset>')
(PROJECT / 'public/sitemap.xml').write_text('\n'.join(sitemap) + '\n', encoding='utf-8')
(PROJECT / 'public/robots.txt').write_text(
    'User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: https://viper.ph/sitemap.xml\n',
    encoding='utf-8',
)
print(f'Refreshed {len(manifest["routes"])} routes and sitemap URLs from {len(posts)} Astro articles.')
