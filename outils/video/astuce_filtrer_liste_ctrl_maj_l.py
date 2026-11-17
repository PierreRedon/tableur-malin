"""Vidéo verticale « Filtrer une liste avec Ctrl + Maj + L » — Tableur Malin.

Usage : python3 astuce_filtrer_liste_ctrl_maj_l.py <dossier_polices> <sortie.mp4> [--apercu dossier]
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

F_KEY_L = titre(88, 800)
F_MENU = titre(38, 600)
F_MENU_B = titre(38, 800)

CLIENTS = ["Martin", "Bernard", "Petit", "Durand", "Moreau", "Roux"]
VILLES = ["Lyon", "Paris", "Lyon", "Nantes", "Paris", "Lyon"]
MONTANTS = [420, 380, 510, 290, 460, 350]
CHOIX = ["Lyon", "Nantes", "Paris"]          # liste du filtre, par ordre alphabétique
GARDE = "Lyon"
BLEU = (38, 98, 200)                         # numéros des lignes filtrées, comme dans Excel

X0, X1 = 60, 960          # largeur utile (les boutons des applis recouvrent le bord droit)
W_NUM, W_A, W_B, W_C = 70, 260, 240, 280
XS = [X0, X0 + W_NUM, X0 + W_NUM + W_A, X0 + W_NUM + W_A + W_B, X0 + W_NUM + W_A + W_B + W_C]
X_DROITE = XS[-1]
Y_CAP, H_CAP = 250, 290   # cellule de légende
Y_FX = 590                # barre de formule
Y0, RH = 700, 88          # tableau : ligne des lettres, ligne de titres, six clients
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




TOUCHES = ["Ctrl", "Maj", "L"]


def largeur_touches(d, police):
    pad = int(police.size * 0.55)
    return sum(d.textlength(x, font=police) + pad * 2 for x in TOUCHES) + police.size * 1.15 * (len(TOUCHES) - 1)


def touches(d, x, cy, police, enfonce=0.0, ombre=JAUNE, couleur_plus=ENCRE):
    """Ctrl + Maj + L, bord gauche en x."""
    pad = int(police.size * 0.55)
    ecart = police.size * 1.15
    for i, nom in enumerate(TOUCHES):
        w = d.textlength(nom, font=police) + pad * 2
        touche(d, x, cy, nom, police, enfonce, ombre)
        x += w
        if i < len(TOUCHES) - 1:
            wp = d.textlength("+", font=police)
            d.text((x + (ecart - wp) / 2 + police.size * 0.1, cy - police.size * 0.55), "+", font=police,
                   fill=couleur_plus)
            x += ecart


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


def bouton_xy(col):
    """Centre du bouton de filtre de la colonne col (1 = A), dans la ligne de titres."""
    return XS[col + 1] - 36, Y0 + RH + RH // 2


def bouton_filtre(d, col, k, actif=False):
    """Petit bouton à flèche dans l'en-tête. k : apparition 0 → 1. actif : un filtre est appliqué (entonnoir)."""
    if k <= 0:
        return
    cx, cy = bouton_xy(col)
    r = int(22 * (0.4 + 0.6 * k))
    d.rectangle((cx - r, cy - r, cx + r, cy + r), fill=JAUNE if actif else PAPIER, outline=VERT_NUIT, width=3)
    if actif:      # entonnoir
        d.polygon([(cx - 13, cy - 12), (cx + 13, cy - 12), (cx + 3, cy), (cx + 3, cy + 13), (cx - 3, cy + 9),
                   (cx - 3, cy)], fill=VERT_NUIT)
    else:          # triangle pointe en bas
        t = int(10 * k)
        d.polygon([(cx - t, cy - t // 2), (cx + t, cy - t // 2), (cx, cy + t - 2)], fill=VERT_NUIT)


def tableau(d, k_boutons=0.0, k_filtre=0.0):
    """k_boutons : apparition des boutons de filtre. k_filtre : repli des lignes qui ne sont pas à GARDE (0 → 1)."""
    X = XS
    hauteurs = [RH, RH] + [RH if v == GARDE else int(round(RH * (1 - k_filtre))) for v in VILLES]
    ys = [Y0]
    for h in hauteurs:
        ys.append(ys[-1] + h)
    bas = ys[-1]
    d.rectangle((X0 + 14, Y0 + 14, X_DROITE + 14, bas + 14), fill=VERT_NUIT)
    d.rectangle((X0, Y0, X_DROITE, bas), fill=PAPIER)
    d.rectangle((X0, Y0, X_DROITE, Y0 + RH), fill=ENTETE)
    d.rectangle((X0, Y0, X[1], bas), fill=ENTETE)
    for i, lettre in enumerate("ABC"):
        w = d.textlength(lettre, font=F_HEAD)
        d.text(((X[i + 1] + X[i + 2] - w) / 2, Y0 + 26), lettre, font=F_HEAD, fill=GRIS)
    for i, nom in enumerate(["Client", "Ville", "Montant"]):
        d.text((X[i + 1] + 18, ys[1] + 18), nom, font=F_CELL_B, fill=VERT_NUIT)
    w = d.textlength("1", font=F_HEAD)
    d.text((X0 + (W_NUM - w) / 2, ys[1] + 26), "1", font=F_HEAD, fill=GRIS)
    for r in range(6):
        y, h = ys[r + 2], hauteurs[r + 2]
        if h < RH * 0.75:
            continue                                  # ligne en cours de repli : on n'écrit plus son contenu
        num = str(r + 2)
        w = d.textlength(num, font=F_HEAD)
        d.text((X0 + (W_NUM - w) / 2, y + 26), num, font=F_HEAD, fill=mix(GRIS, BLEU, k_filtre))
        d.text((X[1] + 18, y + 18), CLIENTS[r], font=F_CELL, fill=ENCRE)
        garde = VILLES[r] == GARDE and k_filtre > 0
        d.text((X[2] + 18, y + 18), VILLES[r], font=F_CELL_B if garde else F_CELL,
               fill=VERT_NUIT if garde else ENCRE)
        txt = f"{MONTANTS[r]} €"
        w = d.textlength(txt, font=F_CELL)
        d.text((X[4] - 18 - w, y + 18), txt, font=F_CELL, fill=ENCRE)
    for x in X:
        d.line((x, Y0, x, bas), fill=TRAIT, width=2)
    for y in ys:
        d.line((X0, y, X_DROITE, y), fill=TRAIT, width=2)
    d.rectangle((X0, Y0, X_DROITE, bas), outline=VERT_NUIT, width=3)
    # cellule active : A1
    x1, y1, x2, y2 = X[1], ys[1], X[2], ys[2]
    d.rectangle((x1, y1, x2, y2), outline=VERT, width=8)
    d.rectangle((x2 - 13, y2 - 13, x2 + 11, y2 + 11), fill=VERT, outline=PAPIER, width=3)
    for col in (1, 2, 3):
        bouton_filtre(d, col, k_boutons, actif=(col == 2 and k_filtre > 0))


# Menu du filtre, ouvert sous l'en-tête « Ville »
MX1, MY1 = XS[2] - 30, Y0 + 2 * RH + 10
MX2 = MX1 + 520
LIGNES_MENU = ["(Sélectionner tout)"] + CHOIX
MH_LIGNE = 78
MY_OK = MY1 + 26 + MH_LIGNE * len(LIGNES_MENU) + 10
MY2 = MY_OK + 84 + 26


def case_xy(i):
    return MX1 + 52, MY1 + 26 + MH_LIGNE * i + MH_LIGNE // 2


OK_BOX = (MX2 - 190, MY_OK, MX2 - 30, MY_OK + 84)
OK_XY = ((OK_BOX[0] + OK_BOX[2]) // 2, (OK_BOX[1] + OK_BOX[3]) // 2)


def menu(d, k, coches):
    """Liste de cases à cocher du filtre. k : ouverture 0 → 1. coches : ensemble des libellés cochés."""
    if k <= 0:
        return
    y2 = MY1 + int((MY2 - MY1) * k)
    d.rectangle((MX1 + 14, MY1 + 14, MX2 + 14, y2 + 14), fill=JAUNE)
    d.rectangle((MX1, MY1, MX2, y2), fill=PAPIER, outline=VERT_NUIT, width=5)
    if k < 1:
        return
    for i, nom in enumerate(LIGNES_MENU):
        cx, cy = case_xy(i)
        coche = nom in coches
        d.rectangle((cx - 22, cy - 22, cx + 22, cy + 22), fill=VERT if coche else PAPIER, outline=VERT_NUIT, width=4)
        if coche:
            d.line([(cx - 12, cy), (cx - 3, cy + 10), (cx + 13, cy - 10)], fill=PAPIER, width=6)
        d.text((cx + 44, cy - 27), nom, font=F_MENU_B if (coche and i > 0) else F_MENU, fill=ENCRE)
    d.rectangle((OK_BOX[0] + 8, OK_BOX[1] + 8, OK_BOX[2] + 8, OK_BOX[3] + 8), fill=JAUNE)
    d.rectangle(OK_BOX, fill=VERT_NUIT)
    w = d.textlength("OK", font=F_MENU_B)
    d.text(((OK_BOX[0] + OK_BOX[2] - w) / 2, OK_BOX[1] + 16), "OK", font=F_MENU_B, fill=PAPIER)


def glisse(a, b, k):
    return tuple(a[i] + (b[i] - a[i]) * ease(k) for i in range(len(a)))


# ---------- scènes : chacune renvoie une image pour l'instant t (secondes) ----------

ACCROCHE = ["Une liste", "trop longue", "à parcourir ?"]


def s_accroche(t, tg):
    im = FOND_CLAIR.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg)
    barre_formule(d, "A1", "=ASTUCE(AUJOURDHUI())", y=470, x1=70, x2=1010)
    boite(d, (70, 590, 1010, 1060), ombre=JAUNE, decal=16, poignee=True)
    reste = int(max(0, t - 0.15) / 0.036)
    y = 640
    for i, l in enumerate(ACCROCHE):
        vis = l[: max(0, min(len(l), reste))]
        d.text((116, y), vis, font=F_HOOK, fill=VERT_NUIT)
        en_cours = 0 <= reste <= len(l) and not (reste == len(l) and i < 2)
        fini = i == 2 and reste > len(l)
        if en_cours or (fini and int(t * 3) % 2 == 0):
            w = d.textlength(vis, font=F_HOOK)
            d.rectangle((124 + w, y + 14, 132 + w, y + 112), fill=VERT)
        reste -= len(l)
        y += 124
    if t > 1.6:
        k = ease((t - 1.6) / 0.3)
        dy = int((1 - k) * 40)
        x1, y1, x2, y2 = 70, 1160 + dy, 800, 1290 + dy
        d.rectangle((x1 + 12, y1 + 12, x2 + 12, y2 + 12), fill=mix(PAPIER, JAUNE, k))
        d.rectangle((x1, y1, x2, y2), fill=mix(PAPIER, VERT_NUIT, k))
        d.text((x1 + 40, y1 + 30), "Filtrez-la en 3 touches", font=F_SUB, fill=mix(VERT_NUIT, PAPIER, k))
    return im


# Repères de la démonstration
T_CAP2, T_APPUI = 1.3, 2.3        # consigne du raccourci, puis appui
T_CAP3, T_CLIC1 = 3.5, 4.5        # clic sur la flèche de « Ville » : le menu s'ouvre
T_CAP4 = 5.2
T_CLIC2 = 5.9                     # clic sur « (Sélectionner tout) » : tout se décoche
T_CLIC3 = 6.8                     # clic sur « Lyon »
T_CLIC4 = 7.8                     # clic sur OK : le menu se ferme, les lignes se replient
T_CAP5 = 8.0
D_DEMO = 11.0


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

    if t < T_CAP2:
        legende(d, ["Voir seulement", "les clients de Lyon ?"], ease(t / 0.3))
    elif t < T_CAP3:
        legende(d, ["Appuyez sur"], ease((t - T_CAP2) / 0.3), avec_touches=appui_k(T_APPUI))
    elif t < T_CAP4:
        legende(d, ["Cliquez sur la", "flèche de Ville"], ease((t - T_CAP3) / 0.3))
    elif t < T_CAP5:
        legende(d, ["Cochez seulement", "Lyon, puis OK"], ease((t - T_CAP4) / 0.3))
    else:
        legende(d, ["Seul Lyon reste.", "Rien n'est effacé !"], ease((t - T_CAP5) / 0.3))

    barre_formule(d, "A1", "Client")
    k_filtre = ease((t - T_CLIC4 - 0.15) / 0.5) if t > T_CLIC4 else 0.0
    tableau(d, ease((t - T_APPUI - 0.05) / 0.3) if t > T_APPUI else 0.0, k_filtre)

    if t < T_CLIC2:
        coches = set(LIGNES_MENU)
    elif t < T_CLIC3:
        coches = set()
    else:
        coches = {GARDE}
    if T_CLIC1 <= t < T_CLIC4:
        menu(d, ease((t - T_CLIC1) / 0.2), coches)
    elif T_CLIC4 <= t < T_CLIC4 + 0.15:
        menu(d, 1 - (t - T_CLIC4) / 0.15 if t > T_CLIC4 else 1, coches)

    # Pointeur de souris
    depart, b = (820, 1480), bouton_xy(2)
    c0, c1 = [(a + 12, b + 10) for a, b in (case_xy(0), case_xy(1))]   # pointe juste à côté de la coche
    if t < T_CAP3:
        x, y = depart
    elif t < T_CLIC1 + 0.4:
        x, y = glisse(depart, b, (t - T_CAP3 - 0.2) / 0.6)
        onde(d, *b, (t - T_CLIC1) / 0.4)
    elif t < T_CLIC2 + 0.4:
        x, y = glisse(b, c0, (t - T_CAP4) / 0.5)
        onde(d, *c0, (t - T_CLIC2) / 0.4)
    elif t < T_CLIC3 + 0.4:
        x, y = glisse(c0, c1, (t - T_CLIC2 - 0.4) / 0.4)
        onde(d, *c1, (t - T_CLIC3) / 0.4)
    elif t < T_CLIC4 + 0.4:
        x, y = glisse(c1, OK_XY, (t - T_CLIC3 - 0.4) / 0.5)
        onde(d, *OK_XY, (t - T_CLIC4) / 0.4)
    else:
        x, y = glisse(OK_XY, (820, 1420), (t - T_CLIC4 - 0.4) / 0.7)
    fleche(d, x, y)
    return im


def s_fin(t, tg):
    im = FOND_SOMBRE.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg, sombre=True)
    k = ease(t / 0.35)
    dy = int((1 - k) * 40)
    lt = largeur_touches(d, F_KEY_L)
    touches(d, X0 + (X1 - X0 - lt) / 2, 520 + dy, F_KEY_L, 0.0, ombre=JAUNE, couleur_plus=PAPIER)
    y = 720
    for l in ["Filtrer", "une liste"]:
        w = d.textlength(l, font=F_HOOK)
        d.text(((X0 + X1 - w) / 2, y), l, font=F_HOOK, fill=mix(VERT_NUIT, PAPIER, k))
        y += 118
    note = "Excel et Google Sheets"
    w = d.textlength(note, font=F_NOTE)
    d.text(((X0 + X1 - w) / 2, y + 16), note, font=F_NOTE, fill=mix(VERT_NUIT, (190, 214, 202), k))
    if t > 0.9:
        k2 = ease((t - 0.9) / 0.3)
        yb = 1170 + int((1 - k2) * 40)
        d.text((70, yb), "À savoir", font=F_SHEETS, fill=mix(VERT_NUIT, JAUNE, k2))
        d.rectangle((82, yb + 82, 962, yb + 236), fill=mix(VERT_NUIT, JAUNE, k2))
        d.rectangle((70, yb + 70, 950, yb + 224), fill=mix(VERT_NUIT, PAPIER, k2), outline=TRAIT, width=3)
        for i, l in enumerate(["Le même raccourci retire le filtre :", "toutes les lignes reviennent."]):
            d.text((100, yb + 88 + i * 60), l, font=F_NOTE, fill=mix(VERT_NUIT, ENCRE, k2))
    return im


D_ACC = 2.9
SCENES = [(s_accroche, D_ACC), (s_demo, D_DEMO), (s_fin, 4.0)]
DUREE_TOTALE = sum(x[1] for x in SCENES)

# Bruitages : (type, instant depuis le début de la vidéo).
_D, _F = D_ACC, D_ACC + D_DEMO
SONS = ([("frappe", 0.15 + k * 0.036 * 3) for k in range(sum(len(l) for l in ACCROCHE) // 3)] + [("pop", 1.6)]
        + [("pop", _D + T_CAP2), ("touche", _D + T_APPUI), ("carillon", _D + T_APPUI + 0.1)]
        + [("clic", _D + T_CLIC1), ("pop", _D + T_CLIC1 + 0.1), ("clic", _D + T_CLIC2), ("clic", _D + T_CLIC3),
           ("clic", _D + T_CLIC4), ("carillon", _D + T_CLIC4 + 0.25), ("fin", _F)])


def apercu(dossier):
    os.makedirs(dossier, exist_ok=True)
    plans = [(s_accroche, 1.0), (s_accroche, 2.5), (s_demo, 0.8), (s_demo, 2.0), (s_demo, 2.45), (s_demo, 3.2),
             (s_demo, 4.4), (s_demo, 5.0), (s_demo, 6.3), (s_demo, 7.3), (s_demo, 7.85), (s_demo, 8.1),
             (s_demo, 9.5), (s_fin, 0.5), (s_fin, 3.0)]
    debuts = {s_accroche: 0.0, s_demo: D_ACC, s_fin: D_ACC + D_DEMO}
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
