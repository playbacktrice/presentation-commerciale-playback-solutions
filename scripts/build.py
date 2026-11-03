#!/usr/bin/env python3
"""Generate the complete static site using only Python's standard library."""
from pathlib import Path
from html import escape
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
NAV = [
    ('index.html', 'Accueil'),
    ('creative-lab.html', 'Creative Lab'),
    ('performing-systems.html', 'Performing Systems'),
    ('reliable-systems.html', 'Reliable Systems'),
    ('projets.html', 'Projets & Références'),
    ('a-propos.html', 'À propos'),
    ('contact.html', 'Contact'),
]


def art(kind):
    """Original abstract vector artwork, never a project/equipment photograph."""
    elements = []
    if kind == 'lab':
        for i in range(65):
            t = i / 64 * math.pi
            radius = math.sin(t) * 345
            y = 450 + math.cos(t) * 345
            intensity = int(90 + 155 * math.sin(t))
            elements.append(f'<ellipse cx="650" cy="{y:.2f}" rx="{radius:.2f}" ry="{radius*.28:.2f}" stroke="rgb({intensity},{intensity},{intensity})"/>')
        transform = 'rotate(-28 650 450)'
    elif kind == 'perform':
        for i in range(54):
            x = 240 + i * 15
            wave = 130 * math.sin(i / 53 * math.pi)
            elements.append(f'<path d="M{x} 95 C{x-260} {300-wave:.1f} {x+260} {600+wave:.1f} {x} 805" stroke="rgb({100+i*2},{100+i*2},{100+i*2})"/>')
        transform = 'rotate(-15 650 450)'
    else:
        for i in range(38):
            size = 60 + i * 16
            angle = i * 1.6
            elements.append(f'<rect x="{650-size/2}" y="{450-size/2}" width="{size}" height="{size}" rx="{size*.13:.1f}" transform="rotate({angle} 650 450)" stroke="rgb({235-i*4},{235-i*4},{235-i*4})"/>')
        transform = 'rotate(-18 650 450)'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="900" viewBox="0 0 1300 900"><defs><radialGradient id="bg"><stop stop-color="#242424"/><stop offset="1" stop-color="#0b0b0b"/></radialGradient></defs><path fill="url(#bg)" d="M0 0h1300v900H0z"/><g fill="none" stroke-width="1.3" transform="{transform}">{''.join(elements)}</g></svg>'''


def arrow_link(href, label):
    return f'<a class="text-link" href="{href}">{label}<span class="circle-arrow" aria-hidden="true">↗</span></a>'


def cta():
    return '''<section class="cta"><div class="container cta-inner" data-reveal><div><p class="eyebrow">Contact</p><h2>Votre projet.</h2></div><a href="contact.html" aria-label="Votre projet : contacter Playback Solutions"><span class="circle-arrow" aria-hidden="true">↗</span></a></div></section>'''


def page(filename, title, description, content, *, contact=False):
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if filename == url else '')+(' class="contact-nav"' if url == 'contact.html' else '')+f'>{escape(label)}</a>' for url, label in NAV)
    footer_nav = ''.join(f'<a href="{url}">{escape(label)}</a>' for url, label in NAV)
    document = f'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#0b0b0b">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta property="og:title" content="{escape(title, quote=True)} — Playback Solutions">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_FR">
  <title>{escape(title)} — Playback Solutions</title>
  <link rel="icon" type="image/png" href="assets/monogramme_playback_BLACK.png" media="(prefers-color-scheme: light)">
  <link rel="icon" type="image/png" href="assets/monogramme_playback_WHITE_Margins.png" media="(prefers-color-scheme: dark)">
  <link rel="stylesheet" href="assets/site.css">
  <script src="assets/site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Aller au contenu</a>
<header class="site-header"><div class="container header-inner">
  <a class="brand" href="index.html" aria-label="Playback Solutions — Accueil"><img src="assets/logo_playback_WHITE_HORIZONTAL.png" alt="Playback Solutions" width="3102" height="476" fetchpriority="high"></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="navigation"><span class="menu-label">Menu</span><span class="menu-icon" aria-hidden="true"></span></button>
  <nav class="navigation" id="navigation" aria-label="Navigation principale">{nav}</nav>
</div></header>
<main id="main" tabindex="-1">{content}</main>
{'' if contact else cta()}
<footer class="site-footer"><div class="container"><div class="footer-top">
  <div><a href="index.html" aria-label="Playback Solutions — Accueil"><img class="footer-logo" src="assets/logo_playback_WHITE_HORIZONTAL.png" alt="Playback Solutions" width="3102" height="476" loading="lazy"></a><p class="footer-tagline" lang="en">Care. Precision. Reliability.</p></div>
  <div><span class="micro">Explorer</span><nav class="footer-links" aria-label="Navigation de pied de page">{footer_nav}</nav></div>
  <div class="footer-contact"><span class="micro">Contact commercial</span><p>Anthony Combe</p><a href="tel:+33602256978">+33 6 02 25 69 78</a><p class="muted">Le Pré-Saint-Gervais · Sur rendez-vous</p></div>
</div><div class="footer-bottom"><span>© 2026 Playback Solutions</span><span>Conception · Développement · Intégration · Exploitation</span><a href="#main">Retour en haut ↑</a></div></div></footer>
</body>
</html>
'''
    icon = '<svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true" focusable="false"><path d="M5 19 19 5M5 5h14v14"/></svg>'
    return document.replace('↗', icon).replace('↓', icon.replace('arrow-icon', 'arrow-icon arrow-down'))


