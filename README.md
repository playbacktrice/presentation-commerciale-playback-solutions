# Playback Solutions — V2 en développement

Cinq pages statiques : Accueil, Creative Lab, Performing Systems, Reliable Systems et Contact. La V2 est développée sur `feat/refonte-site-vitrine`. **Ne pas modifier `main` ni le dossier `/preview/` publié sans une nouvelle autorisation explicite.** Le push de la branche de développement ne déploie pas la V2 sur GitHub Pages, configuré sur `main` / `(root)`.

## Exécuter et vérifier

Depuis la racine du dépôt :

```sh
python3 scripts/build.py
python3 scripts/check_site.py
node --check assets/site.js
python3 -m http.server 8000 --bind 127.0.0.1
```

Les fichiers HTML générés sont versionnés. Le site n’a aucune dépendance de production, aucun backend, aucune police distante et aucun outil de compilation obligatoire à la publication. Python sert à éditer les contenus communs et régénérer les cinq pages.

Les tests Chromium optionnels utilisent Playwright présent dans l’outillage de développement :

```sh
SITE_URL=http://127.0.0.1:8000/ node scripts/check_browser.cjs
```

`PLAYWRIGHT_MODULE` et `BROWSER_PATH` permettent d’utiliser une installation existante. `PREVIEW_DIR` demande les captures ordinateur/mobile. La suite teste les cinq pages à 320, 390, 768 et 1440 px, les liens, les logos, le panneau de navigation, le clavier, le carrousel, la réduction des animations et le fonctionnement sans JavaScript. Elle peut être exécutée sous le sous-chemin du dépôt en servant son dossier parent et en adaptant `SITE_URL`.

## Sources

- `scripts/build.py` : gabarit commun et textes courts des cinq pages.
- `assets/site.css` : compositions, menu latéral, responsive et préférences de mouvement.
- `assets/site.js` : panneau de navigation et carrousel manuel.
- `data/media.json` : douze entrées photographiques réutilisées dans les pages, crédits et autorisations.
- `data/projects.json` : les 40 références communiquées sont conservées comme données, sans catalogue sur les pages de la V2.
- `assets/*.png` : les quatre logos officiels, conservés sans modification.

Les anciennes pages institutionnelles et les visuels abstraits de la V1 sont retirés de cette branche. Ces suppressions ne concernent pas `main` ni le dossier de prévisualisation existant.

## Intégrer progressivement les photographies

Consulter `PHOTO-BRIEF.md`. Placer les fichiers autorisés dans `assets/photos/`, puis renseigner la clé correspondante dans `data/media.json` :

```json
{
  "label": "Concert — Justice",
  "artist": "Justice",
  "src": "assets/photos/justice.webp",
  "alt": "Description factuelle de la photographie fournie",
  "credit": "Crédit et mention de droits validés",
  "approved": true,
  "position": "50% 50%"
}
```

Cet exemple décrit un chemin à créer : aucune photographie de Justice n’est incluse. `src` vide conserve un emplacement explicitement identifié. Un chemin renseigné exige un fichier local, un texte alternatif, un crédit et `approved: true`. Le générateur refuse les ressources externes et les fichiers hors d’`assets/photos/`.

Le thème est noir sur les cinq pages et le panneau de navigation, avec les logos officiels blancs. Les commandes du carrousel restent claires ; un voile sombre protège leur contraste et celui des légendes sur les futures photographies. `position` règle le recadrage. Les vues de matériel utilisent `object-fit: contain`, les panoramas et le carrousel utilisent `cover`. Les légendes artistiques n’attribuent aucune prestation technique ; une intervention doit être documentée et validée avant toute précision.

Après chaque ajout, régénérer et vérifier le cadrage sur ordinateur et mobile. Le carrousel est manuel : boutons précédent/suivant et touches fléchées, sans défilement automatique. Sans JavaScript, la première diapositive et tous les liens du menu restent accessibles.

## Publication

Tous les liens sont relatifs ; la V2 fonctionne sous un sous-chemin GitHub Pages. Aucun paramètre Pages, workflow ou déploiement n’est modifié par la V2. La prévisualisation publique conserve la V2 précédente jusqu’à autorisation de publier ces corrections.

## Corrections éditoriales et coordonnées

Le positionnement porte uniquement sur l’ingénierie et les systèmes techniques pour le spectacle vivant : audio, informatique, logiciels, matériel spécifique, intégration et fiabilisation. Les textes visibles sont en français, hors marque, noms des artistes, intitulés des trois expertises et termes techniques comme playback.

Selon la dernière instruction de l’utilisateur, le téléphone et l’adresse e-mail fournie sont conservés **uniquement dans les sections Contact**. Aucun de ces liens ou coordonnées dans le menu, le pied de page ou les métadonnées. Les contrôles statiques et navigateur vérifient cette restriction.

Une section d’accueil Références présente Justice, Polo & Pan, Mylène Farmer, Eddy de Pretto et les Jeux olympiques de Paris 2024, avec des emplacements photo et sans attribution de prestation.
