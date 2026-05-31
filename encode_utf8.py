def encode_utf8_manuel(caractere):
    """
    Encode un caractère en UTF-8 manuellement
    sans utiliser .encode()
    """
    cp = ord(caractere)

    # ── 1 octet ──────────────────────────
    if cp <= 127:
        octet1 = cp
        return [octet1]

    # ── 2 octets ─────────────────────────
    elif cp <= 2047:
        octet1 = 0b11000000 | (cp >> 6)
        octet2 = 0b10000000 | (cp & 0b00111111)
        return [octet1, octet2]

    # ── 3 octets ─────────────────────────
    elif cp <= 65535:
        octet1 = 0b11100000 | (cp >> 12)
        octet2 = 0b10000000 | ((cp >> 6) & 0b00111111)
        octet3 = 0b10000000 | (cp & 0b00111111)
        return [octet1, octet2, octet3]

    # ── 4 octets ─────────────────────────
    else:
        octet1 = 0b11110000 | (cp >> 18)
        octet2 = 0b10000000 | ((cp >> 12) & 0b00111111)
        octet3 = 0b10000000 | ((cp >> 6)  & 0b00111111)
        octet4 = 0b10000000 | (cp & 0b00111111)
        return [octet1, octet2, octet3, octet4]


def afficher_utf8(caractere):
    """Affiche le résultat complet"""
    octets  = encode_utf8_manuel(caractere)
    hex_str = " ".join(f"{b:02X}" for b in octets)
    bin_str = " ".join(f"{b:08b}" for b in octets)
    cp      = ord(caractere)
    print(f"  Caractère  : {caractere}")
    print(f"  Codepoint  : U+{cp:04X}")
    print(f"  Décimal    : {cp}")
    print(f"  Octets     : {len(octets)}")
    print(f"  Hex UTF-8  : {hex_str}")
    print(f"  Binaire    : {bin_str}")
    # Vérification avec Python
    verif = " ".join(f"{b:02X}" for b in caractere.encode("utf-8"))
    ok    = "✅" if hex_str == verif else "❌"
    print(f"  Vérif      : {ok}  ({verif})")
    print()


# ── Tests ────────────────────────────────
print("=" * 45)
print("  ENCODEUR UTF-8 MANUEL")
print("=" * 45)
print()

for c in ["A", "é", "€", "🐍", "ç", "™", "🌍", "Ω"]:
    afficher_utf8(c)