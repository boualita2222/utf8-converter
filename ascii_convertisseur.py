#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertisseur ASCII vers UTF-8
De 1 à 4 octets - 6 options de conversion
Python 3.14.2
"""

import sys
import argparse

class ASCIItoUTF8:
    """Convertisseur ASCII vers UTF-8 avec 6 options"""
    
    # Plages UTF-8 selon le nombre d'octets
    UTF8_RANGES = {
        1: {'min': 0x00, 'max': 0x7F, 'mask': 0x00, 'bits': 7},
        2: {'min': 0x80, 'max': 0x7FF, 'mask': 0xC0, 'bits': 5},
        3: {'min': 0x800, 'max': 0xFFFF, 'mask': 0xE0, 'bits': 4},
        4: {'min': 0x10000, 'max': 0x10FFFF, 'mask': 0xF0, 'bits': 3}
    }
    
    def __init__(self):
        self.option = 1
        self.bytes_count = 0
    
    def option1_int_to_bytes(self, value):
        """Option 1: Conversion directe valeur entière -> octets UTF-8"""
        if value < 0x00 or value > 0x10FFFF:
            raise ValueError(f"Valeur {hex(value)} hors plage Unicode")
        
        for nb in range(1, 5):
            ranges = self.UTF8_RANGES[nb]
            if value <= ranges['max']:
                break
        else:
            raise ValueError(f"Valeur {hex(value)} trop grande")
        
        self.bytes_count = nb
        return self._encode_utf8(value, nb)
    
    def option2_hex_to_bytes(self, hex_str):
        """Option 2: Conversion hexadécimale -> octets UTF-8"""
        try:
            value = int(hex_str, 16)
            return self.option1_int_to_bytes(value)
        except ValueError:
            raise ValueError(f"Hexadécimal invalide: {hex_str}")
    
    def option3_binary_to_bytes(self, bin_str):
        """Option 3: Conversion binaire -> octets UTF-8"""
        try:
            value = int(bin_str, 2)
            return self.option1_int_to_bytes(value)
        except ValueError:
            raise ValueError(f"Binaire invalide: {bin_str}")
    
    def option4_char_to_bytes(self, char):
        """Option 4: Conversion caractère ASCII -> octets UTF-8"""
        if len(char) != 1:
            raise ValueError("Doit être un seul caractère")
        value = ord(char)
        return self.option1_int_to_bytes(value)
    
    def option5_string_to_bytes(self, string):
        """Option 5: Conversion chaîne ASCII -> octets UTF-8"""
        if not string:
            raise ValueError("Chaîne vide")
        return string.encode('utf-8')
    
    def option6_decode_bytes(self, byte_data):
        """Option 6: Décodage d'octets UTF-8 -> valeur Unicode"""
        if isinstance(byte_data, str):
            byte_data = bytes.fromhex(byte_data.replace(' ', ''))
        
        try:
            decoded = byte_data.decode('utf-8')
            value = ord(decoded) if len(decoded) == 1 else -1
            return decoded, value
        except UnicodeDecodeError:
            raise ValueError("Octets UTF-8 invalides")
    
    def _encode_utf8(self, value, nb):
        """Encode une valeur Unicode en UTF-8"""
        if nb == 1:
            return bytes([value & 0x7F])
        
        result = bytearray(nb)
        # Premier octet: masque + bits de poids fort
        first_byte = self.UTF8_RANGES[nb]['mask']
        shift = (nb - 1) * 6
        first_byte |= (value >> shift) & ((1 << self.UTF8_RANGES[nb]['bits']) - 1)
        result[0] = first_byte
        
        # Octets de continuation: 10xxxxxx
        for i in range(1, nb):
            shift = (nb - 1 - i) * 6
            result[i] = 0x80 | ((value >> shift) & 0x3F)
        
        return bytes(result)
    
    def format_output(self, byte_data, value=None, char=None):
        """Formatage de sortie complet"""
        result = []
        result.append(f"{'='*60}")
        result.append(f"CONVERSION UTF-8 (Python 3.14.2)")
        result.append(f"{'='*60}")
        
        if char:
            result.append(f"Caractère:     {char}")
        
        if value is not None:
            result.append(f"Code point:    U+{value:04X} ({value})")
        
        result.append(f"Octets UTF-8:   {' '.join(f'{b:02X}' for b in byte_data)}")
        result.append(f"Nombre d'octets: {len(byte_data)}")
        
        # Binaire
        bin_str = ' '.join(f'{b:08b}' for b in byte_data)
        result.append(f"Binaire:       {bin_str}")
        
        # Décodage
        try:
            decoded = byte_data.decode('utf-8')
            result.append(f"Décodé:        {decoded}")
        except UnicodeDecodeError:
            result.append(f"Décodé:        Erreur UTF-8")
        
        result.append(f"{'='*60}")
        return '\n'.join(result)


