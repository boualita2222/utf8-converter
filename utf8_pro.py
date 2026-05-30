#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         UTF8ConverterPro — Héritage Python          ║
║         Classe enfant de UTF8Converter              ║
╚══════════════════════════════════════════════════════╝
"""

import os
import unicodedata

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
#  CLASSE PARENT — UTF8Converter
# ════════════════════════════════════════════
class UTF8Converter:
    """Classe parent — convertisseur de base"""

    def __init__(self):
        self.historique    = []
        self.nb_operations = 0
        print(D + f"  [{self.__class__.__name__}] créé !" + R)

    def _encode_char(self, c):
        cp = ord(c)
        if cp <= 127:
            return [cp]
        elif cp <= 2047:
            return [0b11000000|(cp>>6),
                    0b10000000|(cp&0b00111111)]
        elif cp <= 65535:
            return [0b11100000|(cp>>12),
                    0b10000000|((cp>>6) &0b00111111),
                    0b10000000|(cp&0b00111111)]
        else:
            return [0b11110000|(cp>>18),
                    0b10000000|((cp>>12)&0b00111111),
                    0b10000000|((cp>>6) &0b00111111),
                    0b10000000|(cp&0b00111111)]

    def _decode_octets(self, octets):
        b = octets[0]
        if   b&0b10000000 == 0:
            return b
        elif b&0b11100000 == 0b11000000:
            return ((b&0b00011111)<<6)|(octets[1]&0b00111111)
        elif b&0b11110000 == 0b11100000:
            return ((b&0b00001111)<<12)\
                 | ((octets[1]&0b00111111)<<6)\
                 | (octets[2]&0b00111111)
        else:
            return ((b&0b00000111)<<18)\
                 | ((octets[1]&0b00111111)<<12)\
                 | ((octets[2]&0b00111111)<<6)\
                 | (octets[3]&0b00111111)

    def encoder(self, texte):
        tous = []
        for c in texte:
            tous.extend(self._encode_char(c))
        hex_total = " ".join(f"{b:02X}" for b in tous)
        self._log("ENCODE", texte, hex_total)
        return {"texte": texte, "hex": hex_total,
                "nb_octets": len(tous)}

    def decoder(self, hex_string):
        octets = [int(x,16) for x in hex_string.split()]
        texte  = ""
        i      = 0
        while i < len(octets):
            b = octets[i]
            if   b&0b10000000==0:          n=1
            elif b&0b11100000==0b11000000: n=2
            elif b&0b11110000==0b11100000: n=3
            else:                          n=4
            texte += chr(self._decode_octets(octets[i:i+n]))
            i += n
        self._log("DECODE", hex_string, texte)
        return texte

    def _log(self, op, entree, sortie):
        self.nb_operations += 1
        self.historique.append({
            "num": self.nb_operations,
            "op":  op,
            "in":  entree,
            "out": sortie,
        })

    def afficher_historique(self):
        for h in self.historique:
            c = G if h["op"]=="ENCODE" else C
            print(f"  {Y}#{h['num']:02d}{R} {c}{h['op']:<8}{R} "
                  f"{W}{h['in'][:20]:<22}{R}→ "
                  f"{D}{h['out'][:25]}{R}")

    def __str__(self):
        return f"{self.__class__.__name__}" \
               f"({self.nb_operations} ops)"


# ════════════════════════════════════════════
#  CLASSE ENFANT — UTF8ConverterPro
# ════════════════════════════════════════════
class UTF8ConverterPro(UTF8Converter):
    """
    Classe enfant — hérite de UTF8Converter
    Ajoute : fichiers, rapport, recherche
    """

    def __init__(self):
        # Appelle le constructeur du PARENT !
        super().__init__()
        # Ajoute ses propres attributs
        self.fichiers_traites = []
        self.nb_fichiers      = 0

    # ────────────────────────────────────────
    #  NOUVELLE MÉTHODE — Encoder un fichier
    # ────────────────────────────────────────
    def encoder_fichier(self, chemin):
        """Lit un fichier et encode chaque ligne"""
        try:
            with open(chemin, "r",
                      encoding="utf-8") as f:
                lignes = f.readlines()
        except FileNotFoundError:
            print(RE + f"  Fichier introuvable !" + R)
            return None

        resultats = []
        for i, ligne in enumerate(lignes, 1):
            ligne   = ligne.rstrip("\n")
            res     = self.encoder(ligne)
            resultats.append({
                "ligne": i,
                "texte": ligne,
                "hex":   res["hex"],
                "oct":   res["nb_octets"],
            })

        self.fichiers_traites.append(chemin)
        self.nb_fichiers += 1
        return resultats

    # ────────────────────────────────────────
    #  NOUVELLE MÉTHODE — Rapport texte
    # ────────────────────────────────────────
    def rapport(self, texte):
        """Génère un rapport complet d'un texte"""
        stats  = {1:[], 2:[], 3:[], 4:[]}
        for c in texte:
            n = len(self._encode_char(c))
            stats[n].append(c)

        total_oct = sum(len(v)*n for n,v in stats.items())
        lignes    = []
        lignes.append("=" * 50)
        lignes.append("  RAPPORT UTF-8")
        lignes.append("=" * 50)
        lignes.append(f"  Texte      : {texte}")
        lignes.append(f"  Caractères : {len(texte)}")
        lignes.append(f"  Octets     : {total_oct}")
        lignes.append("-" * 50)

        labels = {1:"ASCII 1oct ",2:"Latin 2oct ",
                  3:"Symb. 3oct ",4:"Emoji 4oct "}
        for n in range(1,5):
            chars = stats[n]
            if not chars: continue
            nb  = len(chars)
            pct = nb*n/total_oct*100
            bar = "█" * int(pct/5)
            uniq = "".join(dict.fromkeys(chars))[:10]
            lignes.append(
                f"  {labels[n]} {nb:3d} car "
                f"{pct:5.1f}%  {bar}")
            lignes.append(
                f"    Uniques : {uniq}")

        lignes.append("=" * 50)
        return "\n".join(lignes)

    # ────────────────────────────────────────
    #  NOUVELLE MÉTHODE — Recherche
    # ────────────────────────────────────────
    def rechercher(self, texte, motif):
        """Cherche un motif dans un texte
        et retourne les positions"""
        positions = []
        i = 0
        while i <= len(texte) - len(motif):
            if texte[i:i+len(motif)] == motif:
                positions.append(i)
            i += 1
        return {
            "texte":     texte,
            "motif":     motif,
            "positions": positions,
            "trouvé":    len(positions) > 0,
        }

    # ────────────────────────────────────────
    #  MÉTHODE MODIFIÉE — encoder enrichi
    # ────────────────────────────────────────
    def encoder(self, texte):
        """
        Surcharge de encoder() —
        ajoute le nom Unicode de chaque caractère
        """
        # Appelle encoder() du PARENT
        res = super().encoder(texte)

        # Enrichit avec les noms Unicode
        details = []
        for c in texte:
            oct_c = self._encode_char(c)
            try:    nom = unicodedata.name(c)
            except: nom = "?"
            details.append({
                "char": c,
                "cp":   ord(c),
                "hex":  " ".join(f"{b:02X}"
                        for b in oct_c),
                "nom":  nom,
            })
        res["details"] = details
        return res

    def __str__(self):
        return f"UTF8ConverterPro" \
               f"({self.nb_operations} ops, " \
               f"{self.nb_fichiers} fichiers)"


