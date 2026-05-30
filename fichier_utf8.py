#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         ANALYSEUR DE FICHIERS UTF-8                 ║
║         Python 3.14.2                               ║
╚══════════════════════════════════════════════════════╝
"""

import os
import unicodedata

try:
    from colorama import init, Fore, Style
    init(autoreset=False, strip=False, convert=True)
    HAS_COLOR = True
except ImportError:
    class _D:
        def __getattr__(self, _): return ""
    Fore = Style = _D()
    HAS_COLOR = False

# ── Palette ──────────────────────────────
G  = Fore.GREEN  + Style.BRIGHT
Y  = Fore.YELLOW + Style.BRIGHT
C  = Fore.CYAN   + Style.BRIGHT
M  = Fore.MAGENTA
W  = Fore.WHITE
D  = Style.DIM   + Fore.WHITE
R  = Style.RESET_ALL
RE = Fore.RED    + Style.BRIGHT
LN = G + "=" * 55 + R

def sep():   print(LN)
def pause(): input(D + "\n  Appuyez sur Entrée..." + R)

def banner():
    print(G + """
╔══════════════════════════════════════════════════════╗
║         ANALYSEUR DE FICHIERS UTF-8                 ║
║         Python 3.14.2                               ║
╚══════════════════════════════════════════════════════╝""" + R)


# ════════════════════════════════════════════
#  FONCTION 1 — Lire un fichier UTF-8
# ════════════════════════════════════════════
def lire_fichier(chemin):
    """Lit un fichier et retourne son contenu"""
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
        print(G + f"  ✅ Fichier lu avec succès !" + R)
        return contenu
    except FileNotFoundError:
        print(RE + f"  ❌ Fichier introuvable : {chemin}" + R)
        return None
    except UnicodeDecodeError:
        print(RE + f"  ❌ Fichier non UTF-8 !" + R)
        print(Y  + f"  Essai avec Latin-1..." + R)
        try:
            with open(chemin, "r", encoding="latin-1") as f:
                contenu = f.read()
            print(G + f"  ✅ Lu en Latin-1 !" + R)
            return contenu
        except Exception as e:
            print(RE + f"  ❌ Erreur : {e}" + R)
            return None


# ════════════════════════════════════════════
#  FONCTION 2 — Détecter l'encodage
# ════════════════════════════════════════════
def detecter_encodage(chemin):
    """Détecte si un fichier est UTF-8, ASCII pur ou autre"""
    try:
        with open(chemin, "rb") as f:
            raw = f.read()

        # Vérif BOM UTF-8
        if raw.startswith(b'\xef\xbb\xbf'):
            return "UTF-8 avec BOM", raw[3:]

        # Vérif ASCII pur
        try:
            raw.decode("ascii")
            return "ASCII pur", raw
        except UnicodeDecodeError:
            pass

        # Vérif UTF-8
        try:
            raw.decode("utf-8")
            return "UTF-8", raw
        except UnicodeDecodeError:
            pass

        # Vérif Latin-1
        try:
            raw.decode("latin-1")
            return "Latin-1 (ISO-8859-1)", raw
        except UnicodeDecodeError:
            pass

        return "Inconnu", raw

    except FileNotFoundError:
        return "Fichier introuvable", b""


# ════════════════════════════════════════════
#  FONCTION 3 — Analyser le contenu
# ════════════════════════════════════════════
def analyser_contenu(contenu):
    """Analyse les caractères d'un texte"""
    stats = {1: [], 2: [], 3: [], 4: []}

    for c in contenu:
        if c in ("\n", "\r", "\t"):
            continue
        try:
            octets = c.encode("utf-8")
            n      = len(octets)
            stats[n].append(c)
        except Exception:
            pass

    return stats


