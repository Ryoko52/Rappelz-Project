#!/usr/bin/env python3
"""Add Boss Cards section after Gear in every class page, and update TOC."""
import os
import re

CLASS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'class')

BOSS_CARDS_HTML = '''
  <h2 class="section-heading" id="boss-cards" data-section>Boss Cards</h2>
  <p>Boss cards provide massive stat boosts that rival high-level gear upgrades. Check the full guide for priority cards and collection details:</p>
  <p><a href="../../guide/boss-card-collection/" style="color:var(--gold2);text-decoration:underline;">Boss Card Collection Guide &rarr;</a></p>'''


def process_file(filepath, folder):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Remove any existing boss-cards section
    html = re.sub(r'<h2 class="section-heading" id="boss-cards"[\s\S]*?</h2>[\s\S]*?<p>Boss cards[\s\S]*?</p>\s*<p><a href="[^"]*boss-card-collection[\s\S]*?</p>', '', html, flags=re.DOTALL)
    html = re.sub(r'<li><a href="#boss-cards">Boss Cards</a></li>\s*', '', html)

    # Skip if no gear section (e.g. beast-master stub)
    if 'id="gear"' not in html:
        print(f"  SKIP {folder}: no Gear section")
        return

    # Find the next h2 after the gear section and insert before it
    gear_match = re.search(r'id="gear"[^>]*data-section>.*?</h2>', html, re.DOTALL)
    if not gear_match:
        print(f"  SKIP {folder}: could not find gear heading")
        return

    after_gear = html[gear_match.end():]
    next_h2 = re.search(r'\n(\s*<h2\s)', after_gear)
    if next_h2:
        insert_pos = gear_match.end() + next_h2.start()
        html = html[:insert_pos] + '\n' + BOSS_CARDS_HTML + '\n' + html[insert_pos:]
    else:
        main_close = html.rfind('</main>')
        if main_close != -1:
            html = html[:main_close] + BOSS_CARDS_HTML + '\n\n' + html[main_close:]

    # Update TOC: add Boss Cards after Gear
    toc_gear_pattern = r'(<li><a href="#gear">Gear</a></li>)'
    toc_replacement = r'\1\n        <li><a href="#boss-cards">Boss Cards</a></li>'
    html = re.sub(toc_gear_pattern, toc_replacement, html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  OK  {folder}")


def main():
    count = 0
    for folder in sorted(os.listdir(CLASS_DIR)):
        filepath = os.path.join(CLASS_DIR, folder, 'index.html')
        if not os.path.isfile(filepath):
            continue
        process_file(filepath, folder)
        count += 1
    print(f"\nProcessed {count} class folders.")


if __name__ == '__main__':
    main()
