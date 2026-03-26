"""
Builds docs/js/search-index.js by extracting text from all HTML pages in docs/.
Run from the project root: python build_search_index.py
"""
import os
import re
import json
import html

DOCS = os.path.join(os.path.dirname(__file__), 'docs')
OUT = os.path.join(DOCS, 'js', 'search-index.js')

# Map folder prefixes to categories
CAT_MAP = {
    'class': 'Class',
    'guide': 'Guide',
    'map': 'Map',
}

def strip_html(raw):
    """Remove HTML tags, decode entities, collapse whitespace."""
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', raw, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_title(raw):
    """Extract <title> or first <h1>/<h2>."""
    m = re.search(r'<title[^>]*>(.*?)</title>', raw, re.DOTALL | re.IGNORECASE)
    if m:
        t = strip_html(m.group(1)).replace(' - Rappelz Codex', '').strip()
        if t:
            return t
    for tag in ['h1', 'h2']:
        m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', raw, re.DOTALL | re.IGNORECASE)
        if m:
            return strip_html(m.group(1))
    return ''

entries = []

for root, dirs, files in os.walk(DOCS):
    for fname in files:
        if fname != 'index.html':
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, DOCS).replace('\\', '/')

        # Skip the main index.html (that's the homepage, not a content page)
        if rel == 'index.html':
            continue

        # Determine category from first folder
        parts = rel.split('/')
        if len(parts) < 2:
            continue
        cat_key = parts[0]
        cat = CAT_MAP.get(cat_key)
        if not cat:
            continue

        # URL is the folder path relative to docs/
        url = '/'.join(parts[:-1]) + '/'

        with open(fpath, 'r', encoding='utf-8') as f:
            raw = f.read()

        title = get_title(raw)
        text = strip_html(raw)

        # Truncate very long texts to keep the JS file reasonable (max ~5000 chars)
        if len(text) > 5000:
            text = text[:5000]

        if title:
            entries.append({
                'title': title,
                'cat': cat,
                'url': url,
                'text': text,
            })

# Sort: Classes first, then Guides, then Maps
order = {'Class': 0, 'Guide': 1, 'Map': 2}
entries.sort(key=lambda e: (order.get(e['cat'], 9), e['title']))

js = 'const SEARCH_INDEX = ' + json.dumps(entries, ensure_ascii=False) + ';\n'
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'Built search index with {len(entries)} entries -> {OUT}')
