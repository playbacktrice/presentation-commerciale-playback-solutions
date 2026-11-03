# V2 corrigée — revue avant mise à jour de la prévisualisation

Corrections effectuées exclusivement sur `feat/refonte-site-vitrine`, après la V2 `96e45b9`. Aucun changement de `main`, de `/preview/` publié ou des paramètres GitHub Pages.

## Résultat

- Fonds noirs sur les cinq pages et le panneau latéral, textes et logos officiels blancs. Voiles et commandes adaptés aux futures photographies.
- Positionnement limité à l’ingénierie, la conception et le développement de systèmes techniques pour le spectacle vivant. Aucune offre audiovisuelle généraliste.
- Textes français, y compris les anciennes formulations de marque anglaises ; conservation des trois noms d’expertise.
- Selon la dernière correction de l’utilisateur, téléphone et adresse e-mail fournis conservés uniquement dans les sections Contact. Suppression des coordonnées du menu, des pieds de page et des métadonnées, y compris les liens cachés.
- Section Références visible : Justice, Polo & Pan, Mylène Farmer, Eddy de Pretto et Jeux olympiques de Paris 2024. Aucun rôle, prestation ou résultat inventé.
- Douze entrées photographiques configurées, réutilisées dans quinze emplacements. Aucun remplacement par une réalisation fictive. Les 40 références sources et les quatre logos officiels sont conservés sans modification.

## Contrôles

- Contrôle statique des cinq pages, des 88 liens/ressources/fragments locaux et des coordonnées dans le HTML complet : liens, attributs, métadonnées et textes hors Contact.
- Vérification des textes anglais retirés et de l’absence de positionnement audiovisuel dans les pages.
- Vérification des cinq références et des douze entrées de médias.
- Génération reproductible et syntaxe JavaScript valide.
- Une image locale autorisée est acceptée avec son crédit et sa description dans une copie isolée ; une image non validée est rejetée.
- Chromium à 320, 390, 768 et 1440 px sur les cinq pages : navigation, logos, menu latéral, focus clavier, boutons de fermeture, Échap et fond assombri.
- Carrousel manuel : précédent/suivant, boucle, clavier et compteur. Une seule diapositive active.
- Surfaces sombres, contraste d’au moins 4,5:1 du texte courant et des indications d’emplacement sur leurs fonds unis ; téléphone et e-mail présents uniquement dans Contact sur chaque page.
- Les cinq références sont présentes dans la section dédiée ; cinq emplacements photo de carte, sans catalogue de 40 noms.
- Fonctionnement sans JavaScript et respect de la réduction des animations. Aucun débordement horizontal, titre coupé, erreur JavaScript ou ressource HTTP en échec pendant les tests.
- Même suite sous le sous-chemin `/presentation-commerciale-playback-solutions/` : 40 couples page/largeur au total.

Ces tests Chromium ne constituent pas un audit complet d’accessibilité ou des tests Safari/Firefox. Le contraste et les cadrages des futures photos devront être vérifiés avec les fichiers réels.

## Publication

Les captures de revue sont produites localement. La version publiée reste inchangée. Une nouvelle autorisation explicite est requise pour actualiser `/preview/`.
