#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║         TESTS UNITAIRES UTF-8                       ║
║         Python 3.14.2 — unittest                   ║
╚══════════════════════════════════════════════════════╝
"""

import unittest
import sys
sys.path.insert(0, r"C:\PythonProjets")

from utf8_package.encodeur  import (encoder_char,
                                     encoder_texte)
from utf8_package.decodeur  import decoder_hex
from utf8_package.analyseur import (analyser_char,
                                     analyser_texte,
                                     comparer)
from utf8_package.utils     import (valider_hex,
                                     hex_vers_octets,
                                     octets_vers_hex,
                                     taille_utf8)


# ════════════════════════════════════════════
#  TESTS — UTILS
# ════════════════════════════════════════════
class TestUtils(unittest.TestCase):
    """Tests des utilitaires"""

    def test_valider_hex_valide(self):
        """Hex valides"""
        self.assertTrue(valider_hex("C3"))
        self.assertTrue(valider_hex("FF"))
        self.assertTrue(valider_hex("00"))
        self.assertTrue(valider_hex("41"))

    def test_valider_hex_invalide(self):
        """Hex invalides"""
        self.assertFalse(valider_hex("ZZ"))
        self.assertFalse(valider_hex("GG"))
        self.assertFalse(valider_hex(""))

    def test_octets_vers_hex(self):
        """Conversion octets → hex"""
        self.assertEqual(
            octets_vers_hex([0xC3, 0xA9]),
            "C3 A9")
        self.assertEqual(
            octets_vers_hex([0x41]),
            "41")
        self.assertEqual(
            octets_vers_hex([0xF0,0x9F,0x90,0x8D]),
            "F0 9F 90 8D")

    def test_hex_vers_octets(self):
        """Conversion hex → octets"""
        self.assertEqual(
            hex_vers_octets("C3 A9"),
            [0xC3, 0xA9])
        self.assertEqual(
            hex_vers_octets("41"),
            [0x41])

    def test_hex_vers_octets_invalide(self):
        """Hex invalide lève ValueError"""
        with self.assertRaises(ValueError):
            hex_vers_octets("ZZ FF")

    def test_taille_utf8(self):
        """Taille selon premier octet"""
        self.assertEqual(taille_utf8(0x41), 1)
        self.assertEqual(taille_utf8(0xC3), 2)
        self.assertEqual(taille_utf8(0xE2), 3)
        self.assertEqual(taille_utf8(0xF0), 4)

    def test_taille_utf8_invalide(self):
        """Octet invalide lève ValueError"""
        with self.assertRaises(ValueError):
            taille_utf8(0xFF)


# ════════════════════════════════════════════
#  TESTS — ENCODEUR
# ════════════════════════════════════════════
class TestEncodeur(unittest.TestCase):
    """Tests de l'encodeur UTF-8"""

    # ── encoder_char ────────────────────
    def test_encoder_char_ascii(self):
        """ASCII 1 octet"""
        self.assertEqual(encoder_char("A"), [0x41])
        self.assertEqual(encoder_char("a"), [0x61])
        self.assertEqual(encoder_char(" "), [0x20])

    def test_encoder_char_2octets(self):
        """Latin étendu 2 octets"""
        self.assertEqual(
            encoder_char("é"), [0xC3, 0xA9])
        self.assertEqual(
            encoder_char("ç"), [0xC3, 0xA7])
        self.assertEqual(
            encoder_char("€")[0], 0xE2)

    def test_encoder_char_3octets(self):
        """Symboles 3 octets"""
        self.assertEqual(
            encoder_char("€"),
            [0xE2, 0x82, 0xAC])
        self.assertEqual(
            encoder_char("™"),
            [0xE2, 0x84, 0xA2])

    def test_encoder_char_4octets(self):
        """Emojis 4 octets"""
        self.assertEqual(
            encoder_char("🐍"),
            [0xF0, 0x9F, 0x90, 0x8D])
        self.assertEqual(
            encoder_char("🌍"),
            [0xF0, 0x9F, 0x8C, 0x8D])

    # ── encoder_texte ───────────────────
    def test_encoder_texte_simple(self):
        """Texte ASCII simple"""
        res = encoder_texte("ABC")
        self.assertEqual(res["hex"], "41 42 43")
        self.assertEqual(res["nb_chars"], 3)
        self.assertEqual(res["nb_octets"], 3)

    def test_encoder_texte_accent(self):
        """Texte avec accents"""
        res = encoder_texte("café")
        self.assertEqual(
            res["hex"], "63 61 66 C3 A9")
        self.assertEqual(res["nb_chars"], 4)
        self.assertEqual(res["nb_octets"], 5)

    def test_encoder_texte_emoji(self):
        """Texte avec emoji"""
        res = encoder_texte("🐍")
        self.assertEqual(
            res["hex"], "F0 9F 90 8D")
        self.assertEqual(res["nb_octets"], 4)

    def test_encoder_texte_mixte(self):
        """Texte mixte ASCII+Latin+Emoji"""
        res = encoder_texte("Hi 🐍")
        self.assertEqual(res["nb_chars"], 4)
        self.assertEqual(res["nb_octets"], 7)

    def test_encoder_texte_vide(self):
        """Texte vide lève ValueError"""
        with self.assertRaises(ValueError):
            encoder_texte("")

    def test_encoder_texte_type_invalide(self):
        """Type invalide lève TypeError"""
        with self.assertRaises(TypeError):
            encoder_texte(12345)
        with self.assertRaises(TypeError):
            encoder_texte(["a", "b"])

    def test_encoder_details(self):
        """Vérifier les détails"""
        res = encoder_texte("Aé")
        self.assertEqual(len(res["details"]), 2)
        self.assertEqual(
            res["details"][0]["char"], "A")
        self.assertEqual(
            res["details"][0]["hex"], "41")
        self.assertEqual(
            res["details"][1]["char"], "é")
        self.assertEqual(
            res["details"][1]["hex"], "C3 A9")


