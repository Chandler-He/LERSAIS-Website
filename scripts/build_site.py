#!/usr/bin/env python3
"""Build the static LERSAIS website. Python 3 standard library only."""
from pathlib import Path
from html import escape, unescape
import json
import re

ROOT = Path(__file__).resolve().parent.parent
PEOPLE = json.loads((ROOT / 'data/people.json').read_text())
NEWS = json.loads((ROOT / 'data/news.json').read_text())
IMAGE_SIZES = json.loads((ROOT / 'data/image-sizes.json').read_text())
ARROW = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'
EXTERNAL = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 18 18 6M6 6h12v12"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg>'
NAV = [('research', 'Research'), ('people', 'People'), ('publications', 'Publications'), ('news', 'News'), ('teaching', 'Education'), ('gallery', 'Gallery')]


def size_images(html):
    """Reserve each image's real aspect ratio; CSS owns the display size."""
    def size_tag(match):
        tag = match.group(0)
        source = re.search(r'\bsrc="([^"]+)"', tag)
        dimensions = IMAGE_SIZES.get(source.group(1)) if source else None
        if dimensions:
            tag = re.sub(r'\s+(?:width|height)="[^"]*"', '', tag)
            width, height = dimensions
            tag = tag[:-1] + f' width="{width}" height="{height}">'
        return tag
    return re.sub(r'<img\b[^>]*>', size_tag, html)


def link(url, text, kind='text-link', external=False):
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a class="{kind}" href="{escape(url, quote=True)}"{attrs}>{text}{EXTERNAL if external else ARROW}</a>'


def header(active=''):
    nav = ''.join(f'<a href="{slug}.html"' + (' aria-current="page"' if slug == active else '') + f'>{label}</a>' for slug, label in NAV)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner">
  <div class="identity"><a class="wordmark" href="index.html" aria-label="LERSAIS home">LERSAIS</a><a class="pitt-identity" href="https://www.pitt.edu/" aria-label="University of Pittsburgh"><img src="images/pitt-logo-blue.svg" alt="University of Pittsburgh" width="130" height="40"></a></div>
  <button class="menu-toggle" type="button" aria-label="Open navigation" aria-controls="site-nav" aria-expanded="false"><span></span><span></span></button>
  <nav id="site-nav" class="site-nav" aria-label="Main navigation">{nav}{link('contact.html', 'Contact', 'button nav-contact')}</nav>
</div></header>'''


def footer():
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="footer-top"><div class="footer-about"><a class="wordmark" href="index.html">LERSAIS</a><p>Laboratory for Education and Research on<br>Security Assured Information Systems</p><p>School of Computing and Information<br>University of Pittsburgh</p></div>
  <div><h2>Explore</h2><a href="research.html">Research</a><a href="people.html">People</a><a href="publications.html">Publications</a></div>
  <div><h2>Discover</h2><a href="news.html">News & events</a><a href="teaching.html">Education</a><a href="gallery.html">Life at LERSAIS</a></div>
  <div><h2>Find us</h2><p>Information Sciences Building<br>135 N. Bellefield Avenue, Room 410<br>Pittsburgh, PA 15213</p><a href="mailto:jjoshi@pitt.edu">jjoshi@pitt.edu</a></div></div>
  <div class="footer-bottom"><p>© <span data-year>2026</span> LERSAIS · University of Pittsburgh</p><p>Website by <a href="https://sites.pitt.edu/~peh53/" target="_blank" rel="noopener noreferrer">Peilin He</a></p><a href="#main" class="back-top">Back to top ↑</a></div>
</div></footer>'''


