#!/usr/bin/env python3
"""Verify the generated migration rollout against the imported source inventory."""
import hashlib
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

project = Path(__file__).resolve().parents[1]
posts = json.loads((project / 'src/data/post-index.json').read_text(encoding='utf-8'))
by_slug = {post['slug']: post for post in posts}
assert len(posts) == len(by_slug) == 216
manifest = json.loads((project / 'public/manus-routes.json').read_text())
paths = {route['path'] for route in manifest['routes']}
assert len(paths) == len(manifest['routes']) == 229

for post in posts:
    slug = post['slug']
    assert f'/{slug}/' in paths
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
    assert soup.select_one('.article-cover img')['src'] == post['image'], slug
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

category_count = 0
for route in manifest['routes']:
    path = route['path']
    page = project / 'dist' / path.strip('/') / 'index.html'
    assert page.is_file(), path
    if path.startswith('/category/'):
        category_count += 1
        soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        assert len(soup.select('.top-stories .news-card')) == 3, path
        assert soup.select_one('.category-archive__layout > .briefing'), path
        for anchor in soup.select('.news-card h2 a, .category-row h2 a'):
            assert anchor['href'].strip('/') in by_slug, anchor['href']
assert category_count == 8
print('Verified: 216 unique article pages; preserved body hashes; one H1; R2 image paths; sidebar and 3 valid related links per page; 8 category archives; 229 declared routes.')
