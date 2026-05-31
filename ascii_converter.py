#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║           CONVERTISSEUR ASCII COMPLET — Python 3.14.2           ║
║                     Powered by Colorama                         ║
╚══════════════════════════════════════════════════════════════════╝

Installation des dépendances :
    pip install colorama

Utilisation :
    python ascii_converter.py
"""

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_OK = True
except ImportError:
    COLORAMA_OK = False
    # Fallback : classes vides si colorama n'est pas installé
    class _Dummy:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _Dummy()
    print("[AVERTISSEMENT] colorama non installé. Lancez : pip install colorama")

import sys
import os


# ─────────────────────────────────────────────
#  NOMS DES CARACTÈRES DE CONTRÔLE ASCII
# ─────────────────────────────────────────────
CTRL_NAMES = [
    "NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
    "BS",  "HT",  "LF",  "VT",  "FF",  "CR",  "SO",  "SI",
    "DLE", "DC1", "DC2", "DC3", "DC4", "NAK", "SYN", "ETB",
    "CAN", "EM",  "SUB", "ESC", "FS",  "GS",  "RS",  "US",
]

CTRL_DESC = [
    "Null",                 "Start of Heading",     "Start of Text",
    "End of Text",          "End of Transmission",  "Enquiry",
    "Acknowledge",          "Bell",                 "Backspace",
    "Horizontal Tab",       "Line Feed",            "Vertical Tab",
    "Form Feed",            "Carriage Return",      "Shift Out",
    "Shift In",             "Data Link Escape",     "Device Control 1",
    "Device Control 2",     "Device Control 3",     "Device Control 4",
    "Neg. Acknowledge",     "Synchronous Idle",     "End Trans. Block",
    "Cancel",               "End of Medium",        "Substitute",
    "Escape",               "File Separator",       "Group Separator",
    "Record Separator",     "Unit Separator",
]


# ─────────────────────────────────────────────
#  UTILITAIRES D'AFFICHAGE
# ─────────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    print(Fore.GREEN + Style.BRIGHT + """
╔══════════════════════════════════════════════════════════════════╗
║           CONVERTISSEUR ASCII COMPLET — Python 3.14.2           ║
║                     Powered by Colorama                         ║
╚══════════════════════════════════════════════════════════════════╝""")
    print(Style.RESET_ALL)


def header(title: str):
    print(Fore.YELLOW + Style.BRIGHT + f"\n  ══ {title} ══" + Style.RESET_ALL)


def success(msg: str):
    print(Fore.GREEN + f"  ✔  {msg}" + Style.RESET_ALL)


def error(msg: str):
    print(Fore.RED + f"  ✘  {msg}" + Style.RESET_ALL)


def info(label: str, value: str, color=Fore.CYAN):
    print(f"  {Fore.WHITE}{label:<12}{Style.RESET_ALL}: {color}{value}{Style.RESET_ALL}")


def separator():
    print(Fore.GREEN + Style.DIM + "  " + "─" * 62 + Style.RESET_ALL)


def menu_item(key: str, label: str):
    print(f"  {Fore.CYAN}[{key}]{Style.RESET_ALL} {Fore.WHITE}{label}{Style.RESET_ALL}")


def pause():
    input(Fore.WHITE + Style.DIM + "\n  Appuyez sur Entrée pour continuer..." + Style.RESET_ALL)


# ─────────────────────────────────────────────
#  FONCTIONS DE CONVERSION
# ─────────────────────────────────────────────

def char_name(code: int) -> str:
    if code < 32:
        return f"{CTRL_NAMES[code]} — {CTRL_DESC[code]}"
    if code == 32:
        return "Space"
    if code == 127:
        return "DEL — Delete"
    return ""


def inspect_char(c: str) -> dict:
    code = ord(c)
    return {
        "char":    c if 32 <= code < 127 else f"<{char_name(code) or code}>",
        "decimal": code,
        "hex":     f"0x{code:02X}",
        "octal":   f"0o{code:03o}",
        "binary":  f"0b{code:08b}",
        "html":    f"&#{code};",
        "unicode": f"U+{code:04X}",
        "name":    char_name(code),
    }


def text_to_codes(text: str, base: str = "all") -> None:
    """Convertit un texte en ses représentations numériques."""
    if not text:
        error("Texte vide.")
        return

    codes = [ord(c) for c in text]

    if base in ("all", "dec"):
        info("Décimal", " ".join(str(c) for c in codes), Fore.GREEN)
    if base in ("all", "hex"):
        info("Hexadécimal", " ".join(f"0x{c:02X}" for c in codes), Fore.CYAN)
    if base in ("all", "bin"):
        info("Binaire", " ".join(f"{c:08b}" for c in codes), Fore.YELLOW)
    if base in ("all", "oct"):
        info("Octal", " ".join(f"0o{c:03o}" for c in codes), Fore.MAGENTA)
    if base in ("all", "html"):
        info("HTML entities", "".join(f"&#{c};" for c in codes), Fore.BLUE)


def codes_to_text(codes_str: str, base: int) -> str:
    """Convertit une suite de codes vers du texte."""
    base_map = {2: "binaire", 8: "octal", 10: "décimal", 16: "hexadécimal"}
    tokens = codes_str.strip().split()
    result = []
    for tok in tokens:
        tok = tok.replace("0x", "").replace("0b", "").replace("0o", "")
        try:
            result.append(chr(int(tok, base)))
        except (ValueError, OverflowError):
            result.append("?")
    return "".join(result)


# ─────────────────────────────────────────────
#  MODULE 1 : TEXTE → CODES
# ─────────────────────────────────────────────

def module_text_to_codes():
    clear(); banner()
    header("MODULE 1 — TEXTE → CODES ASCII")
    text = input(Fore.WHITE + "  Entrez votre texte : " + Fore.GREEN).strip()
    print(Style.RESET_ALL)
    if not text:
        error("Aucun texte saisi."); pause(); return
    separator()
    text_to_codes(text, "all")
    separator()
    pause()


# ─────────────────────────────────────────────
#  MODULE 2 : CODES → TEXTE
# ─────────────────────────────────────────────

def module_codes_to_text():
    clear(); banner()
    header("MODULE 2 — CODES → TEXTE")
    print(f"  {Fore.WHITE}Base :{Style.RESET_ALL}")
    menu_item("1", "Décimal     (ex: 72 101 108 108 111)")
    menu_item("2", "Hexadécimal (ex: 48 65 6C 6C 6F)")
    menu_item("3", "Binaire     (ex: 01001000 01100101)")
    menu_item("4", "Octal       (ex: 110 145 154 154 157)")
    choice = input(Fore.CYAN + "\n  Votre choix : " + Style.RESET_ALL).strip()
    base_map = {"1": 10, "2": 16, "3": 2, "4": 8}
    if choice not in base_map:
        error("Choix invalide."); pause(); return
    base = base_map[choice]
    codes_str = input(Fore.WHITE + "  Entrez les codes (séparés par des espaces) : " + Fore.GREEN).strip()
    print(Style.RESET_ALL)
    result = codes_to_text(codes_str, base)
    separator()
    info("Résultat", result, Fore.GREEN + Style.BRIGHT)
    separator()
    pause()


# ─────────────────────────────────────────────
#  MODULE 3 : INSPECTER UN CARACTÈRE
# ─────────────────────────────────────────────

def module_inspect():
    clear(); banner()
    header("MODULE 3 — INSPECTER UN CARACTÈRE / UNE CHAÎNE")
    text = input(Fore.WHITE + "  Entrez un ou plusieurs caractères : " + Fore.CYAN).strip()
    print(Style.RESET_ALL)
    if not text:
        error("Aucun caractère saisi."); pause(); return
    separator()
    for c in text:
        data = inspect_char(c)
        label = Fore.CYAN + Style.BRIGHT + f"  Caractère : '{data['char']}'" + Style.RESET_ALL
        if data["name"]:
            label += Fore.WHITE + Style.DIM + f"  ({data['name']})" + Style.RESET_ALL
        print(label)
        info("  Décimal  ", str(data["decimal"]), Fore.GREEN)
        info("  Hex      ", data["hex"], Fore.CYAN)
        info("  Octal    ", data["octal"], Fore.MAGENTA)
        info("  Binaire  ", data["binary"], Fore.YELLOW)
        info("  HTML     ", data["html"], Fore.BLUE)
        info("  Unicode  ", data["unicode"], Fore.WHITE)
        separator()
    pause()


# ─────────────────────────────────────────────
#  MODULE 4 : TABLE ASCII
# ─────────────────────────────────────────────

def module_table():
    clear(); banner()
    header("MODULE 4 — TABLE ASCII COMPLÈTE")
    print(f"  {Fore.WHITE}Afficher :{Style.RESET_ALL}")
    menu_item("1", "Caractères de contrôle (0–31 + 127)")
    menu_item("2", "Caractères imprimables (32–126)")
    menu_item("3", "ASCII étendu          (128–255)")
    menu_item("4", "Table complète        (0–255)")
    choice = input(Fore.CYAN + "\n  Votre choix : " + Style.RESET_ALL).strip()
    ranges = {
        "1": range(0, 32),
        "2": range(32, 127),
        "3": range(128, 256),
        "4": range(0, 256),
    }
    if choice not in ranges:
        error("Choix invalide."); pause(); return

    rng = ranges[choice]
    print()
    # En-tête
    print(Fore.YELLOW + Style.BRIGHT +
          f"  {'DÉC':>4}  {'HEX':>4}  {'OCT':>4}  {'BIN':>10}  {'CAR':>4}  NOM" +
          Style.RESET_ALL)
    separator()

    for i in rng:
        if i == 127:
            chr_display = "DEL"
            name = "Delete"
        elif i < 32:
            chr_display = CTRL_NAMES[i]
            name = CTRL_DESC[i]
        else:
            try:
                chr_display = chr(i)
            except Exception:
                chr_display = "?"
            name = ""

        color = Fore.WHITE
        if i < 32 or i == 127:
            color = Fore.RED + Style.DIM
        elif i < 128:
            color = Fore.GREEN
        else:
            color = Fore.CYAN

        print(color +
              f"  {i:>4}  {i:>4X}h  {i:>4o}o  {i:>010b}  {chr_display:>4}  {name}" +
              Style.RESET_ALL)

    separator()
    pause()


# ─────────────────────────────────────────────
#  MODULE 5 : DÉMO COLORAMA
# ─────────────────────────────────────────────

def module_colorama_demo():
    clear(); banner()
    header("MODULE 5 — DÉMO COLORAMA")
    separator()

    # Couleurs de premier plan
    print(f"  {Fore.WHITE + Style.BRIGHT}── FOREGROUND (texte) ──{Style.RESET_ALL}")
    colors_fg = [
        (Fore.BLACK   + Back.WHITE, "Fore.BLACK   "),
        (Fore.RED,                  "Fore.RED     "),
        (Fore.GREEN,                "Fore.GREEN   "),
        (Fore.YELLOW,               "Fore.YELLOW  "),
        (Fore.BLUE,                 "Fore.BLUE    "),
        (Fore.MAGENTA,              "Fore.MAGENTA "),
        (Fore.CYAN,                 "Fore.CYAN    "),
        (Fore.WHITE,                "Fore.WHITE   "),
    ]
    for code, name in colors_fg:
        print(f"  {code}{name}  Bonjour depuis Python !{Style.RESET_ALL}")

    separator()

    # Couleurs de fond
    print(f"  {Fore.WHITE + Style.BRIGHT}── BACKGROUND (fond) ──{Style.RESET_ALL}")
    colors_bg = [
        (Back.BLACK   + Fore.WHITE,   "Back.BLACK   "),
        (Back.RED     + Fore.WHITE,   "Back.RED     "),
        (Back.GREEN   + Fore.BLACK,   "Back.GREEN   "),
        (Back.YELLOW  + Fore.BLACK,   "Back.YELLOW  "),
        (Back.BLUE    + Fore.WHITE,   "Back.BLUE    "),
        (Back.MAGENTA + Fore.WHITE,   "Back.MAGENTA "),
        (Back.CYAN    + Fore.BLACK,   "Back.CYAN    "),
        (Back.WHITE   + Fore.BLACK,   "Back.WHITE   "),
    ]
    for code, name in colors_bg:
        print(f"  {code}{name}  Bonjour depuis Python !{Style.RESET_ALL}")

    separator()

    # Styles
    print(f"  {Fore.WHITE + Style.BRIGHT}── STYLES ──{Style.RESET_ALL}")
    print(f"  {Style.BRIGHT + Fore.WHITE}Style.BRIGHT     Texte lumineux / gras{Style.RESET_ALL}")
    print(f"  {Style.DIM   + Fore.WHITE}Style.DIM        Texte atténué{Style.RESET_ALL}")
    print(f"  {Style.NORMAL+ Fore.WHITE}Style.NORMAL     Texte normal{Style.RESET_ALL}")

    separator()

    # Combinaisons
    print(f"  {Fore.WHITE + Style.BRIGHT}── COMBINAISONS ──{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW + Back.BLUE + Style.BRIGHT} Fore.YELLOW + Back.BLUE + Style.BRIGHT {Style.RESET_ALL}")
    print(f"  {Fore.BLACK  + Back.CYAN               } Fore.BLACK  + Back.CYAN                {Style.RESET_ALL}")
    print(f"  {Fore.WHITE  + Back.RED  + Style.BRIGHT} Fore.WHITE  + Back.RED  + Style.BRIGHT {Style.RESET_ALL}")

    separator()

    # Code exemple
    print(f"\n  {Fore.WHITE + Style.BRIGHT}── CODE PYTHON D'EXEMPLE ──{Style.RESET_ALL}")
    exemple = '''\
  from colorama import init, Fore, Back, Style
  init(autoreset=True)

  print(Fore.GREEN + "Succès !")
  print(Fore.RED   + "Erreur !")
  print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "Attention !")
  print(Fore.CYAN  + "Information")
  # autoreset=True réinitialise automatiquement après chaque print
'''
    print(Fore.WHITE + Style.DIM + exemple + Style.RESET_ALL)
    pause()


# ─────────────────────────────────────────────
#  MODULE 6 : ENCODAGE PERSONNALISÉ
# ─────────────────────────────────────────────

def module_custom_encode():
    clear(); banner()
    header("MODULE 6 — ENCODAGE PERSONNALISÉ")
    print(f"  {Fore.WHITE}Choisissez un format de sortie :{Style.RESET_ALL}")
    menu_item("1", "Séquences d'échappement Python  (\\x41\\x42...)")
    menu_item("2", "Tableau C / C++                 ({0x41,0x42,...})")
    menu_item("3", "URL Encoding                    (%41%42...)")
    menu_item("4", "Base-10 CSV                     (65,66,67,...)")
    choice = input(Fore.CYAN + "\n  Votre choix : " + Style.RESET_ALL).strip()
    text = input(Fore.WHITE + "  Texte à encoder : " + Fore.GREEN).strip()
    print(Style.RESET_ALL)
    if not text:
        error("Texte vide."); pause(); return

    codes = [ord(c) for c in text]
    result = ""
    if choice == "1":
        result = "".join(f"\\x{c:02X}" for c in codes)
    elif choice == "2":
        result = "{" + ", ".join(f"0x{c:02X}" for c in codes) + "}"
    elif choice == "3":
        result = "".join(f"%{c:02X}" for c in codes)
    elif choice == "4":
        result = ",".join(str(c) for c in codes)
    else:
        error("Choix invalide."); pause(); return

    separator()
    info("Résultat", result, Fore.GREEN)
    separator()
    pause()


# ─────────────────────────────────────────────
#  MENU PRINCIPAL
# ─────────────────────────────────────────────

def main():
    while True:
        clear()
        banner()
        print(Fore.GREEN + Style.BRIGHT +
              "  Choisissez un module :\n" + Style.RESET_ALL)
        menu_item("1", "Texte → Codes (déc / hex / bin / oct / html)")
        menu_item("2", "Codes → Texte (déc / hex / bin / oct)")
        menu_item("3", "Inspecter un caractère")
        menu_item("4", "Table ASCII complète")
        menu_item("5", "Démo Colorama (couleurs & styles)")
        menu_item("6", "Encodage personnalisé (\\x, C, URL, CSV)")
        menu_item("0", "Quitter")
        separator()

        choice = input(Fore.CYAN + "\n  → " + Style.RESET_ALL).strip()

        if choice == "1":
            module_text_to_codes()
        elif choice == "2":
            module_codes_to_text()
        elif choice == "3":
            module_inspect()
        elif choice == "4":
            module_table()
        elif choice == "5":
            module_colorama_demo()
        elif choice == "6":
            module_custom_encode()
        elif choice == "0":
            clear()
            print(Fore.GREEN + Style.BRIGHT +
                  "\n  Au revoir !\n" + Style.RESET_ALL)
            sys.exit(0)
        else:
            error("Option invalide.")
            pause()


if __name__ == "__main__":
    main()