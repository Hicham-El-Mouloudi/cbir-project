import cv2
import numpy as np
import json
import os
from matplotlib.figure import Figure
import math

class Toolbox :
    def readImage(self, imagePath, colorSpace) :
        image = cv2.imread(imagePath)
        if colorSpace == "RGB" :
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif colorSpace == "HSV" :
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        elif colorSpace == "Lab" :
            image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
        return image
    
    def redimensionnerImage(self, image, size) :
        return cv2.resize(image, size)
    
    def transformerEnRGB(self, image) :
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def transformerEnHSV(self, image) :
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    def transformerEnLab(self, image) :
        return cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    
    def calculerHistogrammeComplet(self, image, imagesSize):
        histogramme = np.zeros((256 * 3))
        # calcul d'histo
        for i in range(imagesSize[0]) :
            for j in range(imagesSize[1]) :
                for canal in range(3) : 
                    index = int(image[i][j][canal]) + 256 * canal
                    histogramme[ index ] += 1
        return histogramme
    
    def calculerHistobine(self, histogrammeComplet, binsNombreParCanal) :
        tailleBine = int(256 / binsNombreParCanal)
        reshapedBins = histogrammeComplet.reshape((binsNombreParCanal*3, tailleBine))
        print("The reshaped new bins are : ", reshapedBins)
        histobine = reshapedBins.sum(axis=1)
        return histobine
    
    def generateHistogrammesPlot(self, histogrammeComplet, histobine, colorSpace) :
        fig = Figure(figsize=(3, 4), dpi=100)
        # 
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.set_title("Histogramme Complet")
        pixelChanelSizeHistogramComplet = len(histogrammeComplet) // 3 # C'est 256 normalement
        pixelChanelSizeHistobine = len(histobine) // 3
        if colorSpace == "HSV" :
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[0:256], color='purple', label='Canal H')
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[256:512], color='gray', label='Canal S')
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[512:768], color='yellow', label='Canal V')
        elif colorSpace == "Lab" :
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[0:256], color='black', label='Canal L')
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[256:512], color='pink', label='Canal a')
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[512:768], color='cyan', label='Canal b')
        elif colorSpace == "RGB" :
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[0:256], color='r', label='Canal Rouge')
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[256:512], color='g', label='Canal Vert')
            ax1.bar(range(0, pixelChanelSizeHistogramComplet), histogrammeComplet[512:768], color='b', label='Canal Bleu')   
        print("The pixel channel size of the complet histogram is : ", pixelChanelSizeHistogramComplet)
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.set_title("Histobine")
        if colorSpace == "HSV" :
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[0:pixelChanelSizeHistobine], color='purple', label='Canal H')
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[pixelChanelSizeHistobine:2*pixelChanelSizeHistobine], color='gray', label='Canal S')
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[2*pixelChanelSizeHistobine:3*pixelChanelSizeHistobine], color='yellow', label='Canal V')
        elif colorSpace == "Lab" :
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[0:pixelChanelSizeHistobine], color='black', label='Canal L')
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[pixelChanelSizeHistobine:2*pixelChanelSizeHistobine], color='pink', label='Canal A')
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[2*pixelChanelSizeHistobine:3*pixelChanelSizeHistobine], color='cyan', label='Canal B')
        elif colorSpace == "RGB" :
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[0:pixelChanelSizeHistobine], color='r', label='Canal Rouge')
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[pixelChanelSizeHistobine:2*pixelChanelSizeHistobine], color='g', label='Canal Vert')
            ax2.bar(range(0, pixelChanelSizeHistobine), histobine[2*pixelChanelSizeHistobine:3*pixelChanelSizeHistobine], color='b', label='Canal Bleu')
        print("The pixel channel size of the histobine is : ", pixelChanelSizeHistobine)
        # ajouter les legendes
        ax1.legend()
        ax2.legend()
        
        return fig
    
    def generateSearchResultsPlot(self, searchResults, imagesSize, queryImagePath) :
        numResults = len(searchResults) + 1
        nombreColonnes = 5
        nombreLignes = math.ceil(numResults / nombreColonnes)
        
        width = nombreColonnes * 2
        height = nombreLignes * 2
        fig = Figure(figsize=(width, height), dpi=100)
        
        print("Search results : ", list(enumerate(searchResults)))
        # afficher l'image de requete
        searchResults.insert(0, (queryImagePath, 0.0))  # on l'ajoute au debut de la liste
        # 
        for i, (imagePath, distance) in list(enumerate(searchResults)):
            image = self.readImage(imagePath, "RGB")
            image = self.redimensionnerImage(image, imagesSize)
            
            ax = fig.add_subplot(nombreLignes, nombreColonnes, i + 1)
            ax.imshow(image)
            ax.axis('off')
            if i == 0 :
                ax.set_title("Image Origine")
            else :
                ax.set_title(f"D={distance:.4f}")
        
        return fig

