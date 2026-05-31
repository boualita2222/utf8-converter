#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

╔══════════════════════════════════════════════════════════════════════════════╗
║         CONVERTISSEUR UTF-8 COMPLET  1 → 4 OCTETS                          ║
║         ASCII : 6 / 8 / 10 car.  |  Python 3.x + Colorama                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import sys
from wsgiref import validate
from colorama import init, Fore, Style

def utf8_converter(code_point):
    if code_point <= 0x7F:
        return [code_point]
    elif code_point <= 0x7FF:
        return [
            0xC0 | (code_point >> 6),
            0x80 | (code_point & 0x3F)
        ]
    elif code_point <= 0xFFFF:
        return [
            0xE0 | (code_point >> 12),
            0x80 | ((code_point >> 6) & 0x3F),
            0x80 | (code_point & 0x3F)
        ]
    elif code_point <= 0x10FFFF:
        return [
            0xF0 | (code_point >> 18),
            0x80 | ((code_point >> 12) & 0x3F),
            0x80 | ((code_point >> 6) & 0x3F),
            0x80 | (code_point & 0x3F)
        ]
    else:
        raise ValueError("Code point out of range")
def main():
    init(autoreset=True)
    print(Fore.CYAN + "╔══════════════════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║         CONVERTISSEUR UTF-8 COMPLET  1 → 4 OCTETS                          ║")
    print(Fore.CYAN + "║         ASCII : 6 / 8 / 10 car.  |  Python 3.x + Colorama                  ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════════════════════════════════╝")
    
    while True:
        try:
            user_input = input(Fore.YELLOW + "Entrez un point de code Unicode (hexadécimal) ou 'exit' pour quitter: ")
            if user_input.lower() == 'exit':
                print(Fore.GREEN + "Au revoir!")
                break
            
            code_point = int(user_input, 16)
            utf8_bytes = utf8_converter(code_point)
            utf8_hex = ' '.join(f"{byte:02X}" for byte in utf8_bytes)
            print(Fore.GREEN + f"UTF-8 Bytes: {utf8_hex}")
        except ValueError as e:
            print(Fore.RED + f"Erreur: {e}. Veuillez entrer un point de code valide.")

if __name__ == "__main__":
    main()

def test_utf8_converter():
    assert utf8_converter(0x24) == [0x24]  # U+0024: $
    assert utf8_converter(0xA2) == [0xC2, 0xA2]  # U+00A2: ¢
    assert utf8_converter(0x20AC) == [0xE2, 0x82, 0xAC]  # U+20AC: €
    assert utf8_converter(0x1F600) == [0xF0, 0x9F, 0x98, 0x80]  # U+1F600: 😀
    print("All tests passed!")
    test_utf8_converter()
    
#  MODULE 1 — Hex -> Analysee du point de code Unicode
#  MODULE 2 — Analyse du point de code Unicode -> Nombre d’octets UTF-8
#  MODULE 3 — Construction des octets UTF-8 à partir du point de code
#  MODULE 4 — Affichage des octets UTF-8 en hexadécimal
#  MODULE 5 — Interface utilisateur pour entrer des points de code et afficher les résultats
#  MODULE 6 — Tests unitaires pour valider la fonction de conversion UTF-8
#  MODULE 7 — Documentation et commentaires pour expliquer le code et les étapes de conversion
#  MODULE 8 — Gestion des erreurs pour les points de code invalides ou hors de portée
#  MODULE 0 — POUR QUITER LE PROGRAMME
def hex_to_code_point(hex_string):
    try:
        return int(hex_string, 16)
    except ValueError:
        raise ValueError("Invalid hexadecimal input")
def analyze_code_point(code_point):
        if code_point <= 0x7F:
            return 1
        elif code_point <= 0x7FF:
            return 2
        elif code_point <= 0xFFFF:
            return 3
        elif code_point <= 0x10FFFF:
            return 4
        else:
            raise ValueError("Code point out of range")
            
def construct_utf8_bytes(code_point):
            if code_point <= 0x7F:
                return [code_point]
            elif code_point <= 0x7FF:
                return [
                    0xC0 | (code_point >> 6),
                    0x80 | (code_point & 0x3F)
                ]
            elif code_point <= 0xFFFF:
                return [
                    0xE0 | (code_point >> 12),
                    0x80 | ((code_point >> 6) & 0x3F),
                    0x80 | (code_point & 0x3F)
                ]
            elif code_point <= 0x10FFFF:
                return [
                    0xF0 | (code_point >> 18),
                    0x80 | ((code_point >> 12) & 0x3F),
                    0x80 | ((code_point >> 6) & 0x3F),
                    0x80 | (code_point & 0x3F)
                ]
            else:
                raise ValueError("Code point out of range")
            
def afficher_utf8_bytes(utf8_bytes):
    return ' '.join(f"{byte:02X}" for byte in utf8_bytes)
def interface_utilisateur():
    init(autoreset=True)
    print(Fore.CYAN + "╔══════════════════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║         CONVERTISSEUR UTF-8 COMPLET  1 → 4 OCTETS                          ║")
    print(Fore.CYAN + "║         ASCII : 6 / 8 / 10 car.  |  Python 3.x + Colorama                  ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════════════════════════════════╝")
    
    while True:
        try:
            user_input = input(Fore.YELLOW + "Entrez un point de code Unicode (hexadécimal) ou 'exit' pour quitter: ")
            if user_input.lower() == 'exit':
                print(Fore.GREEN + "Au revoir!")
                break
            
            code_point = hex_to_code_point(user_input)
            utf8_bytes = construct_utf8_bytes(code_point)
            utf8_hex = afficher_utf8_bytes(utf8_bytes)
            print(Fore.GREEN + f"UTF-8 Bytes: {utf8_hex}")
        except ValueError as e:
            print(Fore.RED + f"Erreur: {e}. Veuillez entrer un point de code valide.")
            
def test_unitaire():
        assert hex_to_code_point("24") == 0x24
        assert hex_to_code_point("A2") == 0xA2
        assert hex_to_code_point("20AC") == 0x20AC
        assert hex_to_code_point("1F600") == 0x1F600
        print("Hex to code point tests passed!")
                
        assert analyze_code_point(0x24) == 1
        assert analyze_code_point(0xA2) == 2
        assert analyze_code_point(0x20AC) == 3
        assert analyze_code_point(0x1F600) == 4
        print("Code point analysis tests passed!")
                
        assert construct_utf8_bytes(0x24) == [0x24]
        assert construct_utf8_bytes(0xA2) == [0xC2, 0xA2]
        assert construct_utf8_bytes(0x20AC) == [0xE2, 0x82, 0xAC]
        assert construct_utf8_bytes(0x1F600) == [0xF0, 0x9F, 0x98, 0x80]
        print("UTF-8 byte construction tests passed!")
                
        assert afficher_utf8_bytes([0xC2, 0xA2]) == "C2 A2"
        assert afficher_utf8_bytes([0xE2, 0x82, 0xAC]) == "E2 82 AC"
        print("UTF-8 byte display tests passed!")
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
    for start, end, n_bytes, pattern in ranges:
        if start <= cp <= end:
            print(f"Code point: U+{cp:04X} ({char})")
            print(f"UTF-8 bytes: {raw.hex().upper()} ({n_bytes} bytes)")
            print(f"Pattern: {pattern}")
            break

if __name__ == "__main__":
    test_unitaire()
    interface_utilisateur()