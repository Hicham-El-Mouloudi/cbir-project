import cv2
import numpy as np
import json
import os

class Toolbox :
    def redimensionnerImage(self, image, size) :
        return cv2.resize(image, size)
    
    def transformerEnRGB(self, image) :
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def calculerHistogrammeComplet(self, image):
        histogramme = np.zeros((256 * 3))
        # calcul d'histo
        for i in range(self.imagesSize[0]) :
            for j in range(self.imagesSize[1]) :
                for color in range(3) : 
                    index = int(image[i][j][color]) + 256 * color
                    histogramme[ index ] += 1
        return histogramme
    
    def calculerHistobine(self, histogrammeComplet, binsNombreParCanal) :
        tailleHistobine = int(256 / self.binsNombreParCanal) * 3
        reshapedBins = histogrammeComplet.reshape((tailleHistobine, binsNombreParCanal))
        print("The reshaped new bins are : ", reshapedBins)
        histobine = reshapedBins.sum(axis=1)
        return histobine

class IndexDBCreator : 
    def __init__(self, datasetPath, toolbox, imagesSize=(256, 256), binsNombreParCanal = 8) :
        self.binsNombreParCanal = binsNombreParCanal
        self.datasetPath = datasetPath
        self.imagesSize = imagesSize
        self.toolbox = toolbox
    
    def setBinsNombreParCanal(self, binsNombreParCanal) : 
        self.binsNombreParCanal = binsNombreParCanal

    def saveIndexDBAsJson(self, jsonBody) : 
        with open('indexDB.json', 'w') as jsonFile:
            json.dump(jsonBody, jsonFile)
    
    def createIndexDB(self) :
        indexDB = {}
        for root, _, files in os.walk(self.datasetPath):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    imagePath = os.path.join(root, file)
                    image = cv2.imread(imagePath)
                    if image is not None:
                        image = self.toolbox.redimensionnerImage(image, self.imagesSize)
                        image = self.toolbox.transformerEnRGB(image)
                        histoComplet = self.toolbox.calculerHistogrammeComplet(image)
                        histoBin = self.toolbox.calculerHistobine(histoComplet, self.binsNombreParCanal)
                        indexDB[imagePath] = histoBin.tolist()

        self.saveIndexDBAsJson(indexDB)