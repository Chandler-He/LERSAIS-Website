#!/usr/bin/env python3
"""Build the static LERSAIS website. Python 3 standard library only."""
from pathlib import Path
from html import escape, unescape
from hashlib import sha256
import json
import re
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
STYLESHEET = 'css/site.css?v=' + sha256((ROOT / 'css/site.css').read_bytes()).hexdigest()[:12]
PEOPLE = json.loads((ROOT / 'data/people.json').read_text())
NEWS = json.loads((ROOT / 'data/news.json').read_text())
GRANTS = json.loads((ROOT / 'data/grants.json').read_text())
IMAGE_SIZES = json.loads((ROOT / 'data/image-sizes.json').read_text())
ARROW = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'
EXTERNAL = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 18 18 6M6 6h12v12"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg>'
NAV = [('research', 'Research'), ('people', 'People'), ('grants', 'Grants'), ('news', 'News'), ('teaching', 'Education'), ('gallery', 'Gallery')]


def size_images(html):
    """Reserve each image's real aspect ratio; CSS owns the display size."""
    def size_tag(match):
        tag = match.group(0)
        source = re.search(r'\bsrc="([^"]+)"', tag)
        dimensions = IMAGE_SIZES.get(source.group(1).split('?', 1)[0]) if source else None
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
  <div class="identity"><a class="wordmark" href="research.html" aria-label="LERSAIS home">LERSAIS</a><a class="pitt-identity" href="https://www.pitt.edu/" aria-label="University of Pittsburgh"><img src="images/pitt-logo-blue.svg" alt="University of Pittsburgh" width="130" height="40"></a></div>
  <button class="menu-toggle" type="button" aria-label="Open navigation" aria-controls="site-nav" aria-expanded="false"><span></span><span></span></button>
  <nav id="site-nav" class="site-nav" aria-label="Main navigation">{nav}{link('contact.html', 'Contact', 'button nav-contact')}</nav>
</div></header>'''


def footer():
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="footer-top"><div class="footer-about"><a class="wordmark" href="research.html">LERSAIS</a><p>Laboratory for Education and Research on<br>Security Assured Information Systems</p><p>School of Computing and Information<br>University of Pittsburgh</p></div>
  <div><h2>Explore</h2><a href="research.html">Research</a><a href="people.html">People</a><a href="grants.html">Grants</a></div>
  <div><h2>Discover</h2><a href="news.html">News & events</a><a href="teaching.html">Education</a><a href="gallery.html">Life at LERSAIS</a></div>
  <div><h2>Find us</h2><p>Information Sciences Building<br>135 N. Bellefield Avenue, Room 410<br>Pittsburgh, PA 15213</p><a href="mailto:jjoshi@pitt.edu">jjoshi@pitt.edu</a></div></div>
  <div class="footer-bottom"><p>© <span data-year>2026</span> LERSAIS · University of Pittsburgh</p><a href="#main" class="back-top">Back to top ↑</a></div>
</div></footer>'''


