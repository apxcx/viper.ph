#!/usr/bin/env python3
"""Import verified migration folders without rewriting article text or frontmatter."""
import argparse
import hashlib
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('batches', nargs='+', type=Path)
args = parser.parse_args()
project = Path(__file__).resolve().parents[1]
content = project / 'src/content/articles'
content.mkdir(parents=True, exist_ok=True)
posts, preview_map, seen = [], {}, set()

for root in args.batches:
    entries = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    for entry in entries:
        slug = entry['slug']
        if slug in seen or not re.fullmatch(r'[a-z0-9-]+', slug):
            raise ValueError(f'Duplicate or invalid slug: {slug}')
        seen.add(slug)
        source = root / 'articles' / Path(entry['markdown_file']).name
        raw = source.read_text(encoding='utf-8')
        match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', raw, re.S)
        if not match:
            raise ValueError(f'Invalid Markdown frontmatter: {source}')
        metadata, body = match.groups()
        lines = body.lstrip('\r\n').splitlines(keepends=True)
        if not lines or lines[0].rstrip() != '# ' + entry['title']:
            raise ValueError(f'Title heading mismatch: {source}')
        # Render the exported title in the approved page header, not a second H1.
        body = ''.join(lines[1:]).lstrip('\r\n')
        destination = content / f'{slug}.md'
        destination.write_text('---\n' + metadata + '\n---\n\n' + body, encoding='utf-8')
        key = entry['featured_image_r2_key']
        if not re.fullmatch(r'articles/\d{4}/\d{2}/[a-z0-9-]+/featured\.(?:jpe?g|png|webp|gif|avif)', key, re.I):
            raise ValueError(f'Invalid R2 key: {key}')
        image = root / 'images' / Path(entry['featured_image_local']).name
        if not image.is_file():
            raise ValueError(f'Missing verified local image: {image}')
        preview_map[key] = str(image.resolve())
        first_paragraph = body.split('\n\n')[0]
        plain = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', first_paragraph)
        plain = re.sub(r'[*_`#]', '', plain)
        plain = ' '.join(plain.split())
        fallback_description = plain if len(plain) <= 160 else plain[:157].rsplit(' ', 1)[0] + '…'
        seo = entry.get('seo') or {}
        posts.append({
            'slug': slug,
            'title': entry['title'],
            'date': entry['date'],
            'modified': entry.get('modified'),
            'author': entry.get('author'),
            'categories': entry.get('categories') or ['Tech News'],
            'tags': entry.get('tags') or [],
            'imageKey': key,
            'image': '/api/media/' + key,
            'imageAlt': entry.get('featured_image_alt') or entry['title'],
            'imageWidth': entry.get('featured_image_width'),
            'imageHeight': entry.get('featured_image_height'),
            'sourceUrl': entry['source_url'],
            'description': seo.get('seo_description') or fallback_description,
            'bodySha256': hashlib.sha256(body.strip().encode('utf-8')).hexdigest(),
        })

posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
index = project / 'src/data/post-index.json'
index.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(project / '.r2-preview-map.json').write_text(json.dumps(preview_map, indent=2) + '\n', encoding='utf-8')
manifest_file = project / 'public/manus-routes.json'
manifest = json.loads(manifest_file.read_text())
category_definitions = [('Tech News', 'tech-news'), ('AI', 'ai'), ('Electric Vehicles', 'electric-vehicles'), ('Fintech and Banking Tech', 'fintech-banking-tech'), ('Products', 'products'), ('E-Commerce', 'e-commerce'), ('Telcos and Internet', 'telcos-and-internet'), ('Auto', 'auto')]
category_roots = [f'/category/{slug}/' for _, slug in category_definitions]
manifest['routes'] = [
    route for route in manifest['routes']
    if route['path'].strip('/') not in seen
    and not any(route['path'] == root or route['path'].startswith(root + 'page/') for root in category_roots)
]
for label, slug in category_definitions:
    root = f'/category/{slug}/'
    manifest['routes'].append({'path': root, 'title': label + ' | Viper.ph'})
    count = sum(label in post['categories'] for post in posts)
    total_pages = max(1, (max(0, count - 3) + 9) // 10)
    manifest['routes'].extend(
        {'path': f'{root}page/{number}/', 'title': f'{label} — Page {number} | Viper.ph'}
        for number in range(2, total_pages + 1)
    )
manifest['routes'].extend({'path': '/' + p['slug'] + '/', 'title': p['title'] + ' | Viper.ph'} for p in posts)
if len(manifest['routes']) > 1000:
    raise ValueError('Route manifest exceeds platform limit')
manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Imported {len(posts)} unique Markdown articles; indexed {len(preview_map)} R2 images; declared {len(manifest["routes"])} pages.')
