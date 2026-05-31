#!/usr/bin/env python3
"""
Convertit un nombre decimal en code XS-3
"""

def decimal_to_xs3(n):
    if n < 0:
        raise ValueError("Le nombre doit être positif ou nul")
    return ''.join(str(int(ch) + 3) for ch in str(n))

def main():
    valeur = input("Entrez un nombre decimal : ").strip()
    if not valeur:
        print("Aucune valeur fournie.")
        return
    if not valeur.isdigit():
        print("Veuillez entrer un nombre decimal positif.")
        return
    xs3 = decimal_to_xs3(int(valeur))
    print("Code XS-3 :", xs3)

if __name__ == "__main__":
    main()