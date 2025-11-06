import tkinter as tk

class MainUI : 
    def __init__(self) :
        self.root = tk.Tk()
        self.root.title("Système CBIR")
        self.root.geometry("400x300")
        # Les sections majeur
        self.sectionIndexation = tk.LabelFrame(self.root, text="Sous-systeme d'indexation")
        self.sectionRecherche = tk.LabelFrame(self.root, text="Sous-systeme de recherche d’Images par le Contenu")

    def setupUI(self) : 
        #--------------------------------- Setup ui principale
        self.sectionIndexation.pack(fill="x", padx=10, pady=5)
        self.sectionRecherche.pack(fill="both", expand=True, padx=10, pady=5)
        label_offline = tk.Label(self.sectionIndexation, text="Contenu hors ligne ici")
        label_offline.pack(pady=20, padx=20)
        label_online = tk.Label(self.sectionRecherche, text="Contenu en ligne ici")
        label_online.pack(pady=20, padx=20)
        # ------------------------------------------------------

        # ---------------- Setup des compsants ui pour "Sous-systeme d'indexation"
        # -------------------------------------------------------------------------
        # -------- Setup des compsants ui pour "Sous-systeme de recherche d’Images par le Contenu"
        # ----------------------------------------------------------------------------------------
    
    def startUI(self) : 
        self.root.mainloop()