from ui import MainUI
from logic import IndexDBCreator, Toolbox, ImageSearcher

# Initialisation des composants principaux
toolbox = Toolbox() # Utilitaire pour le traitement des images
indexDBCreator = IndexDBCreator(".\\dataset", toolbox) # Créateur de la base d'index
imageSearcher = ImageSearcher("descripteurs.json", toolbox) # Moteur de recherche d'images
# Initialisation et démarrage de l'interface utilisateur principale
mainUi = MainUI(imageSearcher=imageSearcher ,indexDBCreator=indexDBCreator, toolbox=toolbox)
mainUi.setupUI()
mainUi.startUI()