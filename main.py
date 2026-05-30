#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme principal — utilise utf8_package
"""

import os
import sys
sys.path.insert(0,
    r"C:\PythonProjets")

try:
    from colorama import init, Fore, Style
    init(autoreset=False, strip=False,
         convert=True)
except ImportError:
    class _D:
        def __getattr__(self, _): return ""
    Fore = Style = _D()

# ── Import du package ────────────────────
from utf8_package import (
    encoder_texte,
    decoder_hex,
    analyser_char,
    analyser_texte,
    comparer,
)
from utf8_package import __version__

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
def pause(): input(D+"\n  Entrée..."+R)

def main():
    os.system("cls" if os.name=="nt"
              else "clear")
    print(G + f"""
╔══════════════════════════════════════════════════════╗
║         UTF-8 Package v{__version__}                      ║
║         Modules et Packages Python                  ║
╚══════════════════════════════════════════════════════╝""" + R)

    # ── Test 1 : encoder ─────────────────
    sep()
    print(Y + "  [1] encoder_texte()\n" + R)
    res = encoder_texte("Bonjour 🌍 été ™")
    print(f"  {W}Texte    : {G}{res['texte']}{R}")
    print(f"  {W}Hex      : {C}{res['hex']}{R}")
    print(f"  {W}Chars    : {W}{res['nb_chars']}{R}")
    print(f"  {W}Octets   : {W}{res['nb_octets']}{R}")
    print()
    for d in res["details"]:
        print(f"    {Y}{d['char']}{R}  "
              f"{C}U+{d['cp']:04X}{R}  "
              f"{W}{d['hex']}{R}")

    # ── Test 2 : decoder ─────────────────
    sep()
    print(Y + "  [2] decoder_hex()\n" + R)
    res = decoder_hex(
        "C3 A9 20 E2 82 AC 20 F0 9F 90 8D")
    for d in res["details"]:
        print(f"    {C}{d['hex']:<15}{R}"
              f"→ {Y}{d['char']}{R}  "
              f"{W}U+{d['cp']:04X}{R}")
    print(f"\n  {G}Texte : {res['texte']}{R}")

    # ── Test 3 : analyser ────────────────
    sep()
    print(Y + "  [3] analyser_char()\n" + R)
    for c in ["A", "é", "€", "🐍"]:
        res = analyser_char(c)
        print(f"  {Y}{res['char']}{R}  "
              f"{C}U+{res['cp']:04X}{R}  "
              f"{W}{res['hex']:<12}{R}  "
              f"{D}{res['nom']}{R}")

    # ── Test 4 : stats ───────────────────
    sep()
    print(Y + "  [4] analyser_texte()\n" + R)
    res  = analyser_texte(
        "Bonjour 🌍 c'est l'été ™ !")
    labels = {1:"ASCII ",2:"Latin ",
              3:"Symb. ",4:"Emoji "}
    colors = {1:W, 2:C, 3:Y, 4:M}
    print(f"  {W}Chars   : {res['nb_chars']}{R}")
    print(f"  {W}Octets  : {res['nb_octets']}{R}")
    print(f"  {W}ASCII%  : "
          f"{res['pct_ascii']:.1f}%{R}\n")
    for n in range(1,5):
        chars = res["types"][n]
        if not chars: continue
        bar = "█" * len(chars)
        print(f"  {colors[n]}{labels[n]}{R} "
              f"{W}{len(chars):3d}{R}  {bar}")

    # ── Test 5 : comparer ────────────────
    sep()
    print(Y + "  [5] comparer()\n" + R)
    res = comparer("café", "cafe")
    print(f"  {W}café ({res['oct1']} oct) "
          f"vs cafe ({res['oct2']} oct){R}")
    for d in res["differences"]:
        print(f"  {Y}Pos {d['pos']}{R} : "
              f"{G}{d['c1'] or '—'}{R} "
              f"{d['h1']} "
              f"{RE}≠{R} "
              f"{G}{d['c2'] or '—'}{R} "
              f"{d['h2']}")

    sep()
    print(G + "  Package utf8_package "
          f"v{__version__} ✅\n" + R)
    pause()


if __name__ == "__main__":
    main()