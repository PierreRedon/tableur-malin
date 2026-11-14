"""Vidéo verticale « La date du jour en deux touches (Ctrl + ;) » — Tableur Malin.

Usage : python3 astuce_date_du_jour_ctrl_point_virgule.py <dossier_polices> <sortie.mp4> [--apercu dossier]
Même langage visuel que astuce_ctrl_e.py (papier quadrillé, cellule active verte, barre de formule,
ombres franches jaunes). Chaque image est dessinée avec Pillow et envoyée à ffmpeg.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

from son import bande_son

W, H, FPS = 1080, 1920, 30
VERT_NUIT = (15, 61, 46)
VERT = (30, 142, 90)
JAUNE = (255, 216, 77)
PAPIER = (255, 255, 255)
GRILLE = (225, 233, 227)
TRAIT = (195, 207, 199)
ENTETE = (238, 243, 239)
ENCRE = (27, 36, 32)
GRIS = (88, 106, 97)

POLICES = sys.argv[1]
SORTIE = sys.argv[2]


def titre(taille, graisse=800):
    f = ImageFont.truetype(os.path.join(POLICES, "bricolage.ttf"), taille)
    f.set_variation_by_axes([graisse])
    return f


def mono(taille, gras=False):
    return ImageFont.truetype(os.path.join(POLICES, "mono700.ttf" if gras else "mono400.ttf"), taille)


F_CAPTION = titre(78)
F_HOOK = titre(104)
F_SUB = titre(56, 700)
F_MARQUE = titre(42, 800)
F_CELL = titre(40, 500)
F_CELL_B = titre(40, 750)
F_HEAD = titre(30, 600)
F_KEY = titre(60, 750)
F_KEY_XL = titre(150, 800)
F_MONO = mono(40, True)
F_MONO_L = mono(40)
F_NOTE = titre(42, 500)
F_SHEETS = titre(44, 700)


COMMANDES = ["Imprimante", "Cartouches", "Papier A4", "Classeurs", "Stylos", "Agrafeuse"]
DATES = ["09/11/2026", "10/11/2026", "12/11/2026", None, None, None]   # B5 sera remplie par le raccourci
DATE_JOUR = "14/11/2026"

X0, X1 = 60, 960          # largeur utile (les boutons des applis recouvrent le bord droit)
COLS = [70, 400, 390]     # le tableau s'arrête à x = 920
XS = [X0]
for c in COLS:
    XS.append(XS[-1] + c)
Y_CAP, H_CAP = 250, 290   # cellule de légende
Y_FX = 590                # barre de formule
Y0, RH = 710, 96          # tableau
DUREE_TOTALE = 0.0        # renseignée plus bas (barre de progression)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def mix(a, b, k):
    k = max(0.0, min(1.0, k))
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def fond(sombre=False):
    base = VERT_NUIT if sombre else PAPIER
    ligne = mix(VERT_NUIT, PAPIER, 0.09) if sombre else GRILLE
    im = Image.new("RGB", (W, H), base)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 60):
        d.line((x, 0, x, H), fill=ligne, width=2)
    for y in range(0, H, 60):
        d.line((0, y, W, y), fill=ligne, width=2)
    return im


FOND_CLAIR, FOND_SOMBRE = fond(False), fond(True)


def entete(d, t_global, sombre=False):
    """Bandeau de marque + barre de progression, comme l'en-tête du site."""
    c = PAPIER if sombre else VERT_NUIT
    if not sombre:
        d.rectangle((0, 0, W, 186), fill=PAPIER)
    d.rectangle((60, 96, 100, 136), outline=JAUNE if sombre else VERT, width=6)
    d.rectangle((92, 128, 108, 144), fill=JAUNE if sombre else VERT, outline=VERT_NUIT if sombre else PAPIER, width=3)
    d.text((126, 88), "Tableur Malin", font=F_MARQUE, fill=c)
    d.rectangle((0, 186, W, 192), fill=mix(VERT_NUIT, PAPIER, 0.25) if sombre else VERT_NUIT)
    if DUREE_TOTALE:
        d.rectangle((0, 186, int(W * t_global / DUREE_TOTALE), 192), fill=JAUNE)


def boite(d, box, fond_=PAPIER, bord=VERT, epaisseur=8, ombre=None, decal=12, poignee=False):
    x1, y1, x2, y2 = box
    if ombre:
        d.rectangle((x1 + decal, y1 + decal, x2 + decal, y2 + decal), fill=ombre)
    d.rectangle(box, fill=fond_, outline=bord, width=epaisseur)
    if poignee:
        d.rectangle((x2 - 14, y2 - 14, x2 + 12, y2 + 12), fill=bord, outline=PAPIER, width=4)