def page(slug, title, description, content):
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | LERSAIS · University of Pittsburgh</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#ffffff"><link rel="icon" href="images/pitt-logo-blue.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/site.css"><script src="js/site.js" defer></script></head>
<body class="page-{slug}">{header(slug)}<main id="main" tabindex="-1">{content}</main>{footer()}</body></html>'''
    (ROOT / f'{slug}.html').write_text(size_images(html) + '\n')


def heading(title, subtitle):
    return f'<div class="page-heading wrap"><h1>{title}</h1><p>{subtitle}</p></div>'


def cta():
    return f'''<section class="join-section wrap"><h2>Let’s build a more<br>trusted world.</h2><div><p>Bring your curiosity. Share your perspective.<br>Explore research and collaboration at LERSAIS.</p>{link('contact.html', 'Get in touch', 'button')}</div></section>'''


AREAS = [
    ('trustworthy-ai', 'Trustworthy AI', 'Understanding and strengthening privacy, trust, and security in machine learning.', 'Our researchers explore privacy in machine learning and AI, differential privacy, and privacy-preserving machine learning. The work brings together questions of data protection, trust, and the security of intelligent systems.', ['Privacy-preserving machine learning', 'Differential privacy', 'Trust and security in AI'], ['james-joshi', 'peilin-he', 'liou-tang']),
    ('privacy', 'Privacy-preserving systems', 'Protecting data across distributed, cloud, and emerging computing environments.', 'We study privacy-conscious computation and data sharing in untrusted and outsourced environments, including cloud and edge computing, distributed systems, blockchains, and extended reality.', ['Distributed systems & data sharing', 'Cloud, edge & blockchain', 'Privacy in emerging environments'], ['balaji-palanisamy', 'ying-song', 'yijun-yuan']),
    ('security', 'Security & access control', 'Developing the foundations of resilient systems and secure information access.', 'Our interests include attribute-based access control, insider threats, security and privacy in IoT, and secure health information exchange. We connect foundational security questions with the systems people depend on.', ['Attribute-based access control', 'IoT & network security', 'Secure information exchange'], ['james-joshi', 'ahmed-ibrahim', 'prashant-v-krishnamurthy']),
]


def research_cards():
    return '<div class="research-grid">' + ''.join(f'''<article class="research-card"><span class="area-number" aria-hidden="true">0{i+1}</span><h3>{title}</h3><p>{desc}</p>{link('research.html#'+id, 'Explore area')}</article>''' for i, (id, title, desc, *_rest) in enumerate(AREAS)) + '</div>'


def news_card(n):
    # Conference artwork is typography native to the page, not an invented event logo.
    if n['category'] in ('conference', 'education'):
        short = {'cic-2024': 'IEEE CIC', 'tps-2024': 'IEEE TPS', 'cogmi-2024': 'IEEE CogMI', 'gencyber-2023': 'GenCyber'}[n['id']]
        visual = f'<div class="conference-art" aria-hidden="true"><span>{short}</span><span>{n["iso_date"][:4]}</span><span class="conference-art-line"></span></div>'
    else:
        visual = f'<img src="{n["image"]}" alt="{escape(n["title"], quote=True)}" loading="lazy" width="640" height="400">'
    return f'''<article class="news-card"><a href="news.html#{n['id']}" class="news-image" tabindex="-1" aria-hidden="true">{visual}</a><p class="meta">{n['category'].title()}<span>·</span><time datetime="{n['iso_date']}">{n['date']}</time></p><h3><a href="news.html#{n['id']}">{escape(n['headline'])}</a></h3></article>'''


def home():
    selected = [next(n for n in NEWS if n['id'] == key) for key in ['federated-learning-2025', 'cic-2024', 'gencyber-2023']]
    body = f'''<section class="home-hero wrap"><h1>Building trust in a<br>connected world.</h1><p>Advancing security, privacy, and trustworthy AI through<br class="desktop-break"> research and education at the University of Pittsburgh.</p>
