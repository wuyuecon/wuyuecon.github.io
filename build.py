"""Build a dependency-free academic website. Run: python build.py"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
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

def education_rows():
    return ''.join(f'''<div class="record"><div><h3>{e(x['degree'])}</h3><p>{e(DATA['department'])}<br>{e(DATA['university'])}</p>{f"<p class='record-note'>{e(x['detail'])}</p>" if x['detail'] else ''}</div><p class="record-date">{e(x['dates'])}</p></div>''' for x in DATA['education'])

def home():
    papers = ''.join(f'''<article class="paper-preview"><span class="paper-index">{i:02d}</span><div><h3><a href="working-papers.html#{e(p['id'])}">{e(p['title'])}</a></h3><p class="coauthors">with {e(p['coauthors'])}</p><p class="paper-summary">{e(p['summary'])}</p></div><a class="row-arrow" href="working-papers.html#{e(p['id'])}" aria-label="Read about {e(p['title'])}">{RIGHT}</a></article>''' for i,p in enumerate(DATA['papers'],1))
    bio = ''.join(f'<p>{e(x)}</p>' for x in DATA['bio'])
    return f'''
<section class="profile wrap" aria-labelledby="profile-heading">
  <div class="profile-main">
    <p class="eyebrow">Economics <span class="small-rule" aria-hidden="true"></span> Peking University</p>
    <h1 id="profile-heading">Yu Wu <span lang="zh-Hans">吴裕</span></h1>
    <p class="position">PhD Candidate in Economics</p>
    <div class="biography">{bio}</div>
    <div class="profile-actions"><a class="button" href="{CV}" target="_blank" rel="noopener">View CV <span class="button-note">PDF</span> {ARROW}</a><a class="text-link" href="working-papers.html">View working papers {RIGHT}</a></div>
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
<section class="research-overview wrap" aria-labelledby="working-heading">
  <div class="section-heading"><div><p class="eyebrow">Research</p><h2 id="working-heading">Working papers</h2></div><a class="text-link" href="working-papers.html">View all papers {RIGHT}</a></div>
  <div class="paper-list">{papers}</div>
</section>
<section class="home-education wrap" aria-labelledby="education-heading"><div class="section-heading"><div><p class="eyebrow">Background</p><h2 id="education-heading">Education</h2></div><a class="text-link" href="{CV}" target="_blank" rel="noopener">Full CV (PDF) {ARROW}</a></div>{education_rows()}</section>
'''

def working_papers():
    papers = ''.join(f'''<article class="paper-full" id="{e(p['id'])}" aria-labelledby="title-{e(p['id'])}"><div class="paper-margin"><span class="paper-index">{i:02d}</span><span class="paper-type">Working paper</span></div><div class="paper-body"><p class="eyebrow topic">{e(p['topic'])}</p><h2 id="title-{e(p['id'])}">{e(p['title'])}</h2><p class="coauthors">with {e(p['coauthors'])}</p><p class="paper-lead">{e(p['summary'])}</p><details><summary><span>Read abstract</span><span class="details-symbol" aria-hidden="true"></span></summary><div class="abstract"><p>{e(p['abstract'])}</p></div></details></div></article>''' for i,p in enumerate(DATA['papers'],1))
    return f'''<div class="wrap inner-page"><section class="page-intro" aria-labelledby="research-heading"><p class="eyebrow">Yu Wu / Research</p><h1 id="research-heading">Working Papers</h1><p class="page-deck">My work studies labor markets, migration, and the Chinese economy.</p>{research_fields()}</section><section class="working-section" aria-labelledby="papers-heading"><div class="section-heading compact"><h2 id="papers-heading">Working papers</h2><span class="count">{len(DATA['papers']):02d}</span></div>{papers}</section><div class="contact-strip"><p>For questions about my research, please get in touch.</p><a class="text-link" href="mailto:{e(DATA['email'])}">Email me {ARROW}</a></div></div>'''

def publications():
    return f'''<div class="wrap inner-page publications-page"><section class="page-intro" aria-labelledby="publications-heading"><p class="eyebrow">Yu Wu / Research</p><h1 id="publications-heading">Publications</h1></section><section class="publication-empty" aria-label="Publication list"><p>No publications listed yet.</p><a class="text-link" href="working-papers.html">View working papers {RIGHT}</a></section></div>'''

PAGES = {
    'index.html': ('home', 'Yu Wu | Economics · Peking University', 'Yu Wu (吴裕) is a PhD Candidate in Economics at Peking University. Research interests: Macro Labor and China Economy.', home()),
    'working-papers.html': ('working-papers', 'Working Papers | Yu Wu', 'Working papers by Yu Wu on migration, public benefits, employer feedback, and job search.', working_papers()),
    'publications.html': ('publications', 'Publications | Yu Wu', 'Publications page of Yu Wu, PhD Candidate in Economics at Peking University.', publications()),
}
for filename, args in PAGES.items():
    (OUT / filename).write_text(frame(*args), encoding='utf-8')
print('Built 3 pages in', OUT)
