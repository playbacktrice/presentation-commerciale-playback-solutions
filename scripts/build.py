#!/usr/bin/env python3
"""Generate the V2 static site; no production dependencies or external assets."""
from pathlib import Path
from html import escape
import json
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
NAV = [('index.html', 'Accueil'), ('creative-lab.html', 'Creative Lab'),
       ('performing-systems.html', 'Performing Systems'),
       ('reliable-systems.html', 'Reliable Systems'), ('contact.html', 'Contact')]
MEDIA = json.loads((ROOT / 'data/media.json').read_text(encoding='utf-8'))
PROJECTS = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))


def icon(name):
    paths = {'left': 'M15 5 8 12l7 7', 'right': 'm9 5 7 7-7 7',
             'close': 'm6 6 12 12M18 6 6 18', 'menu': 'M4 6h16M4 12h16M4 18h16',
             'design': 'm4 20 4-1L20 7l-3-3L5 16l-1 4M14 7l3 3',
             'controls': 'M5 3v18M12 3v18M19 3v18M2 8h6M9 15h6M16 10h6',
             'software': 'M3 5h18v14H3zM3 8h18M10 11l-3 2 3 2m4-4 3 2-3 2',
             'systems': 'M3 3h7v6H3zM14 15h7v6h-7zM3 15h7v6H3zM6.5 9v6M10 6h7.5v9',
             'sync': 'M3 12h4l3-6 4 12 3-6h4',
             'reliable': 'm12 3-8 3v6c0 5 8 9 8 9s8-4 8-9V6l-8-3m-4 9 3 3 5-6',
             'down': 'm6 9 6 6 6-6'}
    return f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{paths[name]}"/></svg>'


def media(key, *, priority=False, cutout=False, item=None):
    item = MEDIA[key] if item is None else item
    caption = escape(item.get('caption', ''))
    if item['src']:
        image = Path(item['src'])
        if not str(image).startswith('assets/photos/') or image.is_absolute() or '..' in image.parts or not (ROOT/image).is_file():
            raise ValueError(f'{key}: photo must exist under assets/photos/')
        if not item['alt'] or not item['credit'] or item.get('approved') is not True:
            raise ValueError(f'{key}: validated photo, alt and credit required')
        loading = 'fetchpriority="high"' if priority else 'loading="lazy"'
        content = f'<img src="{escape(str(image),quote=True)}" alt="{escape(item["alt"],quote=True)}" width="1800" height="1000" {loading} style="object-position:{escape(item.get("position","50% 50%"),quote=True)}">'
        credit = f'<span class="photo-credit">{escape(item["credit"])}</span>'
        state = ' has-photo'
    else:
        content = f'<div class="photo-placeholder" role="img" aria-label="Emplacement photographique : {escape(item["label"],quote=True)}"><span class="placeholder-label">Photographie à fournir</span><span class="placeholder-subject">{escape(item["label"])}</span></div>'
        credit = ''
        state = ' awaiting-photo'
    kind = ' media-cutout' if cutout else ''
    return f'<figure class="media{kind}{state}" data-media="{key}">{content}{credit}{f"<figcaption>{caption}</figcaption>" if caption else ""}</figure>'


def contact_block(*, standalone=False):
    tag = 'h1' if standalone else 'h2'
    return f'''<section class="contact-band" id="contact"><div class="content"><{tag}>Contact.</{tag}><div class="contact-copy"><p>Anthony Combe<br><a class="contact-phone" href="tel:+33602256978">+33 6 02 25 69 78</a><br><a class="contact-email" href="mailto:anthony@playback-solutions.com">anthony@playback-solutions.com</a></p><p>Bureaux & studios au Pré-Saint-Gervais.<br>Rencontre et visite sur rendez-vous.</p></div></div></section>'''