# ════════════════════════════════════════════
#  TESTS — DÉCODEUR
# ════════════════════════════════════════════
class TestDecodeur(unittest.TestCase):
    """Tests du décodeur UTF-8"""

    def test_decoder_ascii(self):
        """Décoder ASCII"""
        res = decoder_hex("41 42 43")
        self.assertEqual(res["texte"], "ABC")

    def test_decoder_accent(self):
        """Décoder accent"""
        res = decoder_hex("C3 A9")
        self.assertEqual(res["texte"], "é")

    def test_decoder_symbole(self):
        """Décoder symbole 3 octets"""
        res = decoder_hex("E2 82 AC")
        self.assertEqual(res["texte"], "€")

    def test_decoder_emoji(self):
        """Décoder emoji 4 octets"""
        res = decoder_hex("F0 9F 90 8D")
        self.assertEqual(res["texte"], "🐍")

    def test_decoder_mixte(self):
        """Décoder texte mixte"""
        res = decoder_hex(
            "C3 A9 20 E2 82 AC 20 F0 9F 90 8D")
        self.assertEqual(res["texte"], "é € 🐍")

    def test_decoder_hex_invalide(self):
        """Hex invalide lève ValueError"""
        with self.assertRaises(ValueError):
            decoder_hex("ZZ FF")

    def test_decoder_vide(self):
        """Hex vide lève ValueError"""
        with self.assertRaises(ValueError):
            decoder_hex("")

    def test_decoder_utf8_invalide(self):
        """Séquence UTF-8 invalide"""
        with self.assertRaises(ValueError):
            decoder_hex("FF FE")

    def test_encodage_decodage_aller_retour(self):
        """Encoder puis décoder = texte original"""
        textes = ["café", "Été ™", "Hello 🐍"]
        for texte in textes:
            res_enc = encoder_texte(texte)
            res_dec = decoder_hex(res_enc["hex"])
            self.assertEqual(
                res_dec["texte"], texte,
                f"Aller-retour échoué : {texte}")


