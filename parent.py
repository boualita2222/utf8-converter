# Cas 1
try:
    x = int("abc")
except ValueError as e:
    print("Erreur !")

# Cas 2
try:
    x = int("123")
except ValueError as e:
    print("Erreur !")
else:
    print("Succès !")

# Cas 3
try:
    x = 10 / 0
except ValueError:
    print("Erreur valeur !")
except ZeroDivisionError:
    print("Division par zéro !")
finally:
    print("Terminé !")