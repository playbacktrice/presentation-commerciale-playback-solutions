#!/usr/bin/env python3
"""Generate the V2 static site; no production dependencies or external assets."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
NAV = [('index.html', 'Accueil'), ('creative-lab.html', 'Creative Lab'),
       ('performing-systems.html', 'Performing Systems'),
       ('reliable-systems.html', 'Reliable Systems'), ('contact.html', 'Contact')]
MEDIA = json.loads((ROOT / 'data/media.json').read_text(encoding='utf-8'))


def icon(name):
    paths = {'left': 'M15 5 8 12l7 7', 'right': 'm9 5 7 7-7 7',
             'close': 'm6 6 12 12M18 6 6 18', 'menu': 'M4 6h16M4 12h16M4 18h16'}
    return f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{paths[name]}"/></svg>'


def media(key, *, priority=False, cutout=False):
    item = MEDIA[key]
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


def references_section():
    featured = [('home-justice', 'Justice'), ('home-polo-pan', 'Polo & Pan'),
                ('home-mylene', 'Mylène Farmer'), ('reference-eddy', 'Eddy de Pretto'),
                ('reference-paris-2024', 'Jeux olympiques de Paris 2024')]
    cards = ''.join(f'<article class="reference-card">{media(key)}<h3>{escape(name)}</h3></article>' for key, name in featured)
    return f'<section class="references-section" id="projets"><div class="references-inner"><h2>Références.</h2><p class="references-intro">Quelques projets et artistes avec lesquels Playback Solutions a travaillé.</p><div class="reference-grid">{cards}</div></div></section>'


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
<section class="presentation" id="presentation"><div class="content"><h1>Playback Solutions.</h1><div class="presentation-copy"><p>Un laboratoire créatif dédié à l’ingénierie des systèmes techniques pour le spectacle vivant.</p><p>Conception et développement de systèmes audio et informatiques, de logiciels et de matériel spécifique. Intégration et fiabilisation, de la recherche à l’exploitation.</p><div class="expertise-links"><a href="creative-lab.html">Creative Lab</a><a href="performing-systems.html">Performing Systems</a><a href="reliable-systems.html">Reliable Systems</a></div></div></div></section>
{references_section()}
{contact_block()}'''


def creative():
    return f'''<section class="editorial content"><h1>Creative<br>Lab.</h1><div class="editorial-copy"><p>Nous concevons avec les artistes des outils matériels et logiciels adaptés à leur pratique.</p><p>Recherche, prototypage et développement avec les artistes et les équipes créatives.</p></div></section>
<div class="panorama">{media('lab-workshop')}</div>
<section class="equipment content"><div class="equipment-visual">{media('lab-controller',cutout=True)}</div><div class="equipment-copy"><h2>Matériel<br>& logiciels.</h2><p>Contrôleurs, interfaces et outils spécifiques. Des solutions développées pour vos usages et vos équipements.</p></div></section>
{contact_block()}'''


def performing():
    return f'''<section class="systems-opening"><div class="system-copy"><h1>Performing<br>Systems.</h1><p>Des systèmes fiables pour les exigences du spectacle vivant.</p></div><div class="system-visual">{media('performing-system',cutout=True)}</div></section>
<section class="equipment equipment-reverse content"><div class="equipment-visual">{media('performing-control',cutout=True)}</div><div class="equipment-copy"><h2>Lecture &<br>synchronisation.</h2><p>Playback, pilotage du spectacle, MIDI, OSC et code temporel. Réseaux audio et informatiques, intégration et exploitation.</p></div></section>
<div class="panorama reference-panorama">{media('performing-justice')}<div class="reference-caption"><span>Référence artistique communiquée</span><p>Justice</p></div></div>
{contact_block()}'''


def reliable():
    return f'''<section class="editorial content"><h1>Reliable<br>Systems.</h1><div class="editorial-copy"><p>Exigence, précision et fiabilité.</p><p>Architecture, redondance et supervision. Concevoir des systèmes adaptés à leurs conditions d’utilisation.</p></div></section>
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
