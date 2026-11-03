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
- `data/media.json` : quinze entrées photographiques réutilisées dans les pages, crédits et autorisations.
- `data/projects.json` : les 40 entrées communiquées sont conservées ; les 35 entrées confirmées alimentent 32 groupes dans le volet « Toutes les références ». Les cinq entrées encore ambiguës ne sont pas exposées.
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

## Laboratoire, compétences et références complètes

L’accueil met d’abord en avant le laboratoire d’ingénierie et ses développements sur mesure. Six pictogrammes SVG originaux au trait, accompagnés de titres et d’une ligne de description, forment une bande compacte dans la présentation. Aucun nouveau lien dans le menu. Creative Lab dispose de deux séquences dédiées aux contrôleurs/interfaces et aux logiciels/systèmes spécifiques, avec des emplacements photographiques réels à compléter.

La sélection photographique contient sept références, dont Kungs et Damso. Le volet natif HTML `details` / `summary` « Toutes les références » fonctionne sans JavaScript. Les 35 entrées marquées `publication_approved: true` dans le fichier source sont regroupées par nom en 32 artistes ou productions, avec leurs éditions. Les entrées non confirmées restent dans les données sans être publiées comme références. L’inventaire exact figure dans `REFERENCES.md`.

Une entrée de collection sans image affiche seulement son nom et ses éditions, sans grande case vide. Pour ajouter une photographie autorisée à une référence confirmée, utiliser les champs `image`, `image_alt` et `image_credit` du fichier de projets. Le fichier doit exister sous `assets/photos/`. Le contrôle des chemins, textes alternatifs et crédits est partagé avec les autres photographies. Aucun résultat ou rôle technique n’est généré depuis le nom d’un artiste.
