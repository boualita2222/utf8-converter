#!/usr/bin/env python3
# -*- coding : utf-8 -*-
"""

CONVERISSEUR_UTF-8 - COMPLET - 1 à 4 octets
Version : python 3.14.2 + colorama
"""
import colorama
from colorama import init, force, Style, Back, Fore
import sys
import unicodedata

# Initialisation de Colorama
init(autoreset=True)

class UTF8Converter:
    def __init__(self):
        self.code_point = None
        self.utf_8_bytes = None
        self.utf_8_hexa = None
        self.utf_8_binary = None
        self.utf_8_length = None
        self.utf_8_decimal = None
        self.exemples = {
            'A': 0x41,
            'é': 0xe9,
            '€': 0x20ac,
            '🏝': 0x1f3dd
        }

    def convert(self, code_point):
        self.code_point = code_point
        if self.code_point <= 0x7f:
            self.utf_8_length = 1
            self.utf_8_bytes = [self.code_point]
        elif self.code_point <= 0x7ff:
            self.utf_8_length = 2
            self.utf_8_bytes = [
                0xc0 | (self.code_point >> 6),
                0x80 | (self.code_point & 0x3f)
            ]
        elif self.code_point <= 0xffff:
            self.utf_8_length = 3
            self.utf_8_bytes = [
                0xe0 | (self.code_point >> 12),
                0x80 | ((self.code_point >> 6) & 0x3f),
                0x80 | (self.code_point & 0x3f)
            ]
        elif self.code_point <= 0x10ffff:
            self.utf_8_length = 4
            self.utf_8_bytes = [
                0xf0 | (self.code_point >> 18),
                0x80 | ((self.code_point >> 12) & 0x3f),
                0x80 | ((self.code_point >> 6) & 0x3f),
                0x80 | (self.code_point & 0x3f)
            ]

        self.utf_8_hexa = ' '.join(f'{bytes:02x}' for bytes in self.utf_8_bytes)
        self.utf_8_binary = ' '.join(f'{bytes:08b}' for bytes in self.utf_8_bytes)
        self.utf_8_decimal = ' '.join(str(bytes) for bytes in self.utf_8_bytes)
    
        def display(self):
            print(f'{Style.BRIGHT}{Fore.CYAN}Code point U+{self.code_point:04x} ({self.code_point}){Style.RESET_ALL}')
    
    
    if __name__ == "__main__":
         converter = "UTF8Converter"
         converter.convert(ord("A"))
        
                        