<div class="site-search" data-site-search><form class="site-search-form" role="search"><label class="sr-only" for="site-search-input">Search LERSAIS</label>{SEARCH}<input id="site-search-input" type="search" name="q" placeholder="Search people, research, news" autocomplete="off" aria-controls="site-search-results" aria-expanded="false"><button type="submit" aria-label="Search website">{ARROW}</button></form><div class="site-search-results" id="site-search-results" hidden><div class="search-results-top"><p role="status" aria-live="polite" data-search-status></p><button type="button" data-search-close aria-label="Close search results">×</button></div><ul data-search-results-list></ul><button type="button" class="search-show-more" data-search-more hidden>Show more results ↓</button></div></div><noscript><p class="search-noscript">Enable JavaScript to search, or explore the pages below.</p></noscript>
<div class="hero-actions">{link('research.html','Explore our research','button')}{link('people.html','Meet the people')}</div></section>
<section class="section wrap home-research"><div class="section-heading"><h2>Research that earns trust.</h2><p>Exploring the foundations of secure systems<br>and responsible intelligence.</p></div>{research_cards()}</section>
<section class="section wrap news-section"><div class="section-heading"><h2>The latest at LERSAIS</h2>{link('news.html','All news')}</div><div class="news-grid">{''.join(news_card(n) for n in selected)}</div></section>
<section class="section wrap community-section"><div class="community-image"><img src="images/lersais1.jpg" alt="LERSAIS researchers and colleagues together at the University of Pittsburgh" loading="lazy" width="3362" height="2707"></div><div class="community-copy"><h2>Great research<br>starts with people.</h2><p>We’re a community of faculty, students, and collaborators brought together by a shared curiosity about a safer digital world.</p><p>Founded by Professor James Joshi, LERSAIS connects researchers across the School of Computing and Information and beyond.</p>{link('people.html', 'Meet our community')}{link('gallery.html', 'Life at LERSAIS')}</div></section>
<section class="section wrap education-section"><div><h2>Knowledge that<br>makes a difference.</h2></div><div><p class="large-copy">Research and education belong together.</p><p>From security and information assurance programs to cybersecurity outreach, we support the next generation of researchers and practitioners.</p>{link('teaching.html', 'Explore education')}</div></section>
{cta()}'''
    page('index', 'Security. Privacy. Possibility.', 'LERSAIS advances security, privacy, and trustworthy AI through research and education at the University of Pittsburgh.', body)


def filters(options, placeholder, label='Filter results'):
    buttons = ''.join(f'<button class="filter-button" type="button" data-filter="{key}" aria-pressed="{str(i==0).lower()}">{name}</button>' for i, (key, name) in enumerate(options))
    return f'''<div class="filter-toolbar" data-filter-toolbar><div class="filter-options" role="group" aria-label="{label}">{buttons}</div><label class="search-field">{SEARCH}<span class="sr-only">{placeholder}</span><input type="search" placeholder="{placeholder}" data-search autocomplete="off"></label></div><p class="sr-only" data-result-count role="status" aria-live="polite"></p><div class="empty-state" data-empty hidden><h2>No matches found.</h2><p>Try a different search or choose another category.</p><button type="button" class="button button-light" data-reset>Clear filters</button></div>'''


def person_card(p):
    image = f'<img src="{p["image"]}" alt="{escape(p["name"])}" loading="lazy" width="600" height="420">' if p['image'] else f'<div class="portrait-placeholder" aria-label="No portrait available">{"".join(w[0] for w in p["name"].split()[:2])}</div>'
    bio = ''.join(p['bio'])
    return f'''<article class="person-card" id="{p['id']}" data-filter-item data-category="{p['group']}"><div class="person-image">{image}</div><h3>{escape(p['name'])}</h3><p class="person-role">{escape(p['role'])}</p>{('<p class="person-summary">'+escape(p['summary'])+'</p>') if p['summary'] else ''}<details class="profile-details"><summary>View profile <span aria-hidden="true">+</span></summary><div class="profile-body">{bio}</div></details></article>'''


def people():
    body = heading('People behind<br>the possibilities.', 'A community of researchers advancing security, privacy,<br class="desktop-break"> and trustworthy systems.')
    body += '<div class="wrap filter-scope" data-filter-scope>' + filters([('all','Everyone'),('faculty','Faculty'),('students','Ph.D. students'),('alumni','Alumni')], 'Search people', 'Filter people')
    for group, name, anchor in [('faculty','Faculty','principalinvestigator'), ('students','Ph.D. students','graduate'), ('alumni','Ph.D. alumni','former')]:
        body += f'<section class="people-section" id="{anchor}" data-result-group><h2>{name}</h2><div class="people-grid">' + ''.join(person_card(p) for p in PEOPLE if p['group']==group) + '</div></section>'
    body += '</div>' + cta()
    page('people', 'People', 'Meet the faculty, Ph.D. students, and alumni of LERSAIS at the University of Pittsburgh.', body)


def research():
    body = heading('Research for a world<br>we can trust.', 'We explore how to make information systems more secure,<br class="desktop-break"> protect privacy, and build trustworthy intelligence.')
    body += '<div class="wrap"><nav class="section-links" aria-label="Research areas">' + ''.join(f'<a href="#{a[0]}">{a[1]} ↓</a>' for a in AREAS) + '</nav>'
    for i, (id, title, desc, text, topics, researchers) in enumerate(AREAS):
        names = [p for p in PEOPLE if p['id'] in researchers]
        body += f'''<section class="research-detail" id="{id}"><div><span class="area-number" aria-hidden="true">0{i+1}</span><h2>{title}</h2></div><div><p class="large-copy">{desc}</p><p>{text}</p><ul class="topic-list">{''.join(f'<li>{t}</li>' for t in topics)}</ul><h3 class="small-heading">Meet the researchers</h3><div class="researcher-links">{''.join(link('people.html#'+p['id'], escape(p['name'])) for p in names)}</div></div></section>'''
    body += f'<section class="mission-section"><h2>One lab. Many perspectives.</h2><p>LERSAIS provides a multidisciplinary forum for researchers within the School of Computing and Information and collaborators across security, privacy, and information assurance. Our mission connects a long-term research program with high-quality education.</p>{link("publications.html", "Explore our publications")}</section></div>' + cta()
    page('research', 'Research', 'Explore LERSAIS research in trustworthy AI, privacy-preserving systems, security, and access control.', body)


def publications():
    body = heading('Ideas, shared.', 'Explore publications from the LERSAIS research community.<br class="desktop-break"> Browse each researcher’s papers on Google Scholar.')
    body += '<div class="wrap filter-scope" data-filter-scope>' + filters([('all','Everyone'),('faculty','Faculty'),('students','Ph.D. students'),('alumni','Alumni')], 'Search researchers', 'Filter publication profiles') + '<div class="publication-list">'
    for p in PEOPLE:
        scholars = [a for a in p['links'] if 'scholar.google.com/citations' in a['href']]
        if not scholars:
            continue
        body += f'''<article class="publication-row" data-filter-item data-category="{p['group']}"><div><p class="meta">{escape(p['role'])}</p><h2>{escape(p['name'])}</h2></div><p>{escape(p['summary']) if p['summary'] else 'Publications, research papers, and citations.'}</p>{link(scholars[0]['href'], 'View publications', external=True)}</article>'''
    body += '</div></div>' + cta()
    page('publications', 'Publications', 'Find research papers and publications by LERSAIS faculty, students, and alumni through their scholarly profiles.', body)


def news():
    body = heading('News & ideas.', 'Research conversations, community milestones,<br class="desktop-break"> and education beyond the lab.')
    body += '<div class="wrap filter-scope" data-filter-scope>' + filters([('all','All updates'),('seminar','Seminars'),('conference','Conferences'),('education','Education')], 'Search updates', 'Filter news') + '<div class="news-list">'
    for n in NEWS:
        body += f'''<article class="news-story" id="{n['id']}" data-filter-item data-category="{n['category']}"><div class="news-story-image"><img src="{n['image']}" alt="{escape(n['title'], quote=True)}" loading="lazy" width="640" height="400"></div><div><p class="meta">{n['category'].title()} <span>·</span> <time datetime="{n['iso_date']}">{n['date']}</time></p><h2>{escape(n['headline'])}</h2><p class="story-title">{escape(n['title'])}</p><p>{escape(n['body'])}</p>{link(n['url'], 'Read the original story' if n['category']!='conference' else 'Visit conference', external=True)}</div></article>'''
    body += '</div></div>' + cta()
    page('news', 'News & events', 'News, seminars, conferences, and cybersecurity education from the LERSAIS community.', body)


def teaching():
    body = heading('Learn today.<br>Secure tomorrow.', 'Connecting research with education in security,<br class="desktop-break"> privacy, and information assurance.')
    body += f'''<div class="wrap"><div class="education-hero"><div><h2>Curiosity is<br>the starting point.</h2></div><div><p>LERSAIS faculty support security and information assurance education through the Department of Informatics and Networked Systems in Pitt’s School of Computing and Information.</p>{link('https://www.sci.pitt.edu/', 'Explore Pitt SCI', external=True)}</div></div>
