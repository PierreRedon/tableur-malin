"""Bande-son synthétique des vidéos Tableur Malin (aucun fichier externe, donc aucun droit musical).

bande_son(sortie_wav, duree, evenements) : fond musical doux + bruitages calés sur l'image.
evenements : liste de (type, instant en secondes depuis le début de la vidéo), avec les types
  "frappe" (un caractère tapé), "clic" (sélection à la souris), "touche" (raccourci ou Entrée),
  "pop" (apparition d'un bandeau), "carillon" (résultat qui apparaît), "fin" (carte de fin).
"""
import wave

import numpy as np

SR = 44100
rng = np.random.default_rng(7)
DUREE, N, mix = 0.0, 0, None

def ajoute(sig, t, gain=1.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i]
    mix[i:i + len(sig)] += sig * gain

def note(f, d, attaque=0.01, chute=4.0, harmo=(1, 0.35, 0.12)):
    t = np.arange(int(SR * d)) / SR
    s = sum(a * np.sin(2 * np.pi * f * (k + 1) * t) for k, a in enumerate(harmo))
    env = np.minimum(t / attaque, 1) * np.exp(-chute * t)
    return s * env

def nappe(f, d):
    t = np.arange(int(SR * d)) / SR
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t + 0.5)
    env = np.minimum(t / 0.5, 1) * np.minimum((d - t) / 0.6, 1)
    return s * env

def clic(aigu=1.0):
    d = 0.035
    t = np.arange(int(SR * d)) / SR
    b = rng.standard_normal(len(t)) * np.exp(-140 * t)
    return b * 0.5 + np.sin(2 * np.pi * 2100 * aigu * t) * np.exp(-110 * t) * 0.5

def touche():
    d = 0.09
    t = np.arange(int(SR * d)) / SR
    return (rng.standard_normal(len(t)) * np.exp(-70 * t) * 0.6 + np.sin(2 * np.pi * 320 * t) * np.exp(-45 * t))

def carillon(base=880.0):
    a = note(base, 0.9, chute=5)
    b = note(base * 1.5, 0.8, chute=5)
    a[int(0.07 * SR):int(0.07 * SR) + len(b)] += b[: len(a) - int(0.07 * SR)] * 0.8
    return a


M = {"C3": 130.81, "E3": 164.81, "G3": 196.0, "B3": 246.94, "A2": 110.0, "C4": 261.63, "E4": 329.63, "G4": 392.0,
     "F2": 87.31, "F3": 174.61, "A3": 220.0, "G2": 98.0, "D3": 146.83, "D4": 293.66, "B4": 493.88, "A4": 440.0,
     "C5": 523.25, "E5": 659.25, "D5": 587.33, "G5": 783.99}
ACCORDS = [(["C3", "G3", "B3", "E4"], ["E5", "G4", "C5", "G4"]), (["A2", "E3", "G3", "C4"], ["C5", "E4", "A4", "E4"]),
           (["F2", "F3", "A3", "E4"], ["A4", "C5", "E5", "C5"]), (["G2", "D3", "G3", "D4"], ["D5", "B4", "G4", "B4"])]


def bande_son(sortie_wav, duree, evenements):
    global DUREE, N, mix
    DUREE, N = duree, int(SR * duree)
    mix = np.zeros(N)
    # --- fond musical : Do maj7, La min7, Fa maj7, Sol, 96 à la minute ---
    temps = 60 / 96
    t0, i = 0.0, 0
    while t0 < DUREE:
        acc, arp = ACCORDS[i % 4]
        for n in acc:
            ajoute(nappe(M[n], temps * 4 + 0.4), t0, 0.035)
        for j in range(8):
            ajoute(note(M[arp[j % 4]], 0.5, chute=7), t0 + j * temps / 2, 0.06)
        t0 += temps * 4; i += 1
    for genre, t in evenements:
        if genre == "frappe":
            ajoute(clic(1 + 0.1 * rng.random()), t, 0.18)
        elif genre == "clic":
            ajoute(clic(), t, 0.3)
        elif genre == "touche":
            ajoute(touche(), t, 0.45)
        elif genre == "pop":
            ajoute(note(660, 0.3, chute=12), t, 0.2)
        elif genre == "carillon":
            ajoute(carillon(), t, 0.22)
        elif genre == "fin":
            ajoute(note(523.25, 1.6, chute=2.5), t, 0.16)
            ajoute(note(783.99, 1.6, chute=2.5), t + 0.06, 0.12)
        else:
            raise ValueError(f"bruitage inconnu : {genre}")
    t = np.arange(N) / SR
    mix *= np.minimum(1, (DUREE - t) / 1.2).clip(0, 1) * np.minimum(1, t / 0.15)
    pcm = (mix / np.abs(mix).max() * 0.5 * 32767).astype("<i2")
    with wave.open(sortie_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.repeat(pcm, 2).tobytes())