# ════════════════════════════════════════════
#  TESTS — ANALYSEUR
# ════════════════════════════════════════════
class TestAnalyseur(unittest.TestCase):
    """Tests de l'analyseur UTF-8"""

    def test_analyser_char_ascii(self):
        """Analyser ASCII"""
        res = analyser_char("A")
        self.assertEqual(res["cp"],  65)
        self.assertEqual(res["hex"], "41")
        self.assertEqual(res["n"],   1)
        self.assertEqual(res["nom"],
                         "LATIN CAPITAL LETTER A")

    def test_analyser_char_accent(self):
        """Analyser accent"""
        res = analyser_char("é")
        self.assertEqual(res["cp"],  233)
        self.assertEqual(res["hex"], "C3 A9")
        self.assertEqual(res["n"],   2)

    def test_analyser_char_emoji(self):
        """Analyser emoji"""
        res = analyser_char("🐍")
        self.assertEqual(res["n"],   4)
        self.assertEqual(res["hex"], "F0 9F 90 8D")
        self.assertEqual(res["nom"], "SNAKE")

    def test_analyser_texte_ascii_pur(self):
        """Texte ASCII pur"""
        res = analyser_texte("Hello")
        self.assertEqual(res["nb_chars"],  5)
        self.assertEqual(res["nb_octets"], 5)
        self.assertEqual(res["pct_ascii"], 100.0)
        self.assertEqual(len(res["types"][1]), 5)

    def test_analyser_texte_mixte(self):
        """Texte mixte"""
        res = analyser_texte("café")
        self.assertEqual(res["nb_chars"],  4)
        self.assertEqual(res["nb_octets"], 5)
        self.assertEqual(len(res["types"][1]), 3)
        self.assertEqual(len(res["types"][2]), 1)

    def test_comparer_identiques(self):
        """Textes identiques"""
        res = comparer("café", "café")
        self.assertTrue(res["identiques"])
        self.assertEqual(len(res["differences"]), 0)

    def test_comparer_differents(self):
        """Textes différents"""
        res = comparer("café", "cafe")
        self.assertFalse(res["identiques"])
        self.assertEqual(len(res["differences"]), 1)
        self.assertEqual(
            res["differences"][0]["pos"], 4)
        self.assertEqual(
            res["differences"][0]["c1"], "é")
        self.assertEqual(
            res["differences"][0]["c2"], "e")

    def test_comparer_octets(self):
        """Vérifier le compte d'octets"""
        res = comparer("café", "cafe")
        self.assertEqual(res["oct1"], 5)
        self.assertEqual(res["oct2"], 4)


# ════════════════════════════════════════════
#  TESTS — ALLER-RETOUR COMPLET
# ════════════════════════════════════════════
class TestAllerRetour(unittest.TestCase):
    """Tests d'aller-retour encode/decode"""

    TEXTES = [
        "Hello World",
        "café thé été",
        "Bonjour 🌍",
        "™ © ® € £",
        "ñ ü ç œ ß",
        "Hello 🐍 €",
        "Ω Ā ƒ",
    ]

    def test_aller_retour_tous(self):
        """Encode puis decode = original"""
        for texte in self.TEXTES:
            with self.subTest(texte=texte):
                enc = encoder_texte(texte)
                dec = decoder_hex(enc["hex"])
                self.assertEqual(
                    dec["texte"], texte)

    def test_nb_octets_coherent(self):
        """Octets cohérents avec Python"""
        for texte in self.TEXTES:
            with self.subTest(texte=texte):
                res      = encoder_texte(texte)
                expected = len(
                    texte.encode("utf-8"))
                self.assertEqual(
                    res["nb_octets"], expected)


# ════════════════════════════════════════════
#  LANCEMENT DES TESTS
# ════════════════════════════════════════════
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║         TESTS UNITAIRES UTF-8                       ║
║         Python 3.14.2 — unittest                   ║
╚══════════════════════════════════════════════════════╝
""")
    # Lance tous les tests avec rapport détaillé
    loader  = unittest.TestLoader()
    suite   = loader.loadTestsFromModule(
              __import__("__main__"))
    runner  = unittest.TextTestRunner(
              verbosity=2)
    result  = runner.run(suite)

    print()
    print("=" * 55)
    if result.wasSuccessful():
        print("  TOUS LES TESTS PASSENT ! ✅")
    else:
        print(f"  ÉCHECS    : "
              f"{len(result.failures)}")
        print(f"  ERREURS   : "
              f"{len(result.errors)}")
    print("=" * 55)