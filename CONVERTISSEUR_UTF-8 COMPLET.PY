#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONVERTISSEUR_UTF-8 COMPLET (1 à 4 octets)
Python 3.14.2 COMPATIBLE_COLORAMAINTERNANT AVEC SUPPORT POUR 1, 2, 3 ET 4 OTETES 
Options: caractère, décimal, hexadécimal, décimal brut (big-endian)
"""
import sys
import colorama

def init_colorama():
    try:
        colorama.init(autoreset=True)
        
        
    except Exception as e:
        print(f"Erreur lors de l'initialisation de colorama: {e}")
import unicodedata
from typing import Optional, Dict, Any

def decode_utf8_sequence(bytes_list: list) -> Dict[str, Any]:
    """Décode une séquence d'octets UTF-8 et retourne toutes les informations."""
    if not bytes_list:
        return {"error": "Séquence vide"}
    
    num_bytes = len(bytes_list)
    
    # 1. Calcul de la valeur brute big-endian
    raw_decimal = 0
    for byte in bytes_list:
        raw_decimal = (raw_decimal << 8) | byte
    
    # 2. Décodage UTF-8 (si valide)
    try:
        utf8_bytes = bytes(bytes_list)
        character = utf8_bytes.decode('utf-8')
        codepoint = ord(character)
        is_valid_utf8 = True
    except (UnicodeDecodeError, ValueError):
        character = None
        codepoint = None
        is_valid_utf8 = False
    
    # 3. Décodage manuel selon le nombre d'octets
    manual_codepoint = None
    if is_valid_utf8:
        manual_codepoint = codepoint
    else:
        # Essayer de décoder manuellement
        if num_bytes == 2 and (bytes_list[0] & 0xE0) == 0xC0 and (bytes_list[1] & 0xC0) == 0x80:
            manual_codepoint = ((bytes_list[0] & 0x1F) << 6) | (bytes_list[1] & 0x3F)
        elif num_bytes == 3 and (bytes_list[0] & 0xF0) == 0xE0 and all((b & 0xC0) == 0x80 for b in bytes_list[1:]):
            manual_codepoint = ((bytes_list[0] & 0x0F) << 12) | ((bytes_list[1] & 0x3F) << 6) | (bytes_list[2] & 0x3F)
        elif num_bytes == 4 and (bytes_list[0] & 0xF8) == 0xF0 and all((b & 0xC0) == 0x80 for b in bytes_list[1:]):
            manual_codepoint = ((bytes_list[0] & 0x07) << 18) | ((bytes_list[1] & 0x3F) << 12) | ((bytes_list[2] & 0x3F) << 6) | (bytes_list[3] & 0x3F)
    
    # 4. Nom Unicode (si disponible)
    unicode_name = None
    if manual_codepoint:
        try:
            unicode_name = unicodedata.name(chr(manual_codepoint))
        except ValueError:
            unicode_name = "Nom inconnu"
    
    return {
        "bytes": bytes_list,
        "num_bytes": num_bytes,
        "hex_string": ' '.join(f'{b:02X}' for b in bytes_list),
        "hex_compact": ''.join(f'{b:02X}' for b in bytes_list),
        "binary": ' '.join(f'{b:08b}' for b in bytes_list),
        "raw_decimal": raw_decimal,
        "character": character,
        "codepoint": manual_codepoint,
        "unicode_hex": f"U+{manual_codepoint:04X}" if manual_codepoint else None,
        "unicode_name": unicode_name,
        "is_valid_utf8": is_valid_utf8 or (manual_codepoint is not None)
    }

