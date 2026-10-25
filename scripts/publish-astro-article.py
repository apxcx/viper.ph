#!/usr/bin/env python3
"""Install a validated Astro article idempotently by slug and Manila slot."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit('PyYAML is required for publisher tooling: python3 -m pip install pyyaml') from exc

PROJECT = Path(__file__).resolve().parents[1]
CONTENT = PROJECT / 'src/content/articles'
FRONTMATTER = re.compile(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', re.S)
parser = argparse.ArgumentParser()
parser.add_argument('article', type=Path)
parser.add_argument('--replace', action='store_true', help='Replace the same slug only when its slot remains unchanged')
args = parser.parse_args()

source = args.article.resolve()
match = FRONTMATTER.match(source.read_text(encoding='utf-8'))
if not match:
    raise SystemExit(f'Invalid Markdown frontmatter: {source}')
metadata = yaml.safe_load(match.group(1)) or {}
body = match.group(2).strip()
slug = str(metadata.get('slug', ''))
slot = str(metadata.get('publication_slot', ''))
date = str(metadata.get('date', ''))
if not re.fullmatch(r'[a-z0-9-]+', slug):
    raise SystemExit('slug must contain only lowercase letters, numbers, and hyphens')
if metadata.get('publisher_status') not in {'ready', 'published'}:
    raise SystemExit('publisher_status must be ready or published')
if slot not in {'06:00', '08:00', '10:00'} or date[11:16] != slot or not date.startswith('20'):
    raise SystemExit('date and publication_slot must match a 6:00, 8:00, or 10:00 Manila slot')
slot_key = f'{date[:10]}/{slot}'
destination = CONTENT / f'{slug}.md'
existing_manifest = PROJECT / 'src/data/publisher-manifest.json'
if existing_manifest.exists():
    manifest = json.loads(existing_manifest.read_text(encoding='utf-8'))
    for entry in manifest.get('entries', []):
        if entry.get('slot_key') == slot_key and entry.get('slug') != slug:
            raise SystemExit(f'Publication slot already belongs to {entry["slug"]}: {slot_key}')
        if entry.get('slug') == slug and entry.get('slot_key') != slot_key:
            raise SystemExit(f'Slug already belongs to a different slot: {entry["slot_key"]}')
if destination.exists():
    incoming = source.read_bytes()
    current = destination.read_bytes()
    if incoming == current:
        print(f'No-op: {slug} already contains the exact article for {slot_key}.')
        raise SystemExit(0)
    if not args.replace:
        raise SystemExit(f'{destination} exists with different content; use --replace for the same slug')
shutil.copyfile(source, destination)
for script in ('build-publisher-index.py', 'generate-publisher-manifest.py', 'refresh-public-routes.py'):
    subprocess.run([sys.executable, str(PROJECT / 'scripts' / script)], check=True)
subprocess.run([sys.executable, str(PROJECT / 'scripts' / 'validate-astro-publisher.py'), '--only', slug, '--network'], check=True)
print(f'Installed {slug} at {destination.relative_to(PROJECT)} with idempotency key {slot_key}.')
