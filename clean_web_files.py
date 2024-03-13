import os

def supprimer_fichiers_web(repertoire):
    # Parcours de tous les éléments du répertoire
    for element in os.listdir(repertoire):
        chemin = os.path.join(repertoire, element)
        # Si c'est un fichier .web, on le supprime
        if os.path.isfile(chemin) and element.endswith('.webm'):
            os.remove(chemin)
            print(f"Fichier {chemin} supprimé.")
        # Si c'est un répertoire, on rappelle la fonction récursivement
        elif os.path.isdir(chemin):
            supprimer_fichiers_web(chemin)

# Utilisation de la fonction
repertoire_a_purger = 'audio'
supprimer_fichiers_web(repertoire_a_purger)