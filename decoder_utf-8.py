def decoder_utf8(hex_string):
    """
    Décode une séquence hex UTF-8 en caractère
    Ex: "C3 A9" → é
    """
    octets = [int(x, 16) for x in hex_string.strip().split()]
    premier = octets[0]

    # ── 1 octet : 0xxxxxxx ──────────────────
    if premier & 0b10000000 == 0:
        cp = premier

    # ── 2 octets : 110xxxxx 10xxxxxx ────────
    elif premier & 0b11100000 == 0b11000000:
        cp = ((premier  & 0b00011111) << 6) \
           | (octets[1] & 0b00111111)

    # ── 3 octets : 1110xxxx 10xxxxxx 10xxxxxx
    elif premier & 0b11110000 == 0b11100000:
        cp = ((premier  & 0b00001111) << 12) \
           | ((octets[1] & 0b00111111) << 6) \
           | (octets[2]  & 0b00111111)

    # ── 4 octets : 11110xxx ×3 ──────────────
    else:
        cp = ((premier  & 0b00000111) << 18) \
           | ((octets[1] & 0b00111111) << 12) \
           | ((octets[2] & 0b00111111) << 6)  \
           | (octets[3]  & 0b00111111)

    return chr(cp)


def decoder_afficher(hex_string):
    """Affiche le décodage complet"""
    octets  = [int(x, 16) for x in hex_string.strip().split()]
    premier = octets[0]

    # recalculer cp
    if premier & 0b10000000 == 0:
        cp = premier
    elif premier & 0b11100000 == 0b11000000:
        cp = ((premier  & 0b00011111) << 6) \
           | (octets[1] & 0b00111111)
    elif premier & 0b11110000 == 0b11100000:
        cp = ((premier  & 0b00001111) << 12) \
           | ((octets[1] & 0b00111111) << 6) \
           | (octets[2]  & 0b00111111)
    else:
        cp = ((premier  & 0b00000111) << 18) \
           | ((octets[1] & 0b00111111) << 12) \
           | ((octets[2] & 0b00111111) << 6)  \
           | (octets[3]  & 0b00111111)

    char    = chr(cp)
    bin_str = " ".join(f"{b:08b}" for b in octets)
    print(f"  Hex        : {hex_string}")
    print(f"  Binaire    : {bin_str}")
    print(f"  Codepoint  : U+{cp:04X}")
    print(f"  Décimal    : {cp}")
    print(f"  Caractère  : {char}")
    print(f"  Octets     : {len(octets)}")
    print()


# ── Tests ────────────────────────────────
print("=" * 45)
print("  DÉCODEUR UTF-8 MANUEL")
print("=" * 45)
print()

for seq in ["C3 A7", "E2 82 AC", "F0 9F 90 8D", "CE A9", "C5 93"]:
    decoder_afficher(seq)