def hex_to_info(hex_input: str) -> Dict[str, Any]:
    """Convertit une chaîne hexadécimale en informations détaillées."""
    # Nettoyer l'entrée
    hex_clean = hex_input.replace(' ', '').replace('0x', '').replace(',', '')
    
    if not hex_clean:
        return {"error": "Chaîne hexadécimale vide"}
    
    # Vérifier la longueur
    if len(hex_clean) % 2 != 0:
        hex_clean = '0' + hex_clean  # Pad avec un zéro à gauche
    
    # Convertir en liste d'octets
    try:
        bytes_list = []
        for i in range(0, len(hex_clean), 2):
            byte_str = hex_clean[i:i+2]
            bytes_list.append(int(byte_str, 16))
    except ValueError:
        return {"error": f"Hexadécimal invalide: {hex_input}"}
    
    # Limiter à 4 octets maximum
    if len(bytes_list) > 4:
        bytes_list = bytes_list[:4]
    
    return decode_utf8_sequence(bytes_list)

def decimal_to_info(decimal_input: int, force_bytes: int = None) -> Dict[str, Any]:
    """Convertit un nombre décimal en informations UTF-8."""
    # Vérifier les limites
    if decimal_input < 0:
        return {"error": "Le décimal doit être positif"}
    
    # Déterminer le nombre d'octets
    if force_bytes:
        num_bytes = force_bytes
        if num_bytes < 1 or num_bytes > 4:
            return {"error": "Nombre d'octets doit être entre 1 et 4"}
    else:
        # Auto-détection basée sur la valeur
        if decimal_input <= 0xFF:
            num_bytes = 1
        elif decimal_input <= 0xFFFF:
            num_bytes = 2
        elif decimal_input <= 0xFFFFFF:
            num_bytes = 3
        else:
            num_bytes = 4
    
    # Extraire les octets (big-endian)
    bytes_list = []
    temp = decimal_input
    for _ in range(num_bytes):
        bytes_list.insert(0, temp & 0xFF)
        temp >>= 8
    
    # Si la valeur est trop grande pour le nombre d'octets
    if temp > 0:
        return {"error": f"Valeur {decimal_input} trop grande pour {num_bytes} octet(s)"}
    
    return decode_utf8_sequence(bytes_list)

def character_to_info(char: str) -> Dict[str, Any]:
    """Convertit un caractère en informations UTF-8."""
    if len(char) != 1:
        return {"error": "Entrez exactement un caractère"}
    
    try:
        # Obtenir le code point
        codepoint = ord(char)
        
        # Encoder en UTF-8
        utf8_bytes = char.encode('utf-8')
        bytes_list = list(utf8_bytes)
        
        # Calculer la valeur brute
        raw_decimal = 0
        for byte in bytes_list:
            raw_decimal = (raw_decimal << 8) | byte
        
        # Obtenir le nom Unicode
        try:
            unicode_name = unicodedata.name(char)
        except ValueError:
            unicode_name = "Nom inconnu"
        
        return {
            "bytes": bytes_list,
            "num_bytes": len(bytes_list),
            "hex_string": ' '.join(f'{b:02X}' for b in bytes_list),
            "hex_compact": ''.join(f'{b:02X}' for b in bytes_list),
            "binary": ' '.join(f'{b:08b}' for b in bytes_list),
            "raw_decimal": raw_decimal,
            "character": char,
            "codepoint": codepoint,
            "unicode_hex": f"U+{codepoint:04X}",
            "unicode_name": unicode_name,
            "is_valid_utf8": True
        }
    except Exception as e:
        return {"error": f"Erreur de conversion: {e}"}

