#!/usr/bin/env python3
"""
CONVERTISSEUR UTF-8 COMPLET - 6 OPTIONS
Python 3.14.2 + Colorama
"""

import sys
import os
import time

# ========== FIX DÉFINITIF KEYBOARDINTERRUPT ==========
if sys.platform == "win32":
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except:
        pass
sys.stdin.flush()
time.sleep(0.1)
# =====================================================

try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init(autoreset=True)
    COLORAMA = True
except:
    COLORAMA = False
    Fore = Back = Style = type('obj', (object,), {'__getattr__': lambda self, name: ''})()

def safe_input(prompt):
    """Input sécurisé contre KeyboardInterrupt."""
    sys.stdin.flush()
    time.sleep(0.05)
    return input(prompt)

def hex_vers_decimal(hex_str):
    """Convertit hexadécimal UTF-8 en décimal."""
    hex_clean = hex_str.replace(' ', '').replace('0x', '')
    try:
        return int(hex_clean, 16)
    except:
        return None

def show(hex1, hex2=None, hex3=None, hex4=None):
    """Fonction show() comme dans vos exemples."""
    hex_list = [h for h in [hex1, hex2, hex3, hex4] if h is not None]
    hex_str = ' '.join(hex_list)
    
    print(f"\n{Fore.CYAN if COLORAMA else ''}{'='*70}")
    print(f"ANALYSE: {hex_str}")
    print(f"{'='*70}")
    
    bytes_list = []
    for h in hex_list:
        try:
            bytes_list.append(int(h, 16))
        except:
            print(f"Hex invalide: {h}")
            return
    
    # Calcul décimal brut
    decimal = 0
    for byte in bytes_list:
        decimal = (decimal << 8) | byte
    
    print(f"Hexadécimal  : {hex_str}")
    print(f"Octets       : {len(bytes_list)}")
    print(f"Octets bruts : {bytes_list}")
    print(f"Décimal brut : {decimal:,} (0x{decimal:X})")
    
    # Essayer de décoder en UTF-8
    try:
        bytes_data = bytes(bytes_list)
        char = bytes_data.decode('utf-8')
        codepoint = ord(char)
        print(f"Caractère    : {char}")
        print(f"Unicode      : U+{codepoint:04X}")
        print(f"Décimal      : {codepoint:,}")
    except:
        print("Caractère    : [Non UTF-8 valide]")
    
    print(f"Séquence UTF-8 valide : {'OUI' if len(bytes_list) <= 4 else 'NON'}")

def menu_principal():
    """Menu interactif avec 6 options."""
    print(f"{Fore.CYAN if COLORAMA else ''}╔{'═'*60}╗")
    print(f"{Fore.CYAN if COLORAMA else ''}║{' '*18}CONVERTISSEUR UTF-8 COMPLET{' '*18}║")
    print(f"{Fore.CYAN if COLORAMA else ''}║{' '*18}Python 3.14.2 (6 options){' '*19}║")
    print(f"{Fore.CYAN if COLORAMA else ''}╚{'═'*60}╝")
    print(f"Colorama: {'✅ Installé' if COLORAMA else '❌ Non installé'}")
    
    while True:
        print(f"\n{Fore.YELLOW if COLORAMA else ''}OPTIONS :")
        print(f"{Fore.WHITE if COLORAMA else ''}  1. Hexadécimal → Analyse (ex: C2 80, F0 9F 9A 81)")
        print(f"{Fore.WHITE if COLORAMA else ''}  2. Décimal → Analyse (ex: 49792, 4036991617)")
        print(f"{Fore.WHITE if COLORAMA else ''}  3. Caractère → Analyse (ex: A, €, 😊)")
        print(f"{Fore.WHITE if COLORAMA else ''}  4. Fonction show() personnalisée")
        print(f"{Fore.WHITE if COLORAMA else ''}  5. Exemples prédéfinis")
        print(f"{Fore.WHITE if COLORAMA else ''}  6. Quitter")
        
        choix = safe_input(f"\n{Fore.GREEN if COLORAMA else ''}Votre choix (1-6): ").strip()
        
        if choix == '6':
            print(f"{Fore.GREEN if COLORAMA else ''}\n👋 Au revoir!")
            break
        
        elif choix == '1':
            hex_input = safe_input("Hexadécimal (1-4 octets): ").strip()
            result = hex_vers_decimal(hex_input)
            if result:
                print(f"✅ {hex_input} = {result:,} (0x{result:X})")
            else:
                print("❌ Format invalide")
        
        elif choix == '2':
            try:
                dec = int(safe_input("Décimal: ").replace(',', ''))
                print(f"✅ {dec:,} = 0x{dec:X}")
            except:
                print("❌ Nombre invalide")
        
        elif choix == '3':
            char = safe_input("Caractère (un seul): ").strip()
            if len(char) == 1:
                codepoint = ord(char)
                print(f"✅ '{char}' = U+{codepoint:04X} ({codepoint:,})")
            else:
                print("❌ Un seul caractère svp")
        
        elif choix == '4':
            print("\nFormat: show(octet1, octet2, [octet3, octet4])")
            hex1 = safe_input("Octet 1 (hex): ").strip()
            hex2 = safe_input("Octet 2 (hex): ").strip()
            hex3 = safe_input("Octet 3 (hex, vide si fin): ").strip()
            hex4 = safe_input("Octet 4 (hex, vide si fin): ").strip()
            
            if hex4:
                show(hex1, hex2, hex3, hex4)
            elif hex3:
                show(hex1, hex2, hex3)
            else:
                show(hex1, hex2)
        
        elif choix == '5':
            print(f"\n{Fore.CYAN if COLORAMA else ''}Exemples prédéfinis:")
            examples = [
                ("C2", "80"),
                ("E2", "82", "AC"),
                ("F0", "9F", "98", "8A")
            ]
            for ex in examples:
                if len(ex) == 2:
                    show(ex[0], ex[1])
                elif len(ex) == 3:
                    show(ex[0], ex[1], ex[2])
                elif len(ex) == 4:
                    show(ex[0], ex[1], ex[2], ex[3])

if __name__ == "__main__":
    menu_principal()