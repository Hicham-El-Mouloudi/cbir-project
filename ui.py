import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2

class SectionIndexationUI : 
    def __init__(self, sectionContainer, indexDBCreator) : 
        # reference a l'instance de la classe IndexDBCreator
        self.indexDBCreator = indexDBCreator

        # container de la section
        self.sectionContainer = sectionContainer
        # label pour le nombre de bins
        self.binsNumberLabel = tk.Label(self.sectionContainer, text="Nombre De Bins Par Canal :")
        # menu d'options pour le nombre de bins
        self.selectedBinsNumber = tk.StringVar()
        self.selectedBinsNumber.set("16")  # valeur par defaut
        selectionOptions = ["8", "16", "32", "64", "128", "256"]
        self.binsNumberField = tk.OptionMenu(self.sectionContainer, self.selectedBinsNumber, *selectionOptions)
        # label pour l'espace de couleur
        self.colorSpaceLabel = tk.Label(self.sectionContainer, text="Espace Couleur :")
        # menu d'options pour l'espace de couleur
        self.selectedColorSpace = tk.StringVar()
        ColorSpaceSelectionOptions = ["RGB", "HSV", "Lab"]
        self.selectedColorSpace.set(ColorSpaceSelectionOptions[0])  # valeur par defaut
        self.colorSpaceField = tk.OptionMenu(self.sectionContainer, self.selectedColorSpace, *ColorSpaceSelectionOptions)
        # bouton pour créer la base d'indexation
        self.createIndexingDBButton = tk.Button(self.sectionContainer, text="Créer La Base d'Indexation", command=self.créerBaseIndexationAction)

        # configuring the layout
        self.sectionContainer.rowconfigure(0, weight=1)
        self.sectionContainer.columnconfigure(0, weight=0)
        self.sectionContainer.columnconfigure(1, weight=0)
        self.sectionContainer.columnconfigure(2, weight=0)
        self.sectionContainer.columnconfigure(3, weight=0)
    
    def getSelectedColorSpace(self) :
        return self.selectedColorSpace.get()

    def getSelectedBinsNumber(self) :
        return int(self.selectedBinsNumber.get())
    
    def setupUI(self) :
        self.binsNumberLabel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.binsNumberField.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.colorSpaceLabel.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.colorSpaceField.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        self.createIndexingDBButton.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

    def créerBaseIndexationAction(self) :
        # disabling the button to prevent multiple clicks
        self.createIndexingDBButton.config(state=tk.DISABLED)

        print("Creating indexing DB...\n")
        binsNombreParCanal = self.getSelectedBinsNumber()
        colorSpace = self.getSelectedColorSpace()
        self.indexDBCreator.setBinsNombreParCanal(binsNombreParCanal)
        self.indexDBCreator.createIndexDB(colorSpace)
        print("Creating indexing DB Completed successfully !\n")

        # re-enabling the button
        self.createIndexingDBButton.config(state=tk.NORMAL)
        # Afficher une popup avec un message de confirmation
        messagebox.showinfo("Succès", "La base d'indexation a été créée avec succès.")

