"""Vidéo verticale « Afficher toutes les formules avec Ctrl + " » — Tableur Malin.

Usage : python3 astuce_afficher_les_formules_ctrl_guillemet.py <dossier_polices> <sortie.mp4> [--apercu dossier]
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
F_MONO_C = mono(34, True)      # formules affichées dans les cellules
F_NOTE = titre(42, 500)
F_SHEETS = titre(44, 700)

F_KEY_L = titre(88, 800)
F_MENU = titre(38, 600)
F_MENU_B = titre(38, 800)


X0, X1 = 60, 960          # largeur utile (les boutons des applis recouvrent le bord droit)
W_NUM, W_A, W_B, W_C = 70, 200, 290, 340
XS = [X0, X0 + W_NUM, X0 + W_NUM + W_A, X0 + W_NUM + W_A + W_B, X0 + W_NUM + W_A + W_B + W_C]
X_DROITE = XS[-1]
Y_CAP, H_CAP = 250, 290   # cellule de légende
Y_FX = 590                # barre de formule
Y0, RH = 700, 80          # tableau : ligne des lettres, ligne de titres, cinq articles, total, deux lignes vides
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



# ---------- données : cinq articles, prix HT, prix TTC (= HT × 1,2), ligne de total ----------
# Chaque cellule : (texte affiché en mode résultats, texte affiché en mode formules).
LIGNES = [("Article", "Prix HT", "Prix TTC"),
          ("Lampe", ("40 €", "40"), ("48 €", "=B2*1,2")),
          ("Coussin", ("25 €", "25"), ("30 €", "=B3*1,2")),
          ("Miroir", ("55 €", "55"), ("66 €", "66")),            # C4 : nombre tapé à la main, pas une formule
          ("Vase", ("30 €", "30"), ("36 €", "=B5*1,2")),
          ("Tapis", ("50 €", "50"), ("60 €", "=B6*1,2")),
          ("Total", ("200 €", "=SOMME(B2:B6)"), ("240 €", "=SOMME(C2:C6)"))]
DERNIERE = len(LIGNES)    # 7 : dernière ligne remplie
NV = 9                    # lignes visibles sous la ligne des lettres
ACTIF = (2, 2)            # cellule active : C2
INTRUS = (4, 2)           # C4 : la valeur tapée à la main, mise en évidence en mode formules
SEL = (214, 238, 224)


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


def tableau(d, im, formules=0.0, intrus=0.0):
    """formules : 0 = résultats, 1 = formules affichées (fondu entre les deux). intrus : surlignage de C4, 0 → 1."""
    X = XS
    bas = Y0 + RH * (NV + 1)
    ar, ac = ACTIF
    d.rectangle((X0 + 14, Y0 + 14, X_DROITE + 14, bas + 14), fill=VERT_NUIT)
    d.rectangle((X0, Y0, X_DROITE, Y0 + RH), fill=ENTETE)
    for i, lettre in enumerate("ABC"):
        w = d.textlength(lettre, font=F_HEAD)
        d.text(((X[i + 1] + X[i + 2] - w) / 2, Y0 + 26), lettre, font=F_HEAD, fill=GRIS)
    for r in range(1, NV + 1):
        y = Y0 + RH * r
        d.rectangle((X[0], y, X[1], y + RH), fill=ENTETE)
        d.rectangle((X[1], y, X[4], y + RH), fill=PAPIER)
        num = str(r)
        w = d.textlength(num, font=F_HEAD)
        d.text((X[0] + (W_NUM - w) / 2, y + 26), num, font=F_HEAD, fill=GRIS)
    if intrus > 0:
        ir, ic = INTRUS
        d.rectangle((X[ic + 1], Y0 + RH * ir, X[ic + 2], Y0 + RH * (ir + 1)), fill=mix(PAPIER, JAUNE, intrus))
    for r in range(1, DERNIERE + 1):
        y = Y0 + RH * r
        v = LIGNES[r - 1]
        gras = r in (1, DERNIERE)
        f = F_CELL_B if gras else F_CELL
        coul = VERT_NUIT if gras else ENCRE
        d.text((X[1] + 18, y + 18), v[0], font=f, fill=coul)
        for col in (1, 2):
            if r == 1:
                d.text((X[col + 1] + 18, y + 18), v[col], font=f, fill=coul)
                continue
            valeur, formule = v[col]
            fond_c = mix(PAPIER, JAUNE, intrus) if (r, col) == INTRUS else PAPIER
            if formules < 1:
                w = d.textlength(valeur, font=f)
                d.text((X[col + 2] - 18 - w, y + 18), valeur, font=f, fill=mix(coul, fond_c, formules))
            if formules > 0:
                c2 = mix(fond_c, VERT if formule.startswith("=") else ENCRE, formules)
                if formule.startswith("="):
                    d.text((X[col + 1] + 16, y + 20), formule, font=F_MONO_C, fill=c2)
                else:
                    w = d.textlength(formule, font=f)
                    d.text((X[col + 2] - 18 - w, y + 18), formule, font=f, fill=c2)
    for r in range(1, NV + 1):
        d.line((X0, Y0 + RH * r, X_DROITE, Y0 + RH * r), fill=TRAIT, width=2)
    for x in X:
        d.line((x, Y0, x, bas), fill=TRAIT, width=2)
    d.rectangle((X0, Y0, X_DROITE, bas), outline=VERT_NUIT, width=3)
    y = Y0 + RH * ar
    d.rectangle((X[ac + 1], y, X[ac + 2], y + RH), outline=VERT, width=8)
    d.rectangle((X[ac + 2] - 13, y + RH - 13, X[ac + 2] + 11, y + RH + 11), fill=VERT, outline=PAPIER, width=3)
    if intrus > 0:
        ir, ic = INTRUS
        d.rectangle((X[ic + 1] - 4, Y0 + RH * ir - 4, X[ic + 2] + 4, Y0 + RH * (ir + 1) + 4),
                    outline=mix(PAPIER, ENCRE, intrus), width=6)


# ---------- scènes : chacune renvoie une image pour l'instant t (secondes) ----------

ACCROCHE = ["Où sont", "cachées les", "formules ?"]
SOUS_ACCROCHE = "Affichez-les d'un coup"


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
T_CAP2, T_AFF = 1.9, 2.9          # consigne Ctrl + ", puis appui : toutes les formules s'affichent
T_CAP3 = 4.0                      # « Les formules s'affichent »
T_CAP4 = 5.9                      # « Ici, un nombre tapé à la main » (C4 surlignée)
T_CAP5, T_RET = 8.2, 9.2          # consigne pour revenir, puis appui : retour aux résultats
T_CAP6 = 10.2                     # « Retour aux résultats »
D_DEMO = 11.8
TOUCHES = ["Ctrl", "\""]


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
        legende(d, ["Une formule", "par cellule ?"], ease(t / 0.3))
    elif t < T_CAP3:
        legende(d, ["Affichez-les toutes"], ease((t - T_CAP2) / 0.3), TOUCHES, appui_k(T_AFF))
    elif t < T_CAP4:
        legende(d, ["Les formules", "s'affichent"], ease((t - T_CAP3) / 0.3))
    elif t < T_CAP5:
        legende(d, ["Ici, un nombre", "tapé à la main"], ease((t - T_CAP4) / 0.3))
    elif t < T_CAP6:
        legende(d, ["Et pour revenir ?"], ease((t - T_CAP5) / 0.3), TOUCHES, appui_k(T_RET))
    else:
        legende(d, ["Retour aux", "résultats"], ease((t - T_CAP6) / 0.3))

    barre_formule(d, "C2", "=B2*1,2")
    if t < T_AFF:
        f = 0.0
    elif t < T_RET:
        f = ease((t - T_AFF) / 0.25)
    else:
        f = 1 - ease((t - T_RET) / 0.25)
    intrus = 0.0
    if T_CAP4 <= t < T_RET:
        intrus = ease((t - T_CAP4) / 0.3)
    elif t >= T_RET:
        intrus = 1 - ease((t - T_RET) / 0.25)
    tableau(d, im, f, intrus)
    return im


def s_fin(t, tg):
    im = FOND_SOMBRE.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg, sombre=True)
    k = ease(t / 0.35)
    dy = int((1 - k) * 40)
    noms = TOUCHES
    lt = largeur_touches(d, F_KEY_L, noms)
    touches(d, X0 + (X1 - X0 - lt) / 2, 520 + dy, F_KEY_L, noms, 0.0, ombre=JAUNE, couleur_plus=PAPIER)
    y = 720
    for l in ["Afficher", "les formules"]:
        w = d.textlength(l, font=F_HOOK)
        d.text(((X0 + X1 - w) / 2, y), l, font=F_HOOK, fill=mix(VERT_NUIT, PAPIER, k))
        y += 118
    note = "Excel, clavier français"
    w = d.textlength(note, font=F_NOTE)
    d.text(((X0 + X1 - w) / 2, y + 16), note, font=F_NOTE, fill=mix(VERT_NUIT, (190, 214, 202), k))
    if t > 0.9:
        k2 = ease((t - 0.9) / 0.3)
        yb = 1170 + int((1 - k2) * 40)
        d.text((70, yb), "À savoir", font=F_SHEETS, fill=mix(VERT_NUIT, JAUNE, k2))
        d.rectangle((82, yb + 82, 962, yb + 236), fill=mix(VERT_NUIT, JAUNE, k2))
        d.rectangle((70, yb + 70, 950, yb + 224), fill=mix(VERT_NUIT, PAPIER, k2), outline=TRAIT, width=3)
        for i, l in enumerate(["La touche \" est celle du 3.", "Sheets : menu Affichage, Afficher."]):
            d.text((100, yb + 88 + i * 60), l, font=F_NOTE, fill=mix(VERT_NUIT, ENCRE, k2))
    return im


D_ACC = 2.9
SCENES = [(s_accroche, D_ACC), (s_demo, D_DEMO), (s_fin, 4.0)]
DUREE_TOTALE = sum(x[1] for x in SCENES)

# Bruitages : (type, instant depuis le début de la vidéo).
_D, _F = D_ACC, D_ACC + D_DEMO
SONS = ([("frappe", 0.15 + k * 0.036 * 3) for k in range(sum(len(l) for l in ACCROCHE) // 3)] + [("pop", 1.6)]
        + [("pop", _D + 0.05), ("pop", _D + T_CAP2), ("touche", _D + T_AFF), ("carillon", _D + T_AFF + 0.15),
           ("pop", _D + T_CAP3), ("pop", _D + T_CAP4), ("clic", _D + T_CAP4 + 0.2), ("pop", _D + T_CAP5),
           ("touche", _D + T_RET), ("carillon", _D + T_RET + 0.15), ("pop", _D + T_CAP6), ("fin", _F)])


def apercu(dossier):
    os.makedirs(dossier, exist_ok=True)
    plans = [(s_accroche, 1.0), (s_accroche, 2.5), (s_demo, 1.0), (s_demo, 2.6), (s_demo, 3.0), (s_demo, 3.3),
             (s_demo, 5.0), (s_demo, 7.5), (s_demo, 8.9), (s_demo, 9.3), (s_demo, 11.0), (s_fin, 0.5), (s_fin, 3.0)]
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