EXPERTISE = [
    dict(file='creative-lab.html', name='Creative Lab', art='lab', label='Recherche & développement', headline='Creative<span>Lab.</span>', slogan='A creative lab. We design and build custom hardware and software instruments with artists.', summary='Recherche, conception et développement de hardware, de software et d’interfaces sur mesure.', intro='Un laboratoire créatif, au service des artistes et des équipes.', body='Nous partons d’un usage, d’un geste ou d’une intention créative pour concevoir les instruments et les outils qui lui correspondent. Nos compétences internes en développement logiciel et matériel permettent de travailler ensemble sur la forme, les interactions et la technique.', capabilities=[
        ('Hardware & software', 'Conception de solutions matérielles et logicielles spécifiques : de l’outil autonome à l’intégration dans un système existant.'),
        ('Contrôleurs & interfaces', 'Développement d’interfaces de commande et de contrôleurs adaptés aux gestes, aux usages et aux contraintes des équipes.'),
        ('Recherche & prototypage', 'Exploration des possibilités techniques, réalisation de prototypes et essais avec les artistes et les équipes créatives.'),
        ('Outils & automatisation', 'Développement d’outils spécifiques et automatisation des tâches pour relier les équipements et accompagner le travail de création.')]),
    dict(file='performing-systems.html', name='Performing Systems', art='perform', label='Intégration & exploitation', headline='Performing<span>Systems.</span>', slogan='Reliable systems for demanding creative environments.', summary='Conception, intégration et exploitation de systèmes pour les performances et les installations.', intro='Des systèmes techniques conçus pour la performance.', body='Playback, show-control, synchronisation et réseaux : nous concevons l’architecture, intégrons les équipements et accompagnons leur déploiement. Nous intervenons avec les équipes artistiques, les productions et les partenaires techniques, en spectacle vivant comme en audiovisuel.', capabilities=[
        ('Playback & show-control', 'Conception et préparation des systèmes de lecture et de pilotage, en fonction du déroulé de la performance et des besoins de l’exploitation.'),
        ('Synchronisation & protocoles', 'MIDI, OSC et timecode : organisation des échanges et de la synchronisation entre les outils audio, informatiques et audiovisuels.'),
        ('Réseaux & intégration', 'Conception des réseaux audio et informatiques et intégration des équipements dans une architecture cohérente.'),
        ('Déploiement & exploitation', 'Préparation, mise en service et accompagnement en conditions réelles : répétitions, spectacle, tournée ou installation.')]),
    dict(file='reliable-systems.html', name='Reliable Systems', art='reliable', label='Ingénierie & fiabilité', headline='Reliable<span>Systems.</span>', slogan='Care. Precision. Reliability.', summary='Architecture, redondance, supervision et maintenance des systèmes techniques.', intro='La fiabilité se travaille à chaque étape.', body='Nous accompagnons la sécurisation et le suivi de systèmes audio, informatiques et audiovisuels. De l’audit à la maintenance, nous adaptons l’architecture et les procédures aux contraintes réelles d’utilisation, avec une attention particulière aux points de défaillance et à la prise en main.', capabilities=[
        ('Architecture & redondance', 'Analyse des contraintes techniques et conception d’architectures intégrant la redondance selon les besoins du projet.'),
        ('Monitoring & supervision', 'Mise en place d’outils de suivi pour rendre l’état des équipements et les informations utiles accessibles aux équipes.'),
        ('Préparation, tests & validation', 'Configuration des équipements, vérification des échanges et tests de fonctionnement avant le déploiement.'),
        ('Audit, maintenance & transmission', 'Audit et optimisation des installations, maintenance, documentation et procédures pour accompagner l’exploitation dans la durée.')]),
]


