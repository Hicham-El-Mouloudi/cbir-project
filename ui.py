import tkinter as tk

class SectionIndexationUI : 
    def __init__(self, sectionContainer) : 
        self.sectionContainer = sectionContainer
        self.binsNumberField = tk.Entry(self.sectionContainer)
        self.createIndexingDBButton = tk.Button(self.sectionContainer, text="Créer La Base d'Indexation", command=self.créerBaseIndexationAction)
        # configuring the layout
        self.sectionContainer.rowconfigure(0, weight=1)
        self.sectionContainer.columnconfigure(0, weight=1)
        self.sectionContainer.columnconfigure(1, weight=0)
    
    def setupUI(self) :
        self.binsNumberField.insert(0, "Entrez le nombre de bins par canal.")
        self.binsNumberField.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.createIndexingDBButton.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    def créerBaseIndexationAction(self) :
        print("Creating indexing DB...\n")

class MainUI : 
    def __init__(self) :
        self.root = tk.Tk()
        self.root.title("Système CBIR")
        self.root.geometry("400x300")
        # Les sections majeur
        self.sectionIndexation = tk.LabelFrame(self.root, text="Sous-systeme d'indexation")
        self.sectionRecherche = tk.LabelFrame(self.root, text="Sous-systeme de recherche d’Images par le Contenu")
        # Les sous-sections UI
        self.sectionIndexationUI = SectionIndexationUI(self.sectionIndexation)

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