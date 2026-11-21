"""Vidéo verticale « Transformer une liste en tableau avec Ctrl + T » — Tableur Malin.

Usage : python3 astuce_liste_en_tableau_ctrl_t.py <dossier_polices> <sortie.mp4> [--apercu dossier]
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
F_FIN = titre(92)
F_MENU = titre(38, 600)
F_MENU_B = titre(38, 800)


X0, X1 = 60, 960          # largeur utile (les boutons des applis recouvrent le bord droit)
W_NUM, W_A, W_B, W_C = 70, 260, 240, 280
XS = [X0, X0 + W_NUM, X0 + W_NUM + W_A, X0 + W_NUM + W_A + W_B, X0 + W_NUM + W_A + W_B + W_C]
X_DROITE = XS[-1]
Y_CAP, H_CAP = 250, 290   # cellule de légende
Y_FX = 590                # barre de formule
Y0, RH = 700, 88          # tableau : ligne des lettres, ligne de titres, six factures
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
    xs = x1 + 150                       # séparateur placé pour une référence de quatre caractères (A250)
    d.line((xs, y + 14, xs, y + 70), fill=TRAIT, width=3)
    d.text((xs + 24, y + 18), "fx", font=F_MONO, fill=VERT)
    d.text((xs + 100, y + 18), contenu, font=F_MONO, fill=ENCRE)
    if curseur:
        w = d.textlength(contenu, font=F_MONO)
        d.rectangle((xs + 104 + w, y + 18, xs + 108 + w, y + 66), fill=ENCRE)


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



# ---------- données : une liste de ventes toute simple, à transformer en tableau ----------
LIGNES = [("Produit", "Ville", "Ventes"),
          ("Stylos", "Lyon", "480 €"), ("Cahiers", "Paris", "1 250 €"), ("Classeurs", "Nantes", "320 €"),
          ("Agendas", "Lille", "760 €"), ("Trousses", "Lyon", "540 €"), ("Carnets", "Paris", "910 €")]
NV = len(LIGNES)          # lignes visibles sous la ligne des lettres (1 = titres)
BANDE = mix(PAPIER, VERT, 0.14)
CLIC_COL, CLIC_LIG = 2, 3  # cellule B3, où l'on clique avant le raccourci
PLAGE = "=$A$1:$C$7"
F_DLG_T = titre(40, 800)
F_DLG = titre(35, 600)


def y_ligne(r):
    return Y0 + RH * r


def touches(d, x, cy, police, noms, enfonce=0.0, ombre=JAUNE, couleur_plus=ENCRE):
    """Suite de touches séparées par des +, bord gauche en x."""
    pad = int(police.size * 0.55)
    ecart = police.size * 1.15
    for i, nom in enumerate(noms):
        w = d.textlength(nom, font=police) + pad * 2
        touche(d, x, cy, nom, police, enfonce, ombre)
        x += w
        if i < len(noms) - 1:
            wp = d.textlength("+", font=police)
            d.text((x + (ecart - wp) / 2 + police.size * 0.1, cy - police.size * 0.55), "+", font=police,
                   fill=couleur_plus)
            x += ecart


def largeur_touches(d, police, noms):
    pad = int(police.size * 0.55)
    return sum(d.textlength(x, font=police) + pad * 2 for x in noms) + police.size * 1.15 * (len(noms) - 1)


def legende(d, lignes, k, noms=None, enfonce=0.0):
    """Cellule active contenant la consigne. k : apparition 0 → 1. noms : touches à dessiner sous la 1re ligne."""
    boite(d, (X0, Y_CAP, X1, Y_CAP + H_CAP), ombre=JAUNE, decal=14, poignee=True)
    dy = int((1 - k) * 26)
    c = mix(PAPIER, VERT_NUIT, k)
    y = Y_CAP + 46 + dy
    if noms is None:
        for l in lignes:
            d.text((X0 + 44, y), l, font=F_CAPTION, fill=c)
            y += 96
    else:
        d.text((X0 + 44, y), lignes[0], font=F_CAPTION, fill=c)
        if k > 0.5:
            touches(d, X0 + 48, Y_CAP + 196 + dy, F_KEY, noms, enfonce)


def tableau(d, actif, style=0.0, plage=False):
    """actif : (colonne 1-3, ligne) de la cellule active. style : 0 → 1, mise en forme « tableau »
    (titres foncés, boutons de filtre, lignes à bandes). plage : contour de toute la liste (boîte de dialogue)."""
    X = XS
    bas = Y0 + RH * (NV + 1)
    d.rectangle((X0 + 14, Y0 + 14, X_DROITE + 14, bas + 14), fill=VERT_NUIT)
    d.rectangle((X0, Y0, X_DROITE, bas), fill=PAPIER)
    d.rectangle((X0, Y0, X_DROITE, Y0 + RH), fill=ENTETE)
    d.rectangle((X0, Y0, X[1], bas), fill=ENTETE)
    if style > 0:
        d.rectangle((X[1], y_ligne(1), X[4], y_ligne(1) + RH), fill=mix(PAPIER, VERT_NUIT, style))
        for r in range(2, NV + 1, 2):
            d.rectangle((X[1], y_ligne(r), X[4], y_ligne(r) + RH), fill=mix(PAPIER, BANDE, style))
    for i, lettre in enumerate("ABC"):
        w = d.textlength(lettre, font=F_HEAD)
        d.text(((X[i + 1] + X[i + 2] - w) / 2, Y0 + 26), lettre, font=F_HEAD, fill=GRIS)
    for r, v in enumerate(LIGNES, 1):
        y = y_ligne(r)
        num = str(r)
        w = d.textlength(num, font=F_HEAD)
        d.text((X0 + (W_NUM - w) / 2, y + 26), num, font=F_HEAD, fill=GRIS)
        if r == 1:
            for c in range(3):
                d.text((X[c + 1] + 18, y + 18), v[c], font=F_CELL_B, fill=mix(VERT_NUIT, PAPIER, style))
                if style > 0:      # bouton de filtre à droite du titre
                    bx, by = X[c + 2] - 58, y + 22
                    d.rectangle((bx, by, bx + 44, by + 44), fill=mix(VERT_NUIT, PAPIER, style),
                                outline=mix(VERT_NUIT, TRAIT, style), width=2)
                    d.polygon([(bx + 11, by + 16), (bx + 33, by + 16), (bx + 22, by + 30)],
                              fill=mix(PAPIER, VERT_NUIT, style))
        else:
            d.text((X[1] + 18, y + 18), v[0], font=F_CELL, fill=ENCRE)
            d.text((X[2] + 18, y + 18), v[1], font=F_CELL, fill=ENCRE)
            w = d.textlength(v[2], font=F_CELL)
            d.text((X[4] - 18 - w, y + 18), v[2], font=F_CELL, fill=ENCRE)
    for r in range(1, NV + 2):
        d.line((X0, y_ligne(r), X_DROITE, y_ligne(r)), fill=TRAIT, width=2)
    for x in X:
        d.line((x, Y0, x, bas), fill=TRAIT, width=2)
    d.rectangle((X0, Y0, X_DROITE, bas), outline=VERT_NUIT, width=3)
    if plage:
        d.rectangle((X[1], y_ligne(1), X[4], bas), outline=VERT, width=6)
    c, r = actif
    d.rectangle((X[c], y_ligne(r), X[c + 1], y_ligne(r) + RH), outline=VERT, width=8)
    d.rectangle((X[c + 1] - 13, y_ligne(r) + RH - 13, X[c + 1] + 11, y_ligne(r) + RH + 11), fill=VERT,
                outline=PAPIER, width=3)


DLG = (110, 880, 910, 1330)


def dialogue(d, k, appui=0.0):
    """Boîte « Créer un tableau ». k : apparition 0 → 1. appui : bouton OK enfoncé 0 → 1."""
    x1, y1, x2, y2 = DLG
    dy = int((1 - k) * 30)
    y1, y2 = y1 + dy, y2 + dy
    d.rectangle((x1 + 16, y1 + 16, x2 + 16, y2 + 16), fill=JAUNE)
    d.rectangle((x1, y1, x2, y2), fill=PAPIER, outline=VERT_NUIT, width=5)
    d.rectangle((x1, y1, x2, y1 + 84), fill=VERT_NUIT)
    d.text((x1 + 30, y1 + 16), "Créer un tableau", font=F_DLG_T, fill=PAPIER)
    d.rectangle((x1 + 30, y1 + 118, x2 - 30, y1 + 196), fill=PAPIER, outline=TRAIT, width=3)
    d.text((x1 + 50, y1 + 130), PLAGE, font=F_MONO, fill=ENCRE)
    cy = y1 + 232
    d.rectangle((x1 + 30, cy, x1 + 78, cy + 48), fill=VERT, outline=VERT_NUIT, width=3)
    d.line((x1 + 40, cy + 25, x1 + 50, cy + 36, x1 + 68, cy + 12), fill=PAPIER, width=6)
    d.text((x1 + 98, cy - 2), "Mon tableau comporte des en-têtes", font=F_DLG, fill=ENCRE)
    bx1, by1, bx2, by2 = x2 - 250, y2 - 124, x2 - 30, y2 - 34
    kk = int(8 * appui)
    d.rectangle((bx1 + 8, by1 + 8, bx2 + 8, by2 + 8), fill=VERT_NUIT)
    d.rectangle((bx1 + kk, by1 + kk, bx2 + kk, by2 + kk), fill=mix(VERT, JAUNE, appui), outline=VERT_NUIT, width=4)
    w = d.textlength("OK", font=F_DLG_T)
    d.text(((bx1 + bx2 - w) / 2 + kk, by1 + 18 + kk), "OK", font=F_DLG_T, fill=mix(PAPIER, VERT_NUIT, appui))


# ---------- scènes : chacune renvoie une image pour l'instant t (secondes) ----------

ACCROCHE = ["Un tableau", "tout prêt en", "2 touches ?"]
SOUS_ACCROCHE = "Filtres et couleurs inclus"


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
        x1, y1 = 70, 1160 + dy
        x2, y2 = x1 + 80 + int(d.textlength(SOUS_ACCROCHE, font=F_SUB)), y1 + 130
        d.rectangle((x1 + 12, y1 + 12, x2 + 12, y2 + 12), fill=mix(PAPIER, JAUNE, k))
        d.rectangle((x1, y1, x2, y2), fill=mix(PAPIER, VERT_NUIT, k))
        d.text((x1 + 40, y1 + 30), SOUS_ACCROCHE, font=F_SUB, fill=mix(VERT_NUIT, PAPIER, k))
    return im


# Repères de la démonstration
T_CAP2, T_CLIC = 1.3, 2.2          # « Cliquez dans la liste » : clic en B3
T_CAP3, T_KEY = 3.1, 4.0           # « Appuyez sur Ctrl + T » : la boîte « Créer un tableau » s'ouvre
T_CAP4, T_VAL = 5.3, 6.3           # « Validez avec Entrée » : la liste devient un tableau
T_CAP5 = 7.5
D_DEMO = 10.0
P_DEPART = (700, 1450)
P_REPOS = (780, 1440)


def p_cell(c, r):
    return (XS[c] + 150, y_ligne(r) + 46)


def entre(a, b, k):
    k = ease(k)
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


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
        legende(d, ["Une liste", "toute plate ?"], ease(t / 0.3))
    elif t < T_CAP3:
        legende(d, ["Cliquez dans", "la liste"], ease((t - T_CAP2) / 0.3))
    elif t < T_CAP4:
        legende(d, ["Appuyez sur"], ease((t - T_CAP3) / 0.3), ["Ctrl", "T"], appui_k(T_KEY))
    elif t < T_CAP5:
        legende(d, ["Validez avec"], ease((t - T_CAP4) / 0.3), ["Entrée"], appui_k(T_VAL))
    else:
        legende(d, ["Un vrai tableau,", "filtres compris !"], ease((t - T_CAP5) / 0.3))

    clique = t >= T_CLIC
    actif = (CLIC_COL, CLIC_LIG) if clique else (1, 1)
    ouvert = T_KEY + 0.15 <= t < T_VAL + 0.25
    style = ease((t - T_VAL - 0.3) / 0.5)
    barre_formule(d, "B3" if clique else "A1", LIGNES[CLIC_LIG - 1][1] if clique else "Produit")
    tableau(d, actif, style, plage=ouvert)

    # pointeur de souris
    cible = p_cell(CLIC_COL, CLIC_LIG)
    if t < T_CAP2:
        p = P_DEPART
    elif t < T_CLIC:
        p = entre(P_DEPART, cible, (t - T_CAP2) / (T_CLIC - T_CAP2 - 0.1))
    else:
        p = entre(cible, P_REPOS, (t - T_CLIC - 0.3) / 0.5)
    onde(d, cible[0], cible[1], (t - T_CLIC) / 0.45)
    if ouvert:
        dialogue(d, ease((t - T_KEY - 0.15) / 0.2), appui_k(T_VAL))
    fleche(d, int(p[0]), int(p[1]))
    return im


def s_fin(t, tg):
    im = FOND_SOMBRE.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg, sombre=True)
    k = ease(t / 0.35)
    dy = int((1 - k) * 40)
    noms = ["Ctrl", "T"]
    lt = largeur_touches(d, F_KEY_L, noms)
    touches(d, X0 + (X1 - X0 - lt) / 2, 520 + dy, F_KEY_L, noms, 0.0, ombre=JAUNE, couleur_plus=PAPIER)
    y = 720
    for l in ["Transformer une", "liste en tableau"]:
        w = d.textlength(l, font=F_FIN)
        d.text(((X0 + X1 - w) / 2, y), l, font=F_FIN, fill=mix(VERT_NUIT, PAPIER, k))
        y += 112
    note = "Excel · Sheets : Ctrl + Alt + T"
    w = d.textlength(note, font=F_NOTE)
    d.text(((X0 + X1 - w) / 2, y + 16), note, font=F_NOTE, fill=mix(VERT_NUIT, (190, 214, 202), k))
    if t > 0.9:
        k2 = ease((t - 0.9) / 0.3)
        yb = 1170 + int((1 - k2) * 40)
        d.text((70, yb), "À savoir", font=F_SHEETS, fill=mix(VERT_NUIT, JAUNE, k2))
        d.rectangle((82, yb + 82, 962, yb + 236), fill=mix(VERT_NUIT, JAUNE, k2))
        d.rectangle((70, yb + 70, 950, yb + 224), fill=mix(VERT_NUIT, PAPIER, k2), outline=TRAIT, width=3)
        for i, l in enumerate(["Ajoutez une ligne en dessous :", "le tableau s'agrandit tout seul."]):
            d.text((100, yb + 88 + i * 60), l, font=F_NOTE, fill=mix(VERT_NUIT, ENCRE, k2))
    return im


D_ACC = 2.9
SCENES = [(s_accroche, D_ACC), (s_demo, D_DEMO), (s_fin, 4.0)]
DUREE_TOTALE = sum(x[1] for x in SCENES)

# Bruitages : (type, instant depuis le début de la vidéo).
_D, _F = D_ACC, D_ACC + D_DEMO
SONS = ([("frappe", 0.15 + k * 0.036 * 3) for k in range(sum(len(l) for l in ACCROCHE) // 3)] + [("pop", 1.6)]
        + [("pop", _D + T_CAP2), ("clic", _D + T_CLIC),
           ("pop", _D + T_CAP3), ("touche", _D + T_KEY), ("pop", _D + T_KEY + 0.15),
           ("pop", _D + T_CAP4), ("touche", _D + T_VAL), ("carillon", _D + T_VAL + 0.3),
           ("pop", _D + T_CAP5), ("fin", _F)])


def apercu(dossier):
    os.makedirs(dossier, exist_ok=True)
    plans = [(s_accroche, 1.0), (s_accroche, 2.5), (s_demo, 0.8), (s_demo, 1.9), (s_demo, 2.4), (s_demo, 3.6),
             (s_demo, 4.1), (s_demo, 4.8), (s_demo, 5.9), (s_demo, 6.45), (s_demo, 6.8),
             (s_demo, 7.2), (s_demo, 8.5), (s_fin, 0.5), (s_fin, 3.0)]
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
