#!/usr/bin/env python3
"""Compare a proposed Astro article against the current published index."""
import argparse
import difflib
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--title', required=True)
parser.add_argument('--focus-keyword', default='')
parser.add_argument('--limit', type=int, default=5)
args = parser.parse_args()
posts = json.loads((Path(__file__).resolve().parents[1] / 'src/data/post-index.json').read_text(encoding='utf-8'))

def normalize(value):
    return re.sub(r'[^a-z0-9 ]+', '', value.lower()).strip()

query = normalize(args.title)
focus = normalize(args.focus_keyword)
ranked = []
for post in posts:
    title = normalize(post['title'])
    similarity = difflib.SequenceMatcher(a=query, b=title).ratio()
    overlap = len(set(query.split()) & set(title.split())) / max(1, len(set(query.split())))
    keyword_hit = 0.1 if focus and focus in title else 0
    score = min(1.0, (similarity * 0.7) + (overlap * 0.3) + keyword_hit)
    ranked.append((score, post['slug'], post['title'], post['date']))
ranked.sort(reverse=True)
for score, slug, title, date in ranked[:args.limit]:
    print(f'{score:.3f}\t{date}\t{slug}\t{title}')
if ranked and ranked[0][0] >= 0.86:
    raise SystemExit('Potential duplicate: review the highest-scoring existing article before publishing.')
