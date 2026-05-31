# utf8_package/analyseur.py
"""
Module d'analyse UTF-8
"""

import unicodedata
from .encodeur import encoder_char
from .utils    import (octets_vers_hex,
                        octets_vers_bin)

def analyser_char(c):
    """Analyse complète d'un caractère"""
    c      = c[0]
    cp     = ord(c)
    octets = encoder_char(c)
    ri     = int.from_bytes(bytes(octets), "big")
    try:    nom = unicodedata.name(c)
    except: nom = "(pas de nom)"

    return {
        "char":    c,
        "cp":      cp,
        "hex":     octets_vers_hex(octets),
        "bin":     octets_vers_bin(octets),
        "n":       len(octets),
        "raw_int": ri,
        "nom":     nom,
        "cat":     unicodedata.category(c),
    }

def analyser_texte(texte):
    """Statistiques UTF-8 d'un texte"""
    types = {1:[], 2:[], 3:[], 4:[]}
    for c in texte:
        n = len(encoder_char(c))
        types[n].append(c)
    total_oct = sum(len(v)*n
                    for n,v in types.items())
    return {
        "texte":     texte,
        "nb_chars":  len(texte),
        "nb_octets": total_oct,
        "types":     types,
        "pct_ascii": len(types[1])/
                     len(texte)*100
                     if texte else 0,
    }

def comparer(texte1, texte2):
    """Compare deux textes UTF-8"""
    from .encodeur import encoder_texte
    r1   = encoder_texte(texte1)
    r2   = encoder_texte(texte2)
    diff = []
    for i in range(max(len(texte1),
                       len(texte2))):
        c1 = texte1[i] if i<len(texte1) else None
        c2 = texte2[i] if i<len(texte2) else None
        if c1 != c2:
            diff.append({
                "pos": i+1,
                "c1":  c1,
                "c2":  c2,
                "h1":  octets_vers_hex(
                       encoder_char(c1))
                       if c1 else "—",
                "h2":  octets_vers_hex(
                       encoder_char(c2))
                       if c2 else "—",
            })
    return {
        "texte1":      texte1,
        "texte2":      texte2,
        "oct1":        r1["nb_octets"],
        "oct2":        r2["nb_octets"],
        "differences": diff,
        "identiques":  len(diff) == 0,
    }