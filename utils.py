# utf8_package/utils.py
"""
Utilitaires partagés par tous les modules
"""

def valider_hex(token):
    """Vérifie qu'un token est un hex valide"""
    tok = token.replace("0x","").replace("0X","")
    if not (1 <= len(tok) <= 2):
        return False
    return all(c in "0123456789ABCDEFabcdef"
               for c in tok)

def hex_vers_octets(hex_string):
    """Convertit une chaîne hex en liste d'octets"""
    tokens = hex_string.strip().split()
    octets = []
    for tok in tokens:
        if not valider_hex(tok):
            raise ValueError(
                f"Token hex invalide : '{tok}'")
        octets.append(
            int(tok.replace("0x",""), 16))
    return octets

def octets_vers_hex(octets):
    """Convertit une liste d'octets en chaîne hex"""
    return " ".join(f"{b:02X}" for b in octets)

def octets_vers_bin(octets):
    """Convertit une liste d'octets en binaire"""
    return " ".join(f"{b:08b}" for b in octets)

def taille_utf8(premier_octet):
    """Retourne le nombre d'octets d'un caractère UTF-8"""
    if   premier_octet & 0b10000000 == 0:          return 1
    elif premier_octet & 0b11100000 == 0b11000000: return 2
    elif premier_octet & 0b11110000 == 0b11100000: return 3
    elif premier_octet & 0b11111000 == 0b11110000: return 4
    else:
        raise ValueError(
            f"Octet UTF-8 invalide : "
            f"{premier_octet:02X}")