# utf8_package/encodeur.py
"""
Module d'encodage UTF-8
"""

from .utils import octets_vers_hex

def encoder_char(c):
    """Encode un seul caractère en liste d'octets"""
    cp = ord(c)
    if cp <= 127:
        return [cp]
    elif cp <= 2047:
        return [
            0b11000000 | (cp >> 6),
            0b10000000 | (cp & 0b00111111)
        ]
    elif cp <= 65535:
        return [
            0b11100000 | (cp >> 12),
            0b10000000 | ((cp >> 6)  & 0b00111111),
            0b10000000 | (cp & 0b00111111)
        ]
    else:
        return [
            0b11110000 | (cp >> 18),
            0b10000000 | ((cp >> 12) & 0b00111111),
            0b10000000 | ((cp >> 6)  & 0b00111111),
            0b10000000 | (cp & 0b00111111)
        ]

def encoder_texte(texte):
    """
    Encode un texte complet en UTF-8.
    Retourne un dict avec hex et détails.
    """
    if not isinstance(texte, str):
        raise TypeError(
            f"Attendu str, reçu "
            f"{type(texte).__name__}")
    if not texte:
        raise ValueError("Texte vide !")

    tous_octets = []
    details     = []

    for c in texte:
        octets = encoder_char(c)
        tous_octets.extend(octets)
        details.append({
            "char":   c,
            "cp":     ord(c),
            "hex":    octets_vers_hex(octets),
            "n":      len(octets),
        })

    return {
        "texte":     texte,
        "hex":       octets_vers_hex(tous_octets),
        "nb_chars":  len(texte),
        "nb_octets": len(tous_octets),
        "details":   details,
    }

def encoder_fichier(chemin_in, chemin_out=None):
    """
    Encode toutes les lignes d'un fichier.
    Sauvegarde dans chemin_out si fourni.
    """
    if not chemin_out:
        chemin_out = chemin_in.replace(
            ".txt", "_encoded.txt")
    try:
        with open(chemin_in, "r",
                  encoding="utf-8") as f:
            lignes = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Fichier introuvable : {chemin_in}")

    resultats = []
    for i, ligne in enumerate(lignes, 1):
        ligne = ligne.rstrip("\n")
        res   = encoder_texte(ligne) if ligne else \
                {"hex": "", "nb_octets": 0}
        resultats.append({
            "num":   i,
            "texte": ligne,
            "hex":   res["hex"],
            "oct":   res["nb_octets"],
        })

    # Sauvegarder
    with open(chemin_out, "w",
              encoding="utf-8") as f:
        for r in resultats:
            f.write(
                f"Ligne {r['num']:02d} "
                f"({r['oct']:3d} oct) : "
                f"{r['hex']}\n")

    return resultats, chemin_out