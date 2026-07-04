import sys
import colorama
from colorama import Fore, Style

# Initialiser Colorama
colorama.init(autoreset=True)

def hex_vers_decimal(hex_str):
    """Convertit hexadécimal UTF-8 en décimal."""
    hex_clean = hex_str.replace(' ', '').replace('0x', '')
    try:
        return int(hex_clean, 16)
    except ValueError:
        return None

def main():
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.GREEN}🔠 CONVERTISSEUR UTF-8 - PYTHON 3.14.2")
    print(f"{Fore.YELLOW}Environnement: {sys.executable}")
    print(f"{Fore.CYAN}{'='*60}")
    
    while True:
        print(f"\n{Fore.MAGENTA}OPTIONS:")
        print(f"{Fore.WHITE}1. Hexadécimal → Décimal")
        print(f"{Fore.WHITE}2. Décimal → Hexadécimal")
        print(f"{Fore.WHITE}3. Quitter")
        
        choix = input(f"\n{Fore.YELLOW}Votre choix (1-3): ").strip()
        
        if choix == '3':
            print(f"{Fore.GREEN}👋 Au revoir!")
            break
            
        elif choix == '1':
            hex_input = input(f"{Fore.CYAN}Hexadécimal (ex: C2 80): ").strip()
            result = hex_vers_decimal(hex_input)
            if result is not None:
                print(f"{Fore.GREEN}✅ {hex_input} = {result:,} (0x{result:X})")
            else:
                print(f"{Fore.RED}❌ Format hexadécimal invalide")
                
        elif choix == '2':
            try:
                dec_input = input(f"{Fore.CYAN}Décimal (ex: 49792): ").strip()
                dec = int(dec_input.replace(',', ''))
                print(f"{Fore.GREEN}✅ {dec:,} = 0x{dec:X}")
            except:
                print(f"{Fore.RED}❌ Nombre décimal invalide")

if __name__ == "__main__":
    main()