class IndexDBCreator : 
    def __init__(self, datasetPath, toolbox, imagesSize=(256, 256), binsNombreParCanal = 8) :
        self.datasetPath = datasetPath
        self.binsNombreParCanal = binsNombreParCanal
        self.imagesSize = imagesSize
        self.toolbox = toolbox
        
    def getImagesSize(self) : 
        return self.imagesSize

    def setBinsNombreParCanal(self, binsNombreParCanal) : 
        self.binsNombreParCanal = binsNombreParCanal

    def saveIndexDBAsJson(self, jsonBody, colorSpace, imagesSize, binsNombreParCanal) : 
        with open('descripteurs.json', 'w') as jsonFile:
            jsonBodyWithMetaData = {
                "colorSpace": colorSpace,
                "imagesSize": imagesSize,
                "binsNombreParCanal": binsNombreParCanal,
                "data": jsonBody
            }
            json.dump(jsonBodyWithMetaData, jsonFile)
    
    def createIndexDB(self, colorSpace) :
        indexDB = {}
        for root, _, files in os.walk(self.datasetPath):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    imagePath = os.path.join(root, file)
                    image = self.toolbox.readImage(imagePath, colorSpace)
                    if image is not None:
                        image = self.toolbox.redimensionnerImage(image, self.imagesSize)
                        # image = self.toolbox.transformerEnRGB(image)
                        histoComplet = self.toolbox.calculerHistogrammeComplet(image, self.imagesSize)
                        histoBin = self.toolbox.calculerHistobine(histoComplet, self.binsNombreParCanal)
                        indexDB[imagePath] = histoBin.tolist()

        self.saveIndexDBAsJson(indexDB, colorSpace, self.imagesSize, self.binsNombreParCanal)