def interactive_mode():
    """Mode interactif avec menu"""
    converter = ASCIItoUTF8()
    
    while True:
        print("\n" + "="*60)
        print("CONVERTISSEUR ASCII → UTF-8 - 6 OPTIONS")
        print("="*60)
        print("1. Entier décimal → UTF-8")
        print("2. Hexadécimal → UTF-8")
        print("3. Binaire → UTF-8")
        print("4. Caractère ASCII → UTF-8")
        print("5. Chaîne ASCII → UTF-8")
        print("6. Octets UTF-8 → Unicode (décodage)")
        print("7. Mode automatique (détection)")
        print("8. Quitter")
        print("-"*60)
        
        choice = input("Votre choix (1-8): ").strip()
        
        if choice == '8':
            print("Au revoir!")
            break
        
        try:
            if choice == '1':
                value = int(input("Entrez la valeur décimale: ").strip())
                result = converter.option1_int_to_bytes(value)
                print(converter.format_output(result, value))
                
            elif choice == '2':
                hex_str = input("Entrez la valeur hexadécimale (ex: 20AC): ").strip()
                result = converter.option2_hex_to_bytes(hex_str)
                value = int(hex_str, 16)
                print(converter.format_output(result, value))
                
            elif choice == '3':
                bin_str = input("Entrez la valeur binaire (ex: 100000): ").strip()
                result = converter.option3_binary_to_bytes(bin_str)
                value = int(bin_str, 2)
                print(converter.format_output(result, value))
                
            elif choice == '4':
                char = input("Entrez un caractère: ").strip()
                result = converter.option4_char_to_bytes(char)
                print(converter.format_output(result, ord(char), char))
                
            elif choice == '5':
                string = input("Entrez une chaîne: ")
                result = converter.option5_string_to_bytes(string)
                print(converter.format_output(result))
                
            elif choice == '6':
                hex_str = input("Entrez les octets hexadécimaux (ex: E2 82 AC): ").strip()
                decoded, value = converter.option6_decode_bytes(hex_str)
                byte_data = bytes.fromhex(hex_str.replace(' ', ''))
                print(converter.format_output(byte_data, value, decoded))
                
            elif choice == '7':
                user_input = input("Entrez votre valeur (décimal, hex, binaire, char, ou chaîne): ").strip()
                try:
                    # Test si décimal
                    if user_input.isdigit():
                        value = int(user_input)
                        result = converter.option1_int_to_bytes(value)
                        print(converter.format_output(result, value))
                    # Test si hexadécimal
                    elif user_input.startswith('0x') or user_input.startswith('0X'):
                        result = converter.option2_hex_to_bytes(user_input)
                        value = int(user_input, 16)
                        print(converter.format_output(result, value))
                    # Test si binaire
                    elif all(c in '01 ' for c in user_input):
                        clean = user_input.replace(' ', '')
                        result = converter.option3_binary_to_bytes(clean)
                        value = int(clean, 2)
                        print(converter.format_output(result, value))
                    # Test si caractère unique
                    elif len(user_input) == 1:
                        result = converter.option4_char_to_bytes(user_input)
                        print(converter.format_output(result, ord(user_input), user_input))
                    # Sinon chaîne
                    else:
                        result = converter.option5_string_to_bytes(user_input)
                        print(converter.format_output(result))
                except Exception as e:
                    print(f"Erreur: {e}")
                    print("Essayez une autre option")
                    
            else:
                print("Option invalide!")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")


def main():
    """Fonction principale avec arguments en ligne de commande"""
    parser = argparse.ArgumentParser(
        description="Convertisseur ASCII vers UTF-8 (1-4 octets)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--int', type=int, metavar='VALUE',
                       help='Convertir un entier décimal')
    group.add_argument('-x', '--hex', metavar='HEX',
                       help='Convertir une valeur hexadécimale')
    group.add_argument('-b', '--bin', metavar='BIN',
                       help='Convertir une valeur binaire')
    group.add_argument('-c', '--char', metavar='CHAR',
                       help='Convertir un caractère ASCII')
    group.add_argument('-s', '--string', metavar='STRING',
                       help='Convertir une chaîne ASCII')
    group.add_argument('-d', '--decode', metavar='BYTES',
                       help='Décoder des octets UTF-8 (ex: E2 82 AC)')
    
    parser.add_argument('-n', '--no-menu', action='store_true',
                        help='Désactiver le menu interactif (mode ligne uniquement)')
    
    args = parser.parse_args()
    
    converter = ASCIItoUTF8()
    
    try:
        if args.int is not None:
            result = converter.option1_int_to_bytes(args.int)
            print(converter.format_output(result, args.int))
            
        elif args.hex is not None:
            result = converter.option2_hex_to_bytes(args.hex)
            value = int(args.hex, 16)
            print(converter.format_output(result, value))
            
        elif args.bin is not None:
            result = converter.option3_binary_to_bytes(args.bin)
            value = int(args.bin, 2)
            print(converter.format_output(result, value))
            
        elif args.char is not None:
            result = converter.option4_char_to_bytes(args.char)
            print(converter.format_output(result, ord(args.char), args.char))
            
        elif args.string is not None:
            result = converter.option5_string_to_bytes(args.string)
            print(converter.format_output(result))
            
        elif args.decode is not None:
            decoded, value = converter.option6_decode_bytes(args.decode)
            byte_data = bytes.fromhex(args.decode.replace(' ', ''))
            print(converter.format_output(byte_data, value, decoded))
            
        else:
            if not args.no_menu:
                interactive_mode()
            else:
                parser.print_help()
                
    except Exception as e:
        print(f"❌ Erreur: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()