# ════════════════════════════════════════════
#  PROGRAMME PRINCIPAL
# ════════════════════════════════════════════
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(G + """
╔══════════════════════════════════════════════════════╗
║         UTF8ConverterPro — Héritage Python          ║
╚══════════════════════════════════════════════════════╝""" + R)

    print(G + "\n  Démonstration de l'héritage :\n" + R)

    # ── Classe PARENT ──
    print(Y + "  ── Classe PARENT ──" + R)
    parent = UTF8Converter()
    res    = parent.encoder("café")
    print(f"  {W}encoder('café') → {C}{res['hex']}{R}")
    print(f"  {W}Type : {G}{type(parent).__name__}{R}\n")

    # ── Classe ENFANT ──
    print(Y + "  ── Classe ENFANT ──" + R)
    pro = UTF8ConverterPro()

    # encoder — méthode surchargée
    print(G + "\n  [1] encoder enrichi :" + R)
    res = pro.encoder("Été 🌍")
    for d in res["details"]:
        print(f"    {Y}{d['char']}{R}  "
              f"{C}U+{d['cp']:04X}{R}  "
              f"{W}{d['hex']:<12}{R}  "
              f"{D}{d['nom']}{R}")
    print(f"  {Y}Hex : {C}{res['hex']}{R}")

    # decoder — hérité du parent
    print(G + "\n  [2] decoder hérité :" + R)
    texte = pro.decoder("C3 A9 20 E2 82 AC 20 F0 9F 90 8D")
    print(f"  {W}→ {G}{texte}{R}")

    # rapport — nouvelle méthode
    print(G + "\n  [3] rapport :" + R)
    print(pro.rapport("Bonjour 🌍 été ™"))

    # recherche — nouvelle méthode
    print(G + "\n  [4] recherche :" + R)
    res = pro.rechercher("abracadabra", "abra")
    print(f"  {W}Motif '{res['motif']}' dans "
          f"'{res['texte']}'{R}")
    print(f"  {Y}Positions : {R}{G}{res['positions']}{R}")

    # encoder un fichier
    print(G + "\n  [5] encoder fichier :" + R)
    chemin = r"C:\PythonProjets\test_utf8.txt"
    resultats = pro.encoder_fichier(chemin)
    if resultats:
        for r in resultats:
            print(f"  {Y}Ligne {r['ligne']}{R} : "
                  f"{W}{r['texte'][:20]:<22}{R}"
                  f"{D}{r['oct']} oct{R}")

    # historique complet
    print(G + "\n  [6] historique :" + R)
    pro.afficher_historique()

    # état final
    print(G + f"\n  État final : {pro}" + R)

    print(LN)
    input(D + "\n  Entrée pour quitter..." + R)


if __name__ == "__main__":
    main()