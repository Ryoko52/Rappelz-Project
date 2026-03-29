#!/usr/bin/env python3
"""Generate a SEARCH_INDEX JS file from HTML files under docs/.

Usage: python scripts/generate_search_index.py
This writes `docs/js/search-index.js` (backing up the previous file to .bak).
"""
import os
import io
import json
import re
from html.parser import HTMLParser


class VisibleTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._texts = []
        self._skip = False
        self._in_title = False
        self.title = ''

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in ("script", "style", "noscript"):
            self._skip = True
        if tag == 'title':
            self._in_title = True

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("script", "style", "noscript"):
            self._skip = False
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
            return
        if self._skip:
            return
        text = data.strip()
        if text:
            # collapse whitespace
            text = re.sub(r"\s+", " ", text)
            self._texts.append(text)

    def get_text(self):
        return ' '.join(self._texts)


def build_index(docs_root='docs', out_js='docs/js/search-index.js'):
    entries = []
    docs_root = os.path.normpath(docs_root)
    for root, dirs, files in os.walk(docs_root):
        # skip assets folders
        skip_dirs = ('js', 'css', 'images')
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in files:
            if not fname.lower().endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, docs_root).replace('\\', '/')
            # infer url
            parts = rel.split('/')
            if parts[-1].lower() == 'index.html':
                url = '/'.join(parts[:-1])
                if url == '':
                    url = ''
                else:
                    url = url + '/'
            else:
                url = rel

            # category as first path part or Home
            cat = parts[0] if len(parts) > 1 else 'Home'

            with io.open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                html = fh.read()

            parser = VisibleTextExtractor()
            try:
                parser.feed(html)
            except Exception:
                # fallback: strip tags naively
                txt = re.sub(r'<[^>]+>', ' ', html)
                txt = re.sub(r'\s+', ' ', txt).strip()
                title = ''
            else:
                txt = parser.get_text()
                title = parser.title or (parts[-2] if len(parts) > 1 else parts[-1])

            # create a short text blob for searching (limit size)
            text_blob = re.sub(r'\s+', ' ', (title + ' ' + txt)).strip()
            if len(text_blob) > 20000:
                text_blob = text_blob[:20000]

            entry = {
                'title': title if title else os.path.splitext(parts[-1])[0].replace('-', ' ').title(),
                'cat': cat.title(),
                'url': url,
                'text': text_blob
            }
            entries.append(entry)

    # write out file (backup old)
    if os.path.exists(out_js):
        try:
            bak = out_js + '.bak'
            os.replace(out_js, bak)
        except Exception:
            pass

    # Dump JSON with pretty formatting for easier diffs
    with io.open(out_js, 'w', encoding='utf-8') as out:
        out.write('const SEARCH_INDEX = ')
        json.dump(entries, out, ensure_ascii=False, indent=2)
        out.write(';\n')

    print('Wrote', out_js, 'with', len(entries), 'entries')


if __name__ == '__main__':
    build_index()
