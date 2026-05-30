#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         CONVERTISSEUR UTF-8 COMPLET  1 → 4 OCTETS                          ║
║         ASCII : 6 / 8 / 10 car.  |  Python 3.x + Colorama                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
  Installation :  pip install colorama
  Lancement    :  python utf8_converter.py
"""

import sys
import os
import unicodedata
import subprocess

# ─────────────────────────────────────────────────────────────────────────────
#  AUTO-INSTALL colorama si absent
# ─────────────────────────────────────────────────────────────────────────────
def _ensure_colorama():
    try:
        import colorama
        return True
    except ImportError:
        print("[INFO] colorama absent — installation automatique…")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "colorama", "--quiet"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            import colorama
            print("[OK]   colorama installe avec succes !\n")
            return True
        except Exception as e:
            print(f"[WARN] Impossible d'installer colorama : {e}")
            return False

HAS_COLOR = _ensure_colorama()

if HAS_COLOR:
    from colorama import init, Fore, Back, Style
    # strip=False + convert=True : force la conversion ANSI sur Windows cmd/PowerShell
    init(autoreset=False, strip=False, convert=True)
else:
    class _D:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _D()

# Désactive les couleurs si la sortie est redirigée (fichier, pipe…)
if not sys.stdout.isatty():
    class _D:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _D()
    HAS_COLOR = False

# ─────────────────────────────────────────────────────────────────────────────
#  PALETTE
# ─────────────────────────────────────────────────────────────────────────────
def _c(*parts): return "".join(parts)

G  = _c(Fore.GREEN,   Style.BRIGHT)
Y  = _c(Fore.YELLOW,  Style.BRIGHT)
C  = _c(Fore.CYAN,    Style.BRIGHT)
M  = _c(Fore.MAGENTA, Style.BRIGHT)
W  = _c(Fore.WHITE)
D  = _c(Style.DIM,    Fore.WHITE)
R  = Style.RESET_ALL
RE = _c(Fore.RED,     Style.BRIGHT)
BL = _c(Fore.BLUE,    Style.BRIGHT)
LN = G + "=" * 80 + R

# ─────────────────────────────────────────────────────────────────────────────
#  NOMS CONTROLES ASCII
# ─────────────────────────────────────────────────────────────────────────────
CTRL_NAMES = [
    "NUL","SOH","STX","ETX","EOT","ENQ","ACK","BEL",
    "BS","HT","LF","VT","FF","CR","SO","SI",
    "DLE","DC1","DC2","DC3","DC4","NAK","SYN","ETB",
    "CAN","EM","SUB","ESC","FS","GS","RS","US",
]
CTRL_DESC = [
    "Null","Start of Heading","Start of Text","End of Text",
    "End of Transmission","Enquiry","Acknowledge","Bell",
    "Backspace","Horizontal Tab","Line Feed","Vertical Tab",
    "Form Feed","Carriage Return","Shift Out","Shift In",
    "Data Link Escape","Device Control 1","Device Control 2","Device Control 3",
    "Device Control 4","Neg. Acknowledge","Synchronous Idle","End Trans. Block",
    "Cancel","End of Medium","Substitute","Escape",
    "File Separator","Group Separator","Record Separator","Unit Separator",
]

# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS AFFICHAGE
# ─────────────────────────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def p(*args):
    print("".join(str(a) for a in args) + R)

def banner():
    p(G, """