def barre_formule(d, ref, contenu, y=Y_FX, x1=X0, x2=X1, curseur=False):
    d.rectangle((x1, y, x2, y + 84), fill=PAPIER, outline=TRAIT, width=3)
    d.text((x1 + 24, y + 18), ref, font=F_MONO_L, fill=GRIS)
    d.line((x1 + 110, y + 14, x1 + 110, y + 70), fill=TRAIT, width=3)
    d.text((x1 + 134, y + 18), "fx", font=F_MONO, fill=VERT)
    d.text((x1 + 210, y + 18), contenu, font=F_MONO, fill=ENCRE)
    if curseur:
        w = d.textlength(contenu, font=F_MONO)
        d.rectangle((x1 + 214 + w, y + 18, x1 + 218 + w, y + 66), fill=ENCRE)



def touche(d, x, cy, texte, police, enfonce=0.0, ombre=JAUNE):
    """Dessine une touche dont le bord gauche est en x ; enfonce : 0 → 1."""
    pad = int(police.size * 0.55)
    w = d.textlength(texte, font=police)
    bw, bh = w + pad * 2, police.size * 1.75
    dec = int(police.size * 0.2)
    k = int(dec * enfonce)
    y1 = cy - bh / 2
    d.rounded_rectangle((x + dec, y1 + dec, x + bw + dec, y1 + bh + dec), 16, fill=ombre)
    d.rounded_rectangle((x + k, y1 + k, x + bw + k, y1 + bh + k), 16,
                        fill=mix(PAPIER, JAUNE, enfonce), outline=ENCRE, width=5)
    d.text((x + k + pad, y1 + k + (bh - police.size) / 2 - police.size * 0.13), texte, font=police, fill=ENCRE)


def touches(d, x, cy, police, enfonce=0.0, ombre=JAUNE, couleur_plus=ENCRE, centre=False, noms=("Ctrl", ";")):
    pad = int(police.size * 0.55)
    w1 = d.textlength(noms[0], font=police) + pad * 2
    w2 = d.textlength(noms[1], font=police) + pad * 2
    ecart = police.size * 1.15
    if centre:
        x = (W - (w1 + ecart + w2)) / 2
    touche(d, x, cy, noms[0], police, enfonce, ombre)
    wp = d.textlength("+", font=police)
    d.text((x + w1 + (ecart - wp) / 2 + police.size * 0.1, cy - police.size * 0.55), "+", font=police, fill=couleur_plus)
    touche(d, x + w1 + ecart, cy, noms[1], police, enfonce, ombre)


def legende(d, lignes, k, avec_touches=None):
    """Cellule active contenant la consigne. k : apparition 0 → 1. avec_touches : enfoncement ou None."""
    boite(d, (X0, Y_CAP, X1, Y_CAP + H_CAP), ombre=JAUNE, decal=14, poignee=True)
    dy = int((1 - k) * 26)
    c = mix(PAPIER, VERT_NUIT, k)
    y = Y_CAP + 46 + dy
    if avec_touches is None:
        for l in lignes:
            d.text((X0 + 44, y), l, font=F_CAPTION, fill=c)
            y += 96
    else:
        d.text((X0 + 44, y), lignes[0], font=F_CAPTION, fill=c)
        if k > 0.5:
            touches(d, X0 + 48, Y_CAP + 196 + dy, F_KEY, avec_touches)


def cellule(col, ligne):
    """Rectangle de la cellule (col 1..2 = A..B, ligne 1..7 comme dans le tableur)."""
    return XS[col], Y0 + RH * ligne, XS[col + 1], Y0 + RH * (ligne + 1)


def fleche(d, x, y):
    """Pointeur de souris classique, pointe en (x, y)."""
    pts = [(0, 0), (0, 58), (15, 44), (26, 68), (38, 62), (27, 39), (46, 39)]
    d.polygon([(x + a + 5, y + b + 5) for a, b in pts], fill=(120, 130, 124))
    d.polygon([(x + a, y + b) for a, b in pts], fill=PAPIER, outline=ENCRE)
    d.line([(x + a, y + b) for a, b in pts] + [(x, y)], fill=ENCRE, width=4)


