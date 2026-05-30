#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         UTF8Converter — Classe Python               ║
║         Programmation Orientée Objet                ║
╚══════════════════════════════════════════════════════╝
"""

import unicodedata
import os

try:
    from colorama import init, Fore, Style
    init(autoreset=False, strip=False, convert=True)
except ImportError:
    class _D:
        def __getattr__(self, _): return ""
    Fore = Style = _D()

G  = Fore.GREEN  + Style.BRIGHT
Y  = Fore.YELLOW + Style.BRIGHT
C  = Fore.CYAN   + Style.BRIGHT
M  = Fore.MAGENTA
W  = Fore.WHITE
D  = Style.DIM   + Fore.WHITE
R  = Style.RESET_ALL
RE = Fore.RED    + Style.BRIGHT
LN = G + "=" * 55 + R


# ════════════════════════════════════════════
#  CLASSE PRINCIPALE
# ════════════════════════════════════════════
class UTF8Converter:
    """
    Convertisseur UTF-8 complet.
    Encode, décode, analyse et compare
    des textes et caractères Unicode.
    """

    def __init__(self):
        """Constructeur — initialise l'historique"""
        self.historique = []   # liste des conversions
        self.nb_operations = 0 # compteur

    # ── MÉTHODE PRIVÉE — encode 1 caractère ──
    def _encode_char(self, c):
        """Encode un seul caractère en liste d'octets"""
        cp = ord(c)
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

    # ── MÉTHODE PRIVÉE — décode octets → cp ──
    def _decode_octets(self, octets):
        """Décode une liste d'octets en codepoint"""
        b = octets[0]
        if b & 0b10000000 == 0:
            return b
        elif b & 0b11100000 == 0b11000000:
            return ((b         & 0b00011111) << 6) \
                 | (octets[1]  & 0b00111111)
        elif b & 0b11110000 == 0b11100000:
            return ((b         & 0b00001111) << 12) \
                 | ((octets[1] & 0b00111111) << 6)  \
                 | (octets[2]  & 0b00111111)
        else:
            return ((b         & 0b00000111) << 18) \
                 | ((octets[1] & 0b00111111) << 12) \
                 | ((octets[2] & 0b00111111) << 6)  \
                 | (octets[3]  & 0b00111111)

    # ────────────────────────────────────────
    #  MÉTHODE 1 — Encoder un texte
    # ────────────────────────────────────────
    def encoder(self, texte):
        """
        Encode un texte en séquence hex UTF-8.
        Retourne un dictionnaire avec tous les détails.
        """
        tous_octets = []
        details     = []

        for c in texte:
            octets = self._encode_char(c)
            tous_octets.extend(octets)
            details.append({
                "char":   c,
                "cp":     ord(c),
                "octets": octets,
                "hex":    " ".join(f"{b:02X}" for b in octets),
            })

        hex_total = " ".join(f"{b:02X}" for b in tous_octets)
        resultat  = {
            "texte":        texte,
            "hex":          hex_total,
            "nb_chars":     len(texte),
            "nb_octets":    len(tous_octets),
            "details":      details,
        }

        # Sauvegarder dans historique
        self._log("ENCODE", texte, hex_total)
        return resultat

    # ────────────────────────────────────────
    #  MÉTHODE 2 — Décoder une séquence hex
    # ────────────────────────────────────────
    def decoder(self, hex_string):
        """
        Décode une séquence hex UTF-8 en texte.
        Retourne un dictionnaire avec tous les détails.
        """
        octets   = [int(x, 16) for x in hex_string.split()]
        resultat_chars = []
        texte    = ""
        i        = 0

        while i < len(octets):
            b = octets[i]
            if   b & 0b10000000 == 0:          n = 1
            elif b & 0b11100000 == 0b11000000: n = 2
            elif b & 0b11110000 == 0b11100000: n = 3
            else:                               n = 4

            seq  = octets[i:i+n]
            cp   = self._decode_octets(seq)
            char = chr(cp)
            texte += char
            resultat_chars.append({
                "hex":  " ".join(f"{b:02X}" for b in seq),
                "cp":   cp,
                "char": char,
                "n":    n,
            })
            i += n

        self._log("DECODE", hex_string, texte)
        return {"texte": texte, "details": resultat_chars}

    # ────────────────────────────────────────
    #  MÉTHODE 3 — Analyser un caractère
    # ────────────────────────────────────────
    def analyser(self, c):
        """
        Analyse complète d'un caractère Unicode.
        Retourne un dictionnaire avec tous les détails.
        """
        c       = c[0]
        cp      = ord(c)
        octets  = self._encode_char(c)
        ri      = int.from_bytes(bytes(octets), "big")
        try:    nom = unicodedata.name(c)
        except: nom = "(pas de nom)"

        return {
            "char":     c,
            "cp":       cp,
            "hex":      " ".join(f"{b:02X}" for b in octets),
            "bin":      " ".join(f"{b:08b}" for b in octets),
            "n":        len(octets),
            "raw_int":  ri,
            "nom":      nom,
            "cat":      unicodedata.category(c),
        }

    # ────────────────────────────────────────
    #  MÉTHODE 4 — Comparer deux textes
    # ────────────────────────────────────────
    def comparer(self, texte1, texte2):
        """Compare deux textes caractère par caractère"""
        r1  = self.encoder(texte1)
        r2  = self.encoder(texte2)
        diff = []

        for i in range(max(len(texte1), len(texte2))):
            c1 = texte1[i] if i < len(texte1) else None
            c2 = texte2[i] if i < len(texte2) else None
            if c1 != c2:
                diff.append({
                    "pos": i+1,
                    "c1":  c1,
                    "c2":  c2,
                    "h1":  " ".join(f"{b:02X}" for b in
                           self._encode_char(c1)) if c1 else "—",
                    "h2":  " ".join(f"{b:02X}" for b in
                           self._encode_char(c2)) if c2 else "—",
                })

        return {
            "texte1":       texte1,
            "texte2":       texte2,
            "oct1":         r1["nb_octets"],
            "oct2":         r2["nb_octets"],
            "differences":  diff,
            "identiques":   len(diff) == 0,
        }

    # ────────────────────────────────────────
    #  MÉTHODE 5 — Statistiques
    # ────────────────────────────────────────
    def stats(self, texte):
        """Calcule les statistiques UTF-8 d'un texte"""
        types = {1: [], 2: [], 3: [], 4: []}
        for c in texte:
            n = len(self._encode_char(c))
            types[n].append(c)
        total_oct = sum(len(v)*n for n, v in types.items())
        return {
            "texte":      texte,
            "nb_chars":   len(texte),
            "nb_octets":  total_oct,
            "types":      types,
        }

    # ────────────────────────────────────────
    #  MÉTHODE 6 — Historique
    # ────────────────────────────────────────
    def _log(self, op, entree, sortie):
        """Enregistre une opération dans l'historique"""
        self.nb_operations += 1
        self.historique.append({
            "num":    self.nb_operations,
            "op":     op,
            "entree": entree,
            "sortie": sortie,
        })

    def afficher_historique(self):
        """Affiche l'historique des opérations"""
        if not self.historique:
            print(D + "  Historique vide." + R)
            return
        for h in self.historique:
            op_color = G if h["op"] == "ENCODE" else C
            print(f"  {Y}#{h['num']:02d}{R} "
                  f"{op_color}{h['op']:<8}{R} "
                  f"{W}{h['entree'][:20]:<22}{R}→ "
                  f"{D}{h['sortie'][:25]}{R}")

    def effacer_historique(self):
        """Efface l'historique"""
        self.historique.clear()
        self.nb_operations = 0
        print(G + "  ✅ Historique effacé." + R)

    # ────────────────────────────────────────
    #  MÉTHODE SPÉCIALE — représentation
    # ────────────────────────────────────────
    def __str__(self):
        return (f"UTF8Converter("
                f"{self.nb_operations} opérations)")

    def __repr__(self):
        return self.__str__()


