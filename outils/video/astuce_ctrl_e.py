"""Vidéo verticale « Remplissage instantané (Ctrl + E) » — Tableur Malin.

Usage : python3 astuce_ctrl_e.py <dossier_polices> <sortie.mp4> [--apercu dossier]
Dessine chaque image avec Pillow et l'envoie directement à ffmpeg (un fichier par scène,
puis assemblage sans ré-encodage).
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
VERT_NUIT = (15, 61, 46)
VERT = (30, 142, 90)
JAUNE = (255, 216, 77)
PAPIER = (255, 255, 255)
GRILLE = (214, 224, 217)
ENTETE = (238, 243, 239)
ENCRE = (27, 36, 32)
GRIS = (108, 122, 114)

POLICES = sys.argv[1]
SORTIE = sys.argv[2]


def titre(taille, graisse=800):
    f = ImageFont.truetype(os.path.join(POLICES, "bricolage.ttf"), taille)
    f.set_variation_by_axes([graisse])
    return f


def mono(taille, gras=False):
    return ImageFont.truetype(os.path.join(POLICES, "mono700.ttf" if gras else "mono400.ttf"), taille)


F_CAPTION = titre(80)
F_HOOK = titre(104)
F_SUB = titre(60, 600)
F_MARQUE = titre(40, 700)
F_CELL = titre(40, 500)
F_CELL_B = titre(40, 750)
F_HEAD = titre(32, 600)
F_KEY = titre(64, 750)
F_KEY_XL = titre(150, 800)
F_MONO = mono(46, True)

NOMS = ["Camille Martin", "Lucas Bernard", "Inès Petit", "Hugo Durand", "Léa Moreau", "Nathan Roux"]
PRENOMS = [n.split()[0] for n in NOMS]
FAMILLE = [n.split()[1] for n in NOMS]

# Géométrie du tableau (zone sûre : rien d'important sous y=1560 ni à droite de x=940)
X0, Y0 = 50, 640
COLS = [70, 350, 230, 230]  # n° de ligne, A, B, C
RH = 100
XS = [X0]
for c in COLS:
    XS.append(XS[-1] + c)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def lignes_centrees(d, lignes, police, y, couleur, interligne=1.12):
    for l in lignes:
        w = d.textlength(l, font=police)
        d.text(((W - w) / 2, y), l, font=police, fill=couleur)
        y += int(police.size * interligne)
    return y


def marque(d, couleur):
    d.rounded_rectangle((60, 120, 96, 156), 6, outline=couleur, width=5)
    d.rectangle((88, 148, 102, 162), fill=couleur)
    d.text((118, 112), "Tableur Malin", font=F_MARQUE, fill=couleur)


def touche(d, cx, cy, texte, police, enfoncee=False, clair=False, pad=44):
    w = d.textlength(texte, font=police)
    h = police.size
    bw, bh = w + pad * 2, h + pad * 1.3
    dy = 10 if enfoncee else 0
    x1, y1 = cx - bw / 2, cy - bh / 2 + dy
    ombre = (9, 38, 28) if clair else (190, 200, 194)
    face = JAUNE if enfoncee else (PAPIER if clair else (246, 248, 246))
    if not enfoncee:
        d.rounded_rectangle((x1, y1 + 12, x1 + bw, y1 + bh + 12), 22, fill=ombre)
    d.rounded_rectangle((x1, y1, x1 + bw, y1 + bh), 22, fill=face, outline=ENCRE, width=4)
    d.text((cx - w / 2, y1 + (bh - h) / 2 - h * 0.12), texte, font=police, fill=ENCRE)
    return bw


def touches(d, cy, enfoncee, police=F_KEY, clair=False, ecart=70):
    w1 = d.textlength("Ctrl", font=police) + 88
    w2 = d.textlength("E", font=police) + 88
    total = w1 + ecart + w2
    x = (W - total) / 2 if clair else (X0 + XS[-1]) / 2 - total / 2
    touche(d, x + w1 / 2, cy, "Ctrl", police, enfoncee, clair)
    wp = d.textlength("+", font=police)
    d.text((x + w1 + (ecart - wp) / 2, cy - police.size * 0.52), "+", font=police, fill=PAPIER if clair else ENCRE)
    touche(d, x + w1 + ecart + w2 / 2, cy, "E", police, enfoncee, clair)


def tableau(d, b_vals, c_vals, selection=None, surlignage=None, curseur=False):
    """b_vals / c_vals : listes de 6 textes (ou None). selection : (col, ligne)."""
    bas = Y0 + RH * 8
    d.rectangle((X0 + 6, Y0 + 10, XS[-1] + 6, bas + 10), fill=(226, 233, 228))
    d.rectangle((X0, Y0, XS[-1], bas), fill=PAPIER)
    d.rectangle((X0, Y0, XS[-1], Y0 + RH), fill=ENTETE)
    d.rectangle((X0, Y0, XS[1], bas), fill=ENTETE)
    for i, lettre in enumerate("ABC"):
        w = d.textlength(lettre, font=F_HEAD)
        d.text(((XS[i + 1] + XS[i + 2] - w) / 2, Y0 + 30), lettre, font=F_HEAD, fill=GRIS)
    for r in range(1, 8):
        t = str(r)
        w = d.textlength(t, font=F_HEAD)
        d.text((X0 + (COLS[0] - w) / 2, Y0 + RH * r + 30), t, font=F_HEAD, fill=GRIS)
    if surlignage:
        col, k = surlignage
        d.rectangle((XS[col], Y0 + RH * 3, XS[col + 1], Y0 + RH * 8), fill=mix(PAPIER, JAUNE, k))
    for x in XS:
        d.line((x, Y0, x, bas), fill=GRILLE, width=2)
    for r in range(9):
        d.line((X0, Y0 + RH * r, XS[-1], Y0 + RH * r), fill=GRILLE, width=2)
    for i, t in enumerate(["Nom complet", "Prénom", "Nom"]):
        d.text((XS[i + 1] + 18, Y0 + RH + 24), t, font=F_CELL_B, fill=VERT_NUIT)
    for r in range(6):
        y = Y0 + RH * (r + 2) + 24
        d.text((XS[1] + 18, y), NOMS[r], font=F_CELL, fill=ENCRE)
        if b_vals[r]:
            d.text((XS[2] + 18, y), b_vals[r], font=F_CELL, fill=ENCRE)
        if c_vals[r]:
            d.text((XS[3] + 18, y), c_vals[r], font=F_CELL, fill=ENCRE)
    if selection:
        col, r = selection
        x1, y1 = XS[col], Y0 + RH * (r + 2)
        x2, y2 = XS[col + 1], y1 + RH
        d.rectangle((x1, y1, x2, y2), outline=VERT, width=7)
        d.rectangle((x2 - 12, y2 - 12, x2 + 8, y2 + 8), fill=VERT, outline=PAPIER, width=3)
        if curseur:
            vals = b_vals if col == 2 else c_vals
            w = d.textlength(vals[r] or "", font=F_CELL)
            d.line((x1 + 22 + w, y1 + 22, x1 + 22 + w, y1 + 78), fill=ENCRE, width=4)


def fond_feuille():
    im = Image.new("RGB", (W, H), (247, 250, 248))
    d = ImageDraw.Draw(im)
    marque(d, VERT_NUIT)
    return im, d


def frappe(mot, t, debut, pas=0.17):
    n = int(max(0, t - debut) / pas)
    return mot[: min(n, len(mot))]


def remplissage(vals, t, debut):
    """Révèle les lignes 2 à 6 en cascade à partir de `debut`."""
    out = [vals[0]] + [None] * 5
    for i in range(1, 6):
        if t >= debut + (i - 1) * 0.05:
            out[i] = vals[i]
    return out


# ---------- scènes : chacune renvoie une image pour l'instant t (secondes) ----------

def s_accroche(t):
    im = Image.new("RGB", (W, H), VERT_NUIT)
    d = ImageDraw.Draw(im)
    marque(d, PAPIER)
    k = ease(t / 0.35)
    y = 560 + int((1 - k) * 40)
    y = lignes_centrees(d, ["Vous retapez", "encore vos listes", "à la main ?"], F_HOOK, y, mix(VERT_NUIT, PAPIER, k))
    if t > 1.0:
        k2 = ease((t - 1.0) / 0.3)
        d.rounded_rectangle((150, y + 70, W - 150, y + 190), 16, fill=mix(VERT_NUIT, JAUNE, k2))
        lignes_centrees(d, ["Excel le fait en 2 touches"], F_SUB, y + 92, mix(VERT_NUIT, ENCRE, k2))
    return im


def s_taper(t):
    im, d = fond_feuille()
    lignes_centrees(d, ["Tapez le premier", "prénom"], F_CAPTION, 260, VERT_NUIT)
    mot = frappe("Camille", t, 0.8)
    fini = t > 2.6
    b = [mot] + [None] * 5
    tableau(d, b, [None] * 6, selection=(2, 1) if fini else (2, 0), curseur=not fini)
    return im


def s_ctrl_e(t):
    im, d = fond_feuille()
    lignes_centrees(d, ["Puis appuyez sur", "Ctrl + E"], F_CAPTION, 260, VERT_NUIT)
    appui = 1.2
    b = remplissage(PRENOMS, t, appui + 0.1)
    sur = (2, 1 - ease((t - appui - 0.5) / 1.2)) if t > appui + 0.1 else None
    tableau(d, b, [None] * 6, selection=(2, 1), surlignage=sur)
    if t > 0.4:
        touches(d, 1560, appui <= t < appui + 0.45)
    return im


def s_nom(t):
    im, d = fond_feuille()
    lignes_centrees(d, ["Pareil pour", "le nom"], F_CAPTION, 260, VERT_NUIT)
    mot = frappe("Martin", t, 0.5)
    appui = 2.3
    tape = t > 1.8
    c = remplissage(FAMILLE, t, appui + 0.1) if tape else [mot] + [None] * 5
    sur = (3, 1 - ease((t - appui - 0.5) / 1.2)) if t > appui + 0.1 else None
    tableau(d, PRENOMS, c, selection=(3, 1) if tape else (3, 0), surlignage=sur, curseur=not tape)
    if t > 1.9:
        touches(d, 1560, appui <= t < appui + 0.45)
    return im


def s_fin(t):
    im = Image.new("RGB", (W, H), VERT_NUIT)
    d = ImageDraw.Draw(im)
    marque(d, PAPIER)
    touches(d, 600, False, police=F_KEY_XL, clair=True, ecart=130)
    y = lignes_centrees(d, ["Remplissage", "instantané"], F_HOOK, 800, PAPIER)
    lignes_centrees(d, ["Excel 2013 et versions suivantes"], titre(44, 500), y + 20, (190, 214, 202))
    if t > 0.8:
        k = ease((t - 0.8) / 0.3)
        d.rounded_rectangle((90, 1190, W - 90, 1420), 18, fill=mix(VERT_NUIT, PAPIER, k))
        lignes_centrees(d, ["Sur Google Sheets :"], titre(42, 600), 1218, mix(VERT_NUIT, GRIS, k))
        lignes_centrees(d, ['=SPLIT(A2;" ")'], F_MONO, 1300, mix(VERT_NUIT, ENCRE, k))
    return im


SCENES = [(s_accroche, 2.6), (s_taper, 3.6), (s_ctrl_e, 4.2), (s_nom, 5.0), (s_fin, 4.0)]


def apercu(dossier):
    os.makedirs(dossier, exist_ok=True)
    for nom, (fn, t) in {"1": (s_accroche, 2.0), "2": (s_taper, 2.0), "3": (s_ctrl_e, 1.35),
                         "4": (s_nom, 4.5), "5": (s_fin, 3.0)}.items():
        fn(t).save(os.path.join(dossier, f"apercu_{nom}.png"))


def rendre():
    tmp = tempfile.mkdtemp()
    fichiers = []
    for i, (fn, duree) in enumerate(SCENES):
        part, final = os.path.join(tmp, f"s{i}.part.mp4"), os.path.join(tmp, f"s{i}.mp4")
        p = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-r", str(FPS), part], stdin=subprocess.PIPE)
        for n in range(int(round(duree * FPS))):
            p.stdin.write(fn(n / FPS).tobytes())
        p.stdin.close()
        if p.wait() != 0:
            raise SystemExit(f"ffmpeg a échoué sur la scène {i}")
        os.rename(part, final)
        fichiers.append(final)
    liste = os.path.join(tmp, "liste.txt")
    with open(liste, "w") as f:
        f.writelines(f"file '{x}'\n" for x in fichiers)
    muet = os.path.join(tmp, "muet.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", liste,
                    "-c", "copy", muet], check=True)
    # Piste audio silencieuse : certaines plateformes refusent les vidéos sans piste son.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", muet, "-f", "lavfi", "-i",
                    "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", SORTIE], check=True)


if __name__ == "__main__":
    if "--apercu" in sys.argv:
        apercu(sys.argv[sys.argv.index("--apercu") + 1])
    else:
        rendre()
