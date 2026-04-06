import re, os

os.chdir(r'c:\Users\Administrateur\RappelzProject')

def strip_images(html):
    # Remove all <img .../> tags
    html = re.sub(r'<img\s+[^>]*/\s*>', '', html)
    # Remove the flex div that wrapped optimization images (Void Mage)
    html = re.sub(
        r'\s*<div style="display:flex;gap:2\.5rem;[^"]*">\s*<div[^>]*>\s*'
        r'<span[^>]*>[^<]*</span>\s*</div>\s*<div[^>]*>\s*'
        r'<span[^>]*>[^<]*</span>\s*</div>\s*</div>',
        '', html
    )
    return html

def make_class_page(source_file, target_file, class_name, tier_badge, original_name):
    with open(source_file, 'r', encoding='utf-8') as f:
        html = f.read()
    html = strip_images(html)
    html = html.replace(f'<title>{original_name} Class Guide</title>', f'<title>{class_name} Class Guide</title>')
    html = html.replace(f'<h1>{original_name}</h1>', f'<h1>{class_name}</h1>')
    html = re.sub(r'<span class="tier-badge">[^<]*</span>', f'<span class="tier-badge">{tier_badge}</span>', html)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Written: {target_file}')

# Void Mage -> Cardinal, Magus, Oracle, Corruptor
for t, n, b in [
    ('docs/class/cardinal/index.html', 'Cardinal', 'A Tier'),
    ('docs/class/magus/index.html', 'Magus', 'A Tier'),
    ('docs/class/oracle/index.html', 'Oracle', 'B Tier'),
    ('docs/class/corruptor/index.html', 'Corruptor', 'C Tier'),
]:
    make_class_page('docs/class/void-mage/index.html', t, n, b, 'Void Mage')

# Slayer -> Berserker, War Kahuna, Templar
for t, n, b in [
    ('docs/class/berserker/index.html', 'Berserker', 'B Tier'),
    ('docs/class/war-kahuna/index.html', 'War Kahuna', 'B Tier'),
    ('docs/class/templar/index.html', 'Templar', 'B Tier'),
]:
    make_class_page('docs/class/slayer/index.html', t, n, b, 'Slayer')

# Deadeye -> Marksman
make_class_page('docs/class/deadeye/index.html', 'docs/class/marksman/index.html', 'Marksman', 'C Tier', 'Deadeye')

# Beast Master - complete rewrite with just a message
beast_master_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Beast Master Class Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap" rel="stylesheet"/>
<style>
    a.content-link { color: var(--gold2); text-decoration: underline; }
    a.content-link:hover { color: var(--gold3); }
  :root { --bg0: #0a0907; --bg1: #111009; --bg2: #1a1710; --bg3: #242015; --gold: #c9a84c; --gold2: #e8c96a; --gold3: #f5e098; --gold-dim: #7a6330; --text: #d4c9a8; --text2: #a09070; --text3: #6a5f45; --border: rgba(201,168,76,0.18); }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body { background: var(--bg0); color: var(--text); font-family: 'Crimson Pro', Georgia, serif; font-size: 20px; line-height: 1.75; min-height: 100vh; }
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg1); }
  ::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 3px; }
  header { position: sticky; top: 0; z-index: 100; background: rgba(10,9,7,0.92); border-bottom: 1px solid var(--border); backdrop-filter: blur(12px); padding: 0 2rem; }
  .header-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; gap: 2rem; height: 58px; }
  .logo { font-family: 'Cinzel', serif; font-size: 1.1rem; font-weight: 700; color: var(--gold2); letter-spacing: 0.12em; text-decoration: none; white-space: nowrap; text-shadow: 0 0 20px rgba(201,168,76,0.4); }
  nav { display: flex; gap: 0; flex: 1; }
  nav a { font-family: 'Cinzel', serif; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; color: var(--text2); text-decoration: none; padding: 0 1rem; height: 58px; display: flex; align-items: center; border-bottom: 2px solid transparent; transition: color 0.2s, border-color 0.2s; }
  nav a:hover { color: var(--gold2); border-bottom-color: var(--gold); }
  .page { max-width: 1200px; margin: 0 auto; padding: 3rem 2rem; }
  h1 { font-family: 'Cinzel', serif; font-size: 2.5rem; font-weight: 700; color: var(--gold3); margin-bottom: 1rem; }
  h2 { font-family: 'Cinzel', serif; font-size: 1.5rem; color: var(--gold2); margin: 2rem 0 1rem; }
  p { margin-bottom: 1rem; color: var(--text2); }
  .back-link { font-family: 'Cinzel', serif; font-size: 0.8rem; color: var(--gold-dim); text-decoration: none; margin-bottom: 2rem; display: inline-block; }
  .back-link:hover { color: var(--gold2); }
  .tier-badge { display: inline-block; background: var(--bg3); border: 1px solid var(--border); padding: 0.25rem 0.75rem; border-radius: 3px; color: var(--text2); font-size: 0.9rem; margin-bottom: 1rem; }
  .info-table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }
  .info-table th, .info-table td { padding: 0.5rem 0.8rem; border: 1px solid var(--border); font-size: 1.05em; }
  .info-table th { background: var(--bg3); color: var(--gold2); font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.08em; text-align: left; }
  .info-table td { color: var(--text2); }
  .info-table td:first-child { color: var(--text); font-weight: 600; white-space: nowrap; width: 160px; }
  h3 { font-family: 'Cinzel', serif; font-size: 1.1rem; color: var(--gold-dim); margin: 1.5rem 0 0.5rem; }
  .placeholder { color: var(--text3); font-style: italic; }
  .priority-list { color: var(--text2); padding-left: 1.5rem; margin-bottom: 1.5rem; }
  .priority-list li { margin-bottom: 0.5rem; }
  .priority-list li::marker { color: var(--gold2); font-weight: 600; }
  footer { border-top: 1px solid var(--border); padding: 2rem; text-align: center; color: var(--text3); font-size: 0.82rem; font-style: italic; margin-top: 4rem; }
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <a class="logo" href="../../">RAPPELZ<span style="color:var(--text3);font-weight:400;font-size:0.75rem;margin-left:4px;">GUIDELINES</span></a>
    <nav>
      <a href="../../">&larr; Back to Home</a>
    </nav>
  </div>
</header>

<div class="page">
  <a class="back-link" href="../../">&larr; Back to Home</a>

  <h1>Beast Master</h1>
  <span class="tier-badge">C Tier</span>

  <p style="margin-top:2rem;font-size:1.1em;">Beast Master is currently in need of a rebalance. In its present state, the class is primarily used as a Rupee farmer. Check out the <a class="content-link" href="../../guide/rupee-farming/">Rupee Farming Guide</a> to learn how to make the most of it.</p>

</div>

<footer>
  <strong>RAPPELZ GUIDELINES</strong> &mdash; Fan-made community guide
</footer>

</body>
</html>
'''

with open('docs/class/beast-master/index.html', 'w', encoding='utf-8') as f:
    f.write(beast_master_html)
print('  Written: docs/class/beast-master/index.html')

print('\nAll 9 class pages updated!')
