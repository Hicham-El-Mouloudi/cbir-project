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
        # bouton pour créer la base d'indexation
        self.createIndexingDBButton = tk.Button(self.sectionContainer, text="Créer La Base d'Indexation", command=self.créerBaseIndexationAction)

        # configuring the layout
        self.sectionContainer.rowconfigure(0, weight=1)
        self.sectionContainer.columnconfigure(0, weight=0)
        self.sectionContainer.columnconfigure(1, weight=0)
        self.sectionContainer.columnconfigure(2, weight=0)
    
    def getSelectedBinsNumber(self) :
        return int(self.selectedBinsNumber.get())
    
    def setupUI(self) :
        self.binsNumberLabel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.binsNumberField.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.createIndexingDBButton.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

    def créerBaseIndexationAction(self) :
        # disabling the button to prevent multiple clicks
        self.createIndexingDBButton.config(state=tk.DISABLED)

        print("Creating indexing DB...\n")
        binsNombreParCanal = int(self.selectedBinsNumber.get())
        self.indexDBCreator.setBinsNombreParCanal(binsNombreParCanal)
        self.indexDBCreator.createIndexDB()
        print("Creating indexing DB Completed successfully !\n")

        # re-enabling the button
        self.createIndexingDBButton.config(state=tk.NORMAL)
        # Afficher une popup avec un message de confirmation
        messagebox.showinfo("Succès", "La base d'indexation a été créée avec succès.")

class SectionRechercheUI : 
    def __init__(self, sectionContainer, indexDBCreator , sectionIndexationUI , toolbox) :
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
        # button de recherche
        self.rechercherButton = tk.Button(self.sectionContainer, text="Rechercher", command=self.rechercherAction)
        # labeled frame pour histogramme complet et histobine de l'image choisie
        self.lesHistogrammesFrame = tk.LabelFrame(self.sectionContainer, text="Histogrammes de l'image choisie")
        # labeled frame pour les resultats de la recherche
        self.résultatsRechercheFrame = tk.LabelFrame(self.sectionContainer, text="Résultats de la recherche")
        self.resultatsPlaceholderLabel = tk.Label(self.résultatsRechercheFrame, text="(Résultats de la recherche apparaîtront ici)")
        self.resultatsPlaceholderLabel.pack(padx=5, pady=5)
        # 
        self.selectedImagePath = None
        self.selectedImage = None

        # configuring the layout
        self.sectionContainer.rowconfigure(0, weight=0)
        self.sectionContainer.rowconfigure(1, weight=0)
        self.sectionContainer.rowconfigure(2, weight=0)
        self.sectionContainer.rowconfigure(3, weight=1)
        self.sectionContainer.rowconfigure(4, weight=2)
        self.sectionContainer.columnconfigure(0, weight=1)
        self.sectionContainer.columnconfigure(1, weight=1)
    
    def setupUI(self) :
        self.imageChooserLabel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.imageChooserButton.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.similariteAlgoLabel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.similariteAlgoField.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.rechercherButton.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        # 
        self.lesHistogrammesFrame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.résultatsRechercheFrame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    def choisirImageAction(self) :
        print("Choisir une image action triggered.")
        try:
            filepath = filedialog.askopenfilename(
                title="Choisir une image",
                filetypes=[("Images", ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif")), ("Tous les fichiers", "*.*")]
            )
            if not filepath:
                return
            self.selectedImagePath = filepath
            self.selectedImage = cv2.imread(self.selectedImagePath)
            print("Image sélectionnée :", filepath)
            
            # Generer et afficher les histogrammes de l'image choisie
            if self.selectedImage is not None:
                resizedImage = self.toolbox.redimensionnerImage(self.selectedImage, (256, 256))
                histogrammeComplet = self.toolbox.calculerHistogrammeComplet(resizedImage, self.indexDBCreator.getImagesSize())
                histobine = self.toolbox.calculerHistobine(histogrammeComplet, self.sectionIndexationUI.getSelectedBinsNumber())
                print("Breakpoint : Etape pass avec succès.")
                fig = self.toolbox.generateHistogrammesPlot(histogrammeComplet, histobine, self.sectionIndexationUI.getSelectedBinsNumber())

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
        messagebox.showinfo("Recherche", "Fonction de recherche non encore implémentée.")

class MainUI : 
    def __init__(self, indexDBCreator, toolbox) :
        self.rootTK = tk.Tk()
        self.rootTK.title("Système CBIR")
        self.rootTK.geometry("400x300")
        #
        self.scrollableArea = tk.Canvas(self.rootTK)
        self.scrollableArea.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self.rootTK, orient="vertical", command=self.scrollableArea.yview)
        scrollbar.pack(side="right", fill="y")
        self.scrollableArea.configure(yscrollcommand=scrollbar.set)
        # 
        self.root = tk.Frame(self.scrollableArea)
        self.root.bind('<Configure>', lambda e: self.scrollableArea.configure(scrollregion=self.scrollableArea.bbox("all")))
        self.scrollableArea.create_window((0,0), window=self.root, anchor="nw")
        # Les sections majeur
        self.sectionIndexation = tk.LabelFrame(self.root, text="Sous-systeme d'indexation")
        self.sectionRecherche = tk.LabelFrame(self.root, text="Sous-systeme de recherche d’Images par le Contenu")
        # Les sous-sections UI
        self.sectionIndexationUI = SectionIndexationUI(self.sectionIndexation, indexDBCreator)
        self.sectionRechercheUI = SectionRechercheUI(self.sectionRecherche, indexDBCreator, self.sectionIndexationUI, toolbox)

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