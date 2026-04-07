#!/usr/bin/env python3
"""Transform all class pages to the new Mercenary-style template.
Reads the CSS from the Mercenary page and applies it to all other class pages,
preserving existing content while wrapping it in the new template structure."""
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLASS_DIR = os.path.join(SCRIPT_DIR, 'docs', 'class')

# Weapon metadata (not in old pages)
WEAPONS = {
    'berserker': '2H Axe',
    'beast-master': 'Crossbow',
    'cardinal': '1H Staff + Magewall',
    'corruptor': '1H Staff + Magewall',
    'deadeye': 'Crossbow',
    'magus': '2H Axe',
    'marksman': 'Crossbow',
    'master-breeder': 'Crossbow / Magewall',
    'oracle': '1H Staff + Magewall',
    'overlord': 'Crossbow / Magewall',
    'slayer': 'Dual 1H Swords',
    'templar': '1H Mace + Shield',
    'void-mage': '1H Staff + Magewall',
    'war-kahuna': '2H Axe',
}

# Fallback overview data for pages that don't have an overview table
OVERVIEW_DEFAULTS = {
    'beast-master': {
        'role': 'DPS',
        'difficulty': 'Easy',
        'strengths': 'Good for Rupee farming',
        'weaknesses': 'Currently in need of rebalance',
        'why_play': 'Rupee farming specialist',
    },
}