def onde(d, x, y, k):
    """Cercle qui s'élargit à l'endroit du clic. k : 0 → 1."""
    if 0 < k < 1:
        r = 18 + 60 * ease(k)
        d.ellipse((x - r, y - r, x + r, y + r), outline=mix(VERT_NUIT, PAPIER, k * 0.7), width=7)


def tableau(d, sel, saisie=False, date_k=0.0, flash=0.0, curseur=False):
    """sel : rectangle de sélection. saisie : la date est en cours de saisie en B5 (alignée à gauche).
    date_k : apparition (0→1) de la date validée en B5. flash : surlignage jaune de B5 (0→1)."""
    bas = Y0 + RH * 8
    d.rectangle((X0 + 14, Y0 + 14, XS[3] + 14, bas + 14), fill=VERT_NUIT)
    d.rectangle((X0, Y0, XS[3], bas), fill=PAPIER)
    d.rectangle((X0, Y0, XS[3], Y0 + RH), fill=ENTETE)
    d.rectangle((X0, Y0, XS[1], bas), fill=ENTETE)
    if flash > 0:
        d.rectangle(cellule(2, 5), fill=mix(PAPIER, JAUNE, flash))
    for i, lettre in enumerate("AB"):
        w = d.textlength(lettre, font=F_HEAD)
        d.text(((XS[i + 1] + XS[i + 2] - w) / 2, Y0 + 30), lettre, font=F_HEAD, fill=GRIS)
    for r in range(1, 8):
        w = d.textlength(str(r), font=F_HEAD)
        d.text((X0 + (COLS[0] - w) / 2, Y0 + RH * r + 30), str(r), font=F_HEAD, fill=GRIS)
    for x in XS:
        d.line((x, Y0, x, bas), fill=TRAIT, width=2)
    for r in range(9):
        d.line((X0, Y0 + RH * r, XS[3], Y0 + RH * r), fill=TRAIT, width=2)
    d.rectangle((X0, Y0, XS[3], bas), outline=VERT_NUIT, width=3)

    def a_droite(ligne, txt, police, couleur):
        w = d.textlength(txt, font=police)
        d.text((XS[3] - 18 - w, Y0 + RH * ligne + 22), txt, font=police, fill=couleur)

    d.text((XS[1] + 18, Y0 + RH + 22), "Commande", font=F_CELL_B, fill=VERT_NUIT)
    a_droite(1, "Reçue le", F_CELL_B, VERT_NUIT)
    for r, commande in enumerate(COMMANDES):
        d.text((XS[1] + 18, Y0 + RH * (r + 2) + 22), commande, font=F_CELL, fill=ENCRE)
        if DATES[r]:
            a_droite(r + 2, DATES[r], F_CELL, ENCRE)
    if saisie:
        d.text((XS[2] + 18, Y0 + RH * 5 + 22), DATE_JOUR, font=F_CELL, fill=ENCRE)
        if curseur:
            w = d.textlength(DATE_JOUR, font=F_CELL)
            d.rectangle((XS[2] + 22 + w, Y0 + RH * 5 + 22, XS[2] + 26 + w, Y0 + RH * 5 + 72), fill=ENCRE)
    elif date_k > 0:
        fond_c = mix(PAPIER, JAUNE, flash)
        a_droite(5, DATE_JOUR, F_CELL_B, mix(fond_c, VERT_NUIT, date_k))
    x1, y1, x2, y2 = sel
    d.rectangle((x1, y1, x2, y2), outline=VERT, width=8)
    d.rectangle((x2 - 13, y2 - 13, x2 + 11, y2 + 11), fill=VERT, outline=PAPIER, width=3)


def glisse(a, b, k):
    return tuple(a[i] + (b[i] - a[i]) * ease(k) for i in range(len(a)))


# ---------- scènes : chacune renvoie une image pour l'instant t (secondes) ----------

