import random

# Générer un nombre entier aléatoire entre 1 et 10
nombre_aleatoire = random.randint(1, 10)
print(f"Nombre aléatoire généré : {nombre_aleatoire}")

# Sélectionner un élément aléatoire dans une liste
fruits = ["pomme", "banane", "cerise", "orange"]
fruit_choisi = random.choice(fruits)
print(f"Fruit choisi au hasard : {fruit_choisi}")

# Mélanger une liste
random.shuffle(fruits)
print(f"Liste mélangée : {fruits}")