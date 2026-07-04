class UTF8Converter():
    def __init__(self):
        self.historique = []
        self.nb_operations = 0

conv = UTF8Converter() 

# → historique = []
# → nb_operations = 0

# Vous utilisez les méthodes PUBLIQUES
conv.encoder("Bonjour")
# → nb_operations = 1
# → historique = ["Bonjour → 42 6F 6E 6A 6F 75 72"]

conv.encoder("café")
# → nb_operations = 2
# → historique = ["Bonjour→ 42 6F 6E 6A 6F 75 72", "café → 63 61 66 C3 A9"]

conv.decoder("C3 A9")
# → nb_operations = 3 
# → historique = 3 operations : ["Bonjour → 42 6F 6E 6A 6F 75 72", "café → 63 61 66 C3 A9", "C3 A9]"]
# Vous affichez l'historique 
conv.afficher_historique() 
# → affiche les 3 opérations ✅ 


print(conv.nb_operations)
# → affiche 3 