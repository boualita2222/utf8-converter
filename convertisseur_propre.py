#!/usr/bin/env python3
"""
CONVERTISSEUR UTF-8 PROPRE - Python 3.14.0
Pas de KeyboardInterrupt, installation propre
"""

import sys
import os

# FIX DÉFINITIF POUR KEYBOARDINTERRUPT
if sys.platform == "win32":
    try:
        import msvcrt
        # Vider buffer clavier
        while msvcrt.kbhit():
            msvcrt.getch()
    except:
        pass

# Vider buffer stdin
sys.stdin.flush()
import time
time.sleep(0.1)

# Maintenant importer colorama SANS RISQUE
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    Fore = Style = type('obj', (object,), {'__getattr__': lambda self, name: ''})()

def main():
    """Fonction principale avec buffer nettoyé."""
    print(f"{Fore.GREEN if HAS_COLOR else ''}🔠 CONVERTISSEUR UTF-8 PROPRE")
    print("="*60)
    print(f"Python {sys.version.split()[0]} | Colorama: {'✅' if HAS_COLOR else '❌'}")
    print("="*60)
    
    # MENU SÉCURISÉ
    while True:
        print(f"\n{Fore.CYAN if HAS_COLOR else ''}OPTIONS:")
        print("1. Hex → Décimal (ex: C2 80)")
        print("2. Décimal → Hex (ex: 49792)")
        print("3. Test rapide")
        print("4. Quitter")
        
        try:
            # INPUT SÉCURISÉ
            choix = input(f"\n{Fore.YELLOW if HAS_COLOR else ''}Choix (1-4): ").strip()
            
            if choix == '4':
                print(f"{Fore.GREEN if HAS_COLOR else ''}👋 Au revoir!")
                break
                
            elif choix == '1':
                hex_input = input("Hexadécimal: ").strip()
                hex_clean = hex_input.replace(' ', '')
                try:
                    decimal = int(hex_clean, 16)
                    print(f"→ {decimal:,} (0x{hex_clean.upper()})")
                except:
                    print("❌ Format hexadécimal invalide")
                    
            elif choix == '2':
                try:
                    dec = int(input("Décimal: ").replace(',', '').strip())
                    print(f"→ 0x{dec:X}")
                except:
                    print("❌ Nombre invalide")
                    
            elif choix == '3':
                # Test automatique
                tests = [("C2 80", 49792), ("E2 82 AC", 14844588)]
                for hex_val, expected in tests:
                    result = int(hex_val.replace(' ', ''), 16)
                    status = "✅" if result == expected else "❌"
                    print(f"{hex_val} = {result:,} {status}")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.RED if HAS_COLOR else ''}⚠️  Nettoyage buffer...")
            sys.stdin.flush()
            continue
        except EOFError:
            break

if __name__ == "__main__":
    # DERNIER NETTOYAGE AVANT EXÉCUTION
    sys.stdin.flush()
    main()