def page(file, title, description, body, *, home=False):
    links = ''.join(f'<a href="{url}"'+(' aria-current="page"' if file==url else '')+f'>{label}</a>' for url,label in NAV)
    white = 'assets/logo_playback_WHITE_HORIZONTAL.png'
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#080808">
<meta name="description" content="{escape(description,quote=True)}">
<meta property="og:title" content="{escape(title,quote=True)} — Playback Solutions">
<meta property="og:description" content="{escape(description,quote=True)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<title>{escape(title)} — Playback Solutions</title>
<link rel="icon" type="image/png" href="assets/monogramme_playback_BLACK.png" media="(prefers-color-scheme: light)">
<link rel="icon" type="image/png" href="assets/monogramme_playback_WHITE_Margins.png" media="(prefers-color-scheme: dark)">
<link rel="stylesheet" href="assets/site.css">
<script src="assets/site.js" defer></script>
</head>
<body class="{'home-page' if home else 'inner-page'}">
<a class="skip-link" href="#main">Aller au contenu</a>
<header class="site-header">
<a class="brand" href="index.html" aria-label="Playback Solutions — Accueil"><img src="{white}" alt="Playback Solutions" width="3102" height="476" fetchpriority="high"></a>
<button class="menu-toggle" type="button" aria-controls="site-menu" aria-expanded="false" aria-label="Ouvrir le menu">{icon('menu')}</button>
</header>
<div class="menu-backdrop" hidden></div>
<aside class="menu-panel" id="site-menu" aria-label="Menu principal">
<div class="menu-top"><a href="index.html" aria-label="Playback Solutions — Accueil"><img src="{white}" alt="Playback Solutions" width="3102" height="476"></a><button class="menu-close" type="button" aria-label="Fermer le menu">{icon('close')}</button></div>
<nav aria-label="Navigation principale">{links}</nav>
</aside>
<main id="main" tabindex="-1">{body}</main>
<footer class="site-footer"><div class="footer-inner"><a href="index.html" aria-label="Playback Solutions — Accueil"><img src="{white}" alt="Playback Solutions" width="3102" height="476" loading="lazy"></a><p>Exigence, précision et fiabilité.</p></div><div class="footer-bottom"><span>© 2026 Playback Solutions</span><a href="contact.html">Contact</a></div></footer>
</body></html>
'''


def approved_references():
    groups = {}
    slugs = set()
    for project in PROJECTS:
        if project['slug'] in slugs:
            raise ValueError('Duplicate project slug')
        slugs.add(project['slug'])
        if project.get('publication_approved') is not True:
            continue
        groups.setdefault(project['name'], []).append(project)
    order = lambda name: ''.join(c for c in unicodedata.normalize('NFD', name.casefold()) if not unicodedata.combining(c))
    return [(name, groups[name]) for name in sorted(groups, key=order)]


def references_section():
    featured = [('justice-2024', 'home-justice'), ('polo-pan', 'home-polo-pan'),
                ('mylene-farmer-nevermore', 'home-mylene'), ('eddy-de-pretto-2024', 'reference-eddy'),
                ('kungs', 'reference-kungs'), ('damso', 'reference-damso'), ('paris-2024', 'reference-paris-2024')]
    projects = {project['slug']: project for project in PROJECTS}
    cards = []
    for slug, photo in featured:
        project = projects[slug]
        if project.get('publication_approved') is not True:
            continue
        name = project['name'] + (' 2024' if slug == 'paris-2024' else '')
        cards.append(f'<article class="reference-card">{media(photo)}<h3>{escape(name)}</h3></article>')
    collection = []
    groups = approved_references()
    for name, entries in groups:
        editions = list(dict.fromkeys(entry['edition'] for entry in entries if entry.get('edition')))
        photo = next((entry for entry in entries if entry.get('image')), None)
        image = ''
        if photo:
            image = media('project-' + photo['slug'], item={'src': photo['image'], 'alt': photo['image_alt'], 'credit': photo['image_credit'], 'approved': True})
        slugs = ' '.join(entry['slug'] for entry in entries)
        edition_text = ' · '.join(editions)
        collection.append(f'<article class="collection-card" data-project-slugs="{escape(slugs,quote=True)}">{image}<h3>{escape(name)}</h3>{f"<p>{escape(edition_text)}</p>" if edition_text else ""}</article>')
    return f'<section class="references-section" id="projets"><div class="references-inner"><h2>Projets & artistes.</h2><p class="references-intro">Une sélection des artistes et des productions avec lesquels Playback Solutions a travaillé.</p><div class="reference-grid">{"".join(cards)}</div><details class="reference-collection"><summary><span>Toutes les références</span><span class="collection-count">{len(groups)}</span>{icon("down")}</summary><div class="collection-grid">{"".join(collection)}</div></details></div></section>'


def skills_strip():
    skills = [('design', 'Sur mesure', 'Recherche, conception et prototypage.'),
              ('controls', 'Contrôleurs', 'Commandes et interfaces adaptées aux usages.'),
              ('software', 'Logiciels', 'Développement d’outils spécifiques.'),
              ('systems', 'Systèmes', 'Intégration audio et informatique.'),
              ('sync', 'Synchronisation', 'Playback et pilotage des équipements.'),
              ('reliable', 'Fiabilité', 'Redondance, tests et supervision.')]
    items = ''.join(f'<li>{icon(symbol)}<h2>{title}</h2><p>{description}</p></li>' for symbol, title, description in skills)
    return f'<div class="skills-wrap"><ul class="skills-strip" aria-label="Nos compétences">{items}</ul></div>'


def home():
    slide_keys = ['home-justice','home-polo-pan','home-mylene']
    slides=[]
    for n,key in enumerate(slide_keys,1):
        item=MEDIA[key]
        slides.append(f'<div class="carousel-slide" id="slide-{n}" role="group" aria-roledescription="diapositive" aria-label="{n} sur {len(slide_keys)}"'+(' hidden' if n>1 else '')+'>'+media(key,priority=n==1)+f'<div class="slide-reference"><span>Référence artistique communiquée</span><p>{escape(item["artist"])}</p></div></div>')
    return f'''<section class="carousel" id="references" aria-roledescription="carrousel" aria-label="Références artistiques Playback Solutions">
