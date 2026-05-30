# utf8_package/decodeur.py
from .utils import hex_vers_octets, taille_utf8

def decoder_octets(octets):
    b = octets[0]
    if   b & 0b10000000 == 0:
        return b
    elif b & 0b11100000 == 0b11000000:
        return ((b & 0b00011111) << 6) | (octets[1] & 0b00111111)
    elif b & 0b11110000 == 0b11100000:
        return ((b & 0b00001111) << 12) \
             | ((octets[1] & 0b00111111) << 6) \
             | (octets[2] & 0b00111111)
    else:
        return ((b & 0b00000111) << 18) \
             | ((octets[1] & 0b00111111) << 12) \
             | ((octets[2] & 0b00111111) << 6) \
             | (octets[3] & 0b00111111)

def decoder_hex(hex_string):
    if not hex_string.strip():
        raise ValueError("Hex vide !")
    try:
        octets = hex_vers_octets(hex_string)
    except ValueError as e:
        raise ValueError(str(e))
    try:
        bytes(octets).decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"Sequence UTF-8 invalide : {e}")
    texte   = ""
    details = []
    i       = 0
    while i < len(octets):
        n    = taille_utf8(octets[i])
        seq  = octets[i:i+n]
        cp   = decoder_octets(seq)
        char = chr(cp)
        texte += char
        details.append({
            "hex":  " ".join(f"{b:02X}" for b in seq),
            "cp":   cp,
            "char": char,
            "n":    n,
        })
        i += n
    return {"texte": texte, "details": details}
