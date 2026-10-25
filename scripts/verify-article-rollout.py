#!/usr/bin/env python3
"""Verify migrated article pages, category pagination, and source preservation."""
import hashlib
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

project = Path(__file__).resolve().parents[1]
posts = json.loads((project / 'src/data/post-index.json').read_text(encoding='utf-8'))
by_slug = {post['slug']: post for post in posts}
assert len(posts) == len(by_slug)
manifest = json.loads((project / 'public/manus-routes.json').read_text())
routes = {route['path']: route for route in manifest['routes']}
assert len(routes) == len(manifest['routes'])

for post in posts:
    slug = post['slug']
    assert f'/{slug}/' in routes
    markdown = (project / 'src/content/articles' / f'{slug}.md').read_text(encoding='utf-8')
    body = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', markdown, re.S).group(2).strip()
    assert hashlib.sha256(body.encode('utf-8')).hexdigest() == post['bodySha256'], slug
    assert not body.startswith('# '), slug
    page = project / 'dist' / slug / 'index.html'
    assert page.is_file(), slug
    soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    assert len(soup.select('h1')) == 1, slug
    assert soup.h1.get_text(strip=True) == post['title'], slug
    assert soup.select_one('.article-body').get_text(strip=True), slug
    assert soup.select_one('.article-layout > .briefing'), slug
    rendered_image = soup.select_one('.article-cover img')['src']
    assert rendered_image == post['image'] or rendered_image == post['image'].split('https://viper.ph', 1)[-1], slug
    assert soup.select_one('.article-cover img')['alt'].strip(), slug
    assert soup.select_one('meta[property="og:image:alt"]')['content'].strip(), slug
    assert soup.select_one('meta[property="og:type"]')['content'] == 'article', slug
    assert soup.select_one('link[rel="canonical"]')['href'] == post['sourceUrl'], slug
    assert 'One moment' not in soup.title.get_text(), slug
    cards = soup.select('.article-related__grid .news-card')
    assert len(cards) == 3, slug
    related = [card.select_one('h2 a')['href'].strip('/') for card in cards]
    assert len(set(related)) == 3 and slug not in related, slug
    assert all(related_slug in by_slug for related_slug in related), slug
    same = [p for p in posts if p['slug'] != slug and set(p['categories']) & set(post['categories'])]
    expected_same = min(3, len(same))
    actual_same = sum(bool(set(by_slug[r]['categories']) & set(post['categories'])) for r in related)
    assert actual_same == expected_same, (slug, actual_same, expected_same)

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
category_route_count = 0
for label, slug, matches in category_definitions:
    category_posts = [post for post in posts if any(match in post['categories'] for match in matches)]
    archive_count = max(0, len(category_posts) - 3)
    page_count = max(1, (archive_count + 9) // 10)
    seen_rows = []
    for current in range(1, page_count + 1):
        path = f'/category/{slug}/' if current == 1 else f'/category/{slug}/page/{current}/'
        assert path in routes, path
        category_route_count += 1
        page = project / 'dist' / path.strip('/') / 'index.html'
        assert page.is_file(), path
        soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        assert len(soup.select('.top-stories .news-card')) == min(3, len(category_posts)), path
        assert soup.select_one('.category-archive__layout > .briefing'), path
        assert soup.select_one('link[rel="canonical"]')['href'] == 'https://viper.ph' + path, path
        rows = soup.select('.category-archive__list .category-row')
        expected_rows = min(10, max(archive_count - ((current - 1) * 10), 0))
        assert len(rows) == expected_rows, (path, len(rows), expected_rows)
        row_slugs = [row.select_one('.category-row__content h2 a')['href'].strip('/') for row in rows]
        assert all(row_slug in by_slug for row_slug in row_slugs), path
        assert all(any(match in by_slug[row_slug]['categories'] for match in matches) for row_slug in row_slugs), path
        seen_rows.extend(row_slugs)
        if page_count > 1:
            nav = soup.select_one('.category-pagination')
            assert nav, path
            current_control = nav.select_one('[aria-current="page"]')
            assert current_control and current_control.get_text(strip=True) == str(current), path
            number_links = nav.select('.category-pagination__numbers li')
            assert len(number_links) == page_count, path
            if current > 1:
                assert nav.select_one('a[rel="prev"]')['href'] == (f'/category/{slug}/' if current == 2 else f'/category/{slug}/page/{current - 1}/'), path
            if current < page_count:
                assert nav.select_one('a[rel="next"]')['href'] == f'/category/{slug}/page/{current + 1}/', path
    assert len(seen_rows) == archive_count and len(set(seen_rows)) == archive_count, (label, len(seen_rows), archive_count)
assert category_route_count == 43
for path in routes:
    assert (project / 'dist' / path.strip('/') / 'index.html').is_file(), path
print(f'Verified: {len(posts)} article pages; preserved body hashes; one H1; R2 paths; sidebars and 3 valid related links; 10 canonical categories plus 4 legacy aliases with unique archive rows paginated at 10/page; page-specific canonicals and navigation; {len(routes)} declared routes.')
