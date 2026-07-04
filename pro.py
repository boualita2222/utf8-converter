# ─────────────────────────────────────────
#  DÉCODEUR UTF-8
# ─────────────────────────────────────────

def decoder_utf8(hex_string):
    """Décode une séquence hex UTF-8 en caractère"""
    octets  = [int(x, 16) for x in hex_string.strip().split()]
    premier = octets[0]

    if premier & 0b10000000 == 0:
        cp = premier

    elif premier & 0b11100000 == 0b11000000:
        cp = ((premier   & 0b00011111) << 6) \
           | (octets[1]  & 0b00111111)

    elif premier & 0b11110000 == 0b11100000:
        cp = ((premier   & 0b00001111) << 12) \
           | ((octets[1] & 0b00111111) << 6)  \
           | (octets[2]  & 0b00111111)

    else:
        cp = ((premier   & 0b00000111) << 18) \
           | ((octets[1] & 0b00111111) << 12) \
           | ((octets[2] & 0b00111111) << 6)  \
           | (octets[3]  & 0b00111111)

    return chr(cp)


def decoder_afficher(hex_string):
    """Affiche le décodage complet"""
    octets  = [int(x, 16) for x in hex_string.strip().split()]
    premier = octets[0]

    if premier & 0b10000000 == 0:
        cp = premier
    elif premier & 0b11100000 == 0b11000000:
        cp = ((premier   & 0b00011111) << 6) \
           | (octets[1]  & 0b00111111)
    elif premier & 0b11110000 == 0b11100000:
        cp = ((premier   & 0b00001111) << 12) \
           | ((octets[1] & 0b00111111) << 6)  \
           | (octets[2]  & 0b00111111)
    else:
        cp = ((premier   & 0b00000111) << 18) \
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


def decoder_chaine(hex_string):
    """Décode une chaîne complète hex UTF-8"""
    octets = [int(x, 16) for x in hex_string.strip().split()]
    result = ""
    i = 0
    while i < len(octets):
        b = octets[i]
        if b & 0b10000000 == 0:
            seq = octets[i:i+1]; i += 1
        elif b & 0b11100000 == 0b11000000:
            seq = octets[i:i+2]; i += 2
        elif b & 0b11110000 == 0b11100000:
            seq = octets[i:i+3]; i += 3
        else:
            seq = octets[i:i+4]; i += 4
        hex_seq = " ".join(f"{b:02X}" for b in seq)
        char    = decoder_utf8(hex_seq)
        result += char
        print(f"    {hex_seq:<15} →  {char}")
    print(f"\n  Texte décodé : {result}")
    print()


# ── Tests décodeur ────────────────────────
print("=" * 45)
print("  DÉCODEUR UTF-8 MANUEL")
print("=" * 45)
print()

print("── Séquences individuelles ──")
print()
for seq in ["C3 A7", "E2 82 AC", "F0 9F 90 8D",
            "CE A9", "C5 93", "E2 9D A4"]:
    decoder_afficher(seq)

print("── Chaînes complètes ──")
print()
print("  Décodage : 42 6F 6E 6A 6F 75 72 20 F0 9F 8C 8D")
decoder_chaine("42 6F 6E 6A 6F 75 72 20 F0 9F 8C 8D")

print("  Décodage : C3 89 74 C3 A9 20 E2 84 A2")
decoder_chaine("C3 89 74 C3 A9 20 E2 84 A2")

print("  Décodage : 63 6F 65 75 72 20 E2 9D A4 EF B8 8F")
decoder_chaine("63 6F 65 75 72 20 E2 9D A4 EF B8 8F")