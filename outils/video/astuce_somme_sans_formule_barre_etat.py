"""Vidéo verticale « Une somme sans formule : la barre d'état » — Tableur Malin.

Usage : python3 astuce_somme_sans_formule_barre_etat.py <dossier_polices> <sortie.mp4> [--apercu dossier]
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


F_ETAT = titre(34, 600)
F_ETAT_B = titre(34, 800)
F_ETAT_XL = titre(84, 800)

MOIS = ["Janvier", "Février", "Mars", "Avril", "Mai"]
VENTES = [420, 380, 510, 290, 460]

X0, X1 = 60, 960          # largeur utile (les boutons des applis recouvrent le bord droit)
X_DROITE = 920            # le tableau s'arrête à x = 920 ; la colonne C est coupée par le bord, comme à l'écran
W_NUM, W_A, W_B = 70, 330, 260
XS = [X0, X0 + W_NUM, X0 + W_NUM + W_A, X0 + W_NUM + W_A + W_B, X_DROITE]
Y_CAP, H_CAP = 250, 290   # cellule de légende
Y_FX = 590                # barre de formule
Y0, RH, NL = 700, 88, 7   # tableau : ligne des lettres, ligne de titres, cinq mois
Y_BAS = Y0 + RH * NL
Y_ETAT, H_ETAT = Y_BAS + 44, 92   # barre d'état, sous la feuille
DUREE_TOTALE = 0.0        # renseignée plus bas (barre de progression)


def nombre(v):
    """Nombre écrit à la française : espace entre les milliers, virgule décimale."""
    s = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    return s[:-3] if s.endswith(",00") else s.rstrip("0")


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



def barre_etat(d, n, halo=0.0, k=1.0):
    """Barre d'état sous la feuille. n : nombre de cellules sélectionnées (0 ou 1 : rien à afficher).
    halo : mise en avant de la somme (0→1). k : apparition des valeurs (0→1)."""
    d.rectangle((X0 + 14, Y_ETAT + 14, X_DROITE + 14, Y_ETAT + H_ETAT + 14), fill=VERT_NUIT)
    d.rectangle((X0, Y_ETAT, X_DROITE, Y_ETAT + H_ETAT), fill=ENTETE, outline=VERT_NUIT, width=3)
    if n < 2:
        d.text((X0 + 26, Y_ETAT + 24), "Prêt", font=F_ETAT, fill=GRIS)
        return
    vals = VENTES[:n]
    morceaux = [("Moyenne : " + nombre(sum(vals) / n), F_ETAT, GRIS),
                ("Nb (non vides) : " + str(n), F_ETAT, GRIS),
                ("Somme : " + nombre(sum(vals)), F_ETAT_B, VERT_NUIT)]
    x = X_DROITE - 26
    for i, (txt, police, couleur) in enumerate(reversed(morceaux)):
        w = d.textlength(txt, font=police)
        x -= w
        if i == 0 and halo > 0:
            e = int(2 + 4 * halo)
            d.rectangle((x - 12 - e, Y_ETAT + 14 - e, x + w + 12 + e, Y_ETAT + H_ETAT - 14 + e),
                        fill=JAUNE, outline=VERT_NUIT, width=3)
        d.text((x, Y_ETAT + 24), txt, font=police, fill=mix(ENTETE, couleur, k) if not (i == 0 and halo > 0) else couleur)
        x -= 30


def tableau(d, sel, fin=None):
    """sel : (colonne, ligne) de la cellule active. fin : dernière ligne de la plage sélectionnée (colonne B)."""
    X = XS
    d.rectangle((X0 + 14, Y0 + 14, X_DROITE + 14, Y_BAS + 14), fill=VERT_NUIT)
    d.rectangle((X0, Y0, X_DROITE, Y_BAS), fill=PAPIER)
    d.rectangle((X0, Y0, X_DROITE, Y0 + RH), fill=ENTETE)
    d.rectangle((X0, Y0, X[1], Y_BAS), fill=ENTETE)
    col, ligne = sel
    if fin and fin > ligne:                      # plage sélectionnée : fond vert pâle sauf la cellule active
        d.rectangle((X[col], Y0 + RH * (ligne + 1), X[col + 1], Y0 + RH * (fin + 1)), fill=mix(PAPIER, VERT, 0.16))
    for i, lettre in enumerate("ABC"):
        w = d.textlength(lettre, font=F_HEAD)
        d.text(((X[i + 1] + X[i + 2] - w) / 2, Y0 + 26), lettre, font=F_HEAD, fill=GRIS)
    for r in range(1, NL):
        w = d.textlength(str(r), font=F_HEAD)
        d.text((X0 + (W_NUM - w) / 2, Y0 + RH * r + 26), str(r), font=F_HEAD, fill=GRIS)
    for x in X:
        d.line((x, Y0, x, Y_BAS), fill=TRAIT, width=2)
    for r in range(NL + 1):
        d.line((X0, Y0 + RH * r, X_DROITE, Y0 + RH * r), fill=TRAIT, width=2)
    d.rectangle((X0, Y0, X_DROITE, Y_BAS), outline=VERT_NUIT, width=3)

    d.text((X[1] + 18, Y0 + RH + 18), "Mois", font=F_CELL_B, fill=VERT_NUIT)
    w = d.textlength("Ventes", font=F_CELL_B)
    d.text((X[3] - 18 - w, Y0 + RH + 18), "Ventes", font=F_CELL_B, fill=VERT_NUIT)
    for r, mois in enumerate(MOIS):
        y = Y0 + RH * (r + 2) + 18
        d.text((X[1] + 18, y), mois, font=F_CELL, fill=ENCRE)
        dans = fin is not None and col == 2 and ligne <= r + 2 <= fin
        police = F_CELL_B if dans else F_CELL
        txt = str(VENTES[r])
        w = d.textlength(txt, font=police)
        d.text((X[3] - 18 - w, y), txt, font=police, fill=VERT_NUIT if dans else ENCRE)
    derniere = fin if fin else ligne
    x1, y1, x2, y2 = X[col], Y0 + RH * ligne, X[col + 1], Y0 + RH * (derniere + 1)
    d.rectangle((x1, y1, x2, y2), outline=VERT, width=8)
    d.rectangle((x2 - 13, y2 - 13, x2 + 11, y2 + 11), fill=VERT, outline=PAPIER, width=3)


def glisse(a, b, k):
    return tuple(a[i] + (b[i] - a[i]) * ease(k) for i in range(len(a)))


# ---------- scènes : chacune renvoie une image pour l'instant t (secondes) ----------

ACCROCHE = ["Une somme", "sans taper", "de formule ?"]


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
        x1, y1, x2, y2 = 70, 1160 + dy, 830, 1290 + dy
        d.rectangle((x1 + 12, y1 + 12, x2 + 12, y2 + 12), fill=mix(PAPIER, JAUNE, k))
        d.rectangle((x1, y1, x2, y2), fill=mix(PAPIER, VERT_NUIT, k))
        d.text((x1 + 40, y1 + 30), "Regardez tout en bas", font=F_SUB, fill=mix(VERT_NUIT, PAPIER, k))
    return im


# Repères de la démonstration
T_CLIC = 1.0                      # clic sur B2, bouton maintenu
T_CAP2 = 1.5
T_TIRE, D_TIRE = 2.3, 1.6         # la souris descend de B2 à B6
T_LACHE = T_TIRE + D_TIRE         # 3,9 s : la plage est sélectionnée
T_CAP3, T_VISE = 4.5, 4.7         # la souris descend vers la barre d'état
T_HALO = 5.4
T_CAP4 = 7.6
D_DEMO = 10.2


def centre(ligne):
    return (XS[2] + W_B // 2 - 30, Y0 + RH * ligne + RH // 2 + 6)


SOMME_XY = (XS[3] + 60, Y_ETAT + H_ETAT - 6)     # sous le mot « Somme », sans le cacher


def lignes_tirees(t):
    """Dernière ligne atteinte par la souris pendant le glissement (2 → 6)."""
    if t < T_TIRE:
        return 2
    return min(6, 2 + int(ease((t - T_TIRE) / D_TIRE) * 4 + 0.5))


def s_demo(t, tg):
    im = FOND_CLAIR.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg)

    if t < T_CLIC:
        sel, fin, ref, contenu = (1, 1), None, "A1", "Mois"
    else:
        sel, fin, ref, contenu = (2, 2), lignes_tirees(t), "B2", str(VENTES[0])
    n = 0 if fin is None else fin - 1

    if t < T_CAP2:
        legende(d, ["Le total des", "ventes, vite ?"], ease(t / 0.3))
    elif t < T_CAP3:
        legende(d, ["Sélectionnez", "les nombres"], ease((t - T_CAP2) / 0.3))
    elif t < T_CAP4:
        legende(d, ["Regardez", "tout en bas"], ease((t - T_CAP3) / 0.3))
    else:
        legende(d, ["Somme, moyenne :", "aucune formule"], ease((t - T_CAP4) / 0.3))

    halo = 0.0
    if t >= T_HALO:
        halo = 0.5 + 0.5 * abs(((t - T_HALO) * 1.6) % 2 - 1)

    barre_formule(d, ref, contenu)
    tableau(d, sel, fin if fin and fin > 2 else None)
    barre_etat(d, n, halo)

    # Pointeur de souris
    depart = (820, 1500)
    if t < T_TIRE:
        x, y = glisse(depart, centre(2), (t - 0.3) / 0.6)
        onde(d, *centre(2), (t - T_CLIC) / 0.4)
    elif t < T_VISE:
        x, y = glisse(centre(2), centre(6), (t - T_TIRE) / D_TIRE)
    else:
        x, y = glisse(centre(6), SOMME_XY, (t - T_VISE) / 0.7)
    fleche(d, x, y)
    return im


def s_fin(t, tg):
    im = FOND_SOMBRE.copy()
    d = ImageDraw.Draw(im)
    entete(d, tg, sombre=True)
    k = ease(t / 0.35)
    dy = int((1 - k) * 40)
    # La barre d'état en grand
    x1, y1, x2, y2 = 150, 420 + dy, 930, 600 + dy
    d.rectangle((x1 + 16, y1 + 16, x2 + 16, y2 + 16), fill=JAUNE)
    d.rectangle((x1, y1, x2, y2), fill=ENTETE, outline=PAPIER, width=6)
    txt = "Somme : " + nombre(sum(VENTES))
    w = d.textlength(txt, font=F_ETAT_XL)
    d.text(((x1 + x2 - w) / 2, y1 + 40), txt, font=F_ETAT_XL, fill=VERT_NUIT)
    y = 760
    for l in ["Sélectionnez,", "regardez en bas"]:
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
        for i, l in enumerate(["Rien ne s'écrit dans la feuille :", "c'est juste pour vérifier un total."]):
            d.text((120, yb + 88 + i * 60), l, font=F_NOTE, fill=mix(VERT_NUIT, ENCRE, k2))
    return im


D_ACC = 2.9
SCENES = [(s_accroche, D_ACC), (s_demo, D_DEMO), (s_fin, 4.0)]
DUREE_TOTALE = sum(x[1] for x in SCENES)

# Bruitages : (type, instant depuis le début de la vidéo).
_D, _F = D_ACC, D_ACC + D_DEMO


def _instants_tires():
    """Instant où la sélection gagne chaque ligne (3 à 6)."""
    out, prec, t = [], 2, T_TIRE
    while t < T_LACHE + 0.05:
        l = lignes_tirees(t)
        if l > prec:
            out.append(t)
            prec = l
        t += 1 / FPS
    return out


SONS = ([("frappe", 0.15 + k * 0.036 * 3) for k in range(sum(len(l) for l in ACCROCHE) // 3)] + [("pop", 1.6)]
        + [("clic", _D + T_CLIC)] + [("frappe", _D + x) for x in _instants_tires()]
        + [("carillon", _D + T_LACHE), ("pop", _D + T_HALO), ("pop", _D + T_CAP4), ("fin", _F)])


def apercu(dossier):
    os.makedirs(dossier, exist_ok=True)
    plans = [(s_accroche, 1.0), (s_accroche, 2.5), (s_demo, 0.7), (s_demo, 1.2), (s_demo, 2.0), (s_demo, 3.0),
             (s_demo, 3.5), (s_demo, 4.2), (s_demo, 5.0), (s_demo, 5.8), (s_demo, 6.4), (s_demo, 8.5), (s_fin, 0.5),
             (s_fin, 3.0)]
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
