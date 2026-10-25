#!/usr/bin/env python3
"""Validate new Astro-native Viper articles, source links, R2 URLs, and 16:9 images."""
import argparse
import io
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

try:
    import yaml
    from PIL import Image
except ImportError as exc:
    raise SystemExit('Publisher validation requires PyYAML and Pillow: python3 -m pip install pyyaml pillow') from exc

parser = argparse.ArgumentParser()
parser.add_argument('--only', help='Validate one slug or Markdown filename')
parser.add_argument('--network', action='store_true', help='Fetch every ready article image and verify dimensions')
args = parser.parse_args()

PROJECT = Path(__file__).resolve().parents[1]
CONTENT = PROJECT / 'src/content/articles'
TAXONOMY = {
    'PH Tech', 'Telcos and Internet', 'Fintech and Banking Tech', 'Gadgets',
    'E-commerce', 'Apps and Software', 'AI', 'International Tech', 'Tech Events',
    'Electric Vehicles',
}
SLOTS = {'06:00', '08:00', '10:00'}
FRONTMATTER = re.compile(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', re.S)
IMAGE_LINE = re.compile(r'^!\[([^\]]+)\]\((https://viper\.ph/api/media/articles/\d{4}/\d{2}/[a-z0-9-]+/image-[1-4]\.(?:jpe?g|png|webp|avif))\)$')
FEATURED_URL = re.compile(r'^https://viper\.ph/api/media/articles/(\d{4})/(\d{2})/([a-z0-9-]+)/featured\.(jpe?g|png|webp|avif)$')
IMAGE_URL = re.compile(r'^https://viper\.ph/api/media/articles/(\d{4})/(\d{2})/([a-z0-9-]+)/image-([1-4])\.(jpe?g|png|webp|avif)$')


def fail(path, message):
    raise ValueError(f'{path.name}: {message}')


def check_image(url, expected_ratio, label):
    request = urllib.request.Request(url, headers={'User-Agent': 'viper-astro-publisher-verifier/1.0'})
    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read(12 * 1024 * 1024)
        content_type = response.headers.get('Content-Type', '')
    if not content_type.startswith('image/'):
        raise ValueError(f'{label}: {url} returned {content_type or "no content type"}')
    with Image.open(io.BytesIO(data)) as image:
        width, height = image.size
    ratio = width / height
    if abs(ratio - expected_ratio) > 0.04:
        raise ValueError(f'{label}: {url} is {width}x{height}, not approximately 16:9')
    return width, height


targets = sorted(CONTENT.glob('*.md'))
if args.only:
    needle = args.only.removesuffix('.md')
    targets = [path for path in targets if path.stem == needle]
    if not targets:
        raise SystemExit(f'No article found for --only {args.only}')
ready = 0
legacy = 0
for path in targets:
    match = FRONTMATTER.match(path.read_text(encoding='utf-8'))
    if not match:
        fail(path, 'invalid frontmatter')
    metadata = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()
    status = metadata.get('publisher_status', 'legacy-migrated')
    if status not in {'draft', 'ready', 'published'}:
        legacy += 1
        continue
    ready += 1
    title = str(metadata.get('title', ''))
    if not 1 <= len(title) < 60:
        fail(path, 'headline must be under 60 characters')
    if not metadata.get('focus_keyword'):
        fail(path, 'focus_keyword is required')
    seo_title = str(metadata.get('seo_title', ''))
    if len(seo_title) > 60 or not seo_title.endswith(' | Viper'):
        fail(path, 'seo_title must end with " | Viper" and be no longer than 60 characters')
    description = str(metadata.get('seo_description', ''))
    if not 145 <= len(description) <= 155:
        fail(path, f'seo_description must be 145–155 characters, got {len(description)}')
    categories = metadata.get('categories') or []
    if not categories or any(category not in TAXONOMY for category in categories):
        fail(path, f'categories must use the authoritative taxonomy: {sorted(TAXONOMY)}')
    date = str(metadata.get('date', ''))
    try:
        parsed = datetime.fromisoformat(date)
    except ValueError as exc:
        fail(path, f'date must be ISO-8601 with Manila offset: {exc}')
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 8 * 60 * 60:
        fail(path, 'date must carry the +08:00 Manila offset')
    slot = metadata.get('publication_slot')
    if slot not in SLOTS or parsed.strftime('%H:%M') != slot:
        fail(path, 'publication_slot and date time must match 06:00, 08:00, or 10:00 Manila')
    sources = metadata.get('sources') or []
    if not sources or any(not str(source.get('url', '')).startswith('https://') for source in sources):
        fail(path, 'at least one HTTPS source link is required')
    blocks = [block.strip() for block in re.split(r'\n\s*\n', body) if block.strip()]
    if len(blocks) != 8:
        fail(path, f'body must contain exactly four paragraphs and four following images, got {len(blocks)} blocks')
    image_urls = []
    for index in range(4):
        paragraph = blocks[index * 2]
        image_block = blocks[index * 2 + 1]
        if paragraph.startswith('![') or not 80 <= len(re.findall(r"\b[\w’'-]+\b", paragraph)) <= 110:
            fail(path, f'paragraph {index + 1} must be 80–110 words')
        image_match = IMAGE_LINE.match(image_block)
        if not image_match:
            fail(path, f'image {index + 1} must immediately follow paragraph {index + 1} and use a public R2 URL')
        image_urls.append(image_match.group(2))
    if {IMAGE_URL.match(url).group(4) for url in image_urls} != {'1', '2', '3', '4'}:
        fail(path, 'body images must contain image-1 through image-4 exactly once')
    images = metadata.get('images') or []
    by_url = {image.get('url'): image for image in images}
    if len(images) != 4 or set(by_url) != set(image_urls):
        fail(path, 'images frontmatter must describe the four body image URLs')
    for url in image_urls:
        image = by_url[url]
        if image.get('rights_cleared') is not True or not image.get('license') or not image.get('credit') or not str(image.get('source_url', '')).startswith('https://'):
            fail(path, f'{url} needs rights_cleared=true, license, credit, and an HTTPS source_url')
        width, height = image.get('width'), image.get('height')
        if not isinstance(width, int) or not isinstance(height, int) or abs((width / height) - (16 / 9)) > 0.04:
            fail(path, f'{url} must declare approximately 16:9 dimensions')
        if args.network:
            check_image(url, 16 / 9, 'body image')
    featured_key = str(metadata.get('featured_image_key', ''))
    expected_key = f"articles/{parsed.year:04d}/{parsed.month:02d}/{path.stem}/featured."
    if not featured_key.startswith(expected_key):
        fail(path, 'featured_image_key must use articles/YYYY/MM/slug/featured.ext')
    featured_url = str(metadata.get('featured_image_url', ''))
    featured_match = FEATURED_URL.match(featured_url)
    if not featured_match or featured_match.group(3) != path.stem:
        fail(path, 'featured_image_url must be the public same-origin R2 endpoint for this slug')
    if args.network:
        check_image(featured_url, 16 / 9, 'featured image')

print(f'Validated Astro publisher contract: {ready} ready/published articles; {legacy} legacy migration articles exempt from the new format.')
