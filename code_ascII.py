mot = input("trouver le code ASCII + code xs-3 : ")
x = len(mot)
liste = []
i = 0
while i < x :
  liste.append(ord(mot[i]))
  i+=1
print(liste + [120, 115, 45, 51])