def show(hex1: str, hex2: str = None, hex3: str = None, hex4: str = None):
    """Fonction similaire à votre exemple avec support 1-4 octets."""
    hex_list = [h for h in [hex1, hex2, hex3, hex4] if h is not None]
    hex_str = ' '.join(hex_list)
    
    print(f"\n{'='*70}")
    print(f"ANALYSE: {hex_str}")
    print('='*70)
    
    result = hex_to_info(hex_str)
    
    if "error" in result:
        print(f"❌ Erreur: {result['error']}")
        return
    
    # Affichage détaillé
    print(f"Hexadécimal  : {result['hex_string']}")
    print(f"Octets       : {result['num_bytes']}")
    print(f"Octets bruts : {result['bytes']}")
    print(f"Binaire      : {result['binary']}")
    print(f"Décimal brut : {result['raw_decimal']:,} (0x{result['raw_decimal']:X})")
    
    if result['character']:
        print(f"Caractère    : {result['character']}")
    
    if result['codepoint']:
        print(f"Unicode      : {result['unicode_hex']}")
        print(f"Décimal      : {result['codepoint']:,}")
        if result['unicode_name']:
            print(f"Nom Unicode  : {result['unicode_name']}")
    
    # Explication du calcul
    print(f"\nCALCUL DÉTAILLÉ:")
    bytes_list = result['bytes']
    
    if len(bytes_list) == 2:
        b1, b2 = bytes_list
        print(f"  ({b1} × 256) + {b2} = ({b1} × 256) + {b2} = {result['raw_decimal']}")
        print(f"  0x{b1:02X} 0x{b2:02X} = (0x{b1:02X} * 0x100) + 0x{b2:02X} = 0x{result['raw_decimal']:X}")
    
    elif len(bytes_list) == 3:
        b1, b2, b3 = bytes_list
        print(f"  ({b1} × 65536) + ({b2} × 256) + {b3} = {result['raw_decimal']}")
        print(f"  0x{b1:02X} 0x{b2:02X} 0x{b3:02X} = (0x{b1:02X} * 0x10000) + (0x{b2:02X} * 0x100) + 0x{b3:02X} = 0x{result['raw_decimal']:X}")
    
    elif len(bytes_list) == 4:
        b1, b2, b3, b4 = bytes_list
        print(f"  ({b1} × 16777216) + ({b2} × 65536) + ({b3} × 256) + {b4} = {result['raw_decimal']}")
        print(f"  0x{b1:02X} 0x{b2:02X} 0x{b3:02X} 0x{b4:02X} = (0x{b1:02X} * 0x1000000) + (0x{b2:02X} * 0x10000) + (0x{b3:02X} * 0x100) + 0x{b4:02X} = 0x{result['raw_decimal']:X}")
    
    print(f"Séquence UTF-8 valide : {'OUI' if result['is_valid_utf8'] else 'NON'}")

def display_result(result: Dict[str, Any], input_type: str):
    """Affiche un résultat de conversion."""
    if "error" in result:
        print(f"\n❌ Erreur: {result['error']}")
        return
    
    print(f"\n{'='*70}")
    print(f"RÉSULTAT ({input_type})")
    print('='*70)
    
    print(f"Hexadécimal  : {result['hex_string']}")
    print(f"Octets       : {result['num_bytes']}")
    print(f"Binaire      : {result['binary']}")
    print(f"Décimal brut : {result['raw_decimal']:,} (0x{result['raw_decimal']:X})")
    
    if result['character']:
        print(f"Caractère    : {result['character']}")
    
    if result['codepoint']:
        print(f"Code point   : {result['unicode_hex']}")
        print(f"Décimal      : {result['codepoint']:,}")
        if result['unicode_name']:
            print(f"Nom          : {result['unicode_name']}")
    
    print(f"UTF-8 valide : {'✅ OUI' if result['is_valid_utf8'] else '❌ NON'}")