# ════════════════════════════════════════════
#  AFFICHAGE DES RÉSULTATS
# ════════════════════════════════════════════
def afficher_encode(res):
    print(G + f"\n  Encodage : {res['texte']}\n" + R)
    for d in res["details"]:
        cp = d["cp"]
        print(f"  {Y}{d['char']}{R}  "
              f"{C}U+{cp:04X}{R}  "
              f"{W}{d['hex']}{R}")
    print(f"\n  {Y}Séquence : {R}{C}{res['hex']}{R}")
    print(f"  {Y}Octets   : {R}{W}{res['nb_octets']}{R}")


def afficher_decode(res):
    print(G + f"\n  Décodage :\n" + R)
    for d in res["details"]:
        print(f"  {C}{d['hex']:<15}{R}→ "
              f"{Y}{d['char']}{R}  "
              f"{W}U+{d['cp']:04X}{R}")
    print(f"\n  {Y}Texte : {R}{G}{res['texte']}{R}")


def afficher_analyse(res):
    print(G + f"\n  Analyse : {res['char']}\n" + R)
    print(f"  {Y}{'Codepoint':<18}{R}: {C}U+{res['cp']:04X}{R}")
    print(f"  {Y}{'Hex UTF-8':<18}{R}: {Y}{res['hex']}{R}")
    print(f"  {Y}{'Binaire':<18}{R}: {C}{res['bin']}{R}")
    print(f"  {Y}{'Octets':<18}{R}: {W}{res['n']}{R}")
    print(f"  {Y}{'Décimal brut':<18}{R}: {M}{res['raw_int']}{R}")
    print(f"  {Y}{'Nom Unicode':<18}{R}: {W}{res['nom']}{R}")


