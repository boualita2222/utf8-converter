#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Texte avec différents caractères
texte = "Bonjour l'ami ! 你好世界 😊"

# Convertir en bytes UTF-8
bytes_utf8 = texte.encode('utf-8')
print(f"Bytes UTF-8 : {bytes_utf8}")

# Reconvertir en string
texte_decode = bytes_utf8.decode('utf-8')
print(f"Texte décodé : {texte_decode}")
