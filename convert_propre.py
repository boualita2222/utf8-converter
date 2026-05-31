import sys

# NETTOYAGE BUFFER (fix définitif KeyboardInterrupt)
if sys.platform == "win32":
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except:
        pass
sys.stdin.flush()

# Importer colorama SANS ERREUR
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

def hex_to_decimal(hex_str):
    """Conversion hexadécimal → décimal."""
    hex_clean = hex_str.replace(' ', '').replace('0x', '')
    try:
        return int(hex_clean, 16)
    except:
        return None

def main():
    print(f"{Fore.GREEN}🔠 CONVERTISSEUR UTF-8 - PYTHON 3.14.2")
    print(f"{Fore.CYAN}{'='*60}")
    print(f"Colorama {colorama.__version__} | Python {sys.version.split()[0]}")
    print(f"{Fore.CYAN}{'='*60}")
    
    while True:
        print(f"\n{Fore.YELLOW}OPTIONS:")
        print("1. Hex → Décimal (ex: C2 80)")
        print("2. Décimal → Hex (ex: 49792)")
        print("3. Quitter")
        
        choix = input(f"\n{Fore.WHITE}Choix (1-3): ").strip()
        
        if choix == '3':
            print(f"{Fore.GREEN}👋 Au revoir!")
            break
        elif choix == '1':
            hex_input = input("Hexadécimal: ").strip()
            result = hex_to_decimal(hex_input)
            if result:
                print(f"{Fore.GREEN}→ {result:,} (0x{result:X})")
            else:
                print(f"{Fore.RED}❌ Format invalide")
        elif choix == '2':
            try:
                dec = int(input("Décimal: ").replace(',', '').strip())
                print(f"{Fore.GREEN}→ 0x{dec:X}")
            except:
                print(f"{Fore.RED}❌ Nombre invalide")

if __name__ == "__main__":
    main()