class SectionRechercheUI : 
    def __init__(self, imageSearcher, sectionContainer, indexDBCreator , sectionIndexationUI , toolbox) :
        self.imageSearcher = imageSearcher
        self.indexDBCreator = indexDBCreator
        self.toolbox = toolbox
        self.sectionIndexationUI = sectionIndexationUI # pour obtenir le nombre de bins par canal

        # container de la section
        self.sectionContainer = sectionContainer
        # image chooser
        self.imageChooserLabel = tk.Label(self.sectionContainer, text="Choisir une image :")
        self.imageChooserButton = tk.Button(self.sectionContainer, text="Parcourir...", command=self.choisirImageAction)
        # choix algo de similarité (distance)
        self.similariteAlgoLabel = tk.Label(self.sectionContainer, text="Type De Distance :")
        selectionOptions = ["Distance de Swain&Ballard", "Distance Euclidienne", "Distance Chi-Carré", "Corrélation"]
        self.selectedSimilariteAlgo = tk.StringVar()
        self.selectedSimilariteAlgo.set(selectionOptions[0])  # valeur par defaut
        self.similariteAlgoField = tk.OptionMenu(self.sectionContainer, self.selectedSimilariteAlgo, *selectionOptions)
        # nombre de résultats à afficher
        self.resultCountLabel = tk.Label(self.sectionContainer, text="Nombre de résultats à afficher :")
        self.resultCountField = tk.Entry(self.sectionContainer)
        # button de recherche
        self.rechercherButton = tk.Button(self.sectionContainer, text="Rechercher", command=self.rechercherAction)
        # labeled frame pour histogramme complet et histobine de l'image choisie
        self.lesHistogrammesFrame = tk.LabelFrame(self.sectionContainer, text="Histogrammes de l'image choisie")
        self.histogramsPlaceholderLabel = tk.Label(self.lesHistogrammesFrame, text="Aucune image choisie")
        self.histogramsPlaceholderLabel.pack(padx=5, pady=5)
        # labeled frame pour les resultats de la recherche
        self.resultatsRechercheFrame = tk.LabelFrame(self.sectionContainer, text="Résultats de la recherche")
        self.resultatsPlaceholderLabel = tk.Label(self.resultatsRechercheFrame, text="Résultats de la recherche apparaîtront ici")
        self.resultatsPlaceholderLabel.pack(padx=5, pady=5)
        # 
        self.selectedImagePath = None
        self.selectedImage = None

        # configuring the layout
        self.sectionContainer.rowconfigure(0, weight=0)
        self.sectionContainer.rowconfigure(1, weight=0)
        self.sectionContainer.rowconfigure(2, weight=0)
        self.sectionContainer.rowconfigure(3, weight=0)
        self.sectionContainer.rowconfigure(4, weight=1)
        self.sectionContainer.rowconfigure(5, weight=2)
        self.sectionContainer.columnconfigure(0, weight=1)
        self.sectionContainer.columnconfigure(1, weight=1)
    
    def getResultsCount(self) :
        try :
            count = int(self.resultCountField.get())
        except ValueError :
            count = 5 # valeur par defaut
        return count
    
    def getSimilariteAlgo(self) :
        return self.selectedSimilariteAlgo.get()
    
    def setupUI(self) :
        self.imageChooserLabel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.imageChooserButton.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.similariteAlgoLabel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.similariteAlgoField.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.resultCountLabel.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.resultCountField.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self.rechercherButton.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        # 
        self.lesHistogrammesFrame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.resultatsRechercheFrame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    def choisirImageAction(self) :
        selectedColorSpace = self.sectionIndexationUI.getSelectedColorSpace()
        selectedBinsNumber = self.sectionIndexationUI.getSelectedBinsNumber()
        # 
        print("Choisir une image action triggered.")
        try:
            filepath = filedialog.askopenfilename(
                title="Choisir une image",
                filetypes=[("Images", ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif")), ("Tous les fichiers", "*.*")]
            )
            if not filepath:
                return
            self.selectedImagePath = filepath
            self.selectedImage = self.toolbox.readImage(filepath, selectedColorSpace)
            print("Image sélectionnée :", filepath)
            
            # Generer et afficher les histogrammes de l'image choisie
            if self.selectedImage is not None:
                resizedImage = self.toolbox.redimensionnerImage(self.selectedImage, (256, 256))
                histogrammeComplet = self.toolbox.calculerHistogrammeComplet(resizedImage, self.indexDBCreator.getImagesSize())
                histobine = self.toolbox.calculerHistobine(histogrammeComplet, selectedBinsNumber)
                fig = self.toolbox.generateHistogrammesPlot(histogrammeComplet, histobine, selectedColorSpace)
                print("Breakpoint : Etape pass avec succès.")

                # vider le frame avant d'ajouter le nouveau plot
                for widget in self.lesHistogrammesFrame.winfo_children():
                    widget.destroy()

                canvas = FigureCanvasTkAgg(fig, master=self.lesHistogrammesFrame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de choisir l'image :\n{e}")
    

    def rechercherAction(self) :
        print("Rechercher action triggered.")
        # disabling the button to prevent multiple clicks
        self.rechercherButton.config(state=tk.DISABLED)

        # vérifier si une image est choisie
        if self.selectedImagePath is None or self.selectedImage is None:
            messagebox.showwarning("Avertissement", "Veuillez choisir une image avant de rechercher.")
            self.rechercherButton.config(state=tk.NORMAL)
            return
        # preparer la recherche et la valider
        try:
            # collecter les parametres necessaires
            selectedColorSpace = self.sectionIndexationUI.getSelectedColorSpace()
            selectedBinsNumber = self.sectionIndexationUI.getSelectedBinsNumber()
            imagesSize = self.indexDBCreator.getImagesSize()
            nombreDeResultatsDemande = self.getResultsCount()
            typeDeDistance = self.getSimilariteAlgo()

            # charger l'indexDB et preparer le descripteur de l'image query
            indexDB, histobineQueryImage = self.imageSearcher.preparerRechercheImagesSimilaires(self.selectedImage, selectedColorSpace, imagesSize, selectedBinsNumber)
            # effectuer la recherche avec la distance choisie
            resultas = None
            if typeDeDistance == "Distance de Swain&Ballard":
                resultas = self.imageSearcher.rechercherDBAvecDistanceSwainBallard(indexDB, histobineQueryImage,imagesSize=imagesSize, topK=nombreDeResultatsDemande)
            elif typeDeDistance == "Distance Euclidienne":
                resultas = self.imageSearcher.rechercherDBAvecDistanceEuclidienne(indexDB, histobineQueryImage, imagesSize=imagesSize, topK=nombreDeResultatsDemande)
            elif typeDeDistance == "Distance Chi-Carré":
                resultas = self.imageSearcher.rechercherDBAvecDistanceChiCarre(indexDB, histobineQueryImage, imagesSize=imagesSize, topK=nombreDeResultatsDemande)
            elif typeDeDistance == "Corrélation":
                resultas = self.imageSearcher.rechercherDBAvecCorrelation(indexDB, histobineQueryImage, imagesSize=imagesSize, topK=nombreDeResultatsDemande)
            else:
                raise Exception(f"L'algorithme de similarité '{typeDeDistance}' n'est pas encore implémenté.")
            lesPlotsDesResultas = self.toolbox.generateSearchResultsPlot(resultas, imagesSize)
            self.afficherResultatsRecherche(lesPlotsDesResultas)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la préparation de la recherche :\n{e}")
            self.rechercherButton.config(state=tk.NORMAL)
            return
        
        # re-enabling the button
        self.rechercherButton.config(state=tk.NORMAL)
    
    # afficher les résultats de recherche
    def afficherResultatsRecherche(self, figurePlot) :
        # vider le frame avant d'ajouter les nouveaux résultats
        for widget in self.resultatsRechercheFrame.winfo_children():
            widget.destroy()
        # afficher les résultats
        canvas = FigureCanvasTkAgg(figurePlot, master=self.resultatsRechercheFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

class MainUI : 
    def __init__(self, imageSearcher, indexDBCreator, toolbox) :
        self.rootTK = tk.Tk()
        self.rootTK.title("Système CBIR")
        self.rootTK.geometry("700x700")
        #
        self.scrollableArea = tk.Canvas(self.rootTK)
        self.scrollableArea.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self.rootTK, orient="vertical", command=self.scrollableArea.yview)
        scrollbar.pack(side="right", fill="y")
        self.scrollableArea.configure(yscrollcommand=scrollbar.set)
        # 
        self.root = tk.Frame(self.scrollableArea)
        self.root.bind('<Configure>', lambda e: self.scrollableArea.configure(scrollregion=self.scrollableArea.bbox("all")))
        self.frame_id = self.scrollableArea.create_window((0,0), window=self.root, anchor="nw")
        self.scrollableArea.bind('<Configure>', self.on_canvas_resize)
        # Les sections majeur
        self.sectionIndexation = tk.LabelFrame(self.root, text="Sous-systeme d'indexation")
        self.sectionRecherche = tk.LabelFrame(self.root, text="Sous-systeme de recherche d’Images par le Contenu")
        # Les sous-sections UI
        self.sectionIndexationUI = SectionIndexationUI(self.sectionIndexation, indexDBCreator)
        self.sectionRechercheUI = SectionRechercheUI(imageSearcher, self.sectionRecherche, indexDBCreator, self.sectionIndexationUI, toolbox)
    def on_canvas_resize(self, event):
        canvas_width = event.width
        self.scrollableArea.itemconfig(self.frame_id, width=canvas_width)

    def setupUI(self) : 
        #--------------------------------- Setup ui principale
        self.sectionIndexation.pack(fill="x", padx=10, pady=5)
        self.sectionRecherche.pack(fill="x", expand=True, padx=10, pady=5)
        # ------------------------------------------------------

        # ---------------- Setup des compsants ui pour "Sous-systeme d'indexation"
        self.sectionIndexationUI.setupUI()
        # -------------------------------------------------------------------------
        # -------- Setup des compsants ui pour "Sous-systeme de recherche d’Images par le Contenu"
        self.sectionRechercheUI.setupUI()
        # ----------------------------------------------------------------------------------------
    
    def startUI(self) : 
        self.rootTK.mainloop()