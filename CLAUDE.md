# Tableur Malin : consignes pour Claude

Projet de Pierre Redon : astuces Excel et Google Sheets en français. Site statique sur GitHub Pages
(https://tableurmalin.fr), une courte vidéo d'astuce par jour, pack de modèles vendu 9 € par lien Stripe.

## Règles fixées par Pierre

- Autonomie maximale : Pierre ne veut plus intervenir, ou presque. Ne pas lui demander de valider chaque astuce.
- Aucune dépense, aucun abonnement, aucun crédit payant sans son accord explicite.
- Ne publier QUE sur les comptes dédiés, jamais sur ses comptes personnels (Lightmare / @lightmare_tv,
  pier_redon, « Pierre Redon259 »), qui sont pourtant visibles dans vidIQ.
- Comptes dédiés dans vidIQ (toujours revérifier avec `vidiq_social_account_list`) :
  - TikTok « tableurmalin » : platformAccountId `_000gVSFKvPZdYKgZobMfCTLqOMnsAThYO1s`
  - Instagram « tableurmalin2026 » : platformAccountId `29331079859836743`
  - YouTube « Tableur Malin » (@TableurMalin) : pas encore connecté au 11/11/2026. S'il apparaît dans la liste, l'ajouter
    aux publications (titre obligatoire, visibilité publique).
- Réglages TikTok choisis par Pierre le 11/11/2026 pour toutes les vidéos : `privacyLevel` PUBLIC_TO_EVERYONE,
  `allowComment` true, `musicUsageConfirmed` true. Ajouter `isAiGenerated` true.
- Vidéos : verticales 1080×1920, 15 à 25 secondes, sans visage ni voix, mais JAMAIS muettes (demandé par Pierre le
  12/11/2026) : fond musical doux et bruitages calés sur l'image, fabriqués par `outils/video/son.py` (synthèse
  maison, gratuite, sans musique sous droits). Pas de voix ni de musique payantes sans son accord.

## Organisation du dépôt

- `outils/site/contenu.py` : tout le contenu (liste `ASTUCES`, pack, réglages). Seule source à modifier pour le site.
- `outils/site/build.py` : régénère les pages HTML à la racine. `python3 outils/site/build.py` depuis la racine.
  Ne jamais éditer le HTML généré à la main.
- `outils/video/astuce_ctrl_e.py` : script de référence d'une vidéo (Pillow + ffmpeg, polices dans `outils/video/polices`).
  Il contient les briques visuelles : `fond`, `entete`, `boite`, `legende`, `barre_formule`, `touches`, `tableau`, `rendre`.
- `videos/<slug>.mp4` et `videos/<slug>.jpg` : vidéo et image d'aperçu, servies par le site.
- Pousser sur `main` déclenche la mise en ligne (GitHub Pages, « Deploy from a branch »). Le fichier `CNAME` doit rester.

## Procédure de l'astuce du jour

1. Lire `ASTUCES` dans `contenu.py` pour ne pas répéter un sujet. Choisir une astuce Excel/Sheets utile au quotidien,
   très visuelle, démontrable en moins de 20 secondes (raccourci, formule courte, réglage en deux clics).
2. Vérifier par une recherche web les noms de fonctions et de menus EN FRANÇAIS (Excel et Google Sheets), le séparateur
   « ; », et les versions concernées. Ne rien affirmer qui n'a pas été vérifié ; en cas de doute, formuler prudemment.
3. Ajouter l'astuce EN TÊTE de `ASTUCES` (mêmes champs que les autres, `date` du jour, `video` = slug), en respectant le ton :
   réponse courte d'abord, étapes, « À savoir », équivalent Google Sheets, pièges. Français correct, vouvoiement, sans jargon.
4. Créer `outils/video/astuce_<slug>.py` en copiant `astuce_ctrl_e.py` et en adaptant les scènes (accroche, démonstration,
   carte de fin) ainsi que la liste `SONS` (un bruitage par action visible : frappe, clic, touche, carillon, fin).
   Garder exactement le style : papier quadrillé, cellule active verte à ombre jaune, barre de formule,
   en-tête Tableur Malin avec barre de progression. Zone utile : x de 60 à 960, rien d'important sous y = 1500.
5. Générer d'abord des images d'aperçu (`--apercu`), LES REGARDER, corriger tout texte coupé, chevauchement ou faute,
   puis rendre la vidéo dans `videos/<slug>.mp4` et extraire `videos/<slug>.jpg` (image de la démonstration, largeur 720).
6. `python3 outils/site/build.py`, contrôler la page de l'astuce, puis commit et push sur `main`.
7. Attendre que `https://tableurmalin.fr/videos/<slug>.mp4` soit en ligne (`gh run list -R PierreRedon/tableur-malin -L 1`
   doit indiquer `success`). Si le déploiement reste bloqué plus de 15 minutes, pousser un commit vide pour le relancer.
8. Importer la vidéo dans vidIQ avec `vidiq_video_upload` (paramètre `url` = lien public ci-dessus), créer UN brouillon
   avec `vidiq_social_post_draft_create` pour les comptes dédiés, puis publier avec `vidiq_social_post_publish`.
   Légende : une phrase d'accroche, la formule ou le raccourci, « Le pas-à-pas complet : tableurmalin.fr », 4 à 6 hashtags.
9. Vérifier avec `vidiq_social_post_status` jusqu'à la fin. Ne jamais republier un contenu déjà envoyé ou en cours.
10. En cas d'échec à n'importe quelle étape : ne rien publier d'incomplet, et laisser un compte rendu clair de ce qui a
    bloqué. Ne pas contourner un blocage par une dépense.

## Enrichir le site (demandé par Pierre le 11/11/2026)

- En plus de l'astuce du jour avec vidéo, ajouter chaque jour UNE page d'astuce supplémentaire sans vidéo (pas de champ
  `video`), sur une question que les gens cherchent vraiment (« comment ... dans Excel »), vérifiée de la même façon.
- Le pack de modèles (vingt fichiers .xlsx et un aide-mémoire, listés dans `PACK_MODELES`) existe depuis le
  11/11/2026. Prix prévu : 9 €. Ses fichiers ne sont PAS dans ce dépôt public et ne doivent jamais y être ajoutés. Il est en vente
  depuis le 11/11/2026 par le lien Stripe renseigné dans `contenu.py` (`stripe_lien`). Les fichiers sont livrés par un dossier
  Google Drive dont le lien ne doit JAMAIS figurer sur le site ni dans ce dépôt.
- Dans une légende sur trois environ, ajouter une ligne : « 20 modèles prêts à remplir : tableurmalin.fr/pack-modeles ».
- Idées d'enrichissement du pack à proposer à Pierre dans le compte rendu quand c'est pertinent, sans rien vendre de
  nouveau sans son accord.

## Commits

Auteur : `-c user.name="Tableur Malin" -c user.email="tableurmalin@gmail.com"`.
