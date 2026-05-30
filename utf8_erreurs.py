#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         GESTION DES ERREURS UTF-8                   ║
║         Python 3.14.2                               ║
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
W  = Fore.WHITE
D  = Style.DIM   + Fore.WHITE
R  = Style.RESET_ALL
RE = Fore.RED    + Style.BRIGHT
LN = G + "=" * 55 + R


# ════════════════════════════════════════════
#  EXCEPTIONS PERSONNALISÉES
# ════════════════════════════════════════════
class UTF8Error(Exception):
    """Erreur de base UTF-8"""
    pass

class HexInvalideError(UTF8Error):
    """Erreur hex invalide"""
    def __init__(self, valeur):
        self.valeur = valeur
        super().__init__(
            f"Hex invalide : '{valeur}' "
            f"— utilisez 00-FF !")

class CodepointInvalideError(UTF8Error):
    """Erreur codepoint hors plage"""
    def __init__(self, cp):
        self.cp = cp
        super().__init__(
            f"Codepoint hors plage : "
            f"{cp} (max: 1114111)")

class FichierUTF8Error(UTF8Error):
    """Erreur fichier UTF-8"""
    def __init__(self, chemin, raison):
        self.chemin = chemin
        super().__init__(
            f"Erreur fichier '{chemin}' : {raison}")


# ════════════════════════════════════════════
#  CLASSE AVEC GESTION D'ERREURS
# ════════════════════════════════════════════
class UTF8Safe:
    """
    Convertisseur UTF-8 avec gestion
    complète des erreurs.
    """

    def __init__(self):
        self.erreurs = []
        self.succes  = 0

    # ── Encodeur sécurisé ────────────────
    def encoder(self, texte):
        """Encode avec gestion d'erreurs"""
        try:
            if not isinstance(texte, str):
                raise TypeError(
                    f"Attendu str, reçu "
                    f"{type(texte).__name__}")

            if not texte:
                raise ValueError(
                    "Texte vide !")

            tous = []
            for c in texte:
                cp = ord(c)
                if cp > 1114111:
                    raise CodepointInvalideError(cp)
                tous.extend(self._encode_char(c))

            hex_res = " ".join(
                f"{b:02X}" for b in tous)
            self.succes += 1
            return hex_res

        except (TypeError, ValueError,
                CodepointInvalideError) as e:
            self._log_erreur("ENCODE", str(e))
            raise

        except Exception as e:
            self._log_erreur("ENCODE",
                f"Inattendue : {e}")
            raise

    # ── Décodeur sécurisé ────────────────
    def decoder(self, hex_string):
        """Décode avec gestion d'erreurs"""
        try:
            if not hex_string.strip():
                raise ValueError("Hex vide !")

            # Valider chaque token
            tokens = hex_string.strip().split()
            octets = []
            for tok in tokens:
                tok_clean = tok.replace(
                    "0x","").replace("0X","")
                if len(tok_clean) > 2 or \
                   not all(c in
                   "0123456789ABCDEFabcdef"
                   for c in tok_clean):
                    raise HexInvalideError(tok)
                octets.append(int(tok_clean, 16))

            # Valider la séquence UTF-8
            try:
                texte = bytes(octets).decode(
                    "utf-8")
            except UnicodeDecodeError as e:
                raise UTF8Error(
                    f"Séquence UTF-8 invalide : "
                    f"{hex_string} — {e}")

            self.succes += 1
            return texte

        except (ValueError, HexInvalideError,
                UTF8Error) as e:
            self._log_erreur("DECODE", str(e))
            raise

        except Exception as e:
            self._log_erreur("DECODE",
                f"Inattendue : {e}")
            raise

    # ── Lire fichier sécurisé ────────────
    def lire_fichier(self, chemin):
        """Lit un fichier avec gestion d'erreurs"""
        try:
            if not os.path.exists(chemin):
                raise FichierUTF8Error(
                    chemin, "introuvable")

            if not chemin.endswith(".txt"):
                raise FichierUTF8Error(
                    chemin,
                    "seuls les .txt acceptés")

            taille = os.path.getsize(chemin)
            if taille == 0:
                raise FichierUTF8Error(
                    chemin, "fichier vide")

            if taille > 1_000_000:
                raise FichierUTF8Error(
                    chemin,
                    f"trop grand : {taille} octets")

            with open(chemin, "r",
                      encoding="utf-8") as f:
                contenu = f.read()

            self.succes += 1
            return contenu

        except FichierUTF8Error:
            raise
        except UnicodeDecodeError:
            raise FichierUTF8Error(
                chemin, "pas un fichier UTF-8")
        except PermissionError:
            raise FichierUTF8Error(
                chemin, "permission refusée")
        except Exception as e:
            raise FichierUTF8Error(
                chemin, str(e))

    # ── Encodeur char ────────────────────
    def _encode_char(self, c):
        cp = ord(c)
        if cp <= 127:
            return [cp]
        elif cp <= 2047:
            return [0b11000000|(cp>>6),
                    0b10000000|(cp&0b00111111)]
        elif cp <= 65535:
            return [0b11100000|(cp>>12),
                    0b10000000|((cp>>6)&0b00111111),
                    0b10000000|(cp&0b00111111)]
        else:
            return [0b11110000|(cp>>18),
                    0b10000000|((cp>>12)&0b00111111),
                    0b10000000|((cp>>6)&0b00111111),
                    0b10000000|(cp&0b00111111)]

    # ── Log erreurs ──────────────────────
    def _log_erreur(self, op, msg):
        self.erreurs.append({
            "op":  op,
            "msg": msg
        })

    def afficher_erreurs(self):
        if not self.erreurs:
            print(G + "  Aucune erreur ! ✅" + R)
            return
        for i, e in enumerate(self.erreurs, 1):
            print(f"  {RE}#{i} {e['op']:<8}{R} "
                  f"{W}{e['msg']}{R}")

    def __str__(self):
        return (f"UTF8Safe("
                f"{self.succes} succès, "
                f"{len(self.erreurs)} erreurs)")


