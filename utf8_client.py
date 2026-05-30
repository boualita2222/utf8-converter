#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UTF-8 API CLIENT
Python 3.14.2 + requests
Consomme l'API Flask locale
"""

import sys
import os
sys.path.insert(0, r"C:\PythonProjets")

try:
    import requests
except ImportError:
    print("Installez requests : pip install requests")
    sys.exit(1)

try:
    from colorama import init, Fore, Style
    init(autoreset=False, strip=False, convert=True)
except ImportError:
    class _D:
        def __getattr__(self, _): return ""
    Fore = Style = _D()

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

BASE_URL = "http://127.0.0.1:5000"


# ════════════════════════════════════════════
#  CLASSE CLIENT
# ════════════════════════════════════════════
class UTF8Client:
    """
    Client Python pour l'API UTF-8 Flask
    Envoie des requêtes HTTP et
    affiche les résultats
    """

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session  = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept":       "application/json",
        })

    # ── Vérifier que l'API tourne ────────
    def ping(self):
        """Vérifie que l'API est accessible"""
        try:
            r = self.session.get(
                self.base_url,
                timeout=3)
            if r.status_code == 200:
                print(G + "  API accessible !" + R)
                return True
            else:
                print(RE + f"  API erreur : {r.status_code}" + R)
                return False
        except requests.ConnectionError:
            print(RE + "  API inaccessible !" + R)
            print(W  + "  Lancez d'abord : python utf8_api.py" + R)
            return False

    # ── ENCODER ─────────────────────────
    def encoder(self, texte):
        """
        GET /api/encoder?texte=...
        Encode un texte en UTF-8
        """
        try:
            r = self.session.get(
                f"{self.base_url}/api/encoder",
                params={"texte": texte},
                timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            return {"erreur": str(e)}
        except Exception as e:
            return {"erreur": str(e)}

    # ── DECODER ─────────────────────────
    def decoder(self, hex_str):
        """
        POST /api/decoder
        Décode une séquence hex UTF-8
        """
        try:
            r = self.session.post(
                f"{self.base_url}/api/decoder",
                json={"hex": hex_str},
                timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            return {"erreur": str(e)}
        except Exception as e:
            return {"erreur": str(e)}

    # ── ANALYSER ────────────────────────
    def analyser(self, char):
        """
        GET /api/analyser?char=...
        Analyse un caractère
        """
        try:
            r = self.session.get(
                f"{self.base_url}/api/analyser",
                params={"char": char},
                timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            return {"erreur": str(e)}
        except Exception as e:
            return {"erreur": str(e)}

    # ── COMPARER ────────────────────────
    def comparer(self, t1, t2):
        """
        GET /api/comparer?t1=...&t2=...
        Compare deux textes
        """
        try:
            r = self.session.get(
                f"{self.base_url}/api/comparer",
                params={"t1": t1, "t2": t2},
                timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            return {"erreur": str(e)}
        except Exception as e:
            return {"erreur": str(e)}

    # ── STATS ───────────────────────────
    def stats(self, texte):
        """
        GET /api/stats?texte=...
        Statistiques d'un texte
        """
        try:
            r = self.session.get(
                f"{self.base_url}/api/stats",
                params={"texte": texte},
                timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            return {"erreur": str(e)}
        except Exception as e:
            return {"erreur": str(e)}

    # ── HISTORIQUE ──────────────────────
    def historique(self, limite=10):
        """
        GET /api/historique
        Récupère l'historique
        """
        try:
            r = self.session.get(
                f"{self.base_url}/api/historique",
                timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"erreur": str(e)}

    # ── RESUME ──────────────────────────
    def resume(self):
        """
        GET /api/resume
        Résumé de la base de données
        """
        try:
            r = self.session.get(
                f"{self.base_url}/api/resume",
                timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"erreur": str(e)}

    def __str__(self):
        return f"UTF8Client({self.base_url})"


# ════════════════════════════════════════════
#  AFFICHAGE
# ════════════════════════════════════════════
def afficher_encode(res):
    if "erreur" in res:
        print(RE + f"  Erreur : {res['erreur']}" + R)
        return
    print(f"  {Y}Texte    :{R} {W}{res['texte']}{R}")
    print(f"  {Y}Hex      :{R} {C}{res['hex']}{R}")
    print(f"  {Y}Chars    :{R} {W}{res['nb_chars']}{R}")
    print(f"  {Y}Octets   :{R} {W}{res['nb_octets']}{R}")
    print()
    for d in res.get("details", []):
        cp = format(d['cp'], '04X')
        print(f"    {Y}{d['char']}{R}  "
              f"{C}U+{cp}{R}  "
              f"{W}{d['hex']:<12}{R}  "
              f"{D}{d['n']} oct{R}")


def afficher_decode(res):
    if "erreur" in res:
        print(RE + f"  Erreur : {res['erreur']}" + R)
        return
    print(f"  {Y}Texte    :{R} {G}{res['texte']}{R}")
    print()
    for d in res.get("details", []):
        cp = format(d['cp'], '04X')
        print(f"    {C}{d['hex']:<15}{R}"
              f"-> {Y}{d['char']}{R}  "
              f"{W}U+{cp}{R}")


def afficher_analyse(res):
    if "erreur" in res:
        print(RE + f"  Erreur : {res['erreur']}" + R)
        return
    print(f"  {Y}Caractere  :{R} {G}{res['char']}{R}")
    print(f"  {Y}Codepoint  :{R} {C}U+{res['cp']:04X}{R}")
    print(f"  {Y}Hex UTF-8  :{R} {Y}{res['hex']}{R}")
    print(f"  {Y}Binaire    :{R} {C}{res['bin']}{R}")
    print(f"  {Y}Octets     :{R} {W}{res['n']}{R}")
    print(f"  {Y}Dec. brut  :{R} {M}{res['raw_int']}{R}")
    print(f"  {Y}Nom        :{R} {W}{res['nom']}{R}")


def afficher_compare(res):
    if "erreur" in res:
        print(RE + f"  Erreur : {res['erreur']}" + R)
        return
    print(f"  {Y}Texte 1  :{R} {W}{res['texte1']}{R} ({res['oct1']} oct)")
    print(f"  {Y}Texte 2  :{R} {W}{res['texte2']}{R} ({res['oct2']} oct)")
    print(D + "  " + "-"*40 + R)
    if res["identiques"]:
        print(G + "  IDENTIQUES !" + R)
    else:
        print(Y + f"  {res['nb_diff']} difference(s) :" + R)
        for d in res["differences"]:
            print(f"    {Y}Pos {d['pos']}{R} : "
                  f"{G}{d['c1'] or '-'}{R} {d['h1']} "
                  f"{RE}!={R} "
                  f"{G}{d['c2'] or '-'}{R} {d['h2']}")


def afficher_stats(res):
    if "erreur" in res:
        print(RE + f"  Erreur : {res['erreur']}" + R)
        return
    labels = {
        "1": "ASCII    (1 oct)",
        "2": "Latin    (2 oct)",
        "3": "Symboles (3 oct)",
        "4": "Emojis   (4 oct)",
    }
    colors = {"1": W, "2": C, "3": Y, "4": M}
    print(f"  {Y}Texte    :{R} {W}{res['texte']}{R}")
    print(f"  {Y}Chars    :{R} {W}{res['nb_chars']}{R}")
    print(f"  {Y}Octets   :{R} {W}{res['nb_octets']}{R}")
    print(f"  {Y}ASCII%   :{R} {W}{res['pct_ascii']:.1f}%{R}")
    print()
    for n in ["1", "2", "3", "4"]:
        chars = res["types"].get(n, [])
        if not chars:
            continue
        nb  = len(chars)
        pct = nb * int(n) / res["nb_octets"] * 100
        bar = "=" * int(pct / 5)
        print(f"  {colors[n]}{labels[n]}{R} "
              f"{W}{nb:3d}  ({pct:5.1f}%)  {bar}{R}")


def afficher_historique(res):
    if "erreur" in res:
        print(RE + f"  Erreur : {res['erreur']}" + R)
        return
    hist = res.get("historique", [])
    if not hist:
        print(D + "  Historique vide." + R)
        return
    print(f"  {Y}{'ID':<4}{'OP':<10}{'ENTREE':<20}{'OCT':<5}DATE{R}")
    print(D + "  " + "-"*55 + R)
    for h in hist:
        print(f"  {W}#{h['id']:<3}"
              f"{h['operation']:<10}"
              f"{str(h['entree'])[:18]:<20}"
              f"{h['nb_octets']:<5}"
              f"{h['date']}{R}")


def afficher_resume(res):
    if "erreur" in res:
        print(RE + f"  Erreur : {res['erreur']}" + R)
        return
    print(f"  {Y}Total operations :{R} {W}{res['total_ops']}{R}")
    print(f"  {Y}Total octets     :{R} {W}{res['total_octets']}{R}")
    print(f"  {Y}Favoris          :{R} {W}{res['nb_favoris']}{R}")
    if res.get("par_type"):
        print(f"  {Y}Par type :{R}")
        for op, nb in res["par_type"].items():
            print(f"    {C}{op:<12}{R}{W}{nb}{R}")
    if res.get("plus_long"):
        pl = res["plus_long"]
        print(f"  {Y}Plus long :{R} {W}{pl['entree'][:25]}"
              f" ({pl['nb_octets']} oct){R}")


# ════════════════════════════════════════════
#  MENU INTERACTIF
# ════════════════════════════════════════════
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(G + """
╔══════════════════════════════════════════════════════╗
║         UTF-8 API CLIENT                            ║
║         Python 3.14.2 + requests                   ║
╚══════════════════════════════════════════════════════╝""" + R)

    client = UTF8Client()
    print(G + f"\n  Client : {client}\n" + R)

    # Vérifier connexion
    if not client.ping():
        input(D + "\n  Entrée pour quitter..." + R)
        return

    while True:
        print()
        print(LN)
        print(f"  {Y}[1]{R} {W}Encoder  un texte{R}")
        print(f"  {Y}[2]{R} {W}Decoder  une sequence hex{R}")
        print(f"  {Y}[3]{R} {W}Analyser un caractere{R}")
        print(f"  {Y}[4]{R} {W}Comparer deux textes{R}")
        print(f"  {Y}[5]{R} {W}Statistiques{R}")
        print(f"  {Y}[6]{R} {W}Historique{R}")
        print(f"  {Y}[7]{R} {W}Resume DB{R}")
        print(f"  {Y}[8]{R} {W}Test automatique (tous les modules){R}")
        print(f"\n  {Y}[0]{R} {W}Quitter{R}")
        print(LN)

        choix = input(C + "\n  -> " + R).strip()

        if choix == "0":
            print(G + "\n  Au revoir !\n" + R)
            break

        elif choix == "1":
            t = input(W + "  Texte : " + Y).strip()
            print(R)
            if t:
                print(G + "\n  Resultat :\n" + R)
                afficher_encode(client.encoder(t))

        elif choix == "2":
            h = input(W + "  Hex : " + Y).strip()
            print(R)
            if h:
                print(G + "\n  Resultat :\n" + R)
                afficher_decode(client.decoder(h))

        elif choix == "3":
            c = input(W + "  Caractere : " + Y).strip()
            print(R)
            if c:
                print(G + "\n  Resultat :\n" + R)
                afficher_analyse(client.analyser(c[0]))

        elif choix == "4":
            t1 = input(W + "  Texte 1 : " + Y).strip()
            t2 = input(W + "  Texte 2 : " + Y).strip()
            print(R)
            if t1 and t2:
                print(G + "\n  Resultat :\n" + R)
                afficher_compare(client.comparer(t1, t2))

        elif choix == "5":
            t = input(W + "  Texte : " + Y).strip()
            print(R)
            if t:
                print(G + "\n  Statistiques :\n" + R)
                afficher_stats(client.stats(t))

        elif choix == "6":
            print(G + "\n  Historique :\n" + R)
            afficher_historique(client.historique())

        elif choix == "7":
            print(G + "\n  Resume :\n" + R)
            afficher_resume(client.resume())

        elif choix == "8":
            _test_auto(client)

        else:
            print(RE + "  Option invalide !" + R)

        input(D + "\n  Entree pour continuer..." + R)
        os.system("cls" if os.name == "nt" else "clear")


def _test_auto(client):
    """Test automatique de tous les modules"""
    tests = [
        ("cafe",         "encode"),
        ("Bonjour",      "encode"),
        ("C3 A9",        "decode"),
        ("F0 9F 90 8D",  "decode"),
        ("A",            "analyse"),
        ("cafe", "cafe", "compare"),
        ("cafe", "cafe2","compare"),
        ("Hello World",  "stats"),
    ]

    print(G + "\n  Test automatique :\n" + R)
    ok = 0
    ko = 0

    for test in tests:
        if test[-1] == "encode":
            res = client.encoder(test[0])
            if "erreur" not in res:
                print(G + f"  OK  encode('{test[0]}')"
                      + f" -> {res['hex'][:20]}..." + R)
                ok += 1
            else:
                print(RE + f"  KO  encode('{test[0]}')"
                      + f" -> {res['erreur']}" + R)
                ko += 1

        elif test[-1] == "decode":
            res = client.decoder(test[0])
            if "erreur" not in res:
                print(G + f"  OK  decode('{test[0]}')"
                      + f" -> '{res['texte']}'" + R)
                ok += 1
            else:
                print(RE + f"  KO  decode('{test[0]}')"
                      + f" -> {res['erreur']}" + R)
                ko += 1

        elif test[-1] == "analyse":
            res = client.analyser(test[0])
            if "erreur" not in res:
                print(G + f"  OK  analyse('{test[0]}')"
                      + f" -> {res['hex']}" + R)
                ok += 1
            else:
                print(RE + f"  KO  analyse('{test[0]}')"
                      + f" -> {res['erreur']}" + R)
                ko += 1

        elif test[-1] == "compare":
            res = client.comparer(test[0], test[1])
            if "erreur" not in res:
                ident = "identiques" if res["identiques"] else f"{res['nb_diff']} diff"
                print(G + f"  OK  compare('{test[0]}','{test[1]}')"
                      + f" -> {ident}" + R)
                ok += 1
            else:
                print(RE + f"  KO  compare -> {res['erreur']}" + R)
                ko += 1

        elif test[-1] == "stats":
            res = client.stats(test[0])
            if "erreur" not in res:
                print(G + f"  OK  stats('{test[0]}')"
                      + f" -> {res['nb_octets']} oct" + R)
                ok += 1
            else:
                print(RE + f"  KO  stats -> {res['erreur']}" + R)
                ko += 1

    print()
    print(LN)
    print(G + f"  OK : {ok}   KO : {ko}" + R)
    if ko == 0:
        print(G + "  TOUS LES TESTS PASSENT ! " + R)
    else:
        print(RE + f"  {ko} test(s) echoue(s) !" + R)


if __name__ == "__main__":
    main()