def expertise_cards():
    cards = []
    for n, item in enumerate(EXPERTISE, 1):
        cards.append(f'''<a class="expertise-card" href="{item['file']}" data-reveal><div class="card-top"><span class="micro">0{n} / {item['label']}</span><span class="card-arrow" aria-hidden="true">↗</span></div><div class="art-frame"><img src="assets/visual-{item['art']}.svg" alt="" width="1300" height="900" loading="lazy"></div><h3>{item['name']}</h3><p>{item['summary']}</p></a>''')
    return '<div class="expertise-grid">'+''.join(cards)+'</div>'


def process():
    return '''<section class="section light"><div class="container"><div class="section-heading" data-reveal><p class="section-index" lang="en">A process you can rely on</p><h2 class="process-title" lang="en">Care. Precision.<br>Reliability.</h2></div><div class="process-grid">
<article class="process-step" data-reveal><span class="micro">01 / Comprendre</span><h3>Cadrer le besoin</h3><p>Échanger avec vos équipes, comprendre les usages et définir les contraintes, les interfaces et le périmètre du projet.</p></article>
<article class="process-step" data-reveal><span class="micro">02 / Concevoir</span><h3>Développer & tester</h3><p>Explorer, prototyper, construire et vérifier le fonctionnement de la solution dans son environnement technique.</p></article>
<article class="process-step" data-reveal><span class="micro">03 / Accompagner</span><h3>Déployer & transmettre</h3><p>Mettre en service, documenter et accompagner l’exploitation et la maintenance selon les besoins du projet.</p></article>
</div></div></section>'''