class ImageSearcher :
    def __init__(self, indexDBPath, toolbox) :
        self.indexDBPath = indexDBPath
        self.toolbox = toolbox
        self.indexDB = self.indexDBPath
    
    # charger l'indexDB depuis le fichier json et valider sa compatibilite avec les parametres données
    def loadIndexDBFromJsonAndCheck(self, colorSpace, imagesSize, binsNombreParCanal) :
        valide = False
        with open(self.indexDBPath, 'r') as jsonFile:
            indexDBWithMetaData = json.load(jsonFile)
            if (indexDBWithMetaData["colorSpace"] == colorSpace and
                indexDBWithMetaData["imagesSize"][0] == imagesSize[0] and
                indexDBWithMetaData["imagesSize"][1] == imagesSize[1] and
                int(indexDBWithMetaData["binsNombreParCanal"]) == binsNombreParCanal) :
                valide = True
            return indexDBWithMetaData["data"], valide
    
    def preparerRechercheImagesSimilaires(self, queryImage, colorSpace, imagesSize, binsNombreParCanal, topK=5) :
        # 
        indexDB, valide = self.loadIndexDBFromJsonAndCheck(colorSpace, imagesSize, binsNombreParCanal)
        # si le database des descripteurs n'est pas compatible avec les parametres actuels, on retourne None
        if not valide :
            raise Exception("Vous devez créer d'abort une database de descripteurs compatible !")
        # 
        histogrameComplete = self.toolbox.calculerHistogrammeComplet(queryImage, imagesSize)
        histobineQueryImage = self.toolbox.calculerHistobine(histogrameComplete, binsNombreParCanal)
        
        return indexDB, histobineQueryImage

    def rechercherDBAvecDistanceSwainBallard(self, indexDB, histobineQueryImage,imagesSize, topK=5) :
        # calculer les distances
        distances = {}
        for imagePath, histobine in list(indexDB.items()) : 
            similarite = 0
            for i in range(len(histobineQueryImage)) : 
                similarite += min(histobine[i], histobineQueryImage[i])
            # normalizing the similarity to [0,1]
            similarite = similarite / (imagesSize[0] * imagesSize[1]*3)
            # storing the distance
            distances[imagePath] = float(similarite)
        
        # trier les distances et obtenir les top K resultats
        allResults = sorted( distances.items(), key= lambda item : item[1], reverse=True )
        print("Les réesultats par Swain&Ballard : ", allResults)
        topKResults = allResults[:topK]
        return topKResults

    def rechercherDBAvecDistanceEuclidienne(self, indexDB, histobineQueryImage,imagesSize, topK=5) :
        # calculer les distances
        distances = {}
        for imagePath, histobine in list(indexDB.items()) : 
            similarite = 0
            for i in range(len(histobineQueryImage)) : 
                similarite += ( histobine[i] - histobineQueryImage[i] ) ** 2
            # calculer la racine carrée pour obtenir la distance euclidienne
            similarite = math.sqrt(similarite)
            # storing the distance
            distances[imagePath] = float(similarite)
        
        # trier les distances et obtenir les top K resultats
        # une valeur de distance plus petite indique une plus grande similarité
        allResults = sorted( distances.items(), key= lambda item : item[1])
        print("Les réesultats par Distance Euclidienne : ", allResults)
        topKResults = allResults[:topK]
        print("Top K Results : ", topKResults)
        return topKResults

    def rechercherDBAvecDistanceChiCarre(self, indexDB, histobineQueryImage,imagesSize, topK=5) :
        # calculer les distances
        distances = {}
        for imagePath, histobine in list(indexDB.items()) : 
            similarite = 0
            for i in range(len(histobineQueryImage)) : 
                denominateur = (histobine[i] + histobineQueryImage[i])
                if denominateur != 0 :
                    similarite += (( histobine[i] - histobineQueryImage[i] ) ** 2) / denominateur
            # storing the distance
            distances[imagePath] = float(similarite)
        
        # trier les distances et obtenir les top K resultats
        # une valeur de distance plus petite indique une plus grande similarité
        allResults = sorted( distances.items(), key= lambda item : item[1])
        print("\n\n\n\nLes réesultats par Distance Chi-Carré : ", allResults, "\n\n\n\n")
        topKResults = allResults[:topK]
        return topKResults

    def rechercherDBAvecCorrelation(self, indexDB, histobineQueryImage,imagesSize, topK=5) :
        # calculer les distances
        distances = {}
        averageHistobineQueryImage = np.mean(histobineQueryImage)
        numerateur = 0
        denominateurHistobineQueryImageSum = 0
        denominateurHistobineSum = 0
        for imagePath, histobine in list(indexDB.items()) : 
            similarite = 0
            AverageHistobine = np.mean(histobine)
            for i in range(len(histobineQueryImage)) : 
                numerateur += (histobine[i] - AverageHistobine) * (histobineQueryImage[i] - averageHistobineQueryImage)
                denominateurHistobineQueryImageSum += (histobineQueryImage[i] - averageHistobineQueryImage) ** 2
                denominateurHistobineSum += (histobine[i] - AverageHistobine) ** 2
            denominateur = math.sqrt(denominateurHistobineQueryImageSum * denominateurHistobineSum)
            similarite = numerateur / denominateur
            # storing the distance
            distances[imagePath] = float(similarite)
        
        # trier les distances et obtenir les top K resultats
        # une valeur de distance plus proche de 1 indique une plus grande similarité
        allResults = sorted( distances.items(), key= lambda item : item[1], reverse=True)
        print("Les réesultats par Correlation : ", allResults)
        topKResults = allResults[:topK]
        return topKResults