#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats

#C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement que pratiquement. D'autre, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les résultats ne sont pas conformes à la théorie probabiliste.
#Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
#Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

#Par convention, on place les fonctions locales au début du code après les bibliothèques.
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Théorie de l'échantillonnage (intervalles de fluctuation)
#L'échantillonnage se base sur la répétitivité.
print("Résultat sur le calcul d'un intervalle de fluctuation")

donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

#Théorie de l'estimation (intervalles de confiance)
#L'estimation se base sur l'effectif.
print("Résultat sur le calcul d'un intervalle de confiance")

#Théorie de la décision (tests d'hypothèse)
#La décision se base sur la notion de risques alpha et bêta.
#Comme à la séance précédente, l'ensemble des tests se trouve au lien : https://docs.scipy.org/doc/scipy/reference/stats.html
print("Théorie de la décision")

# Début des questions et manipulations de la séance 5
print("Résultat sur le calcul d'un intervalle de fluctuation")
donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

#PARTIE 1 : Théorie de l'échantillonnage
print("\n" + "-"*60)
print("Théorie de l'échantillonnage")
print("-"*60 + "\n")

#Calcul des moyennes par colonnes
moyennes = donnees.mean().round(0) 
print("\nMoyennes observées sur 100 échantillons :\n", moyennes)

#Calcul des fréquences observées dans échantillons
somme_moyennes = moyennes.sum()
frequences_echant = (moyennes / somme_moyennes).round(2)
print("\nFréquences observées dans les échantillons :\n", frequences_echant)

#Fréquences réelles pour la population mère
pop_totale = 2185
pop_pour, pop_contre, pop_sans = 852, 911, 422
frequences_reelles = pd.Series({
    "Pour": round(pop_pour / pop_totale, 2),
    "Contre": round(pop_contre / pop_totale, 2),
    "Sans opinion": round(pop_sans / pop_totale, 2)
})
print("\nFréquences réelles de la population mère :\n", frequences_reelles)

#Calcul intervalles de fluctuation 
zC = 1.96
n = len(donnees)

intervalle_fluctuation = {}

for cat, p_obs in frequences_echant.items():
    marge = zC * math.sqrt((p_obs * (1 - p_obs)) / n)
    borne_inf = round(p_obs - marge, 3)
    borne_sup = round(p_obs + marge, 3)
    intervalle_fluctuation[cat] = (borne_inf, borne_sup)

print("\nIntervalles de fluctuation à 95 % :\n")
for cat, (inf, sup) in intervalle_fluctuation.items():
    print(f"{cat} : [{inf}, {sup}]")

#Comparaison fréquences observée et réelles 
print("\nComparaison avec les valeurs réelles :\n")
for cat in frequences_reelles.index:
    fr_real = frequences_reelles[cat]
    inf, sup = intervalle_fluctuation[cat]
    if inf <= fr_real <= sup:
        conclusion = "La fréquence réelle est comprise dans l’intervalle"
    else:
        conclusion = "La fréquence réelle est en dehors de l’intervalle"
    print(f"{cat} : fréquence réelle = {fr_real} → {conclusion}")


#PARTIE 2 : Théorie de l'estimation 
print("\n" + "-"*60)
print("Théorie de l'estimation")
print("-"*60 + "\n")

#Sélection du premier échantillon
premier_ech = donnees.iloc[0]
ligne = list(premier_ech.astype(int))
colonnes = list(donnees.columns)
print("Premier échantillon (ligne 0) :")
for nom, val in zip(colonnes, ligne):
    print(f"{nom} : {val}")

#Calcul de la taille de l'échantillon et des fréquences 
n = sum(ligne)
print(f"\nEffectif total de l’échantillon : n = {n}")

frequences = {nom: round(val / n, 2) for nom, val in zip(colonnes, ligne)}
print("\nFréquences observées sur cet échantillon :")
for nom, freq in frequences.items():
    print(f"{nom} : {freq}")

#Calcul intervalle de confiance 
zC = 1.96
ic_95 = {}

for nom, val in zip(colonnes, ligne):
    p = val / n
    marge = zC * math.sqrt((p * (1 - p)) / n)
    borne_inf = max(0.0, round(p - marge, 3))
    borne_sup = min(1.0, round(p + marge, 3))
    ic_95[nom] = (borne_inf, borne_sup)

print("\nIntervalles de confiance à 95 % :")
for nom, (inf, sup) in ic_95.items():
    print(f"{nom} : [{inf}, {sup}]")

#Comparaison des fréquences réelles et des intervalles 
print("\nComparaison avec les fréquences réelles et les intervalles de fluctuation :\n")

for nom in colonnes:
    fr_real = frequences_reelles.get(nom, None)
    inf_ic, sup_ic = ic_95[nom]
    inf_fluct, sup_fluct = intervalle_fluctuation[nom]

    if inf_ic <= fr_real <= sup_ic:
        conclusion_ic = "fréquence réelle DANS l’IC"
    else:
        conclusion_ic = "fréquence réelle HORS de l’IC"

    if inf_fluct <= fr_real <= sup_fluct:
        conclusion_fluct = "fréquence réelle DANS l’intervalle de fluctuation"
    else:
        conclusion_fluct = "fréquence réelle HORS de l’intervalle de fluctuation"

    print(f"{nom} : réelle={fr_real} → {conclusion_ic} ; {conclusion_fluct}")

#Test sur plusieurs lignes pour valider le jugement 
print("\nAnalyse sur les 5 premiers échantillons (IC 95 %) :")

for i in range(min(5, len(donnees))):
    ligne_i = list(donnees.iloc[i].astype(int))
    n_i = sum(ligne_i)
    print(f"\nÉchantillon {i} — taille n = {n_i}")
    for nom, val in zip(colonnes, ligne_i):
        p_i = val / n_i
        marge_i = zC * math.sqrt((p_i * (1 - p_i)) / n_i)
        borne_inf_i = max(0.0, round(p_i - marge_i, 3))
        borne_sup_i = min(1.0, round(p_i + marge_i, 3))
        print(f"  {nom} : p = {round(p_i,3)} → IC95% [{borne_inf_i}, {borne_sup_i}]")


#PARTIE 3 : Théorie de la décision 
print("\n" + "-"*60)
print("THEORIE DE LA DECISION")
print("-"*60 + "\n")

import scipy.stats as stats

#Changement fichier CSV
fichiers = ["./data/Loi-normale-Test-1.csv", "./data/Loi-normale-Test-2.csv"]
donnees_tests = {}

for f in fichiers:
    try:
        df = pd.read_csv(f, header=None)
        valeurs = pd.to_numeric(df[0], errors='coerce').dropna().tolist()
        donnees_tests[f] = valeurs
        print(f"{f} chargé avec succès, {len(valeurs)} valeurs numériques.")
    except Exception as e:
        print(f"Erreur lors du chargement de {f} : {e}")

#Test de Shapiro-Wilks
print("\nRésultats du test de Shapiro-Wilk :")
for nom_fichier, valeurs in donnees_tests.items():
    stat, p_value = stats.shapiro(valeurs)
    print(f"\nFichier : {nom_fichier}")
    print(f"  Statistique W = {stat:.4f}")
    print(f"  p-value = {p_value:.4f}")
    
    if p_value > 0.05:
        print("Distribution NORMALE (hypothèse de normalité non rejetée)")
    else:
        print("Distribution NON NORMALE (hypothèse de normalité rejetée)")

#Interprétation 
print("\nInterprétation :")
print("- Si p-value > 0.05 : la distribution peut être considérée comme normale.")
print("- Si p-value ≤ 0.05 : la distribution ne suit pas la loi normale.")