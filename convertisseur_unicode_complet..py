#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONVERTISSEUR UNICODE COMPLET
UTF-8, UTF-16BE, UTF-16LE, UTF-32BE, UTF-32LE
Version: Python 3.14.2 + Colorama
"""

import sys
import struct
from colorama import init, Fore, Style, Back

# Initialisation de Colorama
init(autoreset=True)

class UnicodeConverter:
    def __init__(self):
        self.version = "2.0"
        
    def clear_screen(self):
        """Efface l'écran"""
        print("\033c", end="")
    
    def show_banner(self):
        """Affiche la bannière"""
        banner = f"""{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CONVERTISSEUR UNICODE COMPLET                              ║
║           UTF-8 / UTF-16BE / UTF-16LE / UTF-32BE / UTF-32LE                  ║
║                         Python 3.14.2 + Colorama                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
    
    def format_bytes(self, bytes_data):
        """Formate les bytes en chaîne lisible"""
        return ' '.join(f"{b:02X}" for b in bytes_data)
    
    def format_binary(self, bytes_data):
        """Formate les bytes en binaire"""
        return ' '.join(f"{b:08b}" for b in bytes_data)
    
    def format_decimal(self, bytes_data):
        """Formate les bytes en décimal"""
        return ' '.join(str(b) for b in bytes_data)
    
    def analyze_character(self, char):
        """Analyse complète d'un caractère Unicode"""
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Analyse du caractère : {Fore.CYAN}{char}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
        
        # Code point
        codepoint = ord(char)
        print(f"\n{Fore.CYAN}Code point :{Style.RESET_ALL} U+{codepoint:04X} ({codepoint})")
        
        # UTF-8
        utf8_bytes = char.encode('utf-8')
        print(f"\n{Fore.YELLOW}├─ UTF-8{Style.RESET_ALL}")
        print(f"│   Hex      : {self.format_bytes(utf8_bytes)}")
        print(f"│   Octets   : {len(utf8_bytes)}")
        print(f"│   Décimal  : {self.format_decimal(utf8_bytes)}")
        print(f"│   Binaire  : {self.format_binary(utf8_bytes)}")
        print(f"│   Brut     : {int.from_bytes(utf8_bytes, 'big'):,} (0x{int.from_bytes(utf8_bytes, 'big'):X})")
        
        # UTF-16BE (Big Endian)
        utf16be_bytes = char.encode('utf-16be')
        print(f"\n{Fore.YELLOW}├─ UTF-16BE{Style.RESET_ALL}")
        print(f"│   Hex      : {self.format_bytes(utf16be_bytes)}")
        print(f"│   Octets   : {len(utf16be_bytes)}")
        print(f"│   Décimal  : {self.format_decimal(utf16be_bytes)}")
        print(f"│   Binaire  : {self.format_binary(utf16be_bytes)}")
        print(f"│   Brut     : {int.from_bytes(utf16be_bytes, 'big'):,} (0x{int.from_bytes(utf16be_bytes, 'big'):X})")
        
        # UTF-16LE (Little Endian)
        utf16le_bytes = char.encode('utf-16le')
        print(f"\n{Fore.YELLOW}├─ UTF-16LE{Style.RESET_ALL}")
        print(f"│   Hex      : {self.format_bytes(utf16le_bytes)}")
        print(f"│   Octets   : {len(utf16le_bytes)}")
        print(f"│   Décimal  : {self.format_decimal(utf16le_bytes)}")
        print(f"│   Binaire  : {self.format_binary(utf16le_bytes)}")
        print(f"│   Brut     : {int.from_bytes(utf16le_bytes, 'little'):,} (0x{int.from_bytes(utf16le_bytes, 'little'):X})")
        
        # UTF-32BE (Big Endian)
        utf32be_bytes = char.encode('utf-32be')
        print(f"\n{Fore.YELLOW}├─ UTF-32BE{Style.RESET_ALL}")
        print(f"│   Hex      : {self.format_bytes(utf32be_bytes)}")
        print(f"│   Octets   : {len(utf32be_bytes)}")
        print(f"│   Décimal  : {self.format_decimal(utf32be_bytes)}")
        print(f"│   Binaire  : {self.format_binary(utf32be_bytes)}")
        print(f"│   Brut     : {int.from_bytes(utf32be_bytes, 'big'):,} (0x{int.from_bytes(utf32be_bytes, 'big'):X})")
        
        # UTF-32LE (Little Endian)
        utf32le_bytes = char.encode('utf-32le')
        print(f"\n{Fore.YELLOW}└─ UTF-32LE{Style.RESET_ALL}")
        print(f"│   Hex      : {self.format_bytes(utf32le_bytes)}")
        print(f"│   Octets   : {len(utf32le_bytes)}")
        print(f"│   Décimal  : {self.format_decimal(utf32le_bytes)}")
        print(f"│   Binaire  : {self.format_binary(utf32le_bytes)}")
        print(f"│   Brut     : {int.from_bytes(utf32le_bytes, 'little'):,} (0x{int.from_bytes(utf32le_bytes, 'little'):X})")
        
        print(f"\n{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
    
    def hex_to_char(self, hex_str, encoding):
        """Convertit une chaîne hexadécimale en caractère selon l'encodage"""
        try:
            # Nettoyer l'entrée
            hex_bytes = hex_str.replace('0x', '').replace(',', ' ').split()
            bytes_data = bytes(int(b, 16) for b in hex_bytes)
            
            # Décoder selon l'encodage
            if encoding == 'UTF-8':
                char = bytes_data.decode('utf-8')
            elif encoding == 'UTF-16BE':
                char = bytes_data.decode('utf-16be')
            elif encoding == 'UTF-16LE':
                char = bytes_data.decode('utf-16le')
            elif encoding == 'UTF-32BE':
                char = bytes_data.decode('utf-32be')
            elif encoding == 'UTF-32LE':
                char = bytes_data.decode('utf-32le')
            else:
                return None
            
            return char
        except Exception as e:
            return None
    
    def decimal_to_char(self, decimal_str, encoding):
        """Convertit une chaîne décimale en caractère selon l'encodage"""
        try:
            decimals = [int(d) for d in decimal_str.split()]
            bytes_data = bytes(decimals)
            
            # Décoder selon l'encodage
            if encoding == 'UTF-8':
                char = bytes_data.decode('utf-8')
            elif encoding == 'UTF-16BE':
                char = bytes_data.decode('utf-16be')
            elif encoding == 'UTF-16LE':
                char = bytes_data.decode('utf-16le')
            elif encoding == 'UTF-32BE':
                char = bytes_data.decode('utf-32be')
            elif encoding == 'UTF-32LE':
                char = bytes_data.decode('utf-32le')
            else:
                return None
            
            return char
        except Exception as e:
            return None
    
    def show_menu(self):
        """Affiche le menu principal"""
        menu = f"""
{Fore.CYAN}{Style.BRIGHT}OPTIONS :{Style.RESET_ALL}
  {Fore.GREEN}[1]{Style.RESET_ALL} Caractère → Analyse complète (tous les encodages)
  {Fore.GREEN}[2]{Style.RESET_ALL} Hexadécimal → Caractère
  {Fore.GREEN}[3]{Style.RESET_ALL} Décimal → Caractère
  {Fore.GREEN}[4]{Style.RESET_ALL} Exemple détaillé (🐫 - Chameau)
  {Fore.GREEN}[5]{Style.RESET_ALL} Exemples prédéfinis
  {Fore.GREEN}[6]{Style.RESET_ALL} Quitter
  
{Fore.YELLOW}{'='*80}{Style.RESET_ALL}"""
        print(menu)
    
    def show_detailed_example(self):
        """Option 4 : Affiche l'exemple détaillé du chameau 🐫"""
        char = "🐫"
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}EXEMPLE DÉTAILLÉ : Caractère '{char}' (CHAMEAU){Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
        
        # Code point
        codepoint = ord(char)
        print(f"\n{Fore.CYAN}Code point :{Style.RESET_ALL} U+{codepoint:04X} ({codepoint})")
        
        # Tableau comparatif
        print(f"\n{Fore.YELLOW}{'═'*100}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'Encodage':<12} {'Hex':<25} {'Décimal (bytes)':<30} {'Décimal brut':<15} {'Binaire'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'═'*100}{Style.RESET_ALL}")
        
        # UTF-8
        utf8 = char.encode('utf-8')
        print(f"{Fore.GREEN}{'UTF-8':<12} {self.format_bytes(utf8):<25} {self.format_decimal(utf8):<30} {int.from_bytes(utf8, 'big'):<15,} {self.format_binary(utf8)}{Style.RESET_ALL}")
        
        # UTF-16BE
        utf16be = char.encode('utf-16be')
        print(f"{Fore.CYAN}{'UTF-16BE':<12} {self.format_bytes(utf16be):<25} {self.format_decimal(utf16be):<30} {int.from_bytes(utf16be, 'big'):<15,} {self.format_binary(utf16be)}{Style.RESET_ALL}")
        
        # UTF-16LE
        utf16le = char.encode('utf-16le')
        print(f"{Fore.MAGENTA}{'UTF-16LE':<12} {self.format_bytes(utf16le):<25} {self.format_decimal(utf16le):<30} {int.from_bytes(utf16le, 'little'):<15,} {self.format_binary(utf16le)}{Style.RESET_ALL}")
        
        # UTF-32BE
        utf32be = char.encode('utf-32be')
        print(f"{Fore.YELLOW}{'UTF-32BE':<12} {self.format_bytes(utf32be):<25} {self.format_decimal(utf32be):<30} {int.from_bytes(utf32be, 'big'):<15,} {self.format_binary(utf32be)}{Style.RESET_ALL}")
        
        # UTF-32LE
        utf32le = char.encode('utf-32le')
        print(f"{Fore.BLUE}{'UTF-32LE':<12} {self.format_bytes(utf32le):<25} {self.format_decimal(utf32le):<30} {int.from_bytes(utf32le, 'little'):<15,} {self.format_binary(utf32le)}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}{'═'*100}{Style.RESET_ALL}")
        
        # Explication des calculs
        print(f"\n{Fore.GREEN}EXPLICATION DES CALCULS :{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}UTF-8 :{Style.RESET_ALL}")
        b1, b2, b3, b4 = utf8
        print(f"  ({b1} × 16777216) + ({b2} × 65536) + ({b3} × 256) + {b4} = {int.from_bytes(utf8, 'big')}")
        
        print(f"\n{Fore.CYAN}UTF-16BE :{Style.RESET_ALL}")
        b1, b2, b3, b4 = utf16be
        print(f"  ({b1} × 16777216) + ({b2} × 65536) + ({b3} × 256) + {b4} = {int.from_bytes(utf16be, 'big')}")
        
        print(f"\n{Fore.CYAN}UTF-16LE :{Style.RESET_ALL}")
        b1, b2, b3, b4 = utf16le
        print(f"  ({b1} × 1) + ({b2} × 256) + ({b3} × 65536) + ({b4} × 16777216) = {int.from_bytes(utf16le, 'little')}")
        
        print(f"\n{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
    
    def predefined_examples(self):
        """Option 5 : Exemples prédéfinis"""
        print(f"\n{Fore.GREEN}〔 Option 5 : Exemples Prédéfinis 〕{Style.RESET_ALL}")
        
        examples = [
            {"name": "🐫 Chameau", "char": "🐫"},
            {"name": "🐋 Baleine", "char": "🐋"},
            {"name": "€ Euro", "char": "€"},
            {"name": "É É majuscule accent", "char": "É"},
            {"name": "漢 Caractère chinois", "char": "漢"},
            {"name": "😊 Smiley", "char": "😊"},
            {"name": "𠮷 Caractère rare (4 octets)", "char": "𠮷"},
        ]
        
        print(f"{Fore.YELLOW}Choisissez un exemple :{Style.RESET_ALL}\n")
        
        for i, example in enumerate(examples, 1):
            print(f"  {Fore.GREEN}[{i}]{Style.RESET_ALL} {example['name']} → '{example['char']}'")
        
        choice = input(f"\n{Fore.CYAN}Votre choix (1-{len(examples)}) : {Style.RESET_ALL}").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                self.analyze_character(examples[idx]['char'])
            else:
                print(f"{Fore.RED}Choix invalide !{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Entrée invalide !{Style.RESET_ALL}")
    
    def run(self):
        """Lance le programme principal"""
        self.clear_screen()
        
        while True:
            self.show_banner()
            self.show_menu()
            
            choice = input(f"\n{Fore.GREEN}Votre choix (1-6) : {Style.RESET_ALL}").strip()
            
            if choice == '1':
                print(f"\n{Fore.GREEN}〔 Option 1 : Caractère → Analyse complète 〕{Style.RESET_ALL}")
                char_input = input(f"{Fore.CYAN}Entrez un caractère : {Style.RESET_ALL}").strip()
                if char_input:
                    self.analyze_character(char_input[0])
                else:
                    print(f"{Fore.RED}Aucun caractère entré !{Style.RESET_ALL}")
                    
            elif choice == '2':
                print(f"\n{Fore.GREEN}〔 Option 2 : Hexadécimal → Caractère 〕{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Exemples :{Style.RESET_ALL}")
                print("  UTF-8    : F0 9F 90 AC")
                print("  UTF-16BE : D8 3D DC 2C")
                print("  UTF-16LE : 3D D8 2C DC")
                print("  UTF-32BE : 00 01 F4 2C")
                print("  UTF-32LE : 2C F4 01 00")
                
                hex_input = input(f"\n{Fore.CYAN}Entrez les octets hexadécimaux : {Style.RESET_ALL}").strip()
                encoding = input(f"{Fore.CYAN}Encodage (UTF-8/UTF-16BE/UTF-16LE/UTF-32BE/UTF-32LE) : {Style.RESET_ALL}").strip().upper()
                
                char = self.hex_to_char(hex_input, encoding)
                if char:
                    self.analyze_character(char)
                else:
                    print(f"{Fore.RED}Erreur de conversion ! Vérifiez l'encodage et le format.{Style.RESET_ALL}")
                    
            elif choice == '3':
                print(f"\n{Fore.GREEN}〔 Option 3 : Décimal → Caractère 〕{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Exemples :{Style.RESET_ALL}")
                print("  UTF-8    : 240 159 144 172")
                print("  UTF-16BE : 216 61 220 44")
                print("  UTF-16LE : 61 216 44 220")
                print("  UTF-32BE : 0 1 244 44")
                print("  UTF-32LE : 44 244 1 0")
                
                dec_input = input(f"\n{Fore.CYAN}Entrez les valeurs décimales : {Style.RESET_ALL}").strip()
                encoding = input(f"{Fore.CYAN}Encodage (UTF-8/UTF-16BE/UTF-16LE/UTF-32BE/UTF-32LE) : {Style.RESET_ALL}").strip().upper()
                
                char = self.decimal_to_char(dec_input, encoding)
                if char:
                    self.analyze_character(char)
                else:
                    print(f"{Fore.RED}Erreur de conversion ! Vérifiez l'encodage et le format.{Style.RESET_ALL}")
                    
            elif choice == '4':
                self.show_detailed_example()
                
            elif choice == '5':
                self.predefined_examples()
                
            elif choice == '6':
                print(f"\n{Fore.YELLOW}Au revoir ! 👋{Style.RESET_ALL}")
                sys.exit(0)
                
            else:
                print(f"{Fore.RED}Choix invalide ! Veuillez choisir 1-6.{Style.RESET_ALL}")
            
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
            self.clear_screen()

def main():
    """Fonction principale"""
    try:
        converter = UnicodeConverter()
        converter.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Programme interrompu. Au revoir !{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Erreur : {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()