#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv","r") as fichier :
    contenu = pd.read_csv(fichier)

# Sources des données : production de M. Forriez, 2016-2023

data = pd.DataFrame(contenu)
print(data)

# liste des noms des colonnes
nomdescolonnes = list(data.columns)
print(list(data.columns))

# Liste des types déclarés
type = ["str", "str", "int", "int", "int", "int", "int", "int", "str", "str", "str", "float",
        "str", "str", "str", "float", "str", "str", "str", "float", "str", "str", "str",
        "float", "str", "str", "str","float", "str", "str", "str","float", "str", "str", "str",
        "float", "str", "str", "str","float", "str", "str", "str","float", "str", "str", "str",
        "float", "str", "str", "str","float", "str", "str", "str","float", "str", "str", "str"]

# Sélection des colonnes quantitatives
colonnes_quanti = data.select_dtypes(include=['number'])

# Calcul des moyennes pour chaque colonne
moyennes = colonnes_quanti.mean().tolist()

print("Colonnes quantitatives :")
print(list(colonnes_quanti.columns))

print("\nMoyennes des colonnes :")
print(moyennes)

# Sélection des colonnes quantitatives
colonnes_quanti = data.select_dtypes(include=['number'])

# Calcul des médianes pour chaque colonne
medianes = colonnes_quanti.median().tolist()

print("Médianes des colonnes quantitatives :")
print(medianes)

# Sélection des colonnes quantitatives
colonnes_quanti = data.select_dtypes(include=['number'])

# Calcul des modes pour chaque colonne
modes = colonnes_quanti.mode().iloc[0].tolist()

print("Modes des colonnes quantitatives :")
print(modes)

# Sélection des colonnes quantitatives
colonnes_quanti = data.select_dtypes(include=['number'])

# Calcul de l'écart type pour chaque colonne
ecarts_type = colonnes_quanti.std().tolist()

print("Écart type des colonnes quantitatives :")
print(ecarts_type)

# Sélection des colonnes quantitatives
colonnes_quanti = data.select_dtypes(include=['number'])

# Calcul de l'écart absolu à la moyenne
ecart_abs_moyenne = (colonnes_quanti - colonnes_quanti.mean()).abs().mean().tolist()

print("Écart absolu moyen à la moyenne des colonnes quantitatives :")
print(ecart_abs_moyenne)

# Sélection des colonnes quantitatives
colonnes_quanti = data.select_dtypes(include=['number'])

# Calcul de l'étendue pour chaque colonne
etendue = (colonnes_quanti.max() - colonnes_quanti.min()).tolist()

print("Étendue des colonnes quantitatives :")
print(etendue)

# Affichage des paramètres dans le terminal en format tableau
stats = pd.DataFrame({
    'Moyenne': moyennes,
    'Médiane': medianes,
    'Mode': modes,
    'Écart_type': ecarts_type,
    'Écart_abs_moyenne': ecart_abs_moyenne,
    'Étendue': etendue
})

# Arrondi à 2 décimales
stats_arrondi = stats.round(2)

print(stats_arrondi)

# Sélection des colonnes quantitatives
colonnes_quanti = data.select_dtypes(include=['number'])

# Distance interquartile : Q3 - Q1
diq = (colonnes_quanti.quantile(0.75) - colonnes_quanti.quantile(0.25)).round(2).tolist()

# Distance interdécile : D9 - D1
did = (colonnes_quanti.quantile(0.9) - colonnes_quanti.quantile(0.1)).round(2).tolist()

# Affichage
print("Distance interquartile (Q3-Q1) :")
print(diq)

print("\nDistance interdécile (D9-D1) :")
print(did)


# Sélection des colonnes quantitatives
colonnes_quanti = data.select_dtypes(include=['number'])

# Boucle pour créer un boxplot pour chaque colonne
def pourPasser():
    for col in colonnes_quanti.columns:
            plt.figure(figsize=(6, 4))
            plt.boxplot(colonnes_quanti[col].dropna())  # On ignore les NaN
            plt.title(f'Boxplot de {col}')
            plt.ylabel(col)
            
            # Sauvegarde du graphique dans le dossier "boites_à_moustaches"
            plt.savefig("./boites_à_moustaches/{}.png".format(col), bbox_inches='tight')
            plt.close()  # Ferme la figure pour ne pas afficher toutes les figures à l'écran
        
        # print("Boxplots enregistrés dans le dossier 'boites_à_moustaches'.")

# pour ouvrir le second fichier Island 
with open("./data/island-index.csv","r") as fichier :
    contenu = pd.read_csv(fichier)

iles = pd.DataFrame(contenu)
print(iles)

# Sélection de la colonne Surface
surface = iles["Surface (km²)"]

# Catégorisation des îles par une liste
categories = ["0-10km²", "10-25km²", "25-50km²", "50-100km²", "100-2500km²", "2500-5000km²", "5000-10000km²", "=>10000km²"]

# creation d'une nouvelle colonne "Catégorie_surface"
def categoriser_surface(x):
    if 0 < x <= 10:
        return categories[0]
    elif 10 < x <= 25:
        return categories[1]
    elif 25 < x <= 50:
        return categories[2]
    elif 50 < x <= 100: 
        return categories[3]
    elif 100 < x <= 2500:
        return categories[4]
    elif 2500 < x <= 5000:
        return categories[5]
    elif 5000 < x < 10000:
        return categories[6]
    else:
        return categories[7]

# création d'une liste vide pour la remplir ensuite avec une boucle 
testcategorie = []
for element in surface:
    testcategorie.append(categoriser_surface(element))

print(testcategorie)

# Comptage du nombre d'îles par catégorie
compte = []
for element in categories:
    compte.append([element, testcategorie.count(element)])

print("Nombre d'îles par catégorie de surface :")
print(compte)