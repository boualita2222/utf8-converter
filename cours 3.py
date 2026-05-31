for i in range(5):
    print(i)
texte = "Python"

for lettre in texte:
    print(lettre)
nombres = [10, 20, 30]

for n in nombres:
    print(n)
i = 0

while i < 5:
    print(i)
    i += 1
car = input("Caractère : ")
octets = car.encode("utf-8")

for o in octets:
    print(hex(o))
texte = input("Texte : ")

for c in texte:
    print(c, "→", hex(ord(c)))
