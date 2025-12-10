#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv","r") as fichier:
    contenu = pd.read_csv(fichier)

# Mettre dans un commentaire le numéro de la question
# Question 1

data = pd.DataFrame(contenu)
print(data)

# Nombre de lignes
ligne = len(data)
print("Nb de lignes : {}".format(ligne))

# Nombre de colonnes
print("Nb de colonnes :", len(data.columns))

# Liste des noms des colonnes
nomdescolonnes = list(data.columns)

# Liste des types déclarés
type = ["str", "str", "int", "int", "int", "int", "int", "int", "str", "str", "str", "float",
        "str", "str", "str", "float", "str", "str", "str", "float", "str", "str", "str",
        "float", "str", "str", "str","float", "str", "str", "str","float", "str", "str", "str",
        "float", "str", "str", "str","float", "str", "str", "str","float", "str", "str", "str",
        "float", "str", "str", "str","float", "str", "str", "str","float", "str", "str", "str"]

# Liste pour stocker les sommes
liste_effectifs = []

# Boucle pour calculer sum() uniquement sur colonnes quantitatives
for i in range(len(nomdescolonnes)):
    col = nomdescolonnes[i]
    
    if type[i] == "str":
        liste_effectifs.append("non-quantitative")
    else:
        liste_effectifs.append(data[col].sum())

# Affichage final
print("Liste des effectifs (sommes) :")
print(liste_effectifs)

# Exemple pour la colonne Inscrits
colonne = data["Inscrits"]
print(colonne.sum())


# On récupère la liste des codes de département
departements = data["Code du département"].unique()


for dep in departements:
    #    Extraction des données du département
    df_dep = data[data["Code du département"] == dep]

    # Valeurs à représenter
    inscrits = df_dep["Inscrits"].sum()
    votants = df_dep["Votants"].sum()

    categories = ["Inscrits", "Votants"]
    valeurs = [inscrits, votants]

    # Création du graphique
    plt.figure(figsize=(6, 4))
    plt.bar(categories, valeurs, color=["royalblue", "darkorange"])
    plt.title(f"Inscrits / Votants - Département {dep}")
    plt.ylabel("Nombre de personnes")

    # Sauvegarde du fichier image
    filename = f"diagramme_{dep}.png"
    plt.savefig("./Diagrammes/{}".format(filename), dpi=150)
    plt.close()

    print(f"Image créée : {filename}")


# --- Liste des départements ---
departements = data["Code du département"].unique()

# --- Boucle pour créer un diagramme par département ---
for dep in departements:
  # Extraction des données du département
    df_dep = data[data["Code du département"] == dep]

    # Calcul des valeurs à représenter
    abstentions = df_dep["Abstentions"].sum()
    blancs = df_dep["Blancs"].sum() if "Blancs" in df_dep.columns else 0
    nuls = df_dep["Nuls"].sum() if "Nuls" in df_dep.columns else 0
    votants = df_dep["Votants"].sum()
    
    # Votes exprimés = votants - blancs - nuls
     exprimes = votants - blancs - nuls

    categories = ["Abstentions", "Blancs", "Nuls", "Exprimés"]
    valeurs = [abstentions, blancs, nuls, exprimes]

    # --- Création du graphique ---
    plt.figure(figsize=(6, 6))
    plt.pie(valeurs, labels=categories, autopct='%1.1f%%', colors=["lightgrey", "gold", "red", "green"])
    plt.title(f"Répartition des votes - Département {dep}")

    # --- Sauvegarde de l'image ---
    filename = f"diagramme_circulaire_{dep}.png"
    plt.savefig(f"./Diagrammes_circulaires/{filename}", dpi=150)
    plt.close()

   print(f"Image créée : {filename}")


# Récupération des valeurs de la colonne "Inscrits"
inscrits = data["Inscrits"]

# Création de l'histogramme
plt.figure(figsize=(10, 6))
plt.hist(inscrits, bins=20, color='skyblue', edgecolor='black')  # 20 classes par exemple
plt.title("Distribution des inscrits par département")
plt.xlabel("Nombre d'inscrits")
plt.ylabel("Nombre de départements")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Affichage du graphique
plt.show()
print(figure)