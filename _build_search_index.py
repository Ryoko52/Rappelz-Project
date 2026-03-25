import os, re, json, html

def extract_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    text = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    for remove in ['RAPPELZ CODEX', 'Back to Home', 'Fan-made community guide',
                    'Not affiliated', 'Content is community-sourced',
                    'In Progress - This guide is being updated.']:
        text = text.replace(remove, '')
    text = re.sub(r'[←→⚠✓⏱✦·—\u2190\u2192\u26A0\u2713\u23F1\u2726\u00B7\u2014]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_title(filepath, fallback):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', c, re.DOTALL)
    if m:
        return html.unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip())
    return fallback

pages = []

for cat, folder, max_text in [('Class', 'docs/class', 500), ('Guide', 'docs/guide', 800),
                                ('Map', 'docs/map', 500), ('Strategy', 'docs/strategy', 500)]:
    base = folder.split('/')[-1]
    for name in sorted(os.listdir(folder)):
        idx = os.path.join(folder, name, 'index.html')
        if os.path.exists(idx):
            text = extract_text(idx)
            title = name.replace('-', ' ').title() if cat == 'Class' else get_title(idx, name.replace('-', ' ').title())
            pages.append({'title': title, 'cat': cat, 'url': base + '/' + name + '/', 'text': text[:max_text]})

for p in pages:
    print(f"[{p['cat']}] {p['title']} => {p['text'][:100]}...")
print(f"\nTotal: {len(pages)} pages indexed")

js = "const SEARCH_INDEX = " + json.dumps(pages, ensure_ascii=False) + ";"
with open('docs/js/search-index.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Written to docs/js/search-index.js")