# ════════════════════════════════════════════
#  FONCTION 4 — Sauvegarder le rapport
# ════════════════════════════════════════════
def sauvegarder_rapport(chemin_in, contenu, stats, encodage):
    """Sauvegarde un rapport d'analyse dans un fichier .txt"""
    chemin_out = chemin_in.replace(".txt", "_rapport.txt")

    total_car = sum(len(v) for v in stats.values())
    total_oct = sum(len(v) * n for n, v in stats.items())

    lignes = []
    lignes.append("=" * 55)
    lignes.append("  RAPPORT D'ANALYSE UTF-8")
    lignes.append("=" * 55)
    lignes.append(f"  Fichier   : {chemin_in}")
    lignes.append(f"  Encodage  : {encodage}")
    lignes.append(f"  Caractères: {total_car}")
    lignes.append(f"  Octets    : {total_oct}")
    lignes.append("=" * 55)

    labels = {
        1: "ASCII    (1 octet) ",
        2: "Latin    (2 octets)",
        3: "Symboles (3 octets)",
        4: "Emojis   (4 octets)",
    }
    for n in range(1, 5):
        chars  = stats[n]
        if not chars: continue
        nb_car = len(chars)
        nb_oct = nb_car * n
        pct    = nb_oct / total_oct * 100 if total_oct else 0
        uniq   = list(dict.fromkeys(chars))[:15]
        lignes.append(f"\n  {labels[n]}")
        lignes.append(f"    Caractères : {nb_car}  ({pct:.1f}%)")
        lignes.append(f"    Octets     : {nb_oct}")
        lignes.append(f"    Uniques    : {''.join(uniq)}")

    lignes.append("\n" + "=" * 55)
    lignes.append("  CONTENU DU FICHIER")
    lignes.append("=" * 55)
    lignes.append(contenu)

    try:
        with open(chemin_out, "w", encoding="utf-8") as f:
            f.write("\n".join(lignes))
        print(G + f"  ✅ Rapport sauvegardé : {chemin_out}" + R)
        return chemin_out
    except Exception as e:
        print(RE + f"  ❌ Erreur sauvegarde : {e}" + R)
        return None


# ════════════════════════════════════════════
#  PROGRAMME PRINCIPAL
# ════════════════════════════════════════════
def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    sep()

    # Chemin du fichier
    print(D + "  Exemple : C:\\PythonProjets\\test_utf8.txt\n" + R)
    chemin = input(W + "  Chemin du fichier : " + Y).strip()
    print(R)

    if not chemin:
        print(RE + "  Chemin vide !" + R)
        pause(); return

    sep()

    # Détection encodage
    encodage, raw = detecter_encodage(chemin)
    print(f"  {Y}Encodage détecté : {R}{G}{encodage}{R}")
    print(f"  {Y}Taille brute     : {R}{W}{len(raw)} octets{R}")
    sep()

    # Lecture
    contenu = lire_fichier(chemin)
    if not contenu:
        pause(); return

    # Analyse
    stats     = analyser_contenu(contenu)
    total_car = sum(len(v) for v in stats.values())
    total_oct = sum(len(v) * n for n, v in stats.items())

    print(f"\n  {G}Texte :{R}")
    print(f"  {W}{contenu[:100]}{'...' if len(contenu)>100 else ''}{R}")
    sep()

    print(f"  {Y}{'Caractères':<20}{R}: {W}{total_car}{R}")
    print(f"  {Y}{'Octets UTF-8':<20}{R}: {W}{total_oct}{R}")
    print(f"  {Y}{'Lignes':<20}{R}: {W}{contenu.count(chr(10))}{R}")
    sep()

    # Statistiques
    labels = {
        1: "ASCII    (1 octet) ",
        2: "Latin    (2 octets)",
        3: "Symboles (3 octets)",
        4: "Emojis   (4 octets)",
    }
    colors = {1: W, 2: C, 3: Y, 4: M}

    print(G + "  Répartition :\n" + R)
    for n in range(1, 5):
        chars = stats[n]
        if not chars: continue
        nb_car = len(chars)
        nb_oct = nb_car * n
        pct    = nb_oct / total_oct * 100
        bar    = "█" * int(pct / 4)
        uniq   = list(dict.fromkeys(chars))[:10]
        print(f"  {colors[n]}{labels[n]}{R}")
        print(f"    {Y}Caractères : {R}{W}{nb_car:4d}  ({pct:5.1f}%){R}")
        print(f"    {Y}Octets     : {R}{W}{nb_oct:4d}{R}")
        print(f"    {colors[n]}{bar}{R}")
        print(f"    {D}Uniques : {''.join(uniq)}{R}\n")

    # Caractère le plus lourd
    for n in [4, 3, 2]:
        if stats[n]:
            c   = stats[n][0]
            cp  = ord(c)
            try:    nom = unicodedata.name(c)
            except: nom = "?"
            print(f"  {Y}Plus lourd : {R}{G}{c}{R} "
                  f"{C}U+{cp:04X}{R} "
                  f"{W}({n} octets) — {nom}{R}")
            break

    sep()

    # Sauvegarder rapport
    reponse = input(W + "\n  Sauvegarder le rapport ? (o/n) : " + Y).strip().lower()
    print(R)
    if reponse == "o":
        sauvegarder_rapport(chemin, contenu, stats, encodage)

    sep()
    pause()


if __name__ == "__main__":
    main()