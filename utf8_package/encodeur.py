# utf8_package/encodeur.py
from .utils import octets_vers_hex

def encoder_char(c):
    cp = ord(c)
    if cp <= 127:
        return [cp]
    elif cp <= 2047:
        return [0b11000000|(cp>>6),
                0b10000000|(cp&0b00111111)]
    elif cp <= 65535:
        return [0b11100000|(cp>>12),
                0b10000000|((cp>>6)&0b00111111),
                0b10000000|(cp&0b00111111)]
    else:
        return [0b11110000|(cp>>18),
                0b10000000|((cp>>12)&0b00111111),
                0b10000000|((cp>>6)&0b00111111),
                0b10000000|(cp&0b00111111)]

def encoder_texte(texte):
    if not isinstance(texte, str):
        raise TypeError(f"Attendu str, recu {type(texte).__name__}")
    if not texte:
        raise ValueError("Texte vide !")
    tous_octets = []
    details     = []
    for c in texte:
        octets = encoder_char(c)
        tous_octets.extend(octets)
        details.append({
            "char": c,
            "cp":   ord(c),
            "hex":  octets_vers_hex(octets),
            "n":    len(octets),
        })
    return {
        "texte":     texte,
        "hex":       octets_vers_hex(tous_octets),
        "nb_chars":  len(texte),
        "nb_octets": len(tous_octets),
        "details":   details,
    }
