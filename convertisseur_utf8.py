#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONVERTISSEUR UTF-8 COMPLET - 1 à 4 octets
Version: Python 3.14.2 + Colorama
"""

import sys
import unicodedata
from colorama import init, Fore, Style, Back

# Initialisation de Colorama
init(autoreset=True)

class UTF8Converter:
    def __init__(self):
        self.examples = {
            '1': {'name': 'A (ASCII)', 'value': 'A'},
            '2': {'name': '€ (Euro)', 'value': '€'},
            '3': {'name': 'é (e accentué)', 'value': 'é'},
            '4': {'name': '漢 (Chinois)', 'value': '漢'},
            '5': {'name': '😊 (Smiley)', 'value': '😊'},
            '6': {'name': '🐋 (Baleine)', 'value': '🐋'},
            '7': {'name': '𠮷 (Japonais rare)', 'value': '𠮷'},  # 4 octets
        }
    
    def clear_screen(self):
        """Efface l'écran"""
        print("\033c", end="")
    
    def show_banner(self):
        """Affiche la bannière"""
        banner = f"""{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║           CONVERTISSEUR UTF-8 COMPLET (1-4 octets)           ║
║                   Python 3.14.2 + Colorama                   ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
    
    def analyze_char(self, char):
        """Analyse un caractère UTF-8"""
        try:
            # Obtenir les informations de base
            utf8_bytes = char.encode('utf-8')
            hex_bytes = [f"{b:02X}" for b in utf8_bytes]
            binary_bytes = [f"{b:08b}" for b in utf8_bytes]
            num_bytes = len(utf8_bytes)
            
            # Calcul décimal brut (valeur entière des octets)
            decimal_raw = int.from_bytes(utf8_bytes, byteorder='big')
            
            # Obtenir le code point
            codepoint = ord(char)
            codepoint_hex = f"U+{codepoint:04X}"
            
            # Obtenir le nom Unicode
            try:
                char_name = unicodedata.name(char)
            except:
                char_name = "Nom inconnu"
            
            # Vérifier la validité UTF-8
            is_valid = len(char.encode('utf-8', errors='strict')) == num_bytes
            
            # Afficher les résultats
            print(f"\n{Fore.GREEN}{Style.BRIGHT}RÉSULTAT{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Caractère    :{Style.RESET_ALL} {char}")
            print(f"{Fore.CYAN}Octets       :{Style.RESET_ALL} {num_bytes}")
            print(f"{Fore.CYAN}Hexadécimal  :{Style.RESET_ALL} {' '.join(hex_bytes)}")
            print(f"{Fore.CYAN}Binaire      :{Style.RESET_ALL} {' '.join(binary_bytes)}")
            print(f"{Fore.CYAN}Décimal brut :{Style.RESET_ALL} {decimal_raw:,} (0x{decimal_raw:X})")
            print(f"{Fore.CYAN}Code point   :{Style.RESET_ALL} {codepoint_hex}")
            print(f"{Fore.CYAN}Décimal      :{Style.RESET_ALL} {codepoint}")
            print(f"{Fore.CYAN}Nom          :{Style.RESET_ALL} {char_name}")
            
            if is_valid:
                print(f"{Fore.CYAN}UTF-8 valide :{Style.RESET_ALL} {Fore.GREEN}✅ OUI{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}UTF-8 valide :{Style.RESET_ALL} {Fore.RED}❌ NON{Style.RESET_ALL}")
            
            # Afficher le calcul détaillé pour les caractères multi-octets
            if num_bytes >= 2:
                print(f"\n{Fore.YELLOW}CALCUL DÉTAILLÉ:{Style.RESET_ALL}")
                if num_bytes == 2:
                    b1, b2 = utf8_bytes
                    calc = f"({b1} × 256) + {b2} = {b1 * 256 + b2}"
                    hex_calc = f"0x{b1:02X} 0x{b2:02X} = (0x{b1:02X} * 0x100) + 0x{b2:02X} = 0x{b1:02X}{b2:02X}"
                elif num_bytes == 3:
                    b1, b2, b3 = utf8_bytes
                    calc = f"({b1} × 65536) + ({b2} × 256) + {b3} = {b1 * 65536 + b2 * 256 + b3}"
                    hex_calc = f"0x{b1:02X} 0x{b2:02X} 0x{b3:02X} = (0x{b1:02X} * 0x10000) + (0x{b2:02X} * 0x100) + 0x{b3:02X} = 0x{b1:02X}{b2:02X}{b3:02X}"
                elif num_bytes == 4:
                    b1, b2, b3, b4 = utf8_bytes
                    calc = f"({b1} × 16777216) + ({b2} × 65536) + ({b3} × 256) + {b4} = {b1 * 16777216 + b2 * 65536 + b3 * 256 + b4}"
                    hex_calc = f"0x{b1:02X} 0x{b2:02X} 0x{b3:02X} 0x{b4:02X} = (0x{b1:02X} * 0x1000000) + (0x{b2:02X} * 0x10000) + (0x{b3:02X} * 0x100) + 0x{b4:02X} = 0x{b1:02X}{b2:02X}{b3:02X}{b4:02X}"
                
                print(f"  {calc}")
                print(f"  {hex_calc}")
            
            print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}Erreur lors de l'analyse : {e}{Style.RESET_ALL}")
    
    def hex_to_analysis(self):
        """Option 1: Hexadécimal → Analyse"""
        print(f"\n{Fore.CYAN}〔 Option 1 : Hexadécimal → Analyse 〕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Exemples : C2 80, F0 9F 9A 81, E2 82 AC{Style.RESET_ALL}")
        
        hex_input = input(f"{Fore.GREEN}Entrez les octets hexadécimaux :{Style.RESET_ALL} ").strip()
        
        try:
            # Nettoyer l'entrée
            hex_chars = hex_input.replace('0x', '').replace(',', ' ').split()
            bytes_data = bytes(int(h, 16) for h in hex_chars)
            
            # Décoder en UTF-8
            char = bytes_data.decode('utf-8')
            
            # Analyser
            self.analyze_char(char)
            
        except ValueError:
            print(f"{Fore.RED}Format hexadécimal invalide !{Style.RESET_ALL}")
        except UnicodeDecodeError:
            print(f"{Fore.RED}Séquence UTF-8 invalide !{Style.RESET_ALL}")
    
    def decimal_to_analysis(self):
        """Option 2: Décimal → Analyse"""
        print(f"\n{Fore.CYAN}〔 Option 2 : Décimal → Analyse 〕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Exemples : 49792, 4036991617, 14844588{Style.RESET_ALL}")
        
        dec_input = input(f"{Fore.GREEN}Entrez la valeur décimale :{Style.RESET_ALL} ").strip()
        
        try:
            decimal_value = int(dec_input)
            
            # Déterminer le nombre d'octets nécessaires
            if decimal_value <= 0xFF:
                num_bytes = 1
            elif decimal_value <= 0xFFFF:
                num_bytes = 2
            elif decimal_value <= 0xFFFFFF:
                num_bytes = 3
            else:
                num_bytes = 4
            
            # Convertir en bytes
            bytes_data = decimal_value.to_bytes(num_bytes, byteorder='big')
            
            # Décoder en UTF-8
            try:
                char = bytes_data.decode('utf-8')
                self.analyze_char(char)
            except UnicodeDecodeError:
                # Essayer différents nombres d'octets
                for n in [1, 2, 3, 4]:
                    try:
                        bytes_data = decimal_value.to_bytes(n, byteorder='big')
                        char = bytes_data.decode('utf-8')
                        self.analyze_char(char)
                        break
                    except:
                        continue
                else:
                    print(f"{Fore.RED}Impossible de décoder comme UTF-8 valide !{Style.RESET_ALL}")
                    
        except ValueError:
            print(f"{Fore.RED}Valeur décimale invalide !{Style.RESET_ALL}")
    
    def char_to_analysis(self):
        """Option 3: Caractère → Analyse"""
        print(f"\n{Fore.CYAN}〔 Option 3 : Caractère → Analyse 〕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Exemples : A, €, 😊, 🐋{Style.RESET_ALL}")
        
        char_input = input(f"{Fore.GREEN}Entrez un caractère :{Style.RESET_ALL} ").strip()
        
        if char_input:
            self.analyze_char(char_input[0])
        else:
            print(f"{Fore.RED}Aucun caractère entré !{Style.RESET_ALL}")
    
    def show_example(self):
        """Option 4: Fonction show() personnalisée"""
        print(f"\n{Fore.CYAN}〔 Option 4 : Exemple 🐋 〕{Style.RESET_ALL}")
        
        # Caractère baleine
        whale = "🐋"
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}RÉSULTAT (Char: '{whale}'){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
        
        # Encoder en UTF-8
        utf8_bytes = whale.encode('utf-8')
        hex_bytes = [f"{b:02X}" for b in utf8_bytes]
        binary_bytes = [f"{b:08b}" for b in utf8_bytes]
        
        print(f"{Fore.CYAN}Hexadécimal  :{Style.RESET_ALL} {' '.join(hex_bytes)}")
        print(f"{Fore.CYAN}Octets       :{Style.RESET_ALL} {len(utf8_bytes)}")
        print(f"{Fore.CYAN}Binaire      :{Style.RESET_ALL} {' '.join(binary_bytes)}")
        
        # Décimal brut
        decimal_raw = int.from_bytes(utf8_bytes, byteorder='big')
        print(f"{Fore.CYAN}Décimal brut :{Style.RESET_ALL} {decimal_raw:,} (0x{decimal_raw:X})")
        
        # Caractère et code point
        codepoint = ord(whale)
        print(f"{Fore.CYAN}Caractère    :{Style.RESET_ALL} {whale}")
        print(f"{Fore.CYAN}Code point   :{Style.RESET_ALL} U+{codepoint:04X}")
        print(f"{Fore.CYAN}Décimal      :{Style.RESET_ALL} {codepoint}")
        
        # Nom
        try:
            char_name = unicodedata.name(whale)
            print(f"{Fore.CYAN}Nom          :{Style.RESET_ALL} {char_name}")
        except:
            print(f"{Fore.CYAN}Nom          :{Style.RESET_ALL} WHALE")
        
        print(f"{Fore.CYAN}UTF-8 valide :{Style.RESET_ALL} {Fore.GREEN}✅ OUI{Style.RESET_ALL}")
        
        # Calcul détaillé
        b1, b2, b3, b4 = utf8_bytes
        print(f"\n{Fore.YELLOW}CALCUL DÉTAILLÉ:{Style.RESET_ALL}")
        print(f"  ({b1} × 16777216) + ({b2} × 65536) + ({b3} × 256) + {b4} = {b1 * 16777216 + b2 * 65536 + b3 * 256 + b4}")
        print(f"  0x{b1:02X} 0x{b2:02X} 0x{b3:02X} 0x{b4:02X} = (0x{b1:02X} * 0x1000000) + (0x{b2:02X} * 0x10000) + (0x{b3:02X} * 0x100) + 0x{b4:02X} = 0x{b1:02X}{b2:02X}{b3:02X}{b4:02X}")
        print(f"  Séquence UTF-8 valide : {Fore.GREEN}OUI{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    
    def predefined_examples(self):
        """Option 5: Exemples prédéfinis"""
        print(f"\n{Fore.CYAN}〔 Option 5 : Exemples prédéfinis 〕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Choisissez un exemple :{Style.RESET_ALL}\n")
        
        for key, example in self.examples.items():
            char = example['value']
            utf8_bytes = char.encode('utf-8')
            hex_str = ' '.join([f"{b:02X}" for b in utf8_bytes])
            
            print(f"  {Fore.GREEN}[{key}]{Style.RESET_ALL} {example['name']}")
            print(f"      Caractère: {char} | Octets: {len(utf8_bytes)} | Hex: {hex_str}")
            print()
        
        choice = input(f"{Fore.GREEN}Votre choix (1-7) :{Style.RESET_ALL} ").strip()
        
        if choice in self.examples:
            char = self.examples[choice]['value']
            print(f"\n{Fore.YELLOW}Analyse de : {self.examples[choice]['name']}{Style.RESET_ALL}")
            self.analyze_char(char)
        else:
            print(f"{Fore.RED}Choix invalide !{Style.RESET_ALL}")
    
    def show_menu(self):
        """Affiche le menu principal"""
        menu = f"""
{Fore.CYAN}{Style.BRIGHT}OPTIONS :{Style.RESET_ALL}
  {Fore.GREEN}[1]{Style.RESET_ALL} Hexadécimal → Analyse (ex: C2 80, F0 9F 9A 81)
  {Fore.GREEN}[2]{Style.RESET_ALL} Décimal → Analyse (ex: 49792, 4036991617)
  {Fore.GREEN}[3]{Style.RESET_ALL} Caractère → Analyse (ex: A, €, 😊)
  {Fore.GREEN}[4]{Style.RESET_ALL} Fonction show() personnalisée (exemple 🐋)
  {Fore.GREEN}[5]{Style.RESET_ALL} Exemples prédéfinis
  {Fore.GREEN}[6]{Style.RESET_ALL} Quitter
  
{Fore.YELLOW}{'='*60}{Style.RESET_ALL}"""
        print(menu)
    
    def run(self):
        """Lance le programme principal"""
        self.clear_screen()
        
        while True:
            self.show_banner()
            self.show_menu()
            
            choice = input(f"\n{Fore.GREEN}Votre choix (1-6) :{Style.RESET_ALL} ").strip()
            
            if choice == '1':
                self.hex_to_analysis()
            elif choice == '2':
                self.decimal_to_analysis()
            elif choice == '3':
                self.char_to_analysis()
            elif choice == '4':
                self.show_example()
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
        converter = UTF8Converter()
        converter.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Programme interrompu. Au revoir !{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Erreur : {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    # Vérifier les dépendances
    try:
        import colorama
    except ImportError:
        print("Erreur : Le module 'colorama' n'est pas installé.")
        print("Installez-le avec : pip install colorama")
        sys.exit(1)
    
    try:
        import unicodedata
    except ImportError:
        print("Erreur : Le module 'unicodedata' n'est pas disponible.")
        sys.exit(1)
    
    main()