def page(slug, title, description, content):
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | LERSAIS · University of Pittsburgh</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#ffffff"><link rel="icon" href="images/pitt-logo-blue.svg" type="image/svg+xml">
<link rel="stylesheet" href="{STYLESHEET}"><script src="js/site.js" defer></script></head>
<body class="page-{slug}">{header(slug)}<main id="main" tabindex="-1">{content}</main>{footer()}</body></html>'''
    (ROOT / f'{slug}.html').write_text(size_images(html) + '\n')


def heading(title, subtitle):
    return f'<div class="page-heading wrap"><h1>{title}</h1><p>{subtitle}</p></div>'


def cta():
    return f'''<section class="join-section wrap"><div><p class="section-label">Research &amp; collaboration</p><h2>Research inquiries.</h2></div><div><p>For questions about our work, doctoral study, or opportunities to collaborate with LERSAIS.</p>{link('contact.html', 'Contact the lab', 'button')}</div></section>'''


AREAS = [
    ('trustworthy-ai', 'Privacy-preserving AI', 'Developing privacy foundations and methods for machine learning and federated systems.', 'Our researchers study privacy in AI through differential privacy, privacy-preserving machine learning, and privacy-preserving federated learning. The work develops methods for learning from sensitive and distributed data while limiting information exposure.', ['Differential privacy', 'Privacy-preserving machine learning', 'Privacy-preserving federated learning'], ['james-joshi', 'peilin-he', 'liou-tang']),
    ('privacy', 'Privacy-preserving systems', 'Protecting data across distributed, cloud, and emerging computing environments.', 'We study privacy-conscious computation and data sharing in untrusted and outsourced environments, including cloud and edge computing, distributed systems, blockchains, and extended reality.', ['Distributed systems & data sharing', 'Cloud, edge & blockchain', 'Privacy in emerging environments'], ['balaji-palanisamy', 'ying-song', 'yijun-yuan', 'jingzhe-wang']),
    ('security', 'Privacy & access control', 'Developing the foundations of resilient systems and secure information access.', 'Our interests include attribute-based access control, insider threats, security and privacy in IoT, and secure health information exchange. We connect foundational security questions with the systems people depend on.', ['Attribute-based access control', 'IoT & network security', 'Secure information exchange'], ['james-joshi', 'prashant-v-krishnamurthy']),
]


def home_redirect():
    """Keep the site root and old home bookmarks pointing to the research homepage."""
    (ROOT / 'index.html').write_text(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>LERSAIS | University of Pittsburgh</title><link rel="canonical" href="research.html"><link rel="stylesheet" href="{STYLESHEET}">
<script>window.location.replace('research.html' + window.location.search + window.location.hash);</script>
<noscript><meta http-equiv="refresh" content="0;url=research.html"></noscript></head>
<body><main class="page-heading wrap"><h1>LERSAIS</h1><p>{link('research.html', 'Visit our research homepage')}</p></main></body></html>
''')


def filters(options, placeholder, label='Filter results'):
    buttons = ''.join(f'<button class="filter-button" type="button" data-filter="{key}" aria-pressed="{str(i==0).lower()}">{name}</button>' for i, (key, name) in enumerate(options))
    return f'''<div class="filter-toolbar" data-filter-toolbar><div class="filter-options" role="group" aria-label="{label}">{buttons}</div><label class="search-field">{SEARCH}<span class="sr-only">{placeholder}</span><input type="search" placeholder="{placeholder}" data-search autocomplete="off"></label></div><p class="sr-only" data-result-count role="status" aria-live="polite"></p><div class="empty-state" data-empty hidden><h2>No matches found.</h2><p>Try a different search or choose another category.</p><button type="button" class="button button-light" data-reset>Clear filters</button></div>'''


def person_card(p):
    if p['image']:
        # Refresh cached portraits when a photo is replaced under the same filename.
        version = sha256((ROOT / p['image']).read_bytes()).hexdigest()[:12]
        style = f' style="{escape(p["image_style"], quote=True)}"' if p.get('image_style') else ''
        image = f'<img src="{escape(p["image"], quote=True)}?v={version}" alt="{escape(p["name"], quote=True)}"{style} loading="lazy" width="600" height="420">'
    else:
        image = f'<div class="portrait-placeholder" aria-label="No portrait available">{"".join(w[0] for w in p["name"].split()[:2])}</div>'
    bio = ''.join(p['bio'])
    return f'''<article class="person-card" id="{p['id']}" data-filter-item data-category="{p['group']}"><div class="person-image">{image}</div><h3>{escape(p['name'])}</h3><p class="person-role">{escape(p['role'])}</p>{('<p class="person-summary">'+escape(p['summary'])+'</p>') if p['summary'] else ''}<details class="profile-details"><summary>View profile <span aria-hidden="true">+</span></summary><div class="profile-body">{bio}</div></details></article>'''


