import cv2
import numpy as np
import json
import os
from matplotlib.figure import Figure

class Toolbox :
    def redimensionnerImage(self, image, size) :
        return cv2.resize(image, size)
    
    def transformerEnRGB(self, image) :
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def calculerHistogrammeComplet(self, image, imagesSize):
        histogramme = np.zeros((256 * 3))
        # calcul d'histo
        for i in range(imagesSize[0]) :
            for j in range(imagesSize[1]) :
                for color in range(3) : 
                    index = int(image[i][j][color]) + 256 * color
                    histogramme[ index ] += 1
        return histogramme
    
    def calculerHistobine(self, histogrammeComplet, binsNombreParCanal) :
        tailleHistobine = int(256 / binsNombreParCanal) * 3
        reshapedBins = histogrammeComplet.reshape((tailleHistobine, binsNombreParCanal))
        print("The reshaped new bins are : ", reshapedBins)
        histobine = reshapedBins.sum(axis=1)
        return histobine
    
    def generateHistogrammesPlot(self, histogrammeComplet, histobine, binsNombreParCanal):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.set_title("Histogramme Complet")
        ax1.bar(range(len(histogrammeComplet)), histogrammeComplet, color=['r']*256 + ['g']*256 + ['b']*256)
        
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.set_title("Histobine")
        ax2.bar(range(len(histobine)), histobine, color=['r']*(len(histobine)//3) + ['g']*(len(histobine)//3) + ['b']*(len(histobine)//3))
        
        return fig

class IndexDBCreator : 
    def __init__(self, datasetPath, toolbox, imagesSize=(256, 256), binsNombreParCanal = 8) :
        self.binsNombreParCanal = binsNombreParCanal
        self.datasetPath = datasetPath
        self.imagesSize = imagesSize
        self.toolbox = toolbox
        
    def getImagesSize(self) : 
        return self.imagesSize

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
                        histoComplet = self.toolbox.calculerHistogrammeComplet(image, self.imagesSize)
                        histoBin = self.toolbox.calculerHistobine(histoComplet, self.binsNombreParCanal)
                        indexDB[imagePath] = histoBin.tolist()

        self.saveIndexDBAsJson(indexDB)