def home():
    return '''<section class="hero"><img class="hero-art" src="assets/visual-lab.svg" alt="" width="1300" height="900" fetchpriority="high"><div class="container hero-inner"><p class="eyebrow">Playback Solutions / Laboratoire créatif & ingénierie technique</p><h1 lang="en"><span>CREATIVE</span><span>LAB.</span></h1><div class="hero-bottom"><p class="hero-description" lang="en">A creative lab. We design and build custom hardware and software instruments with artists.</p><a class="scroll-link" href="#expertises">Explorer nos expertises <span class="circle-arrow" aria-hidden="true">↓</span></a></div></div></section>
<section class="section light"><div class="container"><div class="section-heading" data-reveal><p class="section-index">01 / Playback Solutions</p><div><div class="intro-copy"><p>Recherche, création<br>et ingénierie technique.</p></div><div class="intro-bottom"><p class="body-copy">Playback Solutions conçoit et développe des solutions sur mesure pour les artistes, les équipes créatives et les professionnels du spectacle vivant et de l’audiovisuel.</p><div><p class="body-copy">Du premier prototype à l’exploitation, nous réunissons développement logiciel et matériel, intégration et fiabilisation des systèmes.</p>'''+arrow_link('a-propos.html', 'À propos')+'''</div></div></div></div></div></section>
<section class="section" id="expertises"><div class="container"><div class="expertise-heading" data-reveal><div><p class="eyebrow">02 / Nos expertises</p><h2>Creative Lab.<br>Performing Systems.<br>Reliable Systems.</h2></div><p class="micro muted">Trois expertises<br>complémentaires</p></div>'''+expertise_cards()+'''</div></section>'''+process()+'''
<section class="section"><div class="container reference-teaser"><div data-reveal><p class="eyebrow">03 / Projets & Références</p><h2>Projets &<br>Références.</h2><p>Retrouvez les références communiquées par Playback Solutions. Les descriptions d’intervention et les photographies seront ajoutées après validation.</p>'''+arrow_link('projets.html','Projets & Références')+'''</div><div class="reference-visual" data-reveal><img src="assets/visual-perform.svg" alt="" width="1300" height="900" loading="lazy"></div></div></section>'''


def expertise_page(item, index):
    capabilities = ''.join(f'<article class="capability" data-reveal><span class="micro">0{n}</span><div><h3>{escape(title)}</h3><p>{escape(body)}</p></div></article>' for n, (title, body) in enumerate(item['capabilities'], 1))
    related = ''.join(arrow_link(other['file'],other['name']) for other in EXPERTISE if other is not item)
    return f'''<section class="container page-hero"><img class="hero-art" src="assets/visual-{item['art']}.svg" alt="" width="1300" height="900" fetchpriority="high"><p class="eyebrow">0{index} / {item['label']}</p><h1 lang="en">{item['headline']}</h1><p class="hero-subtitle" lang="en">{item['slogan']}</p><p class="section-index muted">Playback Solutions / {item['name']}</p></section>
<section class="section light"><div class="container"><div class="section-heading" data-reveal><p class="section-index">L’approche</p><div><h2>{item['intro']}</h2><p class="body-copy" style="margin-top:35px">{item['body']}</p></div></div><div class="capabilities"><p class="section-index">Domaines d’intervention</p><div class="capability-list">{capabilities}</div></div></div></section>
<div class="wide-art"><img src="assets/visual-{item['art']}.svg" alt="" width="1300" height="900" loading="lazy"><span class="micro">{item['name']} / Composition graphique</span></div>
<section class="section"><div class="container"><div class="section-heading" data-reveal><p class="section-index">Collaboration</p><div><h2>De la conception<br>à l’exploitation.</h2><div class="intro-bottom"><p class="body-copy muted">Une intervention ciblée ou un accompagnement global, en lien avec vos équipes et vos partenaires techniques.</p>{arrow_link('contact.html','Échanger sur votre projet')}</div></div></div><div class="related"><p class="micro muted">Les autres expertises</p><div class="related-links">{related}</div></div></div></section>'''


