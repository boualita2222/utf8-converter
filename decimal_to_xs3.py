def decimal_to_xs3(nombre):
    """
    Convertit un nombre décimal en code XS-3
    """
    # Gérer le cas du nombre négatif
    if nombre < 0:
        return "Erreur : Le nombre doit être positif"
    
    # Convertir le nombre en chaîne pour traiter chaque chiffre
    nombre_str = str(nombre)
    resultat = ""
    
    for chiffre in nombre_str:
        chiffre_int = int(chiffre)
        # Ajouter 3 au chiffre
        xs3_chiffre = chiffre_int + 3
        # Convertir en binaire sur 4 bits
        binaire = format(xs3_chiffre, '04b')
        resultat += binaire + " "
    
    return resultat.strip()

def xs3_to_decimal(xs3_code):
    """
    Convertit un code XS-3 en nombre décimal
    """
    # Supprimer les espaces et séparer les groupes de 4 bits
    xs3_code = xs3_code.replace(" ", "")
    
    # Vérifier que la longueur est un multiple de 4
    if len(xs3_code) % 4 != 0:
        return "Erreur : Code XS-3 invalide (longueur incorrecte)"
    
    resultat = ""
    
    # Traiter chaque groupe de 4 bits
    for i in range(0, len(xs3_code), 4):
        groupe = xs3_code[i:i+4]
        
        # Vérifier que le groupe contient uniquement des 0 et 1
        if not all(bit in '01' for bit in groupe):
            return "Erreur : Code XS-3 invalide (caractères non binaires)"
        
        # Convertir le binaire en décimal
        valeur = int(groupe, 2)
        
        # Soustraire 3 pour obtenir le chiffre décimal
        chiffre = valeur - 3
        
        # Vérifier que le chiffre est entre 0 et 9
        if chiffre < 0 or chiffre > 9:
            return "Erreur : Code XS-3 invalide (chiffre hors plage)"
        
        resultat += str(chiffre)
    
    return int(resultat)

def afficher_table_xs3():
    """
    Affiche la table de conversion des chiffres décimaux vers XS-3
    """
    print("\n" + "="*50)
    print("Table de conversion décimal -> XS-3")
    print("="*50)
    print("Décimal | XS-3 (binaire)")
    print("-"*50)
    
    for i in range(10):
        xs3 = i + 3
        binaire = format(xs3, '04b')
        print(f"   {i}     |   {binaire}")
    
    print("="*50 + "\n")

def main():
    """
    Fonction principale avec menu interactif
    """
    print("\n" + "="*50)
    print("CONVERTISSEUR DÉCIMAL <-> CODE XS-3 (EXCÈS 3)")
    print("="*50)
    
    while True:
        print("\nChoisissez une option :")
        print("1. Convertir un nombre décimal en code XS-3")
        print("2. Convertir un code XS-3 en nombre décimal")
        print("3. Afficher la table de conversion")
        print("4. Quitter")
        
        choix = input("\nVotre choix (1-4) : ").strip()
        
        if choix == '1':
            try:
                nombre = int(input("Entrez un nombre décimal positif : "))
                resultat = decimal_to_xs3(nombre)
                print(f"\nRésultat : {nombre} en XS-3 = {resultat}")
            except ValueError:
                print("Erreur : Veuillez entrer un nombre valide")
        
        elif choix == '2':
            xs3_code = input("Entrez le code XS-3 (ex: 0110 1001) : ")
            resultat = xs3_to_decimal(xs3_code)
            print(f"\nRésultat : {xs3_code} en décimal = {resultat}")
        
        elif choix == '3':
            afficher_table_xs3()
        
        elif choix == '4':
            print("\nAu revoir !")
            break
        
        else:
            print("Choix invalide. Veuillez choisir entre 1 et 4.")

# Exemples d'utilisation
if __name__ == "__main__":
    # Afficher quelques exemples
    print("\n" + "="*50)
    print("EXEMPLES D'UTILISATION")
    print("="*50)
    
    exemples = [0, 1, 5, 9, 42, 123]
    for nombre in exemples:
        xs3 = decimal_to_xs3(nombre)
        print(f"{nombre:3d} en décimal = {xs3} en XS-3")
    
    print("\n" + "-"*50)
    
    exemples_xs3 = ["0011", "0100", "1000", "1100", "01010101", "011010011010"]
    for xs3_code in exemples_xs3:
        decimal = xs3_to_decimal(xs3_code)
        print(f"{xs3_code} en XS-3 = {decimal} en décimal")
    
    print("\n" + "="*50)
    
    # Lancer le programme interactif
    main()