def s_accroche(t, tg):
    im = FOND_CLAIR.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg)
    barre_formule(d, "A1", "=ASTUCE(AUJOURDHUI())", y=470, x1=70, x2=1010)
    boite(d, (70, 590, 1010, 1060), ombre=JAUNE, decal=16, poignee=True)
    lignes = ["Vous tapez", "la date du jour", "à la main ?"]
    reste = int(max(0, t - 0.15) / 0.028)
    y = 640
    for i, l in enumerate(lignes):
        vis = l[: max(0, min(len(l), reste))]
        d.text((116, y), vis, font=F_HOOK, fill=VERT_NUIT)
        en_cours = 0 <= reste <= len(l) and not (reste == len(l) and i < 2)
        fini = i == 2 and reste > len(l)
        if en_cours or (fini and int(t * 3) % 2 == 0):
            w = d.textlength(vis, font=F_HOOK)
            d.rectangle((124 + w, y + 14, 132 + w, y + 112), fill=VERT)
        reste -= len(l)
        y += 124
    if t > 1.5:
        k = ease((t - 1.5) / 0.3)
        dy = int((1 - k) * 40)
        x1, y1, x2, y2 = 70, 1160 + dy, 830, 1290 + dy
        d.rectangle((x1 + 12, y1 + 12, x2 + 12, y2 + 12), fill=mix(PAPIER, JAUNE, k))
        d.rectangle((x1, y1, x2, y2), fill=mix(PAPIER, VERT_NUIT, k))
        d.text((x1 + 40, y1 + 30), "Deux touches suffisent", font=F_SUB, fill=mix(VERT_NUIT, PAPIER, k))
    return im


# Repères de la démonstration
T_CLIC, T_CAP2, T_APPUI = 1.0, 2.1, 3.1
T_CAP3, T_ENTREE = 4.6, 5.4
T_CAP4, T_CLIC2 = 6.8, 8.0
D_DEMO = 9.8
CENTRE_B5 = (XS[2] + 90, Y0 + RH * 5 + 52)
REPOS = (XS[2] + 120, Y0 + RH * 8 + 110)


def s_demo(t, tg):
    im = FOND_CLAIR.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg)

    def appui_k(a):
        if a <= t < a + 0.12:
            return (t - a) / 0.12
        if a + 0.12 <= t < a + 0.4:
            return 1.0
        if a + 0.4 <= t < a + 0.55:
            return 1 - (t - a - 0.4) / 0.15
        return 0.0

    saisie = T_APPUI + 0.1 <= t < T_ENTREE
    date_k = ease((t - T_ENTREE) / 0.2) if t >= T_ENTREE else 0.0

    # Sélection et barre de formule
    if t < T_CLIC:
        sel, ref, contenu = cellule(2, 2), "B2", DATES[0]
    elif t < T_ENTREE:
        sel, ref = glisse(cellule(2, 2), cellule(2, 5), (t - T_CLIC) / 0.25), "B5"
        contenu = DATE_JOUR if saisie else ""
    elif t < T_CLIC2:
        sel, ref, contenu = glisse(cellule(2, 5), cellule(2, 6), (t - T_ENTREE) / 0.2), "B6", ""
    else:
        sel, ref, contenu = glisse(cellule(2, 6), cellule(2, 5), (t - T_CLIC2) / 0.2), "B5", DATE_JOUR

    flash = 0.0
    if T_ENTREE < t < T_ENTREE + 1.3:
        flash = 1 - ease((t - T_ENTREE - 0.4) / 0.9)

    if t < T_CAP2:
        legende(d, ["Cliquez dans", "la cellule"], ease(t / 0.3))
    elif t < T_CAP3:
        legende(d, ["Appuyez sur"], ease((t - T_CAP2) / 0.3), avec_touches=appui_k(T_APPUI))
    elif t < T_CAP4:
        legende(d, ["Validez avec", "Entrée"], ease((t - T_CAP3) / 0.3))
    else:
        legende(d, ["Une date fixe,", "sans formule"], ease((t - T_CAP4) / 0.3))

    barre_formule(d, ref, contenu, curseur=saisie and int(t * 4) % 2 == 0)
    tableau(d, sel, saisie, date_k, flash, curseur=saisie and int(t * 4) % 2 == 0)

    # Pointeur de souris
    depart = (820, 1560)
    if t < T_CAP2 + 0.2:
        x, y = glisse(depart, CENTRE_B5, (t - 0.3) / 0.6)
        onde(d, CENTRE_B5[0], CENTRE_B5[1], (t - T_CLIC) / 0.4)
        fleche(d, x, y)
    elif t < T_CAP4 + 0.4:
        x, y = glisse(CENTRE_B5, REPOS, (t - T_CAP2 - 0.2) / 0.6)
        fleche(d, x, y)
    else:
        x, y = glisse(REPOS, CENTRE_B5, (t - T_CAP4 - 0.4) / 0.6)
        onde(d, CENTRE_B5[0], CENTRE_B5[1], (t - T_CLIC2) / 0.4)
        fleche(d, x, y)
    return im


