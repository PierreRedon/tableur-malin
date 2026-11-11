"""Génère le site statique Tableur Malin à la racine du dépôt.

Usage : python3 outils/site/build.py   (depuis la racine du dépôt)
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contenu import ASTUCES, PACK_MODELES, SITE  # noqa: E402

RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
e = html.escape


def texte_brut(s):
    return re.sub(r"<[^>]+>", "", s)


def ecrire(chemin, contenu):
    cible = os.path.join(RACINE, chemin)
    os.makedirs(os.path.dirname(cible) or RACINE, exist_ok=True)
    with open(cible, "w", encoding="utf-8") as f:
        f.write(contenu)


def page(chemin, titre, description, corps, profondeur=0, jsonld=None, og_type="website", index=True):
    p = "../" * profondeur
    url = SITE["url"] + "/" + (chemin[:-10] if chemin.endswith("index.html") else chemin)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n'
                 for x in (jsonld or []))
    robots = "" if index else '<meta name="robots" content="noindex">\n'
    doc = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre)}</title>
<meta name="description" content="{e(description)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE['nom']}">
<meta property="og:title" content="{e(titre)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="fr_FR">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{p}assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/style.css">
{ld}</head>
<body>
<a class="evitement" href="#contenu">Aller au contenu</a>
<header class="barre">
  <a class="marque" href="{p}index.html"><span class="marque-cellule" aria-hidden="true"></span>{SITE['nom']}</a>
  <nav aria-label="Navigation principale">
    <a href="{p}astuces/index.html">Astuces</a>
    <a href="{p}pack-modeles/index.html">Pack de modèles</a>
  </nav>
</header>
<main id="contenu">
{corps}
</main>
<footer class="pied">
  <p>{SITE['nom']} publie une astuce Excel ou Google Sheets par jour, en français.</p>
  <p><a href="{p}astuces/index.html">Toutes les astuces</a> <a href="{p}pack-modeles/index.html">Pack de modèles</a>
  <a href="{p}mentions-legales/index.html">Mentions légales</a></p>
  <p class="discret">Site indépendant, sans lien avec Microsoft ni Google. Excel et Google Sheets sont des marques
  de leurs propriétaires respectifs.</p>
</footer>
<script src="{p}assets/site.js" defer></script>
</body>
</html>
"""
    ecrire(chemin, doc)


def lignes_astuces(astuces, p, debut=1):
    out = ['<ol class="feuille" start="%d">' % debut]
    for i, a in enumerate(astuces, debut):
        out.append(
            f'<li><span class="num" aria-hidden="true">{i}</span>'
            f'<a class="lien-astuce" href="{p}astuces/{a["slug"]}/index.html">{e(a["titre"])}</a>'
            f'<span class="meta">{e(a["outils"])}</span><span class="meta">{e(a["niveau"])}</span></li>')
    out.append("</ol>")
    return "\n".join(out)


def bloc_pack(p):
    return f"""<aside class="bande-pack">
  <h2>Des tableaux déjà prêts, plutôt que de partir d'une feuille vide</h2>
  <p>Le pack de modèles réunit vingt tableaux prêts à remplir (budget, factures, planning, stock, prêt, épargne), avec les formules
  déjà en place. Il fonctionne dans Excel et dans Google Sheets.</p>
  <a class="bouton" href="{p}pack-modeles/index.html">Voir le contenu du pack</a>
</aside>"""


def bloc_video(a, p):
    v = a["video"]
    return (f'<video controls playsinline preload="metadata" poster="{p}videos/{v}.jpg" width="1080" height="1920">'
            f'<source src="{p}videos/{v}.mp4" type="video/mp4">'
            f'Votre navigateur ne lit pas la vidéo. <a href="{p}videos/{v}.mp4">Ouvrir la vidéo</a>.</video>')


def bloc_formule(f, legende=""):
    leg = f"<figcaption>{e(legende)}</figcaption>" if legende else ""
    return (f'<figure class="formule"><div class="formule-ligne"><span class="fx" aria-hidden="true">fx</span>'
            f'<code>{e(f)}</code><button type="button" class="copier" data-copie="{e(f)}">Copier</button></div>'
            f'{leg}</figure>')


