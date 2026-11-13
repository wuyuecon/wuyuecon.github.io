"""Build a dependency-free academic website. Run: python build.py"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'docs'
DATA = json.loads((ROOT / 'site-data.json').read_text(encoding='utf-8'))
OUT.mkdir(exist_ok=True)

def e(value):
    return escape(str(value), quote=True)

ARROW = '<span aria-hidden="true">↗</span>'
RIGHT = '<span aria-hidden="true">→</span>'
CV = 'assets/yu-wu-cv.pdf'

def frame(page, title, description, content):
    links = [('home', 'index.html', 'Home'), ('working-papers', 'working-papers.html', 'Working Papers'), ('publications', 'publications.html', 'Publications')]
    nav = ''.join(f'<a href="{url}" {"aria-current=\"page\"" if key == page else ""}>{label}</a>' for key, url, label in links)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#faf9f6">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body class="page-{page}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="wordmark" href="index.html" aria-label="Yu Wu — Home">Yu Wu <span lang="zh-Hans">吴裕</span></a>
    <nav aria-label="Main navigation">{nav}</nav>
  </div>
</header>
<main id="main" tabindex="-1">{content}</main>
<footer class="site-footer wrap">
  <p>Yu Wu <span class="footer-dot">·</span> <span>Peking University</span></p>
  <a href="mailto:{e(DATA['email'])}">{e(DATA['email'])} {ARROW}</a>
</footer>
</body>
</html>
'''

def research_fields():
    return '<ul class="field-list">' + ''.join(f'<li>{e(x)}</li>' for x in DATA['interests']) + '</ul>'

def home():
    bio = ''.join(f'<p>{e(x)}</p>' for x in DATA['bio'])
    return f'''
<section class="profile wrap" aria-labelledby="profile-heading">
  <div class="profile-main">
    <p class="eyebrow">Economics <span class="small-rule" aria-hidden="true"></span> Peking University</p>
    <h1 id="profile-heading">Yu Wu <span lang="zh-Hans">吴裕</span></h1>
    <p class="position">PhD Candidate in Economics</p>
    <div class="biography">{bio}</div>
    <div class="profile-actions"><a class="button" href="{CV}" target="_blank" rel="noopener">View CV <span class="button-note">PDF</span> {ARROW}</a></div>
  </div>
  <aside class="profile-aside" aria-label="Academic profile">
    <div class="aside-heading"><span class="tiny-square" aria-hidden="true"></span> Academic profile</div>
    <dl>
      <div><dt>Affiliation</dt><dd>National School of Development<br>Peking University</dd></div>
      <div><dt>Research interests</dt><dd>{research_fields()}</dd></div>
      <div><dt>Advisor</dt><dd>Bo Zhao</dd></div>
      <div><dt>Contact</dt><dd><a href="mailto:{e(DATA['email'])}">{e(DATA['email'])} {ARROW}</a></dd></div>
    </dl>
  </aside>
</section>
'''

def paper_entry(p):
    display = DATA.get('paperDisplay', {})
    fields = [p[key] for key, setting, default in [('date', 'dates', False), ('status', 'status', True)] if display.get(setting, default) and p.get(key)]
    metadata = f' <span class="paper-metadata-inline">({e(", ".join(fields))})</span>' if fields else ''
    coauthors = f' <span class="paper-coauthors">(with {e(p["coauthors"])})</span>' if display.get('coauthors', True) and p.get('coauthors') else ''
    title = f'<span class="paper-title-plain">{e(p["title"])}</span>'
    if p.get('pdf'):
        pdf_path = Path(p['pdf'])
        target = (OUT / pdf_path).resolve()
        if pdf_path.is_absolute() or not target.is_relative_to(OUT.resolve()) or not target.is_file() or target.suffix.lower() != '.pdf':
            raise ValueError(f"Paper PDF must exist inside docs/: {p['pdf']}")
        title = f'<a class="paper-title" href="{e(pdf_path.as_posix())}" download>{e(p["title"])}</a>'
    return f'<li class="paper-entry" id="{e(p["id"])}">{title}{coauthors}{metadata}</li>'

def visible_papers(key):
    return [p for p in DATA.get(key, []) if p.get('visible', True)]

def working_papers():
    papers = ''.join(paper_entry(p) for p in visible_papers('papers'))
    return f'''<div class="wrap inner-page research-list-page"><section class="page-intro" aria-labelledby="research-heading"><h1 id="research-heading">Working Papers</h1></section><ol class="paper-list-compact" aria-label="Working paper list">{papers}</ol></div>'''

def publications():
    papers = ''.join(paper_entry(p) for p in visible_papers('publications'))
    content = f'<ol class="paper-list-compact" aria-label="Publication list">{papers}</ol>' if papers else f'<section class="publication-empty" aria-label="Publication list"><p>No publications listed yet.</p><a class="text-link" href="working-papers.html">View working papers {RIGHT}</a></section>'
    return f'''<div class="wrap inner-page publications-page"><section class="page-intro" aria-labelledby="publications-heading"><p class="eyebrow">Yu Wu / Research</p><h1 id="publications-heading">Publications</h1></section>{content}</div>'''

PAGES = {
    'index.html': ('home', 'Yu Wu | Economics · Peking University', 'Yu Wu (吴裕) is a PhD Candidate in Economics at Peking University. Research interests: Macro Labor and China Economy.', home()),
    'working-papers.html': ('working-papers', 'Working Papers | Yu Wu', 'Working papers by Yu Wu on migration, public benefits, employer feedback, and job search.', working_papers()),
    'publications.html': ('publications', 'Publications | Yu Wu', 'Publications page of Yu Wu, PhD Candidate in Economics at Peking University.', publications()),
}
for filename, args in PAGES.items():
    (OUT / filename).write_text(frame(*args), encoding='utf-8')
print('Built 3 pages in', OUT)
