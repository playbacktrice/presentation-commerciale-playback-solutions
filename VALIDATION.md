# V2 — validation de la version de revue

Développement exclusivement sur `feat/refonte-site-vitrine`, à partir de la V1 `e5fca95`. Aucun changement de `main`, de `/preview/` publié ni des paramètres GitHub Pages.

## Résultat préparé

Cinq pages : accueil, trois expertises, contact. Grand carrousel manuel, panneau de navigation blanc depuis la gauche avec fond assombri, compositions éditoriales et matériel/texte inspirées des six captures Opto réellement examinées. Textes courts, grands espaces photographiques, dix emplacements identifiés. Aucun visuel abstrait ou photographie de remplacement. Trois références artistiques mises en contexte ; les 40 références sources restent conservées dans les données.

## Contrôles effectués

- Contrôle statique : cinq pages, 88 liens/ressources/fragments internes, navigation active, dix emplacements photographiques.
- Les quatre logos officiels et le fichier des 40 références sont identiques à la V1.
- Régénération des cinq pages reproductible ; vérification syntaxique JavaScript.
- Contrat d’insertion photographique : image locale autorisée avec texte alternatif et crédit acceptée dans une copie de test isolée ; image non validée refusée. Cette image de test n’est pas intégrée au site.
- Chromium : cinq pages à 320, 390, 768 et 1440 px, soit 20 couples page/largeur.
- Même suite sous `/presentation-commerciale-playback-solutions/`, soit 40 couples page/largeur au total.
- Toutes les destinations du menu sont parcourues par clic. Pas de débordement horizontal ni de titre coupé ; tous les logos chargent.
- Menu : ouverture, fermeture par bouton, Échap et clic sur le fond ; retour et confinement du focus ; contenu derrière le panneau rendu inactif.
- Carrousel : précédent/suivant, boucle, touches gauche/droite, une seule diapositive visible, compteur mis à jour. Aucun autoplay.
- Les cinq pages restent utilisables sans JavaScript ; les préférences de réduction des animations sont respectées.
- Aucune erreur JavaScript, console ou ressource HTTP en échec pendant ces contrôles.

## Limites et éléments à fournir

Les tests de navigateur ont été effectués dans Chromium, pas dans Safari/Firefox. Les six captures décrivent une composition desktop ; l’adaptation mobile a été vérifiée dans Chromium. Elles ne prouvent pas les timings d’animation d’Opto.

Aucune photographie Playback Solutions n’a été fournie pour cette V2. Les emplacements sont volontairement vides et nommés. Le rendu final des photographies, le contraste des légendes et les recadrages devront être validés avec les fichiers réels. `PHOTO-BRIEF.md` détaille les dix emplacements, dont la photographie de Justice peut être réutilisée. Les crédits, droits et éventuels périmètres d’intervention doivent être validés.

Cette version n’est pas déployée. Les captures locales de revue ne constituent pas une mise à jour de `/preview/`. Toute mise en ligne attend une autorisation explicite.
