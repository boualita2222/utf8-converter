#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONVERTISSEUR ASCII COMPLET
Version: Python 3.14.2 + Colorama
"""

import sys
from colorama import init, Fore, Style, Back

# Initialisation de Colorama
init(autoreset=True)

class ASCIIConverter:
    def __init__(self):
        self.version = "1.0"
        self.author = "ASCII Converter Pro"
        
    def clear_screen(self):
        """Efface l'écran"""
        print("\033c", end="")
    
    def show_banner(self):
        """Affiche la bannière"""
        banner = f"""{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                  CONVERTISSEUR ASCII COMPLET                  ║
║                    Python 3.14.2 + Colorama                   ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
    
    def text_to_ascii(self):
        """Option 1 : Texte → codes ASCII"""
        print(f"\n{Fore.GREEN}〔 Option 1 : Texte → Codes ASCII 〕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Entrez du texte à convertir en codes ASCII :{Style.RESET_ALL}")
        
        text = input(f"{Fore.CYAN}Texte : {Style.RESET_ALL}").strip()
        
        if not text:
            print(f"{Fore.GREEN}Aucun texte entré !{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}RÉSULTATS DE CONVERSION :{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Texte original :{Style.RESET_ALL} {text}")
        print(f"{Fore.CYAN}Longueur :{Style.RESET_ALL} {len(text)} caractères")
        
        # Tableau de conversion
        print(f"\n{Fore.YELLOW}{'═'*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'Car.':<5} {'ASCII':<10} {'Hexa':<8} {'Binaire':<15} {'Unicode':<10}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'═'*70}{Style.RESET_ALL}")
        
        for i, char in enumerate(text):
            ascii_val = ord(char)
            hex_val = f"0x{ascii_val:02X}"
            binary_val = f"{ascii_val:08b}"
            unicode_val = f"U+{ascii_val:04X}"
            
            # Couleur selon la plage ASCII
            if ascii_val < 32:
                color = Fore.GREEN  # Caractères de contrôle
            elif ascii_val < 127:
                color = Fore.GREEN  # ASCII standard
            else:
                color = Fore.YELLOW  # ASCII étendu
            
            # Afficher le caractère ou [CTRL] pour les non-imprimables
            display_char = char if ascii_val >= 32 else f"[CTRL-{ascii_val:02X}]"
            
            print(f"{color}{display_char:<5} {ascii_val:<10} {hex_val:<8} {binary_val:<15} {unicode_val:<10}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}{'═'*70}{Style.RESET_ALL}")
        
        # Résumé
        print(f"\n{Fore.GREEN}FORMATS DE SORTIE :{Style.RESET_ALL}")
        
        # 1. Liste des codes ASCII
        ascii_codes = [str(ord(c)) for c in text]
        print(f"{Fore.CYAN}Codes ASCII (décimaux) :{Style.RESET_ALL} {' '.join(ascii_codes)}")
        
        # 2. Hexadécimal
        hex_codes = [f"0x{ord(c):02X}" for c in text]
        print(f"{Fore.CYAN}Codes ASCII (hexadécimaux) :{Style.RESET_ALL} {' '.join(hex_codes)}")
        
        # 3. Binaire
        binary_codes = [f"{ord(c):08b}" for c in text]
        print(f"{Fore.CYAN}Codes ASCII (binaires) :{Style.RESET_ALL}")
        print(f"  {' '.join(binary_codes)}")
        
        # 4. Valeurs séparées par virgules
        print(f"{Fore.CYAN}Format CSV :{Style.RESET_ALL}")
        print(f"  {', '.join(ascii_codes)}")
        
        # Statistiques
        print(f"\n{Fore.GREEN}STATISTIQUES :{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Plages ASCII :{Style.RESET_ALL}")
        
        control = sum(1 for c in text if ord(c) < 32)
        standard = sum(1 for c in text if 32 <= ord(c) < 127)
        extended = sum(1 for c in text if ord(c) >= 127)
        
        print(f"  Contrôle (0-31) : {control} caractères")
        print(f"  Standard (32-126) : {standard} caractères")
        print(f"  Étendu (127+) : {extended} caractères")
    
    def ascii_to_text(self):
        """Option 2 : Codes ASCII → texte"""
        print(f"\n{Fore.GREEN}〔 Option 2 : Codes ASCII → Texte 〕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Exemples : 72 101 108 108 111  ou  0x48 0x65 0x6C 0x6C 0x6F{Style.RESET_ALL}")
        
        ascii_input = input(f"{Fore.CYAN}Entrez les codes ASCII (séparés par des espaces) : {Style.RESET_ALL}").strip()
        
        if not ascii_input:
            print(f"{Fore.GREEN}Aucun code ASCII entré !{Style.RESET_ALL}")
            return
        
        # Traitement des codes
        codes = ascii_input.split()
        text_chars = []
        valid_codes = []
        invalid_codes = []
        
        print(f"\n{Fore.YELLOW}Traitement des codes...{Style.RESET_ALL}")
        
        for code in codes:
            try:
                # Essayer différents formats
                if code.startswith('0x') or code.startswith('0X'):
                    # Format hexadécimal
                    ascii_val = int(code, 16)
                elif code.startswith('b'):
                    # Format binaire
                    ascii_val = int(code[1:], 2)
                else:
                    # Format décimal par défaut
                    ascii_val = int(code)
                
                # Vérifier si c'est un code ASCII valide
                if 0 <= ascii_val <= 255:
                    char = chr(ascii_val)
                    text_chars.append(char)
                    valid_codes.append((code, ascii_val, char))
                else:
                    invalid_codes.append((code, "Hors plage ASCII (0-255)"))
                    
            except ValueError:
                invalid_codes.append((code, "Format invalide"))
        
        # Afficher les résultats
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}RÉSULTATS :{Style.RESET_ALL}")
        
        if text_chars:
            text_result = ''.join(text_chars)
            print(f"\n{Fore.CYAN}Texte reconstitué :{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}'{text_result}'{Style.RESET_ALL}")
            
            # Détails des conversions
            print(f"\n{Fore.CYAN}Détails des conversions :{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'═'*50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'Code entré':<12} {'Décimal':<8} {'Caractère':<10} {'Hex':<6} {'Binaire'}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'═'*50}{Style.RESET_ALL}")
            
            for code, ascii_val, char in valid_codes:
                hex_val = f"0x{ascii_val:02X}"
                binary_val = f"{ascii_val:08b}"
                display_char = char if ascii_val >= 32 else f"[CTRL-{ascii_val:02X}]"
                
                color = Fore.GREEN if ascii_val >= 32 else Fore.YELLOW
                print(f"{color}{code:<12} {ascii_val:<8} {display_char:<10} {hex_val:<6} {binary_val}{Style.RESET_ALL}")
            
            print(f"{Fore.YELLOW}{'═'*50}{Style.RESET_ALL}")
        
        # Afficher les erreurs
        if invalid_codes:
            print(f"\n{Fore.GREEN}CODES INVALIDES :{Style.RESET_ALL}")
            for code, error in invalid_codes:
                print(f"  {code} → {error}")
        
        # Statistiques
        print(f"\n{Fore.GREEN}STATISTIQUES :{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Codes valides : {len(valid_codes)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Codes invalides : {len(invalid_codes)}{Style.RESET_ALL}")
        
        if text_chars:
            print(f"{Fore.CYAN}Longueur du texte : {len(text_chars)} caractères{Style.RESET_ALL}")
    
    def show_menu(self):
        """Affiche le menu principal"""
        menu = f"""
{Fore.CYAN}{Style.BRIGHT}OPTIONS :{Style.RESET_ALL}
  {Fore.GREEN}[1]{Style.RESET_ALL} Texte → Codes ASCII (conversion complète)
  {Fore.GREEN}[2]{Style.RESET_ALL} Codes ASCII → Texte (décodage)
  {Fore.GREEN}[3]{Style.RESET_ALL} Table ASCII complète
  {Fore.GREEN}[4]{Style.RESET_ALL} Exemples prédéfinis
  {Fore.GREEN}[5]{Style.RESET_ALL} Quitter
  
