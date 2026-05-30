#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         UTF-8 INTERACTIF — Python 3.14.2            ║
║         Encodeur + Décodeur manuel                  ║
╚══════════════════════════════════════════════════════╝
"""

import os
import unicodedata

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=False, strip=False, convert=True)
    HAS_COLOR = True
except ImportError:
    class _D:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _D()
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

# ── Helpers ──────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def sep():   print(LN)
def pause(): input(D + "\n  Appuyez sur Entrée..." + R)

def banner():
    print(G + """
╔══════════════════════════════════════════════════════╗
║         UTF-8 INTERACTIF — Python 3.14.2            ║
║         Encodeur + Décodeur manuel                  ║
╚══════════════════════════════════════════════════════╝""" + R)


# ════════════════════════════════════════════
#  NOYAU — ENCODEUR
# ════════════════════════════════════════════
def encode_utf8_manuel(caractere):
    cp = ord(caractere)
    if cp <= 127:
        return [cp]
    elif cp <= 2047:
        return [
            0b11000000 | (cp >> 6),
            0b10000000 | (cp & 0b00111111)
        ]
    elif cp <= 65535:
        return [
            0b11100000 | (cp >> 12),
            0b10000000 | ((cp >> 6)  & 0b00111111),
            0b10000000 | (cp & 0b00111111)
        ]
    else:
        return [
            0b11110000 | (cp >> 18),
            0b10000000 | ((cp >> 12) & 0b00111111),
            0b10000000 | ((cp >> 6)  & 0b00111111),
            0b10000000 | (cp & 0b00111111)
        ]


# ════════════════════════════════════════════
#  NOYAU — DÉCODEUR
# ════════════════════════════════════════════
def decoder_utf8(octets):
    b = octets[0]
    if b & 0b10000000 == 0:
        cp = b
    elif b & 0b11100000 == 0b11000000:
        cp = ((b          & 0b00011111) << 6) \
           | (octets[1]   & 0b00111111)
    elif b & 0b11110000 == 0b11100000:
        cp = ((b          & 0b00001111) << 12) \
           | ((octets[1]  & 0b00111111) << 6)  \
           | (octets[2]   & 0b00111111)
    else:
        cp = ((b          & 0b00000111) << 18) \
           | ((octets[1]  & 0b00111111) << 12) \
           | ((octets[2]  & 0b00111111) << 6)  \
           | (octets[3]   & 0b00111111)
    return cp


# ════════════════════════════════════════════
#  MODULE 1 — Encoder un texte
# ════════════════════════════════════════════
def mod_encoder():
    clear(); banner()
    print(G + "\n  MODULE 1 — Texte → UTF-8\n" + R)
    sep()
    texte = input(W + "  Entrez votre texte : " + Y).strip()
    print(R)
    if not texte:
        print(RE + "  Texte vide !" + R)
        pause(); return

    tous_octets = []
    sep()
    print(G + f"  Texte      : {texte}")
    print(G + f"  Caractères : {len(texte)}\n" + R)

    for c in texte:
        cp      = ord(c)
        octets  = encode_utf8_manuel(c)
        tous_octets.extend(octets)
        hex_c   = " ".join(f"{b:02X}" for b in octets)
        bin_c   = " ".join(f"{b:08b}" for b in octets)
        try:
            nom = unicodedata.name(c)
        except:
            nom = ""

        print(f"  {Y}{c}{R}  "
              f"{C}U+{cp:04X}{R}  "
              f"{W}{hex_c:<12}{R}  "
              f"{D}{bin_c}{R}")
        if nom:
            print(f"  {D}     → {nom}{R}")

    sep()
    hex_total = " ".join(f"{b:02X}" for b in tous_octets)
    verif     = " ".join(f"{b:02X}" for b in texte.encode("utf-8"))
    ok        = "✅" if hex_total == verif else "❌"

    print(f"\n  {Y}Séquence complète :{R}")
    print(f"  {C}{hex_total}{R}")
    print(f"\n  {Y}Total octets : {R}{W}{len(tous_octets)}{R}")
    print(f"  {Y}Vérification : {R}{ok}")
    sep()
    pause()


# ════════════════════════════════════════════
#  MODULE 2 — Décoder une séquence hex
# ════════════════════════════════════════════
def mod_decoder():
    clear(); banner()
    print(G + "\n  MODULE 2 — UTF-8 hex → Texte\n" + R)
    sep()
    print(D + "  Exemple : C3 A9 20 E2 82 AC 20 F0 9F 90 8D\n" + R)
    hex_in = input(W + "  Entrez la séquence hex : " + Y).strip()
    print(R)
    if not hex_in:
        print(RE + "  Séquence vide !" + R)
        pause(); return

    try:
        octets = [int(x, 16) for x in hex_in.split()]
    except ValueError:
        print(RE + "  Hex invalide !" + R)
        pause(); return

    resultat = ""
    i = 0
    sep()
    print(G + f"  Séquence : {hex_in}\n" + R)

    while i < len(octets):
        b = octets[i]
        if   b & 0b10000000 == 0:             n = 1
        elif b & 0b11100000 == 0b11000000:    n = 2
        elif b & 0b11110000 == 0b11100000:    n = 3
        else:                                  n = 4

        seq  = octets[i:i+n]
        cp   = decoder_utf8(seq)
        char = chr(cp)
        resultat += char
        hex_seq  = " ".join(f"{b:02X}" for b in seq)
        bin_seq  = " ".join(f"{b:08b}" for b in seq)
        try:
            nom = unicodedata.name(char)
        except:
            nom = ""

        print(f"  {C}{hex_seq:<15}{R}→  "
              f"{Y}{char}{R}  "
              f"{W}U+{cp:04X}{R}  "
              f"{D}{n} octet(s){R}")
        if nom:
            print(f"  {D}     → {nom}{R}")
        i += n

    sep()
    print(f"\n  {Y}Texte décodé : {R}{G}{resultat}{R}")
    print(f"  {Y}Caractères   : {R}{W}{len(resultat)}{R}")
    sep()
    pause()


# ════════════════════════════════════════════
#  MODULE 3 — Analyser un seul caractère
# ════════════════════════════════════════════
def mod_analyser():
    clear(); banner()
    print(G + "\n  MODULE 3 — Analyser un caractère\n" + R)
    sep()
    c = input(W + "  Entrez un caractère : " + Y).strip()
    print(R)
    if not c:
        print(RE + "  Vide !" + R); pause(); return

    c  = c[0]
    cp = ord(c)
    octets  = encode_utf8_manuel(c)
    hex_str = " ".join(f"{b:02X}" for b in octets)
    bin_str = " ".join(f"{b:08b}" for b in octets)
    ri      = int.from_bytes(bytes(octets), "big")
    try:    nom = unicodedata.name(c)
    except: nom = "(pas de nom)"
    cat = unicodedata.category(c)

    sep()
    print(f"  {Y}{'Caractère':<20}{R}: {G}{c}{R}")
    print(f"  {Y}{'Codepoint':<20}{R}: {C}U+{cp:04X}{R}")
    print(f"  {Y}{'Décimal':<20}{R}: {M}{cp:,}".replace(",", " ") + R)
    print(f"  {Y}{'Hex UTF-8':<20}{R}: {Y}{hex_str}{R}")
    print(f"  {Y}{'Binaire':<20}{R}: {C}{bin_str}{R}")
    print(f"  {Y}{'Octets':<20}{R}: {W}{len(octets)}{R}")
    print(f"  {Y}{'Décimal brut':<20}{R}: {M}{ri:,}".replace(",", " ") + R)
    print(f"  {Y}{'Nom Unicode':<20}{R}: {W}{nom}{R}")
    print(f"  {Y}{'Catégorie':<20}{R}: {D}{cat}{R}")
    sep()
    pause()


# ════════════════════════════════════════════
#  MODULE 4 — Quiz interactif
# ════════════════════════════════════════════
import random

QUIZ_DATA = [
    ("é", "C3 A9"), ("€", "E2 82 AC"), ("ç", "C3 A7"),
    ("à", "C3 A0"), ("ñ", "C3 B1"),   ("ü", "C3 BC"),
    ("™", "E2 84 A2"), ("♥", "E2 99 A5"), ("Ω", "CE A9"),
    ("œ", "C5 93"), ("ß", "C3 9F"),   ("î", "C3 AE"),
]

def mod_quiz():
    clear(); banner()
    print(G + "\n  MODULE 4 — Quiz UTF-8 ⚡\n" + R)
    sep()
    score = 0
    total = 5
    questions = random.sample(QUIZ_DATA, total)

    for i, (char, hex_correct) in enumerate(questions, 1):
        cp = ord(char)
        print(f"\n  {Y}Question {i}/{total}{R}")
        print(f"  Quel est le hex UTF-8 de "
              f"{G}{char}{R} (U+{cp:04X}) ?")
        print(D + "  (séparés par espaces, ex: C3 A9)\n" + R)

        reponse = input(W + "  Votre réponse : " + Y).strip().upper()
        print(R)

        if reponse == hex_correct.upper():
            print(G + f"  ✅ Correct ! {char} = {hex_correct}" + R)
            score += 1
        else:
            print(RE + f"  ❌ Incorrect !" + R)
            print(W  + f"     Correct : {hex_correct}" + R)
            print(W  + f"     Votre   : {reponse}" + R)
        sep()

    print(f"\n  {G}Score : {score}/{total}{R}")
    if score == total:
        print(G + "  PARFAIT ! 🏆" + R)
    elif score >= 3:
        print(Y + "  Bien joué ! 💪" + R)
    else:
        print(RE + "  Continuez à pratiquer ! 📚" + R)
    sep()
    pause()
    
    
    # ════════════════════════════════════════════
#  MODULE 5 — Comparer deux textes
# ════════════════════════════════════════════
def mod_comparer():
    clear(); banner()
    print(G + "\n  MODULE 5 — Comparer deux textes\n" + R)
    sep()
    print(D + "  Exemple : café  vs  cafe\n" + R)
    texte1 = input(W + "  Texte 1 : " + Y).strip()
    texte2 = input(W + "  Texte 2 : " + Y).strip()
    print(R)
    if not texte1 or not texte2:
        print(RE + "  Texte vide !" + R)
        pause(); return

    sep()
    print(G + f"  Comparaison : {texte1}  vs  {texte2}\n" + R)

    # Octets de chaque texte
    oct1 = list(texte1.encode("utf-8"))
    oct2 = list(texte2.encode("utf-8"))
    hex1 = " ".join(f"{b:02X}" for b in oct1)
    hex2 = " ".join(f"{b:02X}" for b in oct2)

    print(f"  {Y}{'Texte 1':<12}{R}: {G}{texte1}{R}")
    print(f"  {Y}{'Hex UTF-8':<12}{R}: {C}{hex1}{R}")
    print(f"  {Y}{'Octets':<12}{R}: {W}{len(oct1)}{R}")
    print()
    print(f"  {Y}{'Texte 2':<12}{R}: {G}{texte2}{R}")
    print(f"  {Y}{'Hex UTF-8':<12}{R}: {C}{hex2}{R}")
    print(f"  {Y}{'Octets':<12}{R}: {W}{len(oct2)}{R}")
    sep()

    # Comparaison caractère par caractère
    print(G + "  Différences caractère par caractère :\n" + R)
    print(f"  {Y}{'Car':<6}{'Texte 1':<20}{'Texte 2':<20}{'Diff'}{R}")
    print(D + "  " + "─" * 55 + R)

    max_len = max(len(texte1), len(texte2))
    differences = 0
    for i in range(max_len):
        c1 = texte1[i] if i < len(texte1) else "—"
        c2 = texte2[i] if i < len(texte2) else "—"

        if c1 != "—":
            h1 = " ".join(f"{b:02X}"
                 for b in encode_utf8_manuel(c1))
        else:
            h1 = "—"
        if c2 != "—":
            h2 = " ".join(f"{b:02X}"
                 for b in encode_utf8_manuel(c2))
        else:
            h2 = "—"

        if c1 == c2:
            diff = G + "=" + R
            couleur = W
        else:
            diff = RE + "≠" + R
            couleur = Y
            differences += 1

        print(f"  {couleur}{i+1:<6}{c1:<6}{h1:<14}{c2:<6}{h2:<14}{R}{diff}")

    sep()
    if differences == 0:
        print(G + "  Textes identiques en UTF-8 ! ✅" + R)
    else:
        print(Y  + f"  {differences} différence(s) trouvée(s)" + R)
        diff_oct = abs(len(oct1) - len(oct2))
        print(W  + f"  Différence en octets : {diff_oct}" + R)
    sep()
    pause()


# ════════════════════════════════════════════
#  MODULE 6 — Statistiques d'un texte
# ════════════════════════════════════════════
def mod_stats():
    clear(); banner()
    print(G + "\n  MODULE 6 — Statistiques UTF-8 📊\n" + R)
    sep()
    texte = input(W + "  Entrez votre texte : " + Y).strip()
    print(R)
    if not texte:
        print(RE + "  Texte vide !" + R)
        pause(); return

    # Calculs
    stats = {1: [], 2: [], 3: [], 4: []}
    total_octets = 0
    char_lourd   = ("", 0)

    for c in texte:
        octets = encode_utf8_manuel(c)
        n      = len(octets)
        stats[n].append(c)
        total_octets += n
        if n > char_lourd[1]:
            char_lourd = (c, n)

    sep()
    print(G + f"  Texte      : {texte}")
    print(G + f"  Caractères : {len(texte)}")
    print(G + f"  Octets     : {total_octets}\n" + R)

    # Tableau par type
    labels = {
        1: "ASCII    (1 octet) ",
        2: "Latin    (2 octets)",
        3: "Symboles (3 octets)",
        4: "Emojis   (4 octets)",
    }
    colors = {1: W, 2: C, 3: Y, 4: M}

    for n in range(1, 5):
        chars  = stats[n]
        nb_car = len(chars)
        nb_oct = nb_car * n
        if nb_car == 0:
            continue
        pct_car = nb_car / len(texte)   * 100
        pct_oct = nb_oct / total_octets * 100
        bar_len = int(pct_oct / 5)
        bar     = "█" * bar_len

        print(f"  {colors[n]}{labels[n]}{R}")
        print(f"    {Y}Caractères : {R}{W}{nb_car:3d}"
              f"  ({pct_car:5.1f}%){R}")
        print(f"    {Y}Octets     : {R}{W}{nb_oct:3d}"
              f"  ({pct_oct:5.1f}%){R}")
        print(f"    {colors[n]}{bar}{R}")
        if chars:
            sample = " ".join(chars[:10])
            print(f"    {D}Exemples : {sample}{R}")
        print()

    sep()
    # Caractère le plus lourd
    if char_lourd[0]:
        cp = ord(char_lourd[0])
        try:    nom = unicodedata.name(char_lourd[0])
        except: nom = "?"
        print(f"  {Y}Caractère le plus lourd :{R} "
              f"{G}{char_lourd[0]}{R} "
              f"{C}U+{cp:04X}{R} "
              f"{W}({char_lourd[1]} octets){R}")
        print(f"  {D}{nom}{R}")

    # Efficacité encodage
    ascii_only = sum(1 for c in texte if ord(c) <= 127)
    pct_ascii  = ascii_only / len(texte) * 100
    print(f"\n  {Y}Efficacité ASCII : {R}"
          f"{W}{pct_ascii:.1f}%{R} "
          f"des caractères sont ASCII pur")

    # Code Python généré
    sep()
    print(G + "  Code Python équivalent :\n" + R)
    print(D + f'  texte  = "{texte}"' + R)
    print(D + f'  octets = texte.encode("utf-8")'  + R)
    print(D + f'  # → {len(total_octets if False else list(texte.encode("utf-8")))} octets au total' + R)
    sep()
    pause()


MENU = [
    ("1", "Encoder   — Texte → UTF-8 hex",       mod_encoder),
    ("2", "Décoder   — UTF-8 hex → Texte",        mod_decoder),
    ("3", "Analyser  — Un caractère complet",     mod_analyser),
    ("4", "Quiz      — Testez vos connaissances", mod_quiz),
    ("5", "Comparer  — Deux textes côte à côte",  mod_comparer),
    ("6", "Stats     — Statistiques d'un texte",  mod_stats),
    ("0", "Quitter",                               None),
]

def main():
    while True:
        clear(); banner()
        print(G + "  Choisissez un module :\n" + R)
        for key, label, _ in MENU:
            if key == "0": print()
            print(f"  {Y}[{key}]{R} {W}{label}{R}")
        print(LN)
        choix = input(C + "\n  → " + R).strip()
        for key, _, fn in MENU:
            if choix == key:
                if fn is None:
                    clear()
                    print(G + "\n  Au revoir ! 🐍\n" + R)
                    exit(0)
                fn(); break
        else:
            print(RE + "  Option invalide !" + R)
            pause()

if __name__ == "__main__":
    main()