def read_css_from_mercenary():
    merc_path = os.path.join(CLASS_DIR, 'mercenary', 'index.html')
    with open(merc_path, 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    return m.group(1) if m else ''


def extract_class_name(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return ''


def extract_tier(html):
    m = re.search(r'<span[^>]+class="tier-badge"[^>]*>(.*?)</span>', html, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return ''


def extract_overview(html, folder):
    """Extract overview data from the first table after Overview heading."""
    data = {'role': '', 'difficulty': '', 'strengths': '', 'weaknesses': '', 'why_play': ''}

    # Check defaults first
    if folder in OVERVIEW_DEFAULTS:
        data.update(OVERVIEW_DEFAULTS[folder])

    # Find overview section
    overview_match = re.search(
        r'(?:id="overview"|>Overview</h2>)(.*?)(?:<h2|$)', html, re.DOTALL
    )
    if not overview_match:
        return data

    section = overview_match.group(1)

    # Extract rows
    rows = re.findall(r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>', section, re.DOTALL)
    for label_html, value_html in rows:
        label = re.sub(r'<[^>]+>', '', label_html).strip().lower()
        value = re.sub(r'<[^>]+>', '', value_html).strip()
        if 'role' in label:
            data['role'] = value
        elif 'difficulty' in label:
            data['difficulty'] = value
        elif 'strength' in label:
            data['strengths'] = value
        elif 'weakness' in label:
            data['weaknesses'] = value
        elif 'why' in label:
            data['why_play'] = value

    return data


def extract_endgame(html):
    perf = solo = None
    m_perf = re.search(r'Performance.*?(\d+)\s*/\s*10', html, re.DOTALL)
    m_solo = re.search(r'Solo\s*(?:Ability)?.*?(\d+)\s*/\s*10', html, re.DOTALL)
    if m_perf:
        perf = int(m_perf.group(1))
    if m_solo:
        solo = int(m_solo.group(1))
    return perf, solo


def extract_toc(html):
    items = []
    # Try existing TOC
    toc_match = re.search(r'<nav class="toc".*?</nav>', html, re.DOTALL)
    if toc_match:
        for m in re.finditer(r'href="#([^"]*)"[^>]*>(.*?)</a>', toc_match.group(0)):
            label = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            label = re.sub(r'^[\u25B8\s]+', '', label).strip()
            items.append((m.group(1), label))

    if not items:
        for m in re.finditer(r'<h2[^>]*id="([^"]*)"[^>]*>(.*?)</h2>', html, re.DOTALL):
            label = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            items.append((m.group(1), label))

    if not items:
        for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL):
            label = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            id_val = re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')
            if id_val and id_val not in [i[0] for i in items]:
                items.append((id_val, label))

    return items


def extract_body_content(html):
    """Extract main content from the page, removing old header/footer/h1/toc."""
    # Find content boundaries
    page_div = html.find('<div class="page">')
    if page_div != -1:
        content_start = page_div + len('<div class="page">')
    else:
        header_end = html.find('</header>')
        content_start = header_end + len('</header>') if header_end != -1 else 0

    footer_pos = html.find('<footer')
    if footer_pos == -1:
        footer_pos = html.find('</body>')
    if footer_pos == -1:
        footer_pos = len(html)

    content = html[content_start:footer_pos]

    # Remove the trailing </div> that matches <div class="page">
    if page_div != -1:
        last_close = content.rfind('</div>')
        if last_close != -1:
            content = content[:last_close]

    # Remove elements that are now in the hero/template
    content = re.sub(r'\s*<a class="back-link"[^>]*>.*?</a>\s*', '\n', content, flags=re.DOTALL)
    content = re.sub(r'\s*<h1[^>]*>.*?</h1>\s*', '\n', content, flags=re.DOTALL)
    content = re.sub(r'\s*<span class="tier-badge"[^>]*>.*?</span>\s*', '\n', content, flags=re.DOTALL)
    content = re.sub(r'\s*<nav class="toc"[^>]*>.*?</nav>\s*', '\n', content, flags=re.DOTALL)
    # Remove template notice (we re-add it separately)
    content = re.sub(
        r'\s*<div style="background:rgba\(180,40,40[^"]*"[^>]*>.*?</div>\s*',
        '\n', content, flags=re.DOTALL
    )

    return content.strip()


def transform_content(content, overview_data, perf_score, solo_score):
    """Apply CSS class transformations to body content."""

    # 1. Transform h2 headings to section-heading
    def replace_h2(m):
        attrs = m.group(1) if m.group(1) else ''
        text = m.group(2)
        if 'section-heading' in attrs:
            return m.group(0)
        id_match = re.search(r'id="([^"]*)"', attrs)
        if id_match:
            id_val = id_match.group(1)
        else:
            id_val = re.sub(r'[^a-z0-9]+', '-',
                            re.sub(r'<[^>]+>', '', text).lower()).strip('-')
        return f'<h2 class="section-heading" id="{id_val}" data-section>{text}</h2>'

    content = re.sub(r'<h2([^>]*)>(.*?)</h2>', replace_h2, content)

    # 2. Replace info-table → data-table
    content = content.replace('class="info-table"', 'class="data-table"')

    # 3. Replace priority-list → gear-steps
    content = content.replace('class="priority-list"', 'class="gear-steps"')

    # 4. Replace overview table with overview-grid
    if overview_data.get('role'):
        overview_grid = f'''
    <div class="overview-grid">
      <div class="overview-cell">
        <div class="ov-label">Role</div>
        <div class="ov-value">{overview_data["role"]}</div>
      </div>
      <div class="overview-cell">
        <div class="ov-label">Difficulty</div>
        <div class="ov-value">{overview_data["difficulty"]}</div>
      </div>
      <div class="overview-cell">
        <div class="ov-label">Strengths</div>
        <div class="ov-value">{overview_data["strengths"]}</div>
      </div>
      <div class="overview-cell">
        <div class="ov-label">Weaknesses</div>
        <div class="ov-value">{overview_data["weaknesses"]}</div>
      </div>
      <div class="overview-cell" style="grid-column: 1 / -1;">
        <div class="ov-label">Why Play It</div>
        <div class="ov-value">{overview_data["why_play"]}</div>
      </div>
    </div>'''

        # Replace old overview table
        content = re.sub(
            r'(<h2[^>]*id="overview"[^>]*>.*?</h2>)\s*<table class="data-table">.*?</table>',
            lambda m: m.group(1) + '\n' + overview_grid,
            content, count=1, flags=re.DOTALL
        )

    # 5. Replace endgame section with ratings grid
    if perf_score is not None and solo_score is not None:
        ratings_html = f'''
    <div class="ratings-grid">
      <div class="rating-card">
        <div class="rating-label">Performance</div>
        <div class="rating-score">{perf_score}<sub>/10</sub></div>
        <div class="rating-bar"><div class="rating-fill" style="width:{perf_score*10}%"></div></div>
      </div>
      <div class="rating-card">
        <div class="rating-label">Solo Ability</div>
        <div class="rating-score">{solo_score}<sub>/10</sub></div>
        <div class="rating-bar"><div class="rating-fill" style="width:{solo_score*10}%"></div></div>
      </div>
    </div>'''

        # Replace the endgame table with ratings grid
        content = re.sub(
            r'(<h2[^>]*id="endgame"[^>]*>.*?</h2>)\s*<table[^>]*>.*?</table>',
            lambda m: m.group(1) + '\n' + ratings_html,
            content, count=1, flags=re.DOTALL
        )

    # 6. Add inline-icon class to skill images in gameplay/text paragraphs
    # (images inside <p> tags that use height:28px or height:24px inline styles)
    content = re.sub(
        r'(<img[^>]*style="height:(?:28|24|22|32)px;vertical-align:middle[^"]*"[^>]*/>)',
        lambda m: m.group(1).replace('style="', 'class="inline-icon" style="') if 'class=' not in m.group(1) else m.group(1),
        content
    )

    return content


def build_page(css, class_name, letter, tier, role, difficulty, weapon,
               toc_items, body_content, has_notice):
    toc_html = '\n'.join([
        f'        <li><a href="#{id}">{label}</a></li>'
        for id, label in toc_items
    ])

    notice_html = ''
    if has_notice:
        notice_html = '''
    <div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.3);border-left:3px solid var(--gold-dim);padding:0.8rem 1.2rem;margin-bottom:1.5rem;color:var(--gold2);font-style:italic;">
      &#9888; Just a template for now &mdash; will be updated when the classes are rebalanced.
    </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{class_name} &mdash; Rappelz Guidelines</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cinzel:wght@400;600;700&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap" rel="stylesheet"/>
<style>
{css}
</style>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="header-inner">
    <a class="logo" href="../../">RAPPELZ<span>GUIDELINES</span></a>
    <nav class="topnav">
      <a href="../../">\u2190 Back to Home</a>
    </nav>
  </div>
</header>

<!-- HERO -->
<div class="hero">
  <div class="hero-inner">
    <div class="breadcrumb">
      <a href="../../">Home</a>
      <span class="sep">\u203a</span>
      Classes
      <span class="sep">\u203a</span>
      {class_name}
    </div>

    <div class="hero-title-block">
      <div class="hero-letter">{letter}</div>
      <div class="hero-text">
        <div class="class-eyebrow">Class Guide</div>
        <h1 class="class-title">{class_name}</h1>
        <div class="tier-pill">
          <span class="tier-dot"></span>
          {tier}
        </div>
        <div class="hero-meta">
          <div class="meta-chip">
            <span class="label">Role</span>
            <span class="value">{role}</span>
          </div>
          <div class="meta-divider"></div>
          <div class="meta-chip">
            <span class="label">Difficulty</span>
            <span class="value">{difficulty}</span>
          </div>
          <div class="meta-divider"></div>
          <div class="meta-chip">
            <span class="label">Weapon</span>
            <span class="value">{weapon}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="divider"></div>

<!-- BODY -->
<div class="page-body">

  <!-- SIDEBAR TOC -->
  <aside class="sidebar">
    <nav class="toc-card" aria-label="Table of contents">
      <div class="toc-title">Contents</div>
      <ul class="toc-list">
{toc_html}
      </ul>
    </nav>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="content">
{notice_html}
    {body_content}

  </main>
</div>

<footer>
  <div class="footer-logo">Rappelz Guidelines</div>
  <div class="footer-sub">Fan-made community guide &mdash; not affiliated with Valofe</div>
</footer>

</body>
</html>'''


def main():
    css = read_css_from_mercenary()
    if not css:
        print("ERROR: Could not read CSS from mercenary page")
        return

    processed = 0
    for folder in sorted(os.listdir(CLASS_DIR)):
        if folder == 'mercenary':
            continue

        filepath = os.path.join(CLASS_DIR, folder, 'index.html')
        if not os.path.isfile(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        class_name = extract_class_name(html)
        if not class_name:
            print(f"  Skipping {folder}: no class name found")
            continue

        tier = extract_tier(html)
        overview = extract_overview(html, folder)
        perf, solo = extract_endgame(html)
        toc_items = extract_toc(html)
        weapon = WEAPONS.get(folder, 'Unknown')
        has_notice = 'Just a template' in html

        body_content = extract_body_content(html)
        body_content = transform_content(body_content, overview, perf, solo)

        role = overview.get('role', '') or 'Unknown'
        difficulty = overview.get('difficulty', '') or 'Unknown'

        # If no toc items found in old content, re-extract from transformed content
        if not toc_items:
            toc_items = []
            for m in re.finditer(r'<h2[^>]*id="([^"]*)"[^>]*>(.*?)</h2>', body_content):
                label = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                toc_items.append((m.group(1), label))

        page = build_page(
            css=css,
            class_name=class_name,
            letter=class_name[0],
            tier=tier,
            role=role,
            difficulty=difficulty,
            weapon=weapon,
            toc_items=toc_items,
            body_content=body_content,
            has_notice=has_notice,
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page)

        processed += 1
        print(f"  OK  {class_name} ({folder})")

    print(f"\nDone! {processed} class pages updated.")


if __name__ == '__main__':
    main()