{Fore.YELLOW}{'='*60}{Style.RESET_ALL}"""
        print(menu)
    
    def show_ascii_table(self):
        """Option 3 : Affiche la table ASCII complète"""
        print(f"\n{Fore.GREEN}〔 Option 3 : Table ASCII Complète 〕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Table des codes ASCII (0-255) :{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'═'*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}TABLE ASCII STANDARD (0-127) :{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═'*80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'Déc.':<6} {'Hex':<6} {'Binaire':<10} {'Car.':<6} {'Nom':<30}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
        
        for i in range(128):
            hex_val = f"0x{i:02X}"
            binary_val = f"{i:08b}"
            
            if i < 32:
                # Caractères de contrôle
                char_name = self.get_control_char_name(i)
                display = f"[CTRL]"
                color = Fore.RED
            elif i == 127:
                char_name = "DELETE"
                display = "[DEL]"
                color = Fore.MAGENTA
            else:
                char_name = chr(i)
                display = chr(i)
                color = Fore.GREEN
            
            print(f"{color}{i:<6} {hex_val:<6} {binary_val:<10} {display:<6} {char_name:<30}{Style.RESET_ALL}")
            
            # Nouvelle ligne après 32 caractères
            if (i + 1) % 32 == 0 and i < 127:
                input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'═'*80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'═'*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}TABLE ASCII ÉTENDUE (128-255) :{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═'*80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'Déc.':<6} {'Hex':<6} {'Binaire':<10} {'Car.':<6} {'Description':<30}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
        
        for i in range(128, 256):
            hex_val = f"0x{i:02X}"
            binary_val = f"{i:08b}"
            char = chr(i)
            
            # Description selon la plage
            if 128 <= i <= 159:
                desc = "Caractères de contrôle étendus"
                color = Fore.YELLOW
            elif 160 <= i <= 255:
                desc = "Caractères spéciaux/accents"
                color = Fore.CYAN
            else:
                desc = "Autre"
                color = Fore.WHITE
            
            print(f"{color}{i:<6} {hex_val:<6} {binary_val:<10} {char:<6} {desc:<30}{Style.RESET_ALL}")
            
            # Nouvelle ligne après 32 caractères
            if (i + 1) % 32 == 0 and i < 255:
                input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'═'*80}{Style.RESET_ALL}")
    
    def get_control_char_name(self, code):
        """Retourne le nom d'un caractère de contrôle ASCII"""
        control_names = {
            0: "NULL", 1: "SOH", 2: "STX", 3: "ETX", 4: "EOT", 5: "ENQ", 6: "ACK", 7: "BEL",
            8: "BS", 9: "TAB", 10: "LF", 11: "VT", 12: "FF", 13: "CR", 14: "SO", 15: "SI",
            16: "DLE", 17: "DC1", 18: "DC2", 19: "DC3", 20: "DC4", 21: "NAK", 22: "SYN",
            23: "ETB", 24: "CAN", 25: "EM", 26: "SUB", 27: "ESC", 28: "FS", 29: "GS",
            30: "RS", 31: "US", 127: "DEL"
        }
        return control_names.get(code, f"CTRL-{code:02X}")
    
    def show_examples(self):
        """Option 4 : Exemples prédéfinis"""
        print(f"\n{Fore.GREEN}〔 Option 4 : Exemples Prédéfinis 〕{Style.RESET_ALL}")
        
        examples = [
            {"name": "Hello World", "text": "Hello World!", "type": "text"},
            {"name": "Nombres", "text": "1234567890", "type": "text"},
            {"name": "Caractères spéciaux", "text": "@#$%&*()", "type": "text"},
            {"name": "Codes ASCII → Bonjour", "codes": "66 111 110 106 111 117 114", "type": "codes"},
            {"name": "Hexadécimal → ASCII", "codes": "0x48 0x65 0x6C 0x6C 0x6F", "type": "codes"},
            {"name": "Mixte", "text": "A=65, B=66, a=97", "type": "text"},
        ]
        
        print(f"{Fore.YELLOW}Choisissez un exemple :{Style.RESET_ALL}\n")
        
        for i, example in enumerate(examples, 1):
            print(f"  {Fore.GREEN}[{i}]{Style.RESET_ALL} {example['name']}")
        
        choice = input(f"\n{Fore.CYAN}Votre choix (1-{len(examples)}) : {Style.RESET_ALL}").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                example = examples[idx]
                
                if example['type'] == 'text':
                    print(f"\n{Fore.GREEN}Exemple : {example['name']}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Texte : {example['text']}{Style.RESET_ALL}")
                    
                    # Simuler l'option 1
                    print(f"\n{Fore.YELLOW}Simulation Texte → ASCII :{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
                    
                    for char in example['text']:
                        ascii_val = ord(char)
                        print(f"{Fore.CYAN}{char} → {ascii_val} (0x{ascii_val:02X}) → {ascii_val:08b}{Style.RESET_ALL}")
                    
                else:  # codes
                    print(f"\n{Fore.GREEN}Exemple : {example['name']}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Codes : {example['codes']}{Style.RESET_ALL}")
                    
                    # Simuler l'option 2
                    print(f"\n{Fore.YELLOW}Simulation ASCII → Texte :{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
                    
                    codes = example['codes'].split()
                    text_chars = []
                    
                    for code in codes:
                        try:
                            if code.startswith('0x'):
                                ascii_val = int(code, 16)
                            else:
                                ascii_val = int(code)
                            
                            char = chr(ascii_val)
                            text_chars.append(char)
                            print(f"{Fore.CYAN}{code} → {ascii_val} → '{char}'{Style.RESET_ALL}")
                        except:
                            print(f"{Fore.RGREEN}{code} → Erreur de conversion{Style.RESET_ALL}")
                    
                    if text_chars:
                        print(f"\n{Fore.GREEN}Texte résultant : '{''.join(text_chars)}'{Style.RESET_ALL}")
                
                print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Choix invalide !{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Entrée invalide !{Style.RESET_ALL}")
    
    def run(self):
        """Lance le programme principal"""
        self.clear_screen()
        
        while True:
            self.show_banner()
            self.show_menu()
            
            choice = input(f"\n{Fore.GREEN}Choix (1-5) : {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self.text_to_ascii()
            elif choice == '2':
                self.ascii_to_text()
            elif choice == '3':
                self.show_ascii_table()
            elif choice == '4':
                self.show_examples()
            elif choice == '5':
                print(f"\n{Fore.YELLOW}Au revoir ! 👋{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.GREEN}Choix invalide ! Veuillez choisir 1-5.{Style.RESET_ALL}")
            
            input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
            self.clear_screen()

def main():
    """Fonction principale"""
    try:
        converter = ASCIIConverter()
        converter.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Programme interrompu. Au revoir !{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.GREEN}Erreur : {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()