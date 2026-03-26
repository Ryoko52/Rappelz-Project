"""
Apply the class guide template to all class pages in docs/class/*/index.html.
Preserves existing class name + tier badge, replaces placeholder content with template.
"""
import os
import re

DOCS = os.path.join(os.path.dirname(__file__), 'docs', 'class')

TEMPLATE_SECTIONS = """
  <h2>Overview</h2>
  <table class="info-table">
    <tr><td><strong>Role</strong></td><td>&mdash;</td></tr>
    <tr><td><strong>Difficulty</strong></td><td>&mdash;</td></tr>
    <tr><td><strong>Strengths</strong></td><td>&mdash;</td></tr>
    <tr><td><strong>Weaknesses</strong></td><td>&mdash;</td></tr>
    <tr><td><strong>Why Play It</strong></td><td>&mdash;</td></tr>
  </table>

  <h2>Skills</h2>
  <h3>Main Skills</h3>
  <p class="placeholder">&mdash;</p>
  <h3>Useful Skills</h3>
  <p class="placeholder">&mdash;</p>
  <h3>Defensive &amp; Utility</h3>
  <p class="placeholder">&mdash;</p>

  <h2>Rotations</h2>
  <h3>Single Target</h3>
  <p class="placeholder">&mdash;</p>
  <h3>AoE / Multi-Target</h3>
  <p class="placeholder">&mdash;</p>

  <h2>Talent Build</h2>
  <table class="info-table">
    <thead><tr><th>Points</th><th>Allocation</th></tr></thead>
    <tbody>
      <tr><td>5 TP</td><td>&mdash;</td></tr>
      <tr><td>6 TP</td><td>&mdash;</td></tr>
      <tr><td>7 TP</td><td>&mdash;</td></tr>
    </tbody>
  </table>

  <h2>Stats</h2>
  <table class="info-table">
    <thead><tr><th>Priority</th><th>Stats</th></tr></thead>
    <tbody>
      <tr><td>Damage</td><td>&mdash;</td></tr>
      <tr><td>Defense</td><td>&mdash;</td></tr>
      <tr><td>Caps</td><td>&mdash;</td></tr>
    </tbody>
  </table>

  <h2>Accessories</h2>
  <table class="info-table">
    <thead><tr><th>Setup</th><th>Accessories</th></tr></thead>
    <tbody>
      <tr><td>Damage</td><td>&mdash;</td></tr>
      <tr><td>Defense</td><td>&mdash;</td></tr>
    </tbody>
  </table>

  <h2>Pets &amp; Belt</h2>
  <table class="info-table">
    <thead><tr><th>Slot</th><th>Recommendation</th></tr></thead>
    <tbody>
      <tr><td>Best in Slot</td><td>&mdash;</td></tr>
      <tr><td>Budget</td><td>&mdash;</td></tr>
    </tbody>
  </table>

  <h2>Gear</h2>
  <h3>Progression Path</h3>
  <p class="placeholder">&mdash;</p>
  <h3>Optimization</h3>
  <p class="placeholder">&mdash;</p>

  <h2>Upgrade Priority</h2>
  <ol class="priority-list">
    <li>&mdash;</li>
    <li>&mdash;</li>
    <li>&mdash;</li>
  </ol>

  <h2>Leveling Progression</h2>
  <p class="placeholder">&mdash;</p>

  <h2>Tips</h2>
  <p class="placeholder">&mdash;</p>

  <h2>Endgame</h2>
  <table class="info-table">
    <thead><tr><th>Aspect</th><th>Rating</th></tr></thead>
    <tbody>
      <tr><td>Performance</td><td>&mdash;</td></tr>
      <tr><td>Solo Ability</td><td>&mdash;</td></tr>
      <tr><td>Budget Friendliness</td><td>&mdash;</td></tr>
    </tbody>
  </table>
"""

EXTRA_CSS = """  .info-table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }
  .info-table th, .info-table td { padding: 0.5rem 0.8rem; border: 1px solid var(--border); font-size: 0.92rem; }
  .info-table th { background: var(--bg3); color: var(--gold2); font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.08em; text-align: left; }
  .info-table td { color: var(--text2); }
  .info-table td:first-child { color: var(--text); font-weight: 600; white-space: nowrap; width: 160px; }
  h3 { font-family: 'Cinzel', serif; font-size: 1.1rem; color: var(--gold-dim); margin: 1.5rem 0 0.5rem; }
  .placeholder { color: var(--text3); font-style: italic; }
  .priority-list { color: var(--text2); padding-left: 1.5rem; margin-bottom: 1.5rem; }
  .priority-list li { margin-bottom: 0.5rem; }
  .priority-list li::marker { color: var(--gold2); font-weight: 600; }"""

for folder in sorted(os.listdir(DOCS)):
    fpath = os.path.join(DOCS, folder, 'index.html')
    if not os.path.isfile(fpath):
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract class name and tier
    name_match = re.search(r'<h1>(.*?)</h1>', html)
    tier_match = re.search(r'<span class="tier-badge">(.*?)</span>', html)
    class_name = name_match.group(1) if name_match else folder.replace('-', ' ').title()
    tier_text = tier_match.group(0) if tier_match else ''

    # Add extra CSS before footer CSS
    if '.info-table' not in html:
        html = html.replace(
            '  footer { border-top:',
            EXTRA_CSS + '\n  footer { border-top:'
        )

    # Replace the page content (everything between <h1>...</h1> line and </div>\n\n<footer>)
    # Find the placeholder paragraph and replace it with template
    old_placeholder = '  <p style="font-size:1rem;color:var(--gold2);background:rgba(201,168,76,0.1);padding:1rem;border-left:3px solid var(--gold2);margin-bottom:2rem;">&#9888; In Progress - This guide is being updated.</p>\n</div>'
    new_content = TEMPLATE_SECTIONS + '\n</div>'

    if old_placeholder in html:
        html = html.replace(old_placeholder, new_content)
    else:
        print(f'  SKIP {folder} - no placeholder found')
        continue

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'  OK {folder} ({class_name}, {tier_text})')

print('Done.')
