# Playback Solutions

Site vitrine statique multipage. HTML, CSS, JavaScript et compositions SVG locales ; aucune dépendance côté site, aucun backend, aucun service tiers ni formulaire qui simule un envoi. Contact téléphonique et rendez-vous au Pré-Saint-Gervais.

## Travailler localement

Depuis la racine du dépôt :

```sh
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Les sept pages HTML sont déjà générées et versionnées : Python sert uniquement à régénérer et à vérifier les fichiers, pas à faire fonctionner le site publié. Aucun `npm install` nécessaire. Ouvrir la page locale dans son navigateur ; ne pas utiliser un serveur de développement comme publication.

## Organisation

- `scripts/build.py` : gabarits communs, textes et génération des pages et des SVG.
- `assets/site.css` et `assets/site.js` : styles, navigation mobile, révélations au défilement et recherche des références.
- `data/projects.json` : références, éditions et futurs contenus des fiches projets.
- `assets/*.png` : quatre logos officiels conservés sans modification.
- `assets/visual-*.svg` : compositions abstraites originales, sans photographie de matériel ou de réalisation fictive.
- `*.html` : pages autonomes générées, à ne pas modifier à la main.

## Ajouter une référence ou une fiche projet

Ajouter une entrée à `data/projects.json`, puis exécuter la génération et le contrôle. `slug` doit être unique, en minuscules avec des tirets. `name` et `edition` reprennent les informations validées ; conserver les années comme des informations de référence, sans inférer de rôle technique.

`publication_approved` indique la validation de l’intitulé pour citation. Les références communiquées sont visibles dans cette version à valider, y compris les intitulés ambigus signalés. Ce champ ne constitue pas une preuve de prestation ni une autorisation de mise en ligne du site. Vérifier ces éléments avant toute publication.

Pour ouvrir une fiche détaillée sur la page Projets & Références, renseigner `description` et `intervention` **validés**, et passer `publication_approved` à `true`. Le nom devient un lien vers la fiche. Aucun rôle ni résultat n’est généré automatiquement. Les textes sont échappés et restent du texte simple.

Les photographies sont facultatives : placer une image autorisée sous `assets/projects/`, renseigner `image` avec son chemin relatif, `image_alt` avec une description et `image_credit` avec le crédit ou la mention des droits. Le générateur refuse les chemins hors de ce dossier et les images sans description/crédit. Préférer WebP/AVIF ou JPEG optimisés et des dimensions adaptées ; vérifier le rendu après ajout.

## Contrôles

`python3 scripts/check_site.py` contrôle les sept pages, liens locaux, fragments, ressources, navigation active et données de références. `node --check assets/site.js` vérifie la syntaxe du script.

Un contrôle optionnel dans un véritable navigateur est disponible avec Playwright installé dans l’outillage de développement (ce n’est pas une dépendance du site) :

```sh
SITE_URL=http://127.0.0.1:8000/ node scripts/check_browser.cjs
```

Les variables `PLAYWRIGHT_MODULE` et `BROWSER_PATH` permettent d’utiliser les outils déjà installés dans un environnement ; `PREVIEW_DIR` demande des captures desktop/mobile. Le contrôle couvre 320, 390, 768 et 1440 px, navigation, images, recherche, clavier, absence de JavaScript et réduction des animations. Pour vérifier le sous-chemin GitHub Pages, servir le dossier parent et définir `SITE_URL` avec `/presentation-commerciale-playback-solutions/`.

## GitHub Pages et validation

Tous les chemins sont relatifs. Les sept pages, `assets/` et `.nojekyll` peuvent être servis tels quels à la racine du projet GitHub Pages, y compris sous `/presentation-commerciale-playback-solutions/`. Aucun routage serveur, outil de compilation ou domaine personnalisé n’est requis. Le fonctionnement via sous-chemin est couvert par les contrôles de navigateur.

La refonte est isolée sur `feat/refonte-site-vitrine`. **Ne pas fusionner vers `main`, changer la source de GitHub Pages ou mettre en ligne sans autorisation explicite.** Aucun mécanisme de déploiement automatique n’a été ajouté.

## Éléments à valider

L’accès à Opto renvoie encore un refus 403 du proxy dans l’environnement actif. Aucune analyse visuelle effective de ce site n’est revendiquée. La proposition applique les principes du brief : minimalisme, noir et blanc, grands visuels abstraits, typographie, navigation cohérente et animations mesurées. L’ajustement à la référence reste à faire dès réception de captures ou rétablissement de l’accès.

La liste de références fournie a été regroupée à 40 entrées (doublons des Victoires de la Musique et Djadja & Dinaz). Les intitulés « Clara Lafut », « MC Solar », « MC 2023 » et « Mylène le retour » restent signalés pour confirmation, sans correction inventée. Les rôles, descriptions d’intervention, photos et droits d’utilisation restent à fournir. Pas de portraits, d’adresse précise ni d’e-mail inventés.
