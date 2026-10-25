#!/usr/bin/env python3
"""Generate a deterministic day/slot index for Astro-native Viper publishing."""
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit('PyYAML is required for publisher tooling: python3 -m pip install pyyaml') from exc

PROJECT = Path(__file__).resolve().parents[1]
CONTENT = PROJECT / 'src/content/articles'
OUTPUT = PROJECT / 'src/data/publisher-manifest.json'
FRONTMATTER = re.compile(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', re.S)
SLOTS = ('06:00', '08:00', '10:00')


def load(path: Path):
    match = FRONTMATTER.match(path.read_text(encoding='utf-8'))
    if not match:
        raise ValueError(f'Invalid Markdown frontmatter: {path}')
    return yaml.safe_load(match.group(1)) or {}, match.group(2).strip()


entries = []
for path in sorted(CONTENT.glob('*.md')):
    metadata, body = load(path)
    slug = metadata.get('slug') or path.stem
    date = str(metadata.get('date', ''))
    day = date[:10]
    time = date[11:16] if len(date) >= 16 else ''
    status = metadata.get('publisher_status', 'legacy-migrated')
    managed = status in {'draft', 'ready', 'published'}
    declared_slot = metadata.get('publication_slot')
    slot = declared_slot or (time if time in SLOTS else None)
    if managed and slot not in SLOTS:
        raise ValueError(f'{path.name}: managed article must declare publication_slot as 06:00, 08:00, or 10:00')
    if managed and date and slot and time != slot:
        raise ValueError(f'{path.name}: date time {time} does not match publication_slot {slot}')
    if slot in SLOTS:
        slot_key = f'{day}/{slot}'
        idempotency_key = slot_key
    else:
        slot = 'legacy'
        slot_key = f'legacy/{day}/{slug}'
        idempotency_key = slot_key
    entries.append({
        'slot_key': slot_key,
        'idempotency_key': idempotency_key,
        'day': day,
        'slot': slot,
        'slug': slug,
        'title': metadata.get('title', ''),
        'status': status,
        'managed': managed,
        'categories': metadata.get('categories') or [],
        'source_count': len(metadata.get('sources') or []),
        'body_image_count': len(metadata.get('images') or []),
        'content_sha256': hashlib.sha256(body.encode('utf-8')).hexdigest(),
    })

entries.sort(key=lambda item: (item['day'], item['slot_key'], item['slug']), reverse=True)
managed_keys = [item['slot_key'] for item in entries if item['managed']]
if len(managed_keys) != len(set(managed_keys)):
    raise ValueError('Duplicate managed publication slot keys detected')

days = {}
for item in entries:
    days.setdefault(item['day'], {})[item['slot_key']] = {
        'slug': item['slug'],
        'status': item['status'],
        'managed': item['managed'],
    }

manifest = {
    'schema': 'viper.astro.publisher/v1',
    'timezone': 'Asia/Manila',
    'slots': list(SLOTS),
    'entries': entries,
    'days': {day: days[day] for day in sorted(days, reverse=True)},
}
OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Generated {len(entries)} publisher entries across {len(days)} days in {OUTPUT.relative_to(PROJECT)}.')