def project_content():
    projects = json.loads((ROOT/'data/projects.json').read_text(encoding='utf-8'))
    rows, details, slugs = [], [], set()
    for n, project in enumerate(projects, 1):
        slug = project['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in slugs:
            raise ValueError('Project slugs must be unique and URL-safe')
        slugs.add(slug)
        approved = project.get('publication_approved') is True
        documented = approved and bool(project.get('description') and project.get('intervention'))
        name = escape(project['name'])
        status = 'Fiche projet' if documented else ('Référence communiquée' if approved else 'Intitulé à confirmer')
        label = f'<a href="#projet-{slug}">{name} <span aria-hidden="true">↗</span></a>' if documented else name
        edition = escape(project.get('edition', ''))
        rows.append(f'<article class="project-row" data-project><span class="micro">{n:02}</span><div><h3>{label}</h3><p class="project-edition">{edition}</p></div><span class="status">{status}</span></article>')
        if documented:
            photo = ''
            if project.get('image'):
                image = Path(project['image'])
                if image.is_absolute() or '..' in image.parts or not str(image).startswith('assets/projects/') or not (ROOT/image).is_file():
                    raise ValueError('Project images must exist under assets/projects/')
                if not project.get('image_alt') or not project.get('image_credit'):
                    raise ValueError('Project photography requires alt text and a credit/rights statement')
                photo = f'<figure><img src="{escape(str(image),quote=True)}" alt="{escape(project["image_alt"],quote=True)}" loading="lazy"><figcaption>{escape(project["image_credit"])}</figcaption></figure>'
            details.append(f'<article class="project-detail" id="projet-{slug}"><h3>{name}</h3>{photo}<div class="detail-copy"><div><h4>Le projet</h4><p>{escape(project["description"])}</p></div><div><h4>Notre intervention</h4><p>{escape(project["intervention"])}</p></div></div></article>')
    return '''<section class="container page-hero"><img class="hero-art" src="assets/visual-perform.svg" alt="" width="1300" height="900"><p class="eyebrow">Projets & Références</p><h1>Projets &<span>Références.</span></h1><p class="hero-subtitle">Les références communiquées par Playback Solutions.</p><p class="section-index muted">Spectacle vivant / Audiovisuel</p></section>
<section class="section light"><div class="container"><div class="projects-intro" data-reveal><h2>Références<br>communiquées.</h2><div><p>Une sélection des artistes, spectacles et productions cités par Playback Solutions. Les éditions et dates correspondent aux informations communiquées.</p><p>Les descriptions précises des interventions et les photographies seront ajoutées après validation. Les intitulés encore ambigus sont signalés.</p></div></div><div class="project-search" hidden><label for="project-query">Rechercher une référence</label><input id="project-query" type="search" placeholder="Artiste, projet ou année…" autocomplete="off" aria-controls="project-list"><p id="project-count" role="status" aria-live="polite"></p></div><div id="project-list">'''+''.join(rows)+'''</div><p id="project-empty" hidden>Aucune référence ne correspond à cette recherche.</p>'''+''.join(details)+'''<p class="notice">Les fiches détaillées seront enrichies avec les descriptions d’intervention et les photographies dont la publication aura été autorisée. Les compositions graphiques du site sont abstraites et ne représentent pas ces projets.</p></div></section>'''


def about():
    return '''<section class="container page-hero"><img class="hero-art" src="assets/visual-reliable.svg" alt="" width="1300" height="900"><p class="eyebrow">À propos</p><h1>Playback<span>Solutions.</span></h1><p class="hero-subtitle">Un laboratoire créatif et une structure d’ingénierie technique pour le spectacle vivant et l’audiovisuel.</p><p class="section-index muted">Le Pré-Saint-Gervais / France</p></section>
<section class="section light"><div class="container about-split"><div class="about-mark" data-reveal><img src="assets/monogramme_playback_BLACK.png" alt="Monogramme officiel Playback Solutions" width="2078" height="2363" loading="lazy"></div><div data-reveal><p class="eyebrow">L’approche</p><h2>Création &<br>ingénierie.</h2><p>Playback Solutions réunit des compétences internes en recherche, développement logiciel et matériel, conception de systèmes et exploitation technique.</p><p>Nous collaborons avec les artistes et les équipes créatives, mais aussi avec les prestataires, productions et intégrateurs qui ont besoin d’une solution spécifique ou d’un partenaire technique complémentaire.</p></div></div></section>
<section class="section"><div class="container"><div class="section-heading" data-reveal><p class="section-index">L’équipe & les collaborations</p><div><h2>Une équipe adaptée<br>au projet.</h2><div class="intro-bottom"><p class="body-copy muted">Notre équipe porte les compétences de conception et de développement en interne. Selon les besoins, nous mobilisons des freelances aux expertises complémentaires.</p><p class="body-copy muted">Nous pouvons accompagner un projet de la recherche à l’exploitation, ou intervenir sur une étape précise en coordination avec les équipes déjà en place.</p></div><div class="audience-list"><span>Prestataires techniques</span><span>Productions</span><span>Managers d’artistes</span><span>Directions techniques</span><span>Intégrateurs audiovisuels</span></div></div></div></div></section>'''+process()+'''
<section class="section"><div class="container reference-teaser"><div data-reveal><p class="eyebrow">Bureaux & studios</p><h2>Le Pré-<br>Saint-Gervais.</h2><p>Rencontrons-nous pour échanger sur vos besoins et visiter les bureaux et studios de Playback Solutions. Les visites s’organisent sur rendez-vous.</p>'''+arrow_link('contact.html','Organiser un rendez-vous')+'''</div><div class="reference-visual" data-reveal><img src="assets/visual-lab.svg" alt="" width="1300" height="900" loading="lazy"></div></div></section>'''


def contact():
    return '''<section class="container page-hero contact-hero"><p class="eyebrow">Contact</p><h1>Contact.</h1><p class="hero-subtitle">Conception, développement, intégration ou fiabilisation : échangeons sur les besoins de votre projet.</p></section>
<section class="section light"><div class="container"><div class="contact-layout"><div data-reveal><p class="micro">Contact commercial</p><h2>Anthony Combe</h2><a class="phone-link" href="tel:+33602256978">+33 6 02 25 69 78</a><p class="contact-note">Prestataires, productions, managers, directions techniques, intégrateurs et équipes artistiques : contactez-nous par téléphone pour présenter votre besoin et convenir d’un échange.</p></div><div class="contact-aside" data-reveal><p class="eyebrow">Sur rendez-vous</p><h3>Bureaux & studios<br>Le Pré-Saint-Gervais.</h3><p>Vous souhaitez rencontrer l’équipe et découvrir notre environnement de travail ? Nous pouvons organiser un rendez-vous et une visite des bureaux et studios.</p><p>Les modalités d’accès vous seront précisées lors de la prise de rendez-vous.</p>'''+arrow_link('tel:+33602256978','Appeler pour un rendez-vous')+'''</div></div><div class="contact-preparation" data-reveal><h3>Pour préparer notre échange</h3><p>Présentez-nous l’usage souhaité, les équipements ou outils concernés, les équipes impliquées et votre calendrier. Nous pourrons définir ensemble le périmètre de notre intervention.</p></div></div></section>'''


def main():
    for kind in ('lab', 'perform', 'reliable'):
        (ROOT/f'assets/visual-{kind}.svg').write_text(art(kind), encoding='utf-8')
    pages = [
        ('index.html', 'Creative Lab, Performing Systems, Reliable Systems', 'Playback Solutions : laboratoire créatif et ingénierie technique. Hardware, software, systèmes sur mesure pour le spectacle vivant et l’audiovisuel.', home(), False),
        ('projets.html', 'Projets & Références', 'Les références communiquées par Playback Solutions et la documentation de leurs périmètres d’intervention.', project_content(), False),
        ('a-propos.html', 'À propos', 'Playback Solutions : compétences internes, laboratoire créatif et collaborations, de la conception à l’exploitation des systèmes.', about(), False),
        ('contact.html', 'Contact', 'Contactez Anthony Combe au +33 6 02 25 69 78. Rendez-vous et visite des bureaux et studios Playback Solutions au Pré-Saint-Gervais.', contact(), True),
    ]
    for n, item in enumerate(EXPERTISE, 1):
        pages.append((item['file'], item['name'], item['summary'], expertise_page(item,n), False))
    for filename, title, description, content, is_contact in pages:
        (ROOT/filename).write_text(page(filename,title,description,content,contact=is_contact), encoding='utf-8')
    print(f'Generated {len(pages)} static pages and 3 original SVG artworks.')


if __name__ == '__main__':
    main()
