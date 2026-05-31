def saluer():
    print("Bonjour !")
    
saluer()
def saluer(nom):
    print("Bonjour", nom)

saluer("abderrahman")
def addition(a, b):
    return a + b

resultat = addition(10, 5)
print(resultat) 

def codepoint(car):
    return hex(ord(car))

print(codepoint("é"))
def utf8_hex(car):
    return car.encode("utf-8").hex()

print(utf8_hex("û"))
def analyse(car):
    cp = hex(ord(car))
    utf = car.encode("utf-8").hex()
    taille = len(car.encode("utf-8"))

    print("Caractère :", car)
    print("Codepoint :", cp)
    print("UTF-8 :", utf)
    print("Taille :", taille, "octet(s)")
def pair_ou_impair(n):
    ...
def maximum(a, b):
    ...
def analyse_utf8(car):
    ...
def analyser_chaine(texte):
    ...

