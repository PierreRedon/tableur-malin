"""Vidéo verticale « Des ##### ? Ajuster la largeur de colonne d'un double-clic » — Tableur Malin.

Usage : python3 astuce_ajuster_largeur_colonne_double_clic.py <dossier_polices> <sortie.mp4> [--apercu dossier]
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


PRODUITS = ["Ordinateur", "Écran", "Imprimante", "Bureau", "Fauteuil", "Tablette"]
PRIX = ["1 249,00 €", "389,90 €", "215,50 €", "1 480,00 €", "329,00 €", "649,99 €"]
SAISIE_B2 = "1249"          # ce que contient réellement B2 (le format monétaire ajoute le reste)

X0, X1 = 60, 960          # largeur utile (les boutons des applis recouvrent le bord droit)
X_DROITE = 920            # le tableau s'arrête à x = 920 ; la colonne C est coupée par le bord, comme à l'écran
W_NUM, W_A = 70, 330
W_ETROIT = 120            # largeur de la colonne B au départ : aucun prix n'y tient
_mesure = ImageDraw.Draw(Image.new("RGB", (10, 10)))
W_LARGE = int(max(_mesure.textlength(p, font=F_CELL_B) for p in PRIX)) + 44   # largeur ajustée au contenu
Y_CAP, H_CAP = 250, 290   # cellule de légende
Y_FX = 590                # barre de formule
Y0, RH = 710, 96          # tableau
DUREE_TOTALE = 0.0        # renseignée plus bas (barre de progression)


def xs(wb):
    """Abscisses des traits verticaux pour une colonne B de largeur wb."""
    a = X0 + W_NUM
    return [X0, a, a + W_A, a + W_A + wb, X_DROITE]


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




def legende(d, lignes, k):
    """Cellule active contenant la consigne. k : apparition 0 → 1."""
    boite(d, (X0, Y_CAP, X1, Y_CAP + H_CAP), ombre=JAUNE, decal=14, poignee=True)
    dy = int((1 - k) * 26)
    c = mix(PAPIER, VERT_NUIT, k)
    y = Y_CAP + 46 + dy
    for l in lignes:
        d.text((X0 + 44, y), l, font=F_CAPTION, fill=c)
        y += 96


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



def double_fleche(d, x, y, echelle=1.0, clair=PAPIER, fonce=ENCRE):
    """Pointeur de redimensionnement : un trait vertical et deux flèches, centré en (x, y)."""
    e = echelle

    def forme(g, couleur):
        d.rectangle((x - 4 * e - g, y - 30 * e - g, x + 4 * e + g, y + 30 * e + g), fill=couleur)
        d.rectangle((x - 34 * e - g, y - 4 * e - g, x + 34 * e + g, y + 4 * e + g), fill=couleur)
        for s in (-1, 1):
            d.polygon([(x + s * (48 * e + g * 1.6), y), (x + s * (28 * e - g), y - 17 * e - g * 1.4),
                       (x + s * (28 * e - g), y + 17 * e + g * 1.4)], fill=couleur)

    forme(5 * e, clair)
    forme(0, fonce)


def tableau(d, wb, sel, flash=0.0, halo=0.0):
    """wb : largeur de la colonne B. sel : (colonne, ligne) de la cellule sélectionnée.
    flash : surlignage jaune des prix (0→1). halo : mise en avant du trait entre B et C (0→1)."""
    X = xs(wb)
    bas = Y0 + RH * 8
    d.rectangle((X0 + 14, Y0 + 14, X_DROITE + 14, bas + 14), fill=VERT_NUIT)
    d.rectangle((X0, Y0, X_DROITE, bas), fill=PAPIER)
    d.rectangle((X0, Y0, X_DROITE, Y0 + RH), fill=ENTETE)
    d.rectangle((X0, Y0, X[1], bas), fill=ENTETE)
    d.rectangle((X[2], Y0, X[3], Y0 + RH), fill=mix(ENTETE, VERT, 0.22))        # en-tête de la colonne concernée
    if flash > 0:
        d.rectangle((X[2], Y0 + RH * 2, X[3], bas), fill=mix(PAPIER, JAUNE, flash))
    for i, lettre in enumerate("ABC"):
        w = d.textlength(lettre, font=F_HEAD)
        d.text(((X[i + 1] + X[i + 2] - w) / 2, Y0 + 30), lettre, font=F_HEAD, fill=VERT_NUIT if i == 1 else GRIS)
    for r in range(1, 8):
        w = d.textlength(str(r), font=F_HEAD)
        d.text((X0 + (W_NUM - w) / 2, Y0 + RH * r + 30), str(r), font=F_HEAD, fill=GRIS)
    for x in X:
        d.line((x, Y0, x, bas), fill=TRAIT, width=2)
    for r in range(9):
        d.line((X0, Y0 + RH * r, X_DROITE, Y0 + RH * r), fill=TRAIT, width=2)
    d.rectangle((X0, Y0, X_DROITE, bas), outline=VERT_NUIT, width=3)

    d.text((X[1] + 18, Y0 + RH + 22), "Produit", font=F_CELL_B, fill=VERT_NUIT)
    w = d.textlength("Prix", font=F_CELL_B)
    d.text((X[3] - 18 - w, Y0 + RH + 22), "Prix", font=F_CELL_B, fill=VERT_NUIT)
    w_diese = d.textlength("#", font=F_CELL)
    for r, produit in enumerate(PRODUITS):
        y = Y0 + RH * (r + 2) + 22
        d.text((X[1] + 18, y), produit, font=F_CELL, fill=ENCRE)
        police = F_CELL_B if flash > 0 or wb >= W_LARGE else F_CELL
        w = d.textlength(PRIX[r], font=police)
        if w + 30 <= wb:                       # le prix tient dans la colonne : il s'affiche
            d.text((X[3] - 18 - w, y), PRIX[r], font=police, fill=VERT_NUIT if police is F_CELL_B else ENCRE)
        else:                                  # sinon le tableur remplit la cellule de dièses
            n = max(1, int((wb - 14) // w_diese))
            d.text((X[2] + 8, y), "#" * n, font=F_CELL, fill=ENCRE)
    if halo > 0:
        e = int(5 + 5 * halo)
        d.rectangle((X[3] - e, Y0 + 3, X[3] + e, Y0 + RH - 2), fill=JAUNE, outline=VERT_NUIT, width=3)
    col, ligne = sel
    x1, y1, x2, y2 = X[col], Y0 + RH * ligne, X[col + 1], Y0 + RH * (ligne + 1)
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
    lignes = ["Des #####", "dans vos", "cellules ?"]
    reste = int(max(0, t - 0.15) / 0.036)
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
        d.text((x1 + 40, y1 + 30), "Rien n'est perdu", font=F_SUB, fill=mix(VERT_NUIT, PAPIER, k))
    return im


# Repères de la démonstration
T_CLIC, T_CAP2, T_VISE = 1.0, 2.6, 3.0
T_CAP3, T_DBL1, T_DBL2 = 5.0, 5.8, 6.02
T_ELARGIT, D_ELARGIT = 6.08, 0.4
T_CAP4, T_PART = 7.6, 7.2
D_DEMO = 10.0
Y_ENTETE = Y0 + RH // 2
CENTRE_B2 = (xs(W_ETROIT)[2] + 62, Y0 + RH * 2 + 52)
REPOS = (700, Y0 + RH * 8 + 120)


def s_demo(t, tg):
    im = FOND_CLAIR.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg)

    wb = W_ETROIT + (W_LARGE - W_ETROIT) * ease((t - T_ELARGIT) / D_ELARGIT) if t >= T_ELARGIT else W_ETROIT
    wb = int(round(wb))
    bord = (xs(wb)[3], Y_ENTETE)

    if t < T_CLIC:
        sel, ref, contenu = (1, 1), "A1", "Produit"
    else:
        sel, ref, contenu = (2, 2), "B2", SAISIE_B2

    flash = 0.0
    if T_ELARGIT + D_ELARGIT * 0.6 < t < T_ELARGIT + 2.0:
        flash = 1 - ease((t - T_ELARGIT - 0.8) / 1.2)
    halo = 0.0
    if T_VISE + 0.6 <= t < T_DBL2:
        halo = 0.5 + 0.5 * abs(((t - T_VISE - 0.6) * 2.2) % 2 - 1)

    if t < T_CAP2:
        legende(d, ["La colonne est", "trop étroite"], ease(t / 0.3))
    elif t < T_CAP3:
        legende(d, ["Visez le trait", "à droite du B"], ease((t - T_CAP2) / 0.3))
    elif t < T_CAP4:
        legende(d, ["Double-cliquez", "dessus"], ease((t - T_CAP3) / 0.3))
    else:
        legende(d, ["La colonne s'ajuste", "au contenu"], ease((t - T_CAP4) / 0.3))

    barre_formule(d, ref, contenu)
    tableau(d, wb, sel, flash, halo)

    # Pointeur de souris
    depart = (820, 1560)
    if t < T_VISE:
        x, y = glisse(depart, CENTRE_B2, (t - 0.3) / 0.6)
        onde(d, CENTRE_B2[0], CENTRE_B2[1], (t - T_CLIC) / 0.4)
        fleche(d, x, y)
    elif t < T_PART:
        k = (t - T_VISE) / 0.6
        x, y = glisse(CENTRE_B2, bord, k)
        onde(d, bord[0], bord[1], (t - T_DBL1) / 0.35)
        onde(d, bord[0], bord[1], (t - T_DBL2) / 0.35)
        if k >= 0.85:
            double_fleche(d, x, y, 0.8)
        else:
            fleche(d, x, y)
    else:
        x, y = glisse(bord, REPOS, (t - T_PART) / 0.7)
        fleche(d, x, y)
    return im


def s_fin(t, tg):
    im = FOND_SOMBRE.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg, sombre=True)
    k = ease(t / 0.35)
    dy = int((1 - k) * 40)
    # Une rangée d'en-têtes de colonnes en grand, avec le pointeur sur le trait entre B et C
    x1, y1, x2, y2 = 200, 430 + dy, 880, 590 + dy
    d.rectangle((x1 + 16, y1 + 16, x2 + 16, y2 + 16), fill=JAUNE)
    d.rectangle((x1, y1, x2, y2), fill=ENTETE, outline=PAPIER, width=6)
    traits = [x1 + 110, x1 + 400]
    for x in traits:
        d.line((x, y1, x, y2), fill=TRAIT, width=5)
    for lettre, xa, xb in (("A", x1, traits[0]), ("B", traits[0], traits[1]), ("C", traits[1], x2)):
        w = d.textlength(lettre, font=F_KEY)
        d.text(((xa + xb - w) / 2, y1 + 44), lettre, font=F_KEY, fill=VERT_NUIT if lettre == "B" else GRIS)
    cy = (y1 + y2) // 2
    d.ellipse((traits[1] - 92, cy - 92, traits[1] + 92, cy + 92), fill=JAUNE, outline=PAPIER, width=5)
    double_fleche(d, traits[1], cy, 1.5, clair=PAPIER, fonce=VERT_NUIT)
    y = 760
    for l in ["Double-clic", "sur ce trait"]:
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
        for i, l in enumerate(["Sélectionnez plusieurs colonnes :", "un double-clic les ajuste toutes."]):
            d.text((120, yb + 88 + i * 60), l, font=F_NOTE, fill=mix(VERT_NUIT, ENCRE, k2))
    return im


SCENES = [(s_accroche, 2.8), (s_demo, D_DEMO), (s_fin, 4.0)]
DUREE_TOTALE = sum(x[1] for x in SCENES)

# Bruitages : (type, instant depuis le début de la vidéo). La démonstration commence à 2,8 s.
_D, _F = 2.8, 2.8 + D_DEMO
SONS = ([("frappe", 0.15 + k * 0.085) for k in range(12)] + [("pop", 1.5)]
        + [("clic", _D + T_CLIC), ("pop", _D + T_VISE + 0.6), ("clic", _D + T_DBL1), ("clic", _D + T_DBL2),
           ("carillon", _D + T_ELARGIT + D_ELARGIT * 0.6), ("fin", _F)])


def apercu(dossier):
    os.makedirs(dossier, exist_ok=True)
    plans = [(s_accroche, 2.3), (s_demo, 0.6), (s_demo, 1.6), (s_demo, 3.3), (s_demo, 4.3), (s_demo, 5.9),
             (s_demo, 6.25), (s_demo, 6.9), (s_demo, 8.4), (s_demo, 9.6), (s_fin, 3.0)]
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
