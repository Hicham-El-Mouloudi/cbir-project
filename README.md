# Mini Projet — CBIR : Indexation et Recherche d'Images par le Contenu

## Description

Ce projet met en œuvre un système de **Recherche d’Images par le Contenu (CBIR)**.  
Il permet d’**indexer une base de données d’images** (Corel-1000) en extrayant des **descripteurs visuels** (histogrammes de couleur), puis de **rechercher des images similaires** à une image « requête » fournie par l’utilisateur.

L’application est développée en **Python** avec une interface graphique basée sur **Tkinter**.

---

## Fonctionnalités

L’application est composée de **deux sous-systèmes principaux** :

### 1. Sous-système d’indexation (hors ligne)

- **Création d’une base d’index** (`indexDB.json`) à partir d’un dossier `dataset/`.
- **Extraction des descripteurs** basés sur les **histogrammes de couleur**.
- **Paramètres configurables** :
  - **Espace de couleur** : `RGB`, `HSV`, ou `Lab`
  - **Nombre de bins (histobine)** : 8, 16, 32, 64, 128, 256  
    (pour ajuster la précision et la taille de l’index)

### 2. Sous-système de recherche (en ligne)

- **Chargement d’une image requête** depuis le disque.
- **Affichage des histogrammes** complets et réduits (histobine).
- **Calcul de similarité** entre l’image requête et la base indexée.
- **Choix de la mesure de distance** :
  -  Swain & Ballard (intersection d’histogramme)  
  -  Distance Euclidienne  
  -  Distance du Chi² (Chi-Carré)  
  -  Corrélation
- **Configuration du nombre de résultats** à afficher.
- **Affichage des images les plus similaires** trouvées dans la base.

---

## Installation et Lancement

### 1. Prérequis

- Python **3.x**
- La base de données d’images **Corel-1000**

### 2. Installation

1. **Clonez** ce dépôt ou **téléchargez** les fichiers :
   ```bash
   git clone <votre-lien-depot>
   cd CBIR
   ```
2. **Installez les dépendances nécessaires** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Téléchargez la base Corel-1000**.
4. **Créez un dossier** nommé `dataset` à la racine du projet et **ajoutez-y les images**.

### 3. Lancement

Exécutez simplement le script principal :
```bash
python main.py
```

---

## Guide d’Utilisation

### Phase 1 — Indexation

1. Lancez l’application :
   ```bash
   python main.py
   ```
2. Dans la section **« Sous-système d’indexation »** :
   - Choisissez le **nombre de bins** (ex. : 16)
   - Choisissez l’**espace couleur** (ex. : RGB)
   - Cliquez sur **« Créer la base d’indexation »**
3. Attendez le message de confirmation :  
   - Le fichier `indexDB.json` sera créé.

---

### 🔎 Phase 2 — Recherche

1. Dans la section **« Sous-système de recherche »** :
   - Cliquez sur **« Parcourir… »** pour choisir votre image requête.
   - Les **histogrammes** de l’image s’afficheront.
2. Sélectionnez :
   - Le **type de distance** (ex. : Swain & Ballard)
   - Le **nombre de résultats** à afficher
3. Cliquez sur **« Rechercher »**.
4. Les **résultats les plus similaires** apparaissent dans la section **« Résultats de la recherche »**.

> ⚠️ **Note importante** :  
> Les paramètres **(Bins, Espace Couleur)** utilisés lors de la recherche **doivent correspondre** à ceux utilisés pour la création de la base d’indexation.  
> L’application vérifie cette cohérence avant de lancer la recherche.

---

## Technologies Utilisées

| Technologie | Rôle |
|--------------|------|
| **Python 3** | Langage principal |
| **Tkinter** | Interface graphique (GUI) |
| **OpenCV-Python (cv2)** | Lecture, redimensionnement et conversion d’espaces de couleur |
| **NumPy** | Calculs d’histogrammes et opérations mathématiques |
| **Matplotlib** | Affichage des histogrammes et images de résultats |

---
