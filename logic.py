import cv2
import numpy as np
import json
import os
from matplotlib.figure import Figure

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
        tailleHistobine = int(256 / binsNombreParCanal) * 3
        reshapedBins = histogrammeComplet.reshape((tailleHistobine, binsNombreParCanal))
        print("The reshaped new bins are : ", reshapedBins)
        histobine = reshapedBins.sum(axis=1)
        return histobine
    
    def generateHistogrammesPlot(self, histogrammeComplet, histobine, colorSpace) :
        fig = Figure(figsize=(3, 4), dpi=100)
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
        with open('indexDB.json', 'w') as jsonFile:
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