def accueil():
    vedette = next(a for a in ASTUCES if a.get("video"))
    corps = f"""<section class="hero">
  <div class="hero-texte">
    <div class="barre-formule" aria-hidden="true"><span class="ref">A1</span><span class="fx">fx</span><span>=ASTUCE(AUJOURDHUI())</span></div>
    <h1 class="cellule-active">Une astuce de tableur par jour, expliquée en vingt secondes</h1>
    <p class="chapo">Excel et Google Sheets en français : des raccourcis et des formules qui font gagner du temps,
    montrés pas à pas, sans jargon.</p>
    <p><a class="bouton" href="astuces/index.html">Parcourir les astuces</a></p>
  </div>
  <figure class="hero-video">
    {bloc_video(vedette, "")}
    <figcaption><a href="astuces/{vedette['slug']}/index.html">{e(vedette['court'])}</a>, l'astuce du jour</figcaption>
  </figure>
</section>
<section>
  <h2>Les dernières astuces</h2>
  {lignes_astuces(ASTUCES, "")}
</section>
{bloc_pack("")}"""
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE["nom"], "url": SITE["url"] + "/",
           "inLanguage": "fr", "description": SITE["accroche"]}]
    page("index.html", "Tableur Malin : astuces Excel et Google Sheets en français",
         "Une astuce Excel ou Google Sheets par jour, en français : raccourcis, formules et réglages expliqués pas à "
         "pas, avec une courte vidéo.", corps, 0, ld)


def liste():
    corps = f"""<section class="entete-page">
  <h1>Toutes les astuces Excel et Google Sheets</h1>
  <p class="chapo">Chaque page répond à une question précise : la réponse courte d'abord, les étapes ensuite,
  puis les pièges à éviter.</p>
</section>
{lignes_astuces(ASTUCES, "../")}
{bloc_pack("../")}"""
    page("astuces/index.html", "Astuces Excel et Google Sheets : la liste complète | Tableur Malin",
         "Toutes les astuces Tableur Malin pour Excel et Google Sheets : raccourcis, formules, listes déroulantes, "
         "doublons, volets figés.", corps, 1)


def fiche(a):
    p = "../../"
    url = f"{SITE['url']}/astuces/{a['slug']}/"
    blocs = [f"""<nav class="fil" aria-label="Fil d'Ariane"><a href="{p}index.html">Accueil</a> / <a href="../index.html">Astuces</a></nav>
<article class="fiche">
<h1>{e(a['titre'])}</h1>
<p class="fiche-meta">Fonctionne dans {e(a['outils'])}. Niveau {e(a['niveau']).lower()}.</p>
<p class="bref">{e(a['bref'])}</p>"""]
    if a.get("video"):
        blocs.append(f'<figure class="fiche-video">{bloc_video(a, p)}<figcaption>L\'astuce en vidéo, sans le son.</figcaption></figure>')
    titre_etapes = "Les étapes dans Excel" if a.get("etapes_excel") else "Les étapes"
    blocs.append(f"<h2>{titre_etapes}</h2><ol class=\"etapes\">" + "".join(f"<li>{s}</li>" for s in a["etapes"]) + "</ol>")
    for f, leg in a["formules"]:
        blocs.append(bloc_formule(f, leg))
    blocs.append(f"<h2>À savoir</h2>{a['texte']}")
    blocs.append(f"<h2>Dans Google Sheets</h2>{a['sheets']}")
    if a.get("sheets_formule"):
        blocs.append(bloc_formule(a["sheets_formule"]))
    blocs.append("<h2>Les pièges à éviter</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in a["pieges"]) + "</ul>")
    blocs.append("</article>")
    autres = [x for x in ASTUCES if x["slug"] != a["slug"]][:3]
    blocs.append(f"<section><h2>D'autres astuces</h2>{lignes_astuces(autres, p)}</section>")
    blocs.append(bloc_pack(p))
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": a["titre"], "description": a["description"],
         "inLanguage": "fr", "datePublished": a["date"], "dateModified": a["date"], "mainEntityOfPage": url,
         "author": {"@type": "Organization", "name": SITE["nom"], "url": SITE["url"] + "/"},
         "publisher": {"@type": "Organization", "name": SITE["nom"]}},
        {"@context": "https://schema.org", "@type": "HowTo", "name": a["titre"], "inLanguage": "fr",
         "step": [{"@type": "HowToStep", "position": i, "text": texte_brut(s)} for i, s in enumerate(a["etapes"], 1)]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE["url"] + "/"},
            {"@type": "ListItem", "position": 2, "name": "Astuces", "item": SITE["url"] + "/astuces/"},
            {"@type": "ListItem", "position": 3, "name": a["court"], "item": url}]},
    ]
    if a.get("video"):
        ld.append({"@context": "https://schema.org", "@type": "VideoObject", "name": a["titre"],
                   "description": a["description"], "uploadDate": a["date"],
                   "contentUrl": f"{SITE['url']}/videos/{a['video']}.mp4",
                   "thumbnailUrl": f"{SITE['url']}/videos/{a['video']}.jpg"})
    page(f"astuces/{a['slug']}/index.html", f"{a['titre']} | Tableur Malin", a["description"], "\n".join(blocs), 2,
         ld, "article")


