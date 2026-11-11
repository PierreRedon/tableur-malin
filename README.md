# Tableur Malin

Site statique d'astuces Excel et Google Sheets en français, publié avec GitHub Pages.

- `outils/site/contenu.py` : le contenu (astuces, pack, réglages du site).
- `outils/site/build.py` : génère les pages HTML à la racine. Lancer `python3 outils/site/build.py`.
- `outils/video/` : scripts qui fabriquent les vidéos d'astuce (Pillow + ffmpeg).
- `videos/` : vidéos hébergées par le site, accessibles par lien public.
- `assets/` : styles, script et polices (licence SIL Open Font, fichiers de licence joints).

Les pages HTML sont générées : modifier `contenu.py` puis relancer le script, sans éditer le HTML à la main.
