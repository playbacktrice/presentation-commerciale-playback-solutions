# Refonte — éléments de revue

Branche : `feat/refonte-site-vitrine`. Base : `e183307`. Aucun changement de `main`, de la configuration GitHub Pages ou de déploiement.

## Réalisation

Sept pages statiques : Accueil, Creative Lab, Performing Systems, Reliable Systems, Projets & Références, À propos et Contact. Navigation commune avec page active, menu mobile, accès rapide aux expertises, recherche des références sans distinction d’accents, appels téléphoniques et prise de rendez-vous par téléphone.

Identité essentiellement noire et blanche, logos officiels préservés à l’octet près, trois compositions vectorielles abstraites originales. Aucun faux équipement, fausse photographie, faux membre d’équipe, faux e-mail ou attribution technique. Les formulations de marque du brief sont conservées. Les références, titres et dates viennent de la liste fournie ; les intitulés ambigus sont signalés et les doublons regroupés.

Structure sans backend ni dépendance de production. Les pages sont générées avec la bibliothèque standard Python et restent de simples fichiers HTML consultables sans compilation. Les données projets sont indépendantes des gabarits et permettent d’ajouter des fiches détaillées et des photographies autorisées.

## Vérifications effectuées

- Génération reproductible : résultat identique après une seconde exécution.
- Contrôle statique : sept pages, 205 liens/ressources/fragments locaux, trois SVG et 40 références.
- Vérification syntaxique de `assets/site.js` avec Node.
- Chromium réel : sept pages à 320, 390, 768 et 1440 px, soit 28 couples page/largeur pour chaque chemin de test.
- Même suite à la racine locale et sous `/presentation-commerciale-playback-solutions/`, soit 56 couples page/largeur au total.
- Réponses HTTP 200, navigation effective entre toutes les pages, titres non coupés, absence de débordement horizontal et chargement de toutes les images.
- Recherche : accents ignorés, combinaison artiste/année, absence de résultat et réinitialisation aux 40 références.
- Menu : ouverture, fermeture par Échap, retour du focus et boucle de tabulation sur mobile/tablette.
- Sept pages utilisables sans JavaScript ; révélations au défilement testées et réduction des animations respectée.
- Aucune erreur de console JavaScript ni ressource HTTP en échec pendant les contrôles.
- Quatre logos PNG identiques à la version originale ; diff sans erreur d’espacement.

Ces contrôles ne constituent pas un audit d’accessibilité exhaustif ni un test dans Safari/Firefox. L’utilisation de HTML/CSS standard et l’absence de ressources externes limitent les dépendances. La compatibilité GitHub Pages a été vérifiée localement sous son sous-chemin ; aucune mise en ligne n’a été réalisée pour ce contrôle.

## En attente de validation

L’accès à `https://www.optolive.com/` reste bloqué par le proxy (403), même après la modification des paramètres annoncée par l’utilisateur. Le statut de l’environnement actif rapporte toujours une politique réseau restreinte sans domaines personnalisés. Aucune analyse effective du site Opto n’a donc pu être réalisée. L’utilisateur ayant demandé de poursuivre malgré le blocage, cette proposition applique les principes visuels du brief et devra être affinée avec des captures ou un accès effectif à la référence.

Reste à confirmer : les intitulés « Clara Lafut », « MC Solar » (2022 et 2023), « MC 2023 » et « Mylène le retour » ; le périmètre réel de chaque intervention ; les descriptions, photos et droits de publication. Les fiches détaillées ne sont pas activées avec des descriptions inventées.

La validation visuelle et éditoriale de l’utilisateur reste nécessaire avant toute fusion ou mise en ligne.