def people():
    body = heading('People behind<br>the possibilities.', 'A community of researchers advancing security, privacy,<br class="desktop-break"> and trustworthy systems.')
    body += '<div class="wrap filter-scope" data-filter-scope>' + filters([('all','Everyone'),('faculty','Faculty'),('students','Ph.D. students'),('alumnus','Alumnus')], 'Search people', 'Filter people')
    for group, name, anchor in [('faculty','Faculty','principalinvestigator'), ('students','Ph.D. students','graduate'), ('alumnus','Ph.D. alumnus','former')]:
        body += f'<section class="people-section" id="{anchor}" data-result-group><h2>{name}</h2><div class="people-grid">' + ''.join(person_card(p) for p in PEOPLE if p['group']==group) + '</div></section>'
    body += '</div>' + cta()
    page('people', 'People', 'Meet the faculty, Ph.D. students, and alumnus of LERSAIS at the University of Pittsburgh.', body)


def research():
    body = f'''<section class="research-hero wrap" aria-labelledby="lab-heading"><div class="research-hero-title"><p class="section-label">University of Pittsburgh · School of Computing and Information</p><h1 id="lab-heading">Privacy.<br>Security.<br>AI.</h1></div><aside class="research-hero-context" aria-label="About LERSAIS"><h2>Laboratory for Education and Research on Security Assured Information Systems</h2><p>LERSAIS studies the foundations and applications of secure information systems, privacy-preserving computation, and trustworthy artificial intelligence.</p><div>{link('people.html', 'People')}{link('grants.html', 'Research grants')}</div></aside></section>
<section class="research-news wrap" aria-labelledby="research-news-heading"><div class="research-band-heading"><div><p class="section-label">Latest from the lab</p><h2 id="research-news-heading">News &amp; events</h2></div>{link('news.html', 'All news &amp; events')}</div><div class="research-news-list">
<article class="research-news-row"><div class="research-news-meta"><time datetime="2026-11-04">November 4–6, 2026</time><span>San Jose, California</span></div><h3>Four co-located IEEE conferences in security, trust, intelligence, and resilient systems.</h3><div class="research-news-summary"><p>Explore each conference.</p><div class="research-event-links">{''.join(link('news.html#'+n['id'], escape(n['headline'])) for n in NEWS if n['iso_date'] == '2026-11-04')}</div></div></article>
</div></section>
<section class="research-areas-band" aria-labelledby="research-areas-heading"><div class="wrap"><div class="research-areas-heading"><div><p class="section-label">Three connected areas of inquiry</p><h2 id="research-areas-heading">Research areas</h2></div><p>Foundational and applied research across intelligent systems, privacy-conscious computation, and secure information access.</p></div><div class="research-area-columns">'''
    for i, (id, title, desc, text, topics, researchers) in enumerate(AREAS):
        names = [p for p in PEOPLE if p['id'] in researchers]
        body += f'''<article class="research-area-column" id="{id}"><span class="area-number" aria-hidden="true">0{i+1}</span><h3>{title}</h3><p>{text}</p><ul class="topic-list">{''.join(f'<li>{t}</li>' for t in topics)}</ul><h4>Researchers</h4><div class="researcher-links">{''.join(link('people.html#'+p['id'], escape(p['name'])) for p in names)}</div></article>'''
    body += f'''</div></div></section>
<section class="research-community" aria-labelledby="community-heading"><div class="research-community-inner wrap"><div class="research-community-image"><img src="images/lersais1.jpg" alt="LERSAIS researchers and colleagues at the University of Pittsburgh" loading="lazy"></div><div class="research-community-copy"><p class="section-label">About LERSAIS</p><h2 id="community-heading">Our research<br class="desktop-break"> community.</h2><p>Founded by Professor James Joshi, LERSAIS brings together faculty, doctoral students, and collaborators across the School of Computing and Information and beyond.</p><div class="community-actions">{link('people.html', 'Meet the lab')}{link('gallery.html', 'Life at LERSAIS')}</div><div class="community-education"><p class="section-label">Education &amp; outreach</p><p>Our research informs security and information assurance education, doctoral study, and GenCyber outreach for high school teachers.</p>{link('teaching.html', 'Education programs')}</div></div></div></section>{cta()}'''
    page('research', 'LERSAIS — Research', 'LERSAIS at the University of Pittsburgh advances privacy, access control, and secure computing across intelligent and connected systems.', body)