<section class="section"><div class="section-heading"><h2>Pathways into security</h2><p>Explore degree programs and study opportunities.</p></div><div class="program-list">
<article><span class="meta">Graduate study</span><h3>Security Assured<br>Information Systems</h3><p>Explore master’s-level study in security and information assurance and the Certificate of Advanced Studies pathway described by LERSAIS.</p>{link('https://www.dins.pitt.edu/', 'Program information', external=True)}</article>
<article><span class="meta">Undergraduate study</span><h3>Networks<br>& security</h3><p>Build a foundation in information science, networks, and security through undergraduate study in the department.</p>{link('https://www.dins.pitt.edu/', 'Explore undergraduate study', external=True)}</article>
<article><span class="meta">Research</span><h3>Doctoral research<br>& collaboration</h3><p>Meet our faculty, explore their research interests, and get in touch about research opportunities at LERSAIS.</p>{link('people.html#principalinvestigator', 'Find a research connection')}</article></div></section>
<section class="outreach-section"><h2>Beyond the classroom.</h2><div><p class="large-copy">Cybersecurity knowledge should travel.</p><p>In 2023, LERSAIS faculty hosted a GenCyber camp for high school teachers, sharing resources and hands-on training to bring cybersecurity into school curricula.</p>{link('news.html#gencyber-2023','Discover GenCyber')}</div></section></div>''' + cta()
    page('teaching', 'Education', 'Explore security and information assurance education, research opportunities, and outreach at LERSAIS.', body)


def gallery():
    photographs = [('images/lersais1.jpg','The LERSAIS community','Researchers and colleagues together at Pitt.'), ('images/cathey.jpg','A place for discovery','University of Pittsburgh campus.'), ('images/joshi.jpeg','Ideas in conversation','Sharing research with the wider community.')]
    body = heading('Life at LERSAIS.', 'The people, places, and conversations<br class="desktop-break"> that bring our work to life.') + '<div class="wrap gallery-grid">'
    for src, title, caption in photographs:
        body += f'''<figure><a class="gallery-open" href="{src}" data-gallery-image data-caption="{escape(title+'. '+caption, quote=True)}"><img src="{src}" alt="{escape(title+'. '+caption, quote=True)}" loading="lazy"><span class="gallery-expand" aria-hidden="true">{EXTERNAL}</span></a><figcaption><h2>{title}</h2><p>{caption}</p></figcaption></figure>'''
    body += '''</div><dialog class="gallery-dialog" aria-label="Photo viewer"><button class="dialog-close" aria-label="Close photo" type="button">×</button><figure><img src="images/lersais1.jpg" alt=""><figcaption></figcaption></figure><div class="gallery-controls"><button type="button" data-gallery-prev aria-label="Previous photo">←</button><span data-gallery-count></span><button type="button" data-gallery-next aria-label="Next photo">→</button></div></dialog>''' + cta()
    page('gallery', 'Life at LERSAIS', 'Explore campus, research, and community life at LERSAIS, University of Pittsburgh.', body)


def contact():
    body = heading('Good questions.<br>New possibilities.', 'Interested in research, joining the lab, or working together?<br class="desktop-break"> We’d like to hear from you.')
    body += f'''<div class="wrap"><div class="contact-grid"><section><h2>Start a conversation.</h2><p>Contact Professor James Joshi,<br>Founder and Director of LERSAIS.</p>{link('mailto:jjoshi@pitt.edu','jjoshi@pitt.edu','button')}<p class="contact-note">For research interests and individual contacts,<br>explore our community.</p>{link('people.html','Meet our people')}</section><section><h2>Find us at Pitt.</h2><address>Information Sciences Building<br>135 N. Bellefield Avenue, Room 410<br>Pittsburgh, PA 15213, USA</address>{link('https://www.google.com/maps/search/?api=1&query=Information+Sciences+Building+135+North+Bellefield+Avenue+Pittsburgh+PA+15213', 'Get directions', external=True)}<h3>Office hours</h3><p>Monday–Friday, 9:00 am–5:00 pm<br>U.S. Eastern Time</p></section></div><figure class="campus-image"><img src="images/cathey.jpg" alt="The University of Pittsburgh campus" width="975" height="640"><figcaption>University of Pittsburgh · Pittsburgh, Pennsylvania</figcaption></figure></div>'''
    page('contact', 'Contact', 'Contact LERSAIS at the University of Pittsburgh for research, collaboration, and education opportunities.', body)


def search_index():
    def plain(value):
        return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', value))).strip()

    entries = []
    for p in PEOPLE:
        entries.append(dict(title=p['name'], category='People', url='people.html#'+p['id'], description=p['summary'] or p['role'], text=plain(p['role']+' '+''.join(p['bio']))))
    for id, title, description, content, topics, _ in AREAS:
        entries.append(dict(title=title, category='Research', url='research.html#'+id, description=description, text=content+' '+' '.join(topics)))
    for n in NEWS:
        entries.append(dict(title=n['headline'], category=n['category'].title(), url='news.html#'+n['id'], description=n['title'], text=n['body']))
    for slug, title, description in [('teaching','Education at LERSAIS','Security and information assurance programs, doctoral research, and GenCyber outreach.'), ('contact','Contact LERSAIS','Get in touch with James Joshi or find our lab at the University of Pittsburgh.'), ('gallery','Life at LERSAIS','Our campus, researchers, and community.'), ('publications','Publications','Find research papers and scholarly profiles from the LERSAIS community.')]:
        html = (ROOT / (slug+'.html')).read_text().split('<main',1)[1].split('</main>',1)[0]
        entries.append(dict(title=title, category='Page', url=slug+'.html', description=description, text=plain(html)))
    (ROOT/'data/search-index.json').write_text(json.dumps(entries, ensure_ascii=False, separators=(',',':'))+'\n')


if __name__ == '__main__':
    for build in [home, people, research, publications, news, teaching, gallery, contact]:
        build()
    (ROOT / 'header.html').write_text(size_images(header()) + '\n')
    (ROOT / 'footer.html').write_text(footer() + '\n')
    search_index()
    print('Built 8 static pages, shared header/footer, and local search index.')
