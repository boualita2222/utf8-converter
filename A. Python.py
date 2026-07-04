# Encodage et décodage
text = "Bonjour 🌍"
utf8_bytes = text.encode('utf-8')  # bytes: b'Bonjour \xf0\x9f\x8c\x8d'
print(utf8_bytes)  # b'Bonjour \xf0\x9f\x8c\x8d'

# Décodage
original = utf8_bytes.decode('utf-8')
print(original)  # Bonjour 🌍

# Vérifier les bytes
for char in text:
    print(f"{char}: {char.encode('utf-8').hex()}")
# B: 42
# o: 6f
# ...
# 🌍: f09f8c8d