# ════════════════════════════════════════════
#  TESTS COMPLETS
# ════════════════════════════════════════════
def tester(description, fn, *args):
    """Teste une fonction et affiche le résultat"""
    print(f"  {Y}Test{R} : {W}{description}{R}")
    try:
        res = fn(*args)
        print(f"  {G}✅ Succès{R} : {C}{res}{R}")
    except UTF8Error as e:
        print(f"  {RE}❌ UTF8Error{R} : {W}{e}{R}")
    except TypeError as e:
        print(f"  {RE}❌ TypeError{R} : {W}{e}{R}")
    except ValueError as e:
        print(f"  {RE}❌ ValueError{R} : {W}{e}{R}")
    except Exception as e:
        print(f"  {RE}❌ Erreur{R} : {W}{e}{R}")
    finally:
        print()


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(G + """
╔══════════════════════════════════════════════════════╗
║         GESTION DES ERREURS UTF-8                   ║
╚══════════════════════════════════════════════════════╝""" + R)

    conv = UTF8Safe()
    print(G + f"\n  Objet : {conv}\n" + R)

    # ── Tests ENCODEUR ───────────────────
    print(Y + "  ── Tests ENCODEUR ──\n" + R)

    tester("Texte valide",
           conv.encoder, "café 🌍")

    tester("Texte vide",
           conv.encoder, "")

    tester("Type invalide (int)",
           conv.encoder, 12345)

    tester("Texte ASCII pur",
           conv.encoder, "Hello World")

    # ── Tests DÉCODEUR ───────────────────
    print(Y + "  ── Tests DÉCODEUR ──\n" + R)

    tester("Hex valide",
           conv.decoder, "C3 A9 20 E2 82 AC")

    tester("Hex invalide ZZ",
           conv.decoder, "ZZ 9F")

    tester("Hex vide",
           conv.decoder, "")

    tester("Séquence UTF-8 invalide",
           conv.decoder, "FF FE")

    tester("Hex avec 0x",
           conv.decoder, "0x43 0x33")

    # ── Tests FICHIER ────────────────────
    print(Y + "  ── Tests FICHIER ──\n" + R)

    tester("Fichier valide",
           conv.lire_fichier,
           r"C:\PythonProjets\test_utf8.txt")

    tester("Fichier introuvable",
           conv.lire_fichier,
           r"C:\PythonProjets\absent.txt")

    tester("Extension invalide",
           conv.lire_fichier,
           r"C:\PythonProjets\test.py")

    # ── Bilan ────────────────────────────
    print(LN)
    print(G + f"\n  Bilan final : {conv}\n" + R)
    print(Y + "  Erreurs enregistrées :\n" + R)
    conv.afficher_erreurs()
    print()
    print(LN)
    input(D + "\n  Entrée pour quitter..." + R)


if __name__ == "__main__":
    main()
    
    