def interactive_menu():
    """Menu interactif principal."""
    print("🎯 CONVERTISSEUR UTF-8 COMPLET (1 à 4 octets)")
    print("="*70)
    
    while True:
        print("\nOPTIONS :")
        print("  1. Hexadécimal → Analyse (ex: C2 80, F0 9F 9A 81)")
        print("  2. Décimal → Analyse (ex: 49792, 4036991617)")
        print("  3. Caractère → Analyse (ex: A, €, 😊)")
        print("  4. Fonction show() personnalisée (comme votre exemple)")
        print("  5. Exemples prédéfinis")
        print("  6. Quitter")
        
        choix = input("\nVotre choix (1-6): ").strip()
        
        if choix == '6':
            print("\nAu revoir! 👋")
            break
        
        elif choix == '1':
            hex_input = input("Hexadécimal (1-4 octets, espaces optionnels): ").strip()
            result = hex_to_info(hex_input)
            display_result(result, f"Hex: {hex_input}")
        
        elif choix == '2':
            try:
                dec_input = input("Décimal: ").strip().replace(',', '')
                decimal = int(dec_input)
                result = decimal_to_info(decimal)
                display_result(result, f"Dec: {decimal:,}")
            except ValueError:
                print("❌ Entrez un nombre valide")
        
        elif choix == '3':
            char_input = input("Caractère (un seul): ").strip()
            result = character_to_info(char_input)
            display_result(result, f"Char: '{char_input}'")
        
        elif choix == '4':
            print("\nFormat: show(octet1, [octet2, octet3, octet4])")
            print("Exemple: show('C2', '80')")
            
            hex_values = []
            for i in range(1, 5):
                value = input(f"Octet {i} (hex, vide pour terminer): ").strip().upper()
                if not value:
                    break
                hex_values.append(value)
            
            if len(hex_values) == 1:
                show(hex_values[0])
            elif len(hex_values) == 2:
                show(hex_values[0], hex_values[1])
            elif len(hex_values) == 3:
                show(hex_values[0], hex_values[1], hex_values[2])
            elif len(hex_values) == 4:
                show(hex_values[0], hex_values[1], hex_values[2], hex_values[3])
        
        elif choix == '5':
            run_examples()
        
        else:
            print("❌ Choix invalide")

def run_examples():
    """Exécute les exemples demandés et plus."""
    print("\n" + "="*70)
    print("EXEMPLES PRÉDÉFINIS")
    print("="*70)
    
    examples = [
        # (description, fonction, paramètres)
        ("1 octet: 'A'", character_to_info, ["A"]),
        ("2 octets: 'é'", character_to_info, ["é"]),
        ("2 octets: C3 80 = 50048", hex_to_info, ["C3 80"]),
        ("3 octets: '€'", character_to_info, ["€"]),
        ("3 octets: E2 82 AC = 14844588", hex_to_info, ["E2 82 AC"]),
        ("4 octets: '😊'", character_to_info, ["😊"]),
        ("4 octets: F0 9F 9F A0 = 4036992928", hex_to_info, ["F0 9F 9F A0"]),
        ("4 octets: F0 9F 9A 81 = 4036991617 (hélicoptère)", hex_to_info, ["F0 9F 9A 81"]),
    ]
    
    for desc, func, params in examples:
        print(f"\n{desc}")
        print("-" * 40)
        result = func(*params)
        
        if "error" not in result:
            print(f"Hex: {result['hex_string']}")
            print(f"Dec brut: {result['raw_decimal']:,}")
            if result['codepoint']:
                print(f"Unicode: {result['unicode_hex']} ({result['codepoint']:,})")
            if result['character']:
                print(f"Caractère: {result['character']}")
        else:
            print(f"Erreur: {result['error']}")
    
    # Exemples de la fonction show()
    print("\n" + "="*70)
    print("EXEMPLES FONCTION show()")
    print("="*70)
    
    show_examples = [
        ("D0", "A0"),
        ("CE", "84"),
        ("D1", "89"),
        ("DA", "aa"),
        ("DF", "80"),
        ("C2", "80"),
        ("E2", "82", "AC"),
        ("F0", "9F", "9F", "A0"),
    ]
    
    for example in show_examples:
        if len(example) == 2:
            show(example[0], example[1])
        elif len(example) == 3:
            show(example[0], example[1], example[2])
        elif len(example) == 4:
            show(example[0], example[1], example[2], example[3])

def main():
    """Fonction principale."""
    print("\n" + "="*70)
    print("CONVERTISSEUR UTF-8 1 à 4 OCTETS")
    print("Python 3.14.0 compatible")
    print("="*70)
    
    # Démontrer la fonction show() comme dans votre exemple
    print("\nDÉMONSTRATION DE show():")
    print("-" * 40)
    
    # Votre exemple exact
    print("C2 80 = (0xC2 * 256) + 0x80 = (194 * 256) + 128 = 49792")
    
    # Nos tests
    show("C2", "80")
    show("E2", "82", "AC")
    show("F0", "9F", "9F", "A0")
    
    # Menu interactif
    interactive_menu()

if __name__ == "__main__":
    main()