def afficher_stats(res):
    labels = {1:"ASCII 1oct",2:"Latin 2oct",
              3:"Symb. 3oct",4:"Emoji 4oct"}
    colors = {1: W, 2: C, 3: Y, 4: M}
    print(G + f"\n  Stats : {res['texte']}\n" + R)
    print(f"  {Y}Caractères : {R}{W}{res['nb_chars']}{R}")
    print(f"  {Y}Octets     : {R}{W}{res['nb_octets']}{R}\n")
    for n in range(1, 5):
        chars = res["types"][n]
        if not chars: continue
        nb  = len(chars)
        pct = nb * n / res["nb_octets"] * 100
        bar = "█" * int(pct / 5)
        print(f"  {colors[n]}{labels[n]:<12}{R} "
              f"{W}{nb:3d} car  {pct:5.1f}%  {bar}{R}")


# ════════════════════════════════════════════
#  PROGRAMME PRINCIPAL — MENU
# ════════════════════════════════════════════
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(G + """
╔══════════════════════════════════════════════════════╗
║         UTF8Converter — Classe Python               ║
║         Programmation Orientée Objet                ║
╚══════════════════════════════════════════════════════╝""" + R)

    # Créer l'objet !
    conv = UTF8Converter()
    print(G + f"\n  Objet créé : {conv}\n" + R)

    while True:
        print(LN)
        print(f"  {Y}[1]{R} {W}Encoder  un texte{R}")
        print(f"  {Y}[2]{R} {W}Décoder  une séquence hex{R}")
        print(f"  {Y}[3]{R} {W}Analyser un caractère{R}")
        print(f"  {Y}[4]{R} {W}Comparer deux textes{R}")
        print(f"  {Y}[5]{R} {W}Statistiques{R}")
        print(f"  {Y}[6]{R} {W}Historique  ({conv.nb_operations} op.){R}")
        print(f"  {Y}[7]{R} {W}Effacer historique{R}")
        print(f"\n  {Y}[0]{R} {W}Quitter{R}")
        print(LN)

        choix = input(C + "\n  → " + R).strip()

        if choix == "0":
            print(G + f"\n  Au revoir ! {conv}\n" + R)
            break

        elif choix == "1":
            t = input(W + "  Texte : " + Y).strip()
            print(R)
            if t:
                res = conv.encoder(t)
                afficher_encode(res)

        elif choix == "2":
            h = input(W + "  Hex : " + Y).strip()
            print(R)
            if h:
                try:
                    res = conv.decoder(h)
                    afficher_decode(res)
                except Exception as e:
                    print(RE + f"  Erreur : {e}" + R)

        elif choix == "3":
            c = input(W + "  Caractère : " + Y).strip()
            print(R)
            if c:
                res = conv.analyser(c)
                afficher_analyse(res)

        elif choix == "4":
            t1 = input(W + "  Texte 1 : " + Y).strip()
            t2 = input(W + "  Texte 2 : " + Y).strip()
            print(R)
            if t1 and t2:
                res = conv.comparer(t1, t2)
                print(G + f"\n  {t1}  vs  {t2}\n" + R)
                print(f"  {Y}Octets 1 : {R}{W}{res['oct1']}{R}")
                print(f"  {Y}Octets 2 : {R}{W}{res['oct2']}{R}")
                if res["identiques"]:
                    print(G + "\n  Identiques ! ✅" + R)
                else:
                    print(Y + f"\n  {len(res['differences'])} différence(s) :\n" + R)
                    for d in res["differences"]:
                        print(f"  {Y}Pos {d['pos']}{R} : "
                              f"{G}{d['c1'] or '—'}{R} {d['h1']} "
                              f"{RE}≠{R} "
                              f"{G}{d['c2'] or '—'}{R} {d['h2']}")

        elif choix == "5":
            t = input(W + "  Texte : " + Y).strip()
            print(R)
            if t:
                res = conv.stats(t)
                afficher_stats(res)

        elif choix == "6":
            print(G + "\n  Historique :\n" + R)
            conv.afficher_historique()

        elif choix == "7":
            conv.effacer_historique()

        else:
            print(RE + "  Option invalide !" + R)

        input(D + "\n  Entrée pour continuer..." + R)
        os.system("cls" if os.name == "nt" else "clear")
        print(G + f"  {conv}\n" + R)


if __name__ == "__main__":
    main()