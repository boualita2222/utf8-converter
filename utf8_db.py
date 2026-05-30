#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         UTF-8 DATABASE — SQLite                     ║
║         Python 3.14.2                               ║
╚══════════════════════════════════════════════════════╝
"""

import sqlite3
import os
import sys
from datetime import datetime
sys.path.insert(0, r"C:\PythonProjets")

from utf8_package.encodeur  import encoder_texte
from utf8_package.decodeur  import decoder_hex
from utf8_package.analyseur import analyser_texte

try:
    from colorama import init, Fore, Style
    init(autoreset=False, strip=False,
         convert=True)
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

DB_PATH = r"C:\PythonProjets\utf8_history.db"


# ════════════════════════════════════════════
#  CLASSE DATABASE
# ════════════════════════════════════════════
class UTF8Database:
    """
    Gestionnaire de base de données SQLite
    pour l'historique UTF-8
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn    = None
        self.cursor  = None
        self._connecter()
        self._creer_tables()

    # ────────────────────────────────────────
    #  CONNEXION
    # ────────────────────────────────────────
    def _connecter(self):
        """Ouvre la connexion SQLite"""
        try:
            self.conn = sqlite3.connect(
    self.db_path,
    check_same_thread=False)
            self.conn.row_factory = \
                sqlite3.Row
            self.cursor = self.conn.cursor()
            print(G +
                f"  ✅ Base connectée : "
                f"{self.db_path}" + R)
        except sqlite3.Error as e:
            print(RE +
                f"  ❌ Erreur connexion : "
                f"{e}" + R)
            raise

    # ────────────────────────────────────────
    #  CRÉATION DES TABLES
    # ────────────────────────────────────────
    def _creer_tables(self):
        """Crée les tables si inexistantes"""
        # Table principale — historique
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            historique (
                id          INTEGER
                            PRIMARY KEY
                            AUTOINCREMENT,
                operation   TEXT NOT NULL,
                entree      TEXT NOT NULL,
                sortie      TEXT NOT NULL,
                nb_chars    INTEGER DEFAULT 0,
                nb_octets   INTEGER DEFAULT 0,
                date        TEXT NOT NULL,
                note        TEXT DEFAULT ''
            )
        """)

        # Table statistiques globales
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            stats_globales (
                id          INTEGER
                            PRIMARY KEY
                            AUTOINCREMENT,
                texte       TEXT NOT NULL,
                nb_chars    INTEGER,
                nb_octets   INTEGER,
                pct_ascii   REAL,
                nb_1oct     INTEGER DEFAULT 0,
                nb_2oct     INTEGER DEFAULT 0,
                nb_3oct     INTEGER DEFAULT 0,
                nb_4oct     INTEGER DEFAULT 0,
                date        TEXT NOT NULL
            )
        """)

        # Table favoris
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            favoris (
                id          INTEGER
                            PRIMARY KEY
                            AUTOINCREMENT,
                nom         TEXT NOT NULL,
                texte       TEXT NOT NULL,
                hex         TEXT NOT NULL,
                date        TEXT NOT NULL
            )
        """)

        self.conn.commit()
        print(G +
            "  ✅ Tables créées / vérifiées"
            + R)

    # ────────────────────────────────────────
    #  INSÉRER
    # ────────────────────────────────────────
    def ajouter_historique(self,
            operation, entree, sortie,
            nb_chars=0, nb_octets=0,
            note=""):
        """Ajoute une entrée dans l'historique"""
        date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute("""
                INSERT INTO historique
                (operation, entree, sortie,
                 nb_chars, nb_octets,
                 date, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (operation, entree, sortie,
                  nb_chars, nb_octets,
                  date, note))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(RE +
                f"  ❌ Erreur insert : {e}"
                + R)
            return None

    def ajouter_stats(self, texte,
                      stats_dict):
        """Sauvegarde les stats d'un texte"""
        date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        types = stats_dict["types"]
        try:
            self.cursor.execute("""
                INSERT INTO stats_globales
                (texte, nb_chars, nb_octets,
                 pct_ascii, nb_1oct, nb_2oct,
                 nb_3oct, nb_4oct, date)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                texte,
                stats_dict["nb_chars"],
                stats_dict["nb_octets"],
                stats_dict["pct_ascii"],
                len(types[1]),
                len(types[2]),
                len(types[3]),
                len(types[4]),
                date,
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(RE +
                f"  ❌ Erreur stats : {e}"
                + R)
            return None

    def ajouter_favori(self, nom,
                       texte, hex_str):
        """Ajoute un favori"""
        date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute("""
                INSERT INTO favoris
                (nom, texte, hex, date)
                VALUES (?, ?, ?, ?)
            """, (nom, texte, hex_str, date))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(RE +
                f"  ❌ Erreur favori : {e}"
                + R)
            return None

    # ────────────────────────────────────────
    #  LIRE
    # ────────────────────────────────────────
    def get_historique(self, limite=20):
        """Retourne les N dernières entrées"""
        self.cursor.execute("""
            SELECT id, operation, entree,
                   sortie, nb_octets, date
            FROM historique
            ORDER BY date DESC
            LIMIT ?
        """, (limite,))
        return self.cursor.fetchall()

    def get_stats(self, limite=10):
        """Retourne les stats sauvegardées"""
        self.cursor.execute("""
            SELECT texte, nb_chars,
                   nb_octets, pct_ascii,
                   nb_4oct, date
            FROM stats_globales
            ORDER BY date DESC
            LIMIT ?
        """, (limite,))
        return self.cursor.fetchall()

    def get_favoris(self):
        """Retourne tous les favoris"""
        self.cursor.execute("""
            SELECT id, nom, texte,
                   hex, date
            FROM favoris
            ORDER BY nom
        """)
        return self.cursor.fetchall()

    def rechercher(self, motif):
        """Cherche dans l'historique"""
        self.cursor.execute("""
            SELECT id, operation,
                   entree, sortie, date
            FROM historique
            WHERE entree LIKE ?
               OR sortie LIKE ?
            ORDER BY date DESC
        """, (f"%{motif}%",
               f"%{motif}%"))
        return self.cursor.fetchall()

    # ────────────────────────────────────────
    #  STATISTIQUES GLOBALES
    # ────────────────────────────────────────
    def get_resume(self):
        """Résumé global de la base"""
        stats = {}

        # Total opérations
        self.cursor.execute(
            "SELECT COUNT(*) FROM historique")
        stats["total_ops"] = \
            self.cursor.fetchone()[0]

        # Par type
        self.cursor.execute("""
            SELECT operation, COUNT(*)
            FROM historique
            GROUP BY operation
        """)
        stats["par_type"] = dict(
            self.cursor.fetchall())

        # Total octets traités
        self.cursor.execute("""
            SELECT SUM(nb_octets)
            FROM historique
        """)
        stats["total_octets"] = \
            self.cursor.fetchone()[0] or 0

        # Nb favoris
        self.cursor.execute(
            "SELECT COUNT(*) FROM favoris")
        stats["nb_favoris"] = \
            self.cursor.fetchone()[0]

        # Texte le plus long
        self.cursor.execute("""
            SELECT entree, nb_octets
            FROM historique
            WHERE operation = 'ENCODE'
            ORDER BY nb_octets DESC
            LIMIT 1
        """)
        row = self.cursor.fetchone()
        stats["plus_long"] = \
            dict(row) if row else None

        return stats

    # ────────────────────────────────────────
    #  SUPPRIMER
    # ────────────────────────────────────────
    def supprimer_historique(self, id_=None):
        """Supprime une entrée ou tout"""
        if id_:
            self.cursor.execute(
                "DELETE FROM historique "
                "WHERE id = ?", (id_,))
        else:
            self.cursor.execute(
                "DELETE FROM historique")
        self.conn.commit()
        nb = self.cursor.rowcount
        return nb

    def supprimer_favori(self, id_):
        """Supprime un favori"""
        self.cursor.execute(
            "DELETE FROM favoris "
            "WHERE id = ?", (id_,))
        self.conn.commit()

    # ────────────────────────────────────────
    #  FERMETURE
    # ────────────────────────────────────────
    def fermer(self):
        """Ferme la connexion"""
        if self.conn:
            self.conn.close()
            print(D +
                "  Base de données fermée."
                + R)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.fermer()

    def __str__(self):
        r = self.get_resume()
        return (f"UTF8Database("
                f"{r['total_ops']} ops, "
                f"{r['nb_favoris']} favoris)")


# ════════════════════════════════════════════
#  AFFICHAGE
# ════════════════════════════════════════════
def afficher_historique(rows):
    print(G + "\n  Historique :\n" + R)
    print(f"  {Y}{'ID':<4}{'OP':<10}"
          f"{'ENTREE':<20}"
          f"{'SORTIE':<20}"
          f"OCT  DATE{R}")
    print(D + "  " + "─"*65 + R)
    for row in rows:
        print(f"  {W}#{row['id']:<3}"
              f"{row['operation']:<10}"
              f"{str(row['entree'])[:18]:<20}"
              f"{str(row['sortie'])[:18]:<20}"
              f"{row['nb_octets']:<5}"
              f"{row['date']}{R}")


def afficher_favoris(rows):
    if not rows:
        print(D + "  Aucun favori." + R)
        return
    print(G + "\n  Favoris :\n" + R)
    for row in rows:
        print(f"  {Y}#{row['id']:<3}{R}"
              f"{W}{row['nom']:<15}{R}"
              f"{C}{row['texte']:<12}{R}"
              f"{D}{row['hex'][:25]}{R}")


def afficher_resume(stats):
    print(G + "\n  Résumé base de données :\n" + R)
    print(f"  {Y}Total opérations : "
          f"{R}{W}{stats['total_ops']}{R}")
    print(f"  {Y}Total octets     : "
          f"{R}{W}{stats['total_octets']}{R}")
    print(f"  {Y}Favoris          : "
          f"{R}{W}{stats['nb_favoris']}{R}")
    if stats["par_type"]:
        print(f"  {Y}Par type :{R}")
        for op, nb in \
                stats["par_type"].items():
            print(f"    {C}{op:<10}{R}"
                  f"{W}{nb}{R}")
    if stats["plus_long"]:
        print(f"  {Y}Plus long :{R} "
              f"{W}{stats['plus_long']['entree'][:20]}"
              f" ({stats['plus_long']['nb_octets']}"
              f" oct){R}")


# ════════════════════════════════════════════
#  PROGRAMME PRINCIPAL
# ════════════════════════════════════════════
def main():
    os.system("cls" if os.name=="nt"
              else "clear")
    print(G + """
╔══════════════════════════════════════════════════════╗
║         UTF-8 DATABASE — SQLite                     ║
╚══════════════════════════════════════════════════════╝""" + R)

    print()

    with UTF8Database() as db:
        print(G + f"\n  {db}\n" + R)

        # ── Encodages ────────────────────
        print(Y + "  ── Encodages ──\n" + R)
        textes = [
            "Bonjour 🌍",
            "café thé été",
            "Hello 🐍 €",
            "™ © ® £",
            "Été 🌙",
        ]
        for texte in textes:
            res = encoder_texte(texte)
            id_ = db.ajouter_historique(
                "ENCODE",
                texte,
                res["hex"],
                res["nb_chars"],
                res["nb_octets"])
            print(f"  {G}#{id_:<3}{R}"
                  f"{W}{texte:<15}{R}"
                  f"{C}{res['hex'][:25]}"
                  f"...{R}")

        # ── Décodages ────────────────────
        print(Y + "\n  ── Décodages ──\n" + R)
        sequences = [
            "C3 A9 20 E2 82 AC",
            "F0 9F 90 8D",
            "E2 84 A2",
        ]
        for seq in sequences:
            res = decoder_hex(seq)
            id_ = db.ajouter_historique(
                "DECODE",
                seq,
                res["texte"],
                len(res["texte"]),
                len(seq.split()))
            print(f"  {G}#{id_:<3}{R}"
                  f"{C}{seq:<20}{R}"
                  f"→ {Y}{res['texte']}{R}")

        # ── Stats sauvegardées ───────────
        print(Y + "\n  ── Stats ──\n" + R)
        for texte in textes[:3]:
            res = analyser_texte(texte)
            id_ = db.ajouter_stats(
                texte, res)
            print(f"  {G}#{id_:<3}{R}"
                  f"{W}{texte:<15}{R}"
                  f"{C}{res['nb_octets']}"
                  f" oct{R}")

        # ── Favoris ──────────────────────
        print(Y + "\n  ── Favoris ──\n" + R)
        favoris = [
            ("Baleine",  "🐋",
             encoder_texte("🐋")["hex"]),
            ("Euro",     "€",
             encoder_texte("€")["hex"]),
            ("Serpent",  "🐍",
             encoder_texte("🐍")["hex"]),
        ]
        for nom, texte, hex_ in favoris:
            id_ = db.ajouter_favori(
                nom, texte, hex_)
            print(f"  {G}#{id_:<3}{R}"
                  f"{Y}{nom:<12}{R}"
                  f"{W}{texte}{R}  "
                  f"{C}{hex_}{R}")

        # ── Lire l'historique ────────────
        print()
        print(LN)
        rows = db.get_historique(8)
        afficher_historique(rows)

        # ── Lire les favoris ─────────────
        print()
        rows = db.get_favoris()
        afficher_favoris(rows)

        # ── Recherche ────────────────────
        print(G + "\n  Recherche 'café' :\n" + R)
        rows = db.rechercher("café")
        for row in rows:
            print(f"  {Y}#{row['id']}{R} "
                  f"{W}{row['entree']}{R}")

        # ── Résumé ───────────────────────
        print()
        print(LN)
        stats = db.get_resume()
        afficher_resume(stats)

        print()
        print(LN)
        input(D +
            "\n  Entrée pour quitter..." + R)


if __name__ == "__main__":
    main()