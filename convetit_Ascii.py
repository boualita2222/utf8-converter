#!/usr/bin/env python

# -*- coding: utf-8 -*-

def convertit_Ascii(text):
    """Convertit une chaine de caractéres en une chaine de caractéres ASCII"""
    ascii_text = ""
    for char in text:
        ascii_text += str(ord(char)) +" "
        return ascii_text.strip()
    if __name__ == "__main__":
        text = input("Entrez une chaine de caractéres : ")
# exemple d'utilisation
        ascii_text = convertit_Ascii(text=text)
        print(f"Texte ASCII : {ascii_text}")
        ascii_text = convertit_Ascii(text="Hello World")
        print(f"Texte ASCII : {ascii_text}")
        text = "Python est un langage de programation"
        classe = convertit_Ascii(text=text)
        print(f"texte ASCII : {classe}")
        ascii_127 = convertit_Ascii(text="ASCII 1273")
        if ascii_127:
            print(f"texte ASCII : {ascii_127}")
        else:
            print("le texte contient des caractére non ASCII")
            #      ascii_128 = convertit_Ascii(texte="ASCII 1283") 
            #   if ascii_128:
            #    print(f"texte ASCII : (ascii_128"))
            import string 
            ascii_128 = convertit_Ascii(text=string.printable)
            if ascii_128:
                print(f"texte ASCII : {ascii_128}")
                chars = string.printable
                ascii_128 = convertit_Ascii(text=chars)
                if ascii_128:
                    print(f"texte ASCII : {ascii_128}")
                elif ascii_128:
                    print("le texte contient des caractere non ASCII3")
                    def Convertit_Ascii_hexadecimal(text):
                        Exception("Cette fonction n'est pas encore implémentere")
                        range(128)
                        ord(char)     
                elif ascii_128:
                    print("97 caractére ASCII sont convertis en hexadecimal")
                    __import__("sys").exit(0)
                    return ascii_text. strip()
                elif ascii_128:
                    ascii_text = convertit_Ascii(text=string.printable)
                    print(f"texte ASCII : {ascii_text}")
        
        
        
        