def pack():
    modeles = "".join(f"<li><strong>{e(n)}</strong><span>{e(d)}</span></li>" for n, d in PACK_MODELES)
    if SITE["stripe_lien"]:
        achat = (f'<p class="prix">{e(SITE["pack_prix"])}, paiement unique</p>'
                 f'<p><a class="bouton" href="{e(SITE["stripe_lien"])}">Acheter le pack</a></p>'
                 '<p class="discret">Paiement sécurisé par Stripe. Les fichiers sont envoyés par e-mail après le paiement.</p>')
    else:
        achat = ('<p class="etat">Le pack est en préparation : il n\'est pas encore en vente.</p>'
                 '<p>En attendant, toutes les astuces du site sont gratuites.</p>'
                 '<p><a class="bouton" href="../astuces/index.html">Parcourir les astuces</a></p>')
    corps = f"""<section class="entete-page">
  <h1>Le pack de modèles Excel et Google Sheets</h1>
  <p class="chapo">Vingt tableaux prêts à remplir, avec les formules déjà en place, et un aide-mémoire des formules. Un seul paiement, pas d'abonnement.</p>
</section>
<section class="pack">
  <div>
    <h2>Ce que contient le pack</h2>
    <ul class="modeles">{modeles}</ul>
    <p>Chaque modèle est un fichier .xlsx avec son mode d'emploi. Il s'ouvre dans Excel et s'importe dans Google Sheets (Fichier, Importer).</p>
  </div>
  <div class="achat">{achat}</div>
</section>"""
    page("pack-modeles/index.html", "Pack de modèles Excel et Google Sheets | Tableur Malin",
         "Vingt modèles de tableaux prêts à remplir pour Excel et Google Sheets : budget, factures, planning, "
         "stock, prêt, épargne. Paiement unique.", corps, 1)


def mentions():
    manque = '<mark>à compléter avant la mise en ligne</mark>'
    corps = f"""<section class="entete-page"><h1>Mentions légales</h1></section>
<article class="fiche">
<h2>Éditeur du site</h2>
<p>{e(SITE['editeur'])}<br>SIRET : {e(SITE['siret']) or manque}<br>Adresse : {e(SITE['adresse']) or manque}<br>
Contact : <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
<h2>Hébergement</h2>
<p>GitHub Pages, service de GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<h2>Données personnelles</h2>
<p>Ce site ne dépose aucun cookie de suivi et ne collecte aucune donnée personnelle. L'hébergeur enregistre les
adresses IP des visiteurs dans ses journaux techniques. Les paiements du pack de modèles sont traités par Stripe :
aucune donnée bancaire ne transite par ce site.</p>
<h2>Marques</h2>
<p>Excel est une marque de Microsoft. Google Sheets est une marque de Google. {SITE['nom']} est un site indépendant,
sans lien avec ces sociétés.</p>
</article>"""
    page("mentions-legales/index.html", "Mentions légales | Tableur Malin",
         "Mentions légales du site Tableur Malin : éditeur, hébergeur, données personnelles.", corps, 1, index=False)


def divers():
    page("404.html", "Page introuvable | Tableur Malin", "Cette page n'existe pas.",
         f"""<section class="entete-page"><h1>Cette page n'existe pas</h1>
<p class="chapo">L'adresse est peut-être incomplète, ou la page a été déplacée.</p>
<p><a class="bouton" href="{SITE['url']}/astuces/">Voir toutes les astuces</a></p></section>""", 0, index=False)
    # La page 404 est servie depuis n'importe quel chemin : liens absolus.
    chemin = os.path.join(RACINE, "404.html")
    with open(chemin, encoding="utf-8") as f:
        d = f.read()
    d = re.sub(r'(href|src)="(?!https?:|#|mailto:)([^"]+)"', lambda m: f'{m.group(1)}="{SITE["url"]}/{m.group(2)}"', d)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(d)
    urls = ["", "astuces/", "pack-modeles/"] + [f"astuces/{a['slug']}/" for a in ASTUCES]
    dates = {f"astuces/{a['slug']}/": a["date"] for a in ASTUCES}
    dernier = max(a["date"] for a in ASTUCES)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{SITE['url']}/{u}</loc><lastmod>{dates.get(u, dernier)}</lastmod></url>" for u in urls]
    sm.append("</urlset>")
    ecrire("sitemap.xml", "\n".join(sm) + "\n")
    ecrire("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    ecrire(".nojekyll", "")


if __name__ == "__main__":
    accueil()
    liste()
    for a in ASTUCES:
        fiche(a)
    pack()
    mentions()
    divers()
    print(f"{len(ASTUCES)} astuces générées.")