def s_fin(t, tg):
    im = FOND_SOMBRE.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg, sombre=True)
    k = ease(t / 0.35)
    dy = int((1 - k) * 40)
    touches(d, 0, 560 + dy, F_KEY_XL, 0.0, ombre=JAUNE, couleur_plus=PAPIER, centre=True)
    y = 800
    for l in ["La date du jour", "en deux touches"]:
        w = d.textlength(l, font=F_HOOK)
        d.text(((W - w) / 2, y), l, font=F_HOOK, fill=mix(VERT_NUIT, PAPIER, k))
        y += 118
    note = "Excel et Google Sheets"
    w = d.textlength(note, font=F_NOTE)
    d.text(((W - w) / 2, y + 16), note, font=F_NOTE, fill=mix(VERT_NUIT, (190, 214, 202), k))
    if t > 0.9:
        k2 = ease((t - 0.9) / 0.3)
        yb = 1200 + int((1 - k2) * 40)
        d.text((90, yb), "À savoir", font=F_SHEETS, fill=mix(VERT_NUIT, JAUNE, k2))
        d.rectangle((102, yb + 82, 1002, yb + 236), fill=mix(VERT_NUIT, JAUNE, k2))
        d.rectangle((90, yb + 70, 990, yb + 224), fill=mix(VERT_NUIT, PAPIER, k2), outline=TRAIT, width=3)
        for i, l in enumerate(["Cette date ne changera plus.", "=AUJOURDHUI() change chaque jour."]):
            d.text((120, yb + 88 + i * 60), l, font=F_NOTE, fill=mix(VERT_NUIT, ENCRE, k2))
    return im


SCENES = [(s_accroche, 2.8), (s_demo, D_DEMO), (s_fin, 4.0)]
DUREE_TOTALE = sum(x[1] for x in SCENES)

# Bruitages : (type, instant depuis le début de la vidéo). La démonstration commence à 2,8 s.
_D, _F = 2.8, 2.8 + D_DEMO
SONS = ([("frappe", 0.15 + k * 0.085) for k in range(12)] + [("pop", 1.5)]
        + [("clic", _D + T_CLIC), ("touche", _D + T_APPUI), ("carillon", _D + T_APPUI + 0.1),
           ("touche", _D + T_ENTREE), ("carillon", _D + T_ENTREE + 0.05), ("clic", _D + T_CLIC2), ("fin", _F)])


def apercu(dossier):
    os.makedirs(dossier, exist_ok=True)
    plans = [(s_accroche, 2.3), (s_demo, 0.6), (s_demo, 1.6), (s_demo, 2.8), (s_demo, 3.3), (s_demo, 4.2),
             (s_demo, 5.2), (s_demo, 5.9), (s_demo, 7.6), (s_demo, 9.0), (s_fin, 3.0)]
    debuts = {s_accroche: 0.0, s_demo: 2.8, s_fin: 2.8 + D_DEMO}
    for i, (fn, t) in enumerate(plans, 1):
        fn(t, debuts[fn] + t).save(os.path.join(dossier, f"apercu_{i:02d}.png"))


def rendre():
    tmp = tempfile.mkdtemp()
    fichiers, ecoule = [], 0.0
    for i, (fn, duree) in enumerate(SCENES):
        part, final = os.path.join(tmp, f"s{i}.part.mp4"), os.path.join(tmp, f"s{i}.mp4")
        p = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-r", str(FPS), part], stdin=subprocess.PIPE)
        for n in range(int(round(duree * FPS))):
            p.stdin.write(fn(n / FPS, ecoule + n / FPS).tobytes())
        p.stdin.close()
        if p.wait() != 0:
            raise SystemExit(f"ffmpeg a échoué sur la scène {i}")
        os.rename(part, final)
        fichiers.append(final)
        ecoule += duree
    liste = os.path.join(tmp, "liste.txt")
    with open(liste, "w") as f:
        f.writelines(f"file '{x}'\n" for x in fichiers)
    muet = os.path.join(tmp, "muet.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", liste,
                    "-c", "copy", muet], check=True)
    # Bande-son : fond musical et bruitages synthétiques (son.py), calés sur la liste SONS.
    wav = os.path.join(tmp, "son.wav")
    bande_son(wav, DUREE_TOTALE, SONS)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", muet, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-17:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac",
                    "-b:a", "128k", "-shortest", "-movflags", "+faststart", SORTIE], check=True)


if __name__ == "__main__":
    if "--apercu" in sys.argv:
        apercu(sys.argv[sys.argv.index("--apercu") + 1])
    else:
        rendre()
