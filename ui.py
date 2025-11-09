import tkinter as tk
from tkinter import messagebox

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

class MainUI : 
    def __init__(self, indexDBCreator) :
        self.root = tk.Tk()
        self.root.title("Système CBIR")
        self.root.geometry("400x300")
        # Les sections majeur
        self.sectionIndexation = tk.LabelFrame(self.root, text="Sous-systeme d'indexation")
        self.sectionRecherche = tk.LabelFrame(self.root, text="Sous-systeme de recherche d’Images par le Contenu")
        # Les sous-sections UI
        self.sectionIndexationUI = SectionIndexationUI(self.sectionIndexation, indexDBCreator)

    def setupUI(self) : 
        #--------------------------------- Setup ui principale
        self.sectionIndexation.pack(fill="x", padx=10, pady=5)
        self.sectionRecherche.pack(fill="both", expand=True, padx=10, pady=5)
        label_online = tk.Label(self.sectionRecherche, text="Contenu en ligne ici")
        label_online.pack(pady=20, padx=20)
        # ------------------------------------------------------

        # ---------------- Setup des compsants ui pour "Sous-systeme d'indexation"
        self.sectionIndexationUI.setupUI()
        # -------------------------------------------------------------------------
        # -------- Setup des compsants ui pour "Sous-systeme de recherche d’Images par le Contenu"
        # ----------------------------------------------------------------------------------------
    
    def startUI(self) : 
        self.root.mainloop()