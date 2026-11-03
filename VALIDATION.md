# Laboratoire et références — revue de développement

Changements limités à `feat/refonte-site-vitrine`, à partir de `7f719bc`. Le thème noir, les cinq pages, les coordonnées uniquement dans Contact et la navigation existante sont conservés. Aucun changement de `main`, de `/preview/` publié ni des paramètres GitHub Pages.

## Modifications

- Accueil recentré sur le laboratoire d’ingénierie et les développements sur mesure.
- Six compétences avec pictogrammes SVG au trait, intégrées à la présentation : Sur mesure, Contrôleurs, Logiciels, Systèmes, Synchronisation et Fiabilité. Une ligne sur ordinateur, deux colonnes sur mobile.
- Creative Lab renforcé : contrôleurs/interfaces puis logiciels/systèmes spécifiques. Trois emplacements pour les photographies des réalisations réelles.
- Sept références mises en avant : Justice, Polo & Pan, Mylène Farmer, Eddy de Pretto, Kungs, Damso et Jeux olympiques de Paris 2024.
- Collection complète repliée par défaut via HTML natif : les 35 entrées confirmées du fichier existant sont regroupées en 32 artistes ou productions, avec leurs éditions. Sans photographie, une entrée est uniquement typographique. Une photo autorisée peut être intégrée progressivement sans créer une page de plus.
- Les cinq entrées marquées à confirmer restent dans les données, hors affichage : Clara Lafut 2021, MC Solar 2022, MC 2023, MC Solar 2023 et Mylène le retour. Aucune référence, prestation, responsabilité ou résultat inventé. Inventaire exact dans `REFERENCES.md`.

## Vérifications réalisées

- Cinq pages, 88 liens/ressources/fragments locaux, coordonnées uniquement dans Contact et textes français hors noms propres/termes techniques autorisés.
- Six pictogrammes et bande compacte contrôlés en navigateur : hauteur inférieure à 160 px sur ordinateur/tablette et à 380 px sur petit mobile.
- Sept références sélectionnées ; 32 groupes dans le volet ; correspondance exacte de chacun des 35 slugs confirmés, sans doublon ni entrée non confirmée.
- Regroupement des éditions de Mylène Farmer et Jean-Michel Jarre vérifié ; ouverture et fermeture du volet au clavier et à la souris ; ouverture également sans JavaScript.
- Quinze entrées de médias, emplacements de photos réelles identifiés. Dans une copie isolée, photo locale validée acceptée dans le carrousel et dans une référence de collection ; photo non validée rejetée.
- Logos et fichier source des 40 entrées inchangés ; génération HTML reproductible ; syntaxe JavaScript et diff vérifiés.
- Chromium : cinq pages à 320, 390, 768 et 1440 px à la racine locale, puis sous `/presentation-commerciale-playback-solutions/` : 40 couples page/largeur.
- Navigation entre les cinq pages, images, carrousel (boutons, boucle, clavier, compteur), menu (Échap, fond, fermeture, focus), contrastes sur fonds unis et réduction des animations contrôlés.
- Aucun débordement horizontal ni erreur JavaScript, console ou ressource HTTP en échec pendant les contrôles.

Tests effectués dans Chromium ; pas d’audit d’accessibilité exhaustif ni de test Safari/Firefox. Les crédits, droits et recadrages des futures photographies restent à valider avec les fichiers réels.

## Mise en ligne

Cette évolution n’est pas publiée. Les captures sont locales. Attendre une autorisation explicite avant de mettre à jour `/preview/`.