+==============================================================================+
|         CONVERTISSEUR UTF-8 COMPLET  1 -> 4 OCTETS                          |
|         ASCII 6 / 8 / 10 col.  |  Python 3.x + Colorama                     |
+==============================================================================+""")

def sep():
    p(LN)

def row(label: str, value: str, color: str = W):
    print(f"  {Y}{label:<24}{R}: {color}{value}{R}")

def ok(msg):   p(G,  f"  [OK]  {msg}")
def err(msg):  p(RE, f"  [ERR] {msg}")
def pause():   input(_c(D, "\n  Appuyez sur Entree...") + R)

def menu_item(key, label):
    print(f"  {Y}[{key}]{R} {W}{label}{R}")

# ─────────────────────────────────────────────────────────────────────────────
#  NOYAU UTF-8
# ─────────────────────────────────────────────────────────────────────────────
def validate_utf8(raw: bytes) -> bool:
    try:
        raw.decode("utf-8"); return True
    except UnicodeDecodeError:
        return False

def char_name(code: int) -> str:
    if code < 32:   return f"{CTRL_NAMES[code]} - {CTRL_DESC[code]}"
    if code == 32:  return "Space"
    if code == 127: return "DEL - Delete"
    return ""

def analyse(cp: int) -> dict:
    char = chr(cp)
    raw  = char.encode("utf-8")
    n    = len(raw)
    ri   = int.from_bytes(raw, "big")
    try:    name = unicodedata.name(char)
    except: name = "(pas de nom)"
    cat  = unicodedata.category(char)
    def asc(w): s = repr(char)[1:-1]; return s.ljust(w)[:w]
    return {
        "char": char, "cp": cp, "bytes": raw, "n": n,
        "hex":  " ".join(f"{b:02X}" for b in raw),
        "bin":  " ".join(f"{b:08b}" for b in raw),
        "raw_int": ri, "raw_hex": f"0x{ri:0{n*2}X}",
        "name": name,  "cat": cat, "valid": validate_utf8(raw),
        "asc6": asc(6), "asc8": asc(8), "asc10": asc(10),
    }

# ─────────────────────────────────────────────────────────────────────────────
#  AFFICHAGE RESULTAT
# ─────────────────────────────────────────────────────────────────────────────
def display(d: dict):
    sep()
    p(G, f"\n  Resultat pour : {d['char']}  (U+{d['cp']:04X})\n")
    sep()
    row("Hexadecimal",       d["hex"],                           Y)
    row("Octets",            str(d["n"]),                        W)
    row("Binaire",           d["bin"],                           C)
    dec_fmt = f"{d['raw_int']:,}".replace(",", " ")
    row("Decimal brut",      f"{dec_fmt}  ({d['raw_hex']})",     M)
    row("Caractere",         d["char"],                          _c(W, Style.BRIGHT))
    row("Point Unicode",     f"U+{d['cp']:04X}",                 BL)
    row("Decimal Unicode",   f"{d['cp']:,}".replace(",", " "),   M)
    row("Nom",               d["name"],                          W)
    row("Categorie Unicode", d["cat"],                           D)
    row("UTF-8 valide",
        "[OK] Oui" if d["valid"] else "[NON] Non",
        G if d["valid"] else RE)
    sep()
    p(G, "  Representation ASCII :")
    row("6  colonnes",  f"[{d['asc6' ]}]", Y)
    row("8  colonnes",  f"[{d['asc8' ]}]", C)
    row("10 colonnes",  f"[{d['asc10']}]", M)
    sep()
    _schema(d["cp"], d["bytes"])
    sep()

def _schema(cp: int, raw: bytes):
    n = len(raw)
    templates = {
        1: ["0xxxxxxx"],
        2: ["110xxxxx", "10xxxxxx"],
        3: ["1110xxxx", "10xxxxxx", "10xxxxxx"],
        4: ["11110xxx", "10xxxxxx", "10xxxxxx", "10xxxxxx"],
    }
    payload = [7, 11, 16, 21][n - 1]
    bits    = f"{cp:0{payload}b}"
    p(G, "  Schema UTF-8 :")
    bit_idx = 0
    for i, tmpl in enumerate(templates[n]):
        filled = ""
        for ch in tmpl:
            if ch == "x":
                filled += _c(C, bits[bit_idx], R)
                bit_idx += 1
            else:
                filled += _c(Y, ch, R)
        bv = raw[i]
        print(f"    Octet {i+1} : {filled}   ({Y}{bv:02X}h{R} = {M}{bv:3d}{R})")

# ─────────────────────────────────────────────────────────────────────────────
#  MODULE 1 — Hex -> Analyse
# ─────────────────────────────────────────────────────────────────────────────
def mod_hex():
    clear(); banner()
    p(G, "\n  MODULE 1 - Hexadecimal -> Analyse\n")
    p(D, "  Exemples : C2 80   F0 9F 90 8B   E2 82 AC   41\n")
    raw_in = input(_c(W, "  Octets hex (espaces) : ", Y)).strip()
    print(R)
    try:
        raw = bytes(int(x, 16) for x in raw_in.split())
        if not raw: raise ValueError("Vide")
        if not validate_utf8(raw):
            err(f"Sequence UTF-8 invalide : {raw.hex(' ').upper()}")
            pause(); return
        cp = ord(raw.decode("utf-8"))
        display(analyse(cp))
    except Exception as e:
        err(str(e))
    pause()

# ─────────────────────────────────────────────────────────────────────────────
#  MODULE 2 — Decimal -> Analyse
# ─────────────────────────────────────────────────────────────────────────────
def mod_decimal():
    clear(); banner()
    p(G, "\n  MODULE 2 - Decimal -> Analyse\n")
    p(D, "  Exemples : 65   8364   128011   4036989067\n")
    val_in = input(_c(W, "  Valeur decimale : ", Y)).strip()
    print(R)
    try:
        val = int(val_in.replace(" ", "").replace("\u202f","").replace(",",""))
        if 0 <= val <= 0x10FFFF:
            display(analyse(val))
        else:
            n = (val.bit_length() + 7) // 8
            raw = val.to_bytes(n, "big")
            if validate_utf8(raw):
                display(analyse(ord(raw.decode("utf-8"))))
            else:
                err("Valeur hors plage Unicode et sequence UTF-8 invalide.")
    except Exception as e:
        err(str(e))
    pause()

# ─────────────────────────────────────────────────────────────────────────────
#  MODULE 3 — Caractere -> Analyse
# ─────────────────────────────────────────────────────────────────────────────
def mod_char():
    clear(); banner()
    p(G, "\n  MODULE 3 - Caractere -> Analyse\n")
    p(D, "  Exemples : A   euro   smiley   baleine\n")
    char_in = input(_c(W, "  Caractere : ", Y)).strip()
    print(R)
    if not char_in: err("Aucun caractere."); pause(); return
    display(analyse(ord(char_in[0])))
    pause()

# ─────────────────────────────────────────────────────────────────────────────
#  MODULE 4 — show() universelle
# ─────────────────────────────────────────────────────────────────────────────
def show(value):
    """show(char) / show(codepoint_int) / show('F0 9F 90 8B') / show('U+1F40B')"""
    d = None
    if isinstance(value, int):
        d = analyse(value)
    elif isinstance(value, str):
        tokens = value.strip().split()
        if (len(tokens) >= 1 and len(tokens[0]) == 2 and
                all(len(t) == 2 and all(c in "0123456789ABCDEFabcdef" for c in t)
                    for t in tokens)):
            try:
                raw = bytes(int(x, 16) for x in tokens)
                d = analyse(ord(raw.decode("utf-8")))
            except Exception:
                pass
        if d is None:
            d = analyse(ord(value[0]))
    if d: display(d)
    else: err(f"Impossible d'analyser : {value!r}")

def mod_show():
    clear(); banner()
    p(G, "\n  MODULE 4 - Fonction show() universelle\n")
    p(D, "  Entree libre : caractere, codepoint dec/hex, octets hex, U+xxxx\n")
    raw_in = input(_c(W, "  Valeur : ", Y)).strip()
    print(R)
    if not raw_in: err("Entree vide."); pause(); return
    try:
        if raw_in.upper().startswith("U+"):
            show(int(raw_in[2:], 16))
        elif raw_in.lower().startswith("0x"):
            show(int(raw_in, 16))
        elif raw_in.replace(" ","").isdigit():
            show(int(raw_in.replace(" ","")))
        else:
            show(raw_in)
    except Exception as e:
        err(str(e))
    pause()

# ─────────────────────────────────────────────────────────────────────────────
#  MODULE 5 — Exemples predéfinis
# ─────────────────────────────────────────────────────────────────────────────
EXEMPLES = [
    ("A",    "ASCII 1 octet  - Lettre latine"),
    ("\xa2", "2 octets       - Cent"),
    ("\xe9", "2 octets       - e accent"),
    ("\u4e2d","3 octets      - Sinogramme"),
    ("\U0001F40B","4 octets  - Baleine"),
    ("\U0001F60A","4 octets  - Smiley"),
    ("\U0001F680","4 octets  - Fusee"),
    ("\x00", "NUL            - Controle ASCII"),
    ("\x7f", "DEL            - Suppression"),
    ("\xa9", "Copyright      - (c)"),
]

def mod_exemples():
    clear(); banner()
    p(G, "\n  MODULE 5 - Exemples predéfinis\n")
    for i, (ch, desc) in enumerate(EXEMPLES, 1):
        cp  = ord(ch)
        nb  = len(ch.encode("utf-8"))
        try:
            disp = ch if 33 <= cp < 127 else f"U+{cp:04X}"
        except Exception:
            disp = f"U+{cp:04X}"
        print(f"  {Y}[{i:2d}]{R} {W}{disp:<10}{R} {D}{nb} oct.  {desc}{R}")
    print()
    choice = input(_c(W, "  Numero (ou Entree = tout) : ", Y)).strip()
    print(R)
    if choice == "":
        for ch, _ in EXEMPLES:
            display(analyse(ord(ch)))
            input(_c(D, "  -> Entree pour le suivant...") + R)
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(EXEMPLES):
                display(analyse(ord(EXEMPLES[idx][0])))
            else:
                err("Numero hors liste.")
        except ValueError:
            err("Entree invalide.")
    pause()

# ─────────────────────────────────────────────────────────────────────────────
#  MODULE 6 — ASCII etendu
# ─────────────────────────────────────────────────────────────────────────────
def mod_ascii():
    while True:
        clear(); banner()
        p(G, "\n  MODULE 6 - Conversion ASCII\n")
        menu_item("1", "Texte       -> Decimal / Hex / Bin / Oct / HTML")
        menu_item("2", "Decimal     -> Texte")
        menu_item("3", "Hexadecimal -> Texte")
        menu_item("4", "Binaire     -> Texte")
        menu_item("5", "Octal       -> Texte")
        menu_item("0", "Retour")
        sep()
        c = input(_c(W, "  Choix : ", Y)).strip(); print(R)
        if c == "0": break
        elif c == "1":
            txt = input(_c(W, "  Texte : ", Y)).strip(); print(R)
            if not txt: err("Vide."); pause(); continue
            codes = [ord(ch) for ch in txt]
            sep()
            row("Decimal",  " ".join(str(v)      for v in codes), M)
            row("Hex",      " ".join(f"{v:02X}"  for v in codes), Y)
            row("Binaire",  " ".join(f"{v:08b}"  for v in codes), C)
            row("Octal",    " ".join(f"0{v:03o}" for v in codes), M)
            row("HTML",     "".join(f"&#{v};"    for v in codes), BL)
            sep(); pause()
        elif c in ("2","3","4","5"):
            bases  = {"2":10,"3":16,"4":2,"5":8}
            labels = {"2":"Decimal","3":"Hex","4":"Binaire","5":"Octal"}
            base   = bases[c]
            raw    = input(_c(W, f"  Codes {labels[c]} (espaces) : ", Y)).strip()
            print(R)
            tokens = raw.replace("0x","").replace("0b","").replace("0o","").split()
            result = ""
            for t in tokens:
                try:    result += chr(int(t, base))
                except: result += "?"
            sep()
            row("Texte", result, G)
            sep(); pause()
        else:
            err("Option invalide."); pause()

# ─────────────────────────────────────────────────────────────────────────────
#  MODULE 7 — Calcul détaillé pas a pas
# ─────────────────────────────────────────────────────────────────────────────
def _detail(cp: int):
    char = chr(cp)
    raw  = char.encode("utf-8")
    n    = len(raw)
    ranges = [
        (0x000000, 0x00007F, 1, "0xxxxxxx"),
        (0x000080, 0x0007FF, 2, "110xxxxx 10xxxxxx"),
        (0x000800, 0x00FFFF, 3, "1110xxxx 10xxxxxx 10xxxxxx"),
        (0x010000, 0x10FFFF, 4, "11110xxx 10xxxxxx 10xxxxxx 10xxxxxx"),
    ]
    sep()
    p(G, f"\n  Calcul pas a pas pour U+{cp:04X}\n")
    for lo, hi, nb, tmpl in ranges:
        if lo <= cp <= hi:
            row("Plage",   f"{lo:#07X} -> {hi:#07X}", Y)
            row("Gabarit", tmpl,                       C)
            row("Octets",  str(nb),                    W)
            break
    print()
    payload = [7, 11, 16, 21][n - 1]
    bits    = f"{cp:0{payload}b}"
    row(f"Codepoint ({payload} bits)", bits, C)
    print()
    cuts     = {1:[7], 2:[5,6], 3:[4,6,6], 4:[3,6,6,6]}[n]
    prefixes = {1:["0"], 2:["110","10"], 3:["1110","10","10"],
                4:["11110","10","10","10"]}[n]
    p(G, "  Decoupage et construction :")
    idx = 0
    for i, (cut, pref) in enumerate(zip(cuts, prefixes)):
        seg   = bits[idx:idx+cut]
        bval  = int(pref + seg, 2)
        print(f"    Octet {i+1} : "
              f"{Y}{pref}{R}{C}{seg}{R}"
              f"  ->  {Y}{bval:02X}h{R} = {M}{bval:3d}{R}")
        idx += cut
    sep()
    row("Resultat hex", " ".join(f"{b:02X}" for b in raw), Y)
    row("Decodage",     char,                               _c(W, Style.BRIGHT))
    row("UTF-8 valide", "[OK] Oui" if validate_utf8(raw) else "[NON] Non",
        G if validate_utf8(raw) else RE)
    sep()

def mod_detail():
    clear(); banner()
    p(G, "\n  MODULE 7 - Calcul detaille pas a pas\n")
    p(D, "  Exemples : A   euro sign   U+1F40B   0x1F40B   128011\n")
    raw_in = input(_c(W, "  Entree : ", Y)).strip(); print(R)
    try:
        if   raw_in.upper().startswith("U+"): cp = int(raw_in[2:], 16)
        elif raw_in.lower().startswith("0x"): cp = int(raw_in, 16)
        elif raw_in.isdigit():                cp = int(raw_in)
        else:                                 cp = ord(raw_in[0])
        _detail(cp)
    except Exception as e:
        err(str(e))
    pause()

# ─────────────────────────────────────────────────────────────────────────────
#  MODULE 8 — Diagnostic Colorama
# ─────────────────────────────────────────────────────────────────────────────
def mod_diag():
    clear(); banner()
    p(G, "\n  MODULE 8 - Diagnostic Colorama\n")
    sep()
    row("Python version",   sys.version.split()[0],           W)
    row("Plateforme",       sys.platform,                      W)
    row("Terminal (isatty)",str(sys.stdout.isatty()),          W)
    row("TERM",             os.environ.get("TERM", "n/d"),     W)
    row("COLORTERM",        os.environ.get("COLORTERM","n/d"), W)
    sep()
    try:
        import colorama
        row("colorama version", colorama.__version__, G)
        row("colorama chemin",  colorama.__file__,    D)
        ok("colorama importe avec succes")
    except ImportError:
        err("colorama NON installe  ->  pip install colorama")
        pause(); return
    sep()
    p(G, "  Test des couleurs foreground :")
    print()
    tests_fg = [
        ("Fore.RED",     Fore.RED),
        ("Fore.GREEN",   Fore.GREEN),
        ("Fore.YELLOW",  Fore.YELLOW),
        ("Fore.BLUE",    Fore.BLUE),
        ("Fore.MAGENTA", Fore.MAGENTA),
        ("Fore.CYAN",    Fore.CYAN),
        ("Style.BRIGHT", Style.BRIGHT + Fore.WHITE),
        ("Style.DIM",    Style.DIM    + Fore.WHITE),
    ]
    for nom, code in tests_fg:
        print(f"    {code}  ###  {nom}  ###{R}")
    print()
    sep()
    p(G, "  Test des fonds background :")
    print()
    tests_bg = [
        ("Back.RED",     Fore.WHITE + Back.RED),
        ("Back.GREEN",   Fore.BLACK + Back.GREEN),
        ("Back.YELLOW",  Fore.BLACK + Back.YELLOW),
        ("Back.BLUE",    Fore.WHITE + Back.BLUE),
        ("Back.CYAN",    Fore.BLACK + Back.CYAN),
        ("Back.MAGENTA", Fore.WHITE + Back.MAGENTA),
    ]
    for nom, code in tests_bg:
        print(f"    {code}  {nom}  {R}")
    print()
    sep()
    if sys.platform == "win32":
        p(G, "  Conseils Windows :")
        p(W, "  1. Utilisez Windows Terminal (meilleur support ANSI)")
        p(W, "  2. PowerShell 7+ supporte les couleurs ANSI nativement")
        p(W, "  3. Pour activer ANSI dans cmd.exe classique :")
        p(Y, "     REG ADD HKCU\\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f")
        p(W, "  4. Si les couleurs s'affichent comme ^[[32m etc. :")
        p(Y, "     Ajoutez  init(wrap=True)  au debut du script")
        sep()
    pause()

# ─────────────────────────────────────────────────────────────────────────────
#  MENU PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
MENU = [
    ("1", "Hexadecimal       -> Analyse",           mod_hex),
    ("2", "Decimal           -> Analyse",           mod_decimal),
    ("3", "Caractere         -> Analyse",           mod_char),
    ("4", "Fonction show()   universelle",           mod_show),
    ("5", "Exemples predéfinis (10 cas)",            mod_exemples),
    ("6", "Conversion ASCII (texte <-> bases)",      mod_ascii),
    ("7", "Calcul detaille   pas a pas",             mod_detail),
    ("8", "Diagnostic Colorama",                     mod_diag),
    ("0", "Quitter",                                 None),
]

def main():
    while True:
        clear(); banner()
        p(G, "  Choisissez un module :\n")
        for key, label, _ in MENU:
            if key == "0": print()
            menu_item(key, label)
        sep()
        choice = input(_c(C, "\n  -> ") + R).strip()
        for key, _, fn in MENU:
            if choice == key:
                if fn is None:
                    clear()
                    p(G, "\n  Au revoir !\n")
                    sys.exit(0)
                fn(); break
        else:
            err("Option invalide."); pause()

if __name__ == "__main__":
    main()