<div class="carousel-track">{''.join(slides)}</div>
<div class="carousel-controls" hidden><button class="slide-prev" type="button" aria-label="Photographie précédente">{icon('left')}</button><button class="slide-next" type="button" aria-label="Photographie suivante">{icon('right')}</button><span class="slide-counter" role="status" aria-live="polite" aria-atomic="true">01 / 03</span></div>
</section>
<section class="presentation" id="presentation"><div class="content"><h1>Un laboratoire d’ingénierie.</h1><div class="presentation-copy"><p>Playback Solutions conçoit et développe des outils et des systèmes techniques sur mesure pour le spectacle vivant : contrôleurs, interfaces, logiciels et matériel spécifique.</p><p>Nous associons recherche, prototypage et intégration pour répondre aux besoins des artistes et des équipes techniques.</p><div class="expertise-links"><a href="creative-lab.html">Creative Lab</a><a href="performing-systems.html">Performing Systems</a><a href="reliable-systems.html">Reliable Systems</a></div></div></div>{skills_strip()}</section>
{references_section()}
{contact_block()}'''


def creative():
    return f'''<section class="editorial content"><h1>Creative<br>Lab.</h1><div class="editorial-copy"><p class="expertise-lead">Développer sur mesure.</p><p>Nous concevons des contrôleurs, des interfaces, des logiciels et du matériel spécifique, avec les artistes et les équipes techniques.</p></div></section>
<div class="panorama">{media('lab-workshop')}</div>
<section class="equipment content"><div class="equipment-visual">{media('lab-controller',cutout=True)}</div><div class="equipment-copy"><h2>Contrôleurs &<br>interfaces.</h2><p>Des commandes conçues pour les gestes, les usages et les équipements du projet.</p></div></section>
<section class="equipment equipment-reverse content"><div class="equipment-visual">{media('lab-software')}</div><div class="equipment-copy"><h2>Logiciels &<br>systèmes spécifiques.</h2><p>Du prototype à l’intégration, développer les outils nécessaires à votre fonctionnement.</p></div></section>
{contact_block()}'''


def performing():
    return f'''<section class="systems-opening"><div class="system-copy"><h1>Performing<br>Systems.</h1><p class="expertise-lead">Intégrer & synchroniser.</p><p>Playback, pilotage, synchronisation et réseaux : nous intégrons les outils et les équipements pour leur exploitation sur le terrain.</p></div><div class="system-visual">{media('performing-system',cutout=True)}</div></section>
<section class="equipment equipment-reverse content"><div class="equipment-visual">{media('performing-control',cutout=True)}</div><div class="equipment-copy"><h2>Lecture &<br>synchronisation.</h2><p>Playback, pilotage du spectacle, MIDI, OSC et code temporel. Réseaux audio et informatiques, intégration et exploitation.</p></div></section>
<div class="panorama reference-panorama">{media('performing-justice')}<div class="reference-caption"><span>Référence artistique communiquée</span><p>Justice</p></div></div>
{contact_block()}'''


def reliable():
    return f'''<section class="editorial content"><h1>Reliable<br>Systems.</h1><div class="editorial-copy"><p class="expertise-lead">Fiabiliser & superviser.</p><p>Architecture, redondance, préparation et tests : nous accompagnons la fiabilité des systèmes et leur suivi en exploitation.</p></div></section>
<div class="panorama">{media('reliable-racks')}</div>
<section class="equipment content"><div class="equipment-visual">{media('reliable-monitoring',cutout=True)}</div><div class="equipment-copy"><h2>Tests &<br>validation.</h2><p>Préparation, configuration, audit et maintenance. Des procédures et une documentation pour accompagner les équipes.</p></div></section>
{contact_block()}'''


def main():
    pages=[('index.html','Accueil','Ingénierie, conception et développement de systèmes techniques pour le spectacle vivant.',home(),True),
           ('creative-lab.html','Creative Lab','Recherche, prototypage, contrôleurs et développement de matériel et de logiciels sur mesure.',creative(),False),
           ('performing-systems.html','Performing Systems','Playback, pilotage du spectacle, synchronisation, intégration et exploitation des systèmes techniques.',performing(),False),
           ('reliable-systems.html','Reliable Systems','Architecture, redondance, supervision, tests et maintenance des systèmes.',reliable(),False),
           ('contact.html','Contact','Anthony Combe. Bureaux et studios au Pré-Saint-Gervais, sur rendez-vous.',contact_block(standalone=True),False)]
    for file,title,description,body,is_home in pages:
        (ROOT/file).write_text(page(file,title,description,body,home=is_home),encoding='utf-8')
    print(f'Generated {len(pages)} V2 pages. Photo slots: {len(MEDIA)}. No generated photography.')


if __name__=='__main__':
    main()