def grants():
    reviewed = date.fromisoformat(GRANTS['reviewed_on'])
    reviewed_label = f'{reviewed:%B} {reviewed.day}, {reviewed.year}'
    body = heading('Research grants.', 'Active and selected past awards supporting James Joshi’s research in security, privacy, and trustworthy information systems.')
    body += f'''<div class="wrap grants-intro"><p>Grant record based on James Joshi’s curriculum vitae and NSF award records.<br>Amounts and project periods appear as reported in the source.</p><div>{link('people.html#james-joshi', 'James Joshi')}{link(GRANTS['source_url'], 'Curriculum vitae', external=True)}</div></div>
<div class="wrap filter-scope grants-content" data-filter-scope>'''
    body += filters([('all', 'All grants'), ('recent', 'Active & recent'), ('past', 'Past grants')], 'Search grants', 'Filter grants')
    body += f'''<p class="grants-reviewed">Record reviewed <time datetime="{GRANTS["reviewed_on"]}">{reviewed_label}</time></p>'''
    for category, title, description in [('recent', 'Active & recent grants', 'Current research support.'), ('past', 'Past grants', 'Selected awards from earlier research and education projects.')]:
        category_count = sum(grant['category'] == category for grant in GRANTS['grants'])
        body += f'<section class="grant-section" id="{category}-grants" data-result-group><div class="grant-section-heading"><div><p class="grant-section-number">{category_count:02}</p><h2>{title}</h2></div><p>{description}</p></div>'
        for grant in GRANTS['grants']:
            if grant['category'] != category:
                continue
            note = f'<p class="grant-note">{escape(grant["note"])}</p>' if grant['note'] else ''
            if grant.get('source_url'):
                note += link(grant['source_url'], 'Award record', external=True)
            status_class = ' grant-status-active' if grant['status'] == 'Active' else ''
            status = f'<span class="grant-status{status_class}">{escape(grant["status"])}</span>' if category == 'recent' else ''
            body += f'''<article class="grant-row" id="{grant['id']}" data-filter-item data-category="{category}"><div class="grant-overview"><p class="grant-meta">{status}<span>{escape(grant['sponsor'])} · {escape(grant['program'])}</span></p><h3>{escape(grant['title'])}</h3>{note}</div><dl class="grant-facts"><div><dt>Funding</dt><dd>{escape(grant['amount'])}</dd></div><div><dt>Project period</dt><dd>{escape(grant['period'])}</dd></div><div><dt>James Joshi’s role</dt><dd>{escape(grant['role'])}</dd></div></dl></article>'''
        body += '</section>'
    body += f'''<div class="grants-source"><p><span>Source</span> James Joshi, Curriculum Vitae, “External Grants,” page 6. See the full CV for additional external and internal awards.</p>{link(GRANTS['source_url'], 'Open source', external=True)}</div></div>'''
    page('grants', 'Research grants', 'Explore James Joshi’s active, recent, and past research grants at LERSAIS, including Cisco, NSF, and NSA awards.', body)
    # Keep bookmarks to the removed publications directory working on static hosts.
    (ROOT / 'publications.html').write_text(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research grants | LERSAIS · University of Pittsburgh</title><meta http-equiv="refresh" content="0;url=grants.html"><link rel="canonical" href="grants.html"><link rel="stylesheet" href="{STYLESHEET}"></head>
<body><main class="page-heading wrap"><h1>Research grants.</h1><p>This page has moved to <a class="text-link" href="grants.html">Research grants →</a>.</p></main></body></html>
''')


def news():
    body = heading('News & ideas.', 'Research conversations, community milestones,<br class="desktop-break"> and education beyond the lab.')
    body += '<div class="wrap filter-scope" data-filter-scope>' + filters([('all','All updates'),('seminar','Seminars'),('conference','Conferences'),('education','Education')], 'Search news and events', 'Filter news and events')
    body += '<section class="past-updates" data-result-group aria-labelledby="past-updates-heading"><h2 id="past-updates-heading">Past updates</h2><div class="news-list">'
    for n in NEWS:
        body += f'''<article class="news-story" id="{n['id']}" data-filter-item data-category="{n['category']}"><div class="news-story-image"><img src="{n['image']}" alt="{escape(n['title'], quote=True)}" loading="lazy" width="640" height="400"></div><div><p class="meta">{n['category'].title()} <span>·</span> <time datetime="{n['iso_date']}">{n['date']}</time></p><h2>{escape(n['headline'])}</h2><p class="story-title">{escape(n['title'])}</p><p>{escape(n['body'])}</p>{link(n['url'], 'Read the original story' if n['category']!='conference' else 'Visit conference', external=True)}</div></article>'''
    body += '</div></section></div>' + cta()
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
    photographs = [('images/lersais1.jpg','The LERSAIS community','Researchers and colleagues together at Pitt.'), ('images/cathey.jpg','A place for discovery','University of Pittsburgh campus.'), ('images/joshi.jpeg','Ideas in conversation','Sharing research with the wider community.'), ('images/events/conference-2026-executive-chairs.jpg','Four conferences, together','Executive co-chairs introduced at IEEE CIC, CogMI, RISC, and TPS 2026.'), ('images/events/conference-2026-cic-chairs.jpg','IEEE CIC 2026','General and program committee co-chairs introduced in San Jose.'), ('images/events/conference-2026-risc-chairs.jpg','IEEE RISC 2026','General and program committee co-chairs of the first conference.'), ('images/events/conference-2026-looking-ahead.jpg','Looking ahead to 2027','Announcing the next conference leadership.')]
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
    for grant in GRANTS['grants']:
        entries.append(dict(title=grant['title'], category='Grants', url='grants.html#'+grant['id'], description=f'{grant["sponsor"]} · {grant["period"]} · {grant["status"]}', text='James Joshi '+ ' '.join(grant[key] for key in ['program', 'role', 'amount', 'note'])))
    for slug, title, description in [('research','LERSAIS research homepage','About the lab, research areas, researchers, education, and news.'), ('teaching','Education at LERSAIS','Security and information assurance programs, doctoral research, and GenCyber outreach.'), ('contact','Contact LERSAIS','Get in touch with James Joshi or find our lab at the University of Pittsburgh.'), ('gallery','Life at LERSAIS','Our campus, researchers, and community.'), ('grants','James Joshi’s research grants','Active, recent, and past research funding from Cisco, NSF, and NSA.')]:
        html = (ROOT / (slug+'.html')).read_text().split('<main',1)[1].split('</main>',1)[0]
        entries.append(dict(title=title, category='Page', url=slug+'.html', description=description, text=plain(html)))
    (ROOT/'data/search-index.json').write_text(json.dumps(entries, ensure_ascii=False, separators=(',',':'))+'\n')


if __name__ == '__main__':
    for build in [research, people, grants, news, teaching, gallery, contact]:
        build()
    home_redirect()
    (ROOT / 'header.html').write_text(size_images(header()) + '\n')
    (ROOT / 'footer.html').write_text(footer() + '\n')
    search_index()
    print('Built 7 content pages, home/publications redirects, shared header/footer, and local search index.')
