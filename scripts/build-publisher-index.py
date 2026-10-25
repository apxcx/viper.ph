#!/usr/bin/env python3
"""Build the Astro publisher index from src/content/articles/*.md without WordPress."""
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit('PyYAML is required for publisher tooling: python3 -m pip install pyyaml') from exc

PROJECT = Path(__file__).resolve().parents[1]
CONTENT = PROJECT / 'src/content/articles'
OUTPUT = PROJECT / 'src/data/post-index.json'
FRONTMATTER = re.compile(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', re.S)


def read_article(path: Path):
    match = FRONTMATTER.match(path.read_text(encoding='utf-8'))
    if not match:
        raise ValueError(f'Invalid Markdown frontmatter: {path}')
    metadata = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()
    if not metadata.get('slug'):
        raise ValueError(f'Missing slug: {path}')
    if metadata['slug'] != path.stem:
        raise ValueError(f'Slug/path mismatch: {path}')
    if not metadata.get('featured_image_key'):
        raise ValueError(f'Missing featured_image_key: {path}')
    first_text = next((block.strip() for block in re.split(r'\n\s*\n', body) if block.strip() and not block.lstrip().startswith('![')), '')
    plain = re.sub(r'!\[[^]]*\]\([^)]*\)', '', first_text)
    plain = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', plain)
    plain = re.sub(r'[*_`#]', '', plain)
    fallback = ' '.join(plain.split())
    if len(fallback) > 160:
        fallback = fallback[:157].rsplit(' ', 1)[0] + '…'
    key = metadata['featured_image_key']
    entry = {
        'slug': metadata['slug'],
        'title': metadata['title'],
        'date': metadata['date'],
        'modified': metadata.get('modified'),
        'author': metadata.get('author'),
        'categories': metadata.get('categories') or [],
        'tags': metadata.get('tags') or [],
        'imageKey': key,
        'image': metadata.get('featured_image_url') or '/api/media/' + key,
        'imageAlt': metadata.get('featured_image_alt') or metadata['title'],
        'imageWidth': metadata.get('featured_image_width'),
        'imageHeight': metadata.get('featured_image_height'),
        'sourceUrl': metadata.get('canonical_url') or metadata.get('source_url') or f"https://viper.ph/{metadata['slug']}/",
        'description': metadata.get('seo_description') or fallback,
        'bodySha256': hashlib.sha256(body.encode('utf-8')).hexdigest(),
    }
    if metadata.get('publisher_status'):
        entry['publisherStatus'] = metadata['publisher_status']
    if metadata.get('publication_slot'):
        entry['publicationSlot'] = metadata['publication_slot']
    return entry


posts = [read_article(path) for path in sorted(CONTENT.glob('*.md'))]
slugs = [post['slug'] for post in posts]
if len(slugs) != len(set(slugs)):
    raise SystemExit('Duplicate article slugs detected')
posts.sort(key=lambda post: (post['date'], post['slug']), reverse=True)
OUTPUT.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Indexed {len(posts)} Astro Markdown articles in {OUTPUT.relative_to(PROJECT)}.')
