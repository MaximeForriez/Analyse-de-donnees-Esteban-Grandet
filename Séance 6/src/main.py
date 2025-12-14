#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import math

#Fonction pour ouvrir les fichiers
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Fonction pour convertir les données en données logarithmiques
def conversionLog(liste):
    log = []
    for element in liste:
        log.append(math.log(element))
    return log

#Fonction pour trier par ordre décroissant les listes (îles et populations)
def ordreDecroissant(liste):
    liste.sort(reverse = True)
    return liste

#Fonction pour obtenir le classement des listes spécifiques aux populations
def ordrePopulation(pop, etat):
    ordrepop = []
    for element in range(0, len(pop)):
        if np.isnan(pop[element]) == False:
            ordrepop.append([float(pop[element]), etat[element]])
    ordrepop = ordreDecroissant(ordrepop)
    for element in range(0, len(ordrepop)):
        ordrepop[element] = [element + 1, ordrepop[element][1]]
    return ordrepop

#Fonction pour obtenir l'ordre défini entre deux classements (listes spécifiques aux populations)
def classementPays(ordre1, ordre2):
    classement = []
    if len(ordre1) <= len(ordre2):
        for element1 in range(0, len(ordre2) - 1):
            for element2 in range(0, len(ordre1) - 1):
                if ordre2[element1][1] == ordre1[element2][1]:
                    classement.append([ordre1[element2][0], ordre2[element1][0], ordre1[element2][1]])
    else:
        for element1 in range(0, len(ordre1) - 1):
            for element2 in range(0, len(ordre2) - 1):
                if ordre2[element2][1] == ordre1[element1][1]:
                    classement.append([ordre1[element1][0], ordre2[element2][0], ordre1[element][1]])
    return classement

#Partie sur les îles
iles = pd.DataFrame(ouvrirUnFichier("./data/island-index.csv"))

#Attention ! Il va falloir utiliser des fonctions natives de Python dans les fonctions locales que je vous propose pour faire l'exercice. Vous devez caster l'objet Pandas en list().



#Partie sur les populations des États du monde
#Source. Depuis 2007, tous les ans jusque 2025, M. Forriez a relevé l'intégralité du nombre d'habitants dans chaque États du monde proposé par un numéro hors-série du monde intitulé États du monde. Vous avez l'évolution de la population et de la densité par année.
monde = pd.DataFrame(ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv"))


print("\n" + "="*80)
print("                 Partie 1 — ANALYSE LOI RANG–TAILLE (ISLAND INDEX)")
print("="*80 + "\n")

#Etape 1.0 - Chargement du fichier island-index.csv
print("\n" + "-"*60)
print("Étape 1.0 — Importation du fichier island-index.csv")
print("-"*60)

iles = pd.DataFrame(ouvrirUnFichier("./data/island-index.csv"))
print("\nFichier chargé avec succès :")
print(iles.head())

#Etape 1.1 - Extraction colonne surfaces et ajout continents 
print("\n" + "-"*60)
print("Étape 1.1 — Extraction des surfaces des îles")
print("-"*60)

surfaces = list(iles["Surface (km²)"])
surfaces = [float(x) for x in surfaces]   # typage forcé en float

print("Nombre de surfaces initiales :", len(surfaces))

continents = [
    85545323,   # Asie / Afrique / Europe combinés
    37856841,   # Amérique
    7768030,    # Antarctique
    7605049     # Australie
]

surfaces.extend([float(v) for v in continents])

print("Nouveau nombre de surfaces :", len(surfaces))

#Etape 1.2 - Ordre décroissant 
print("\n" + "-"*60)
print("Étape 1.2 — Tri décroissant des surfaces")
print("-"*60)

surfaces_triees = ordreDecroissant(surfaces)
print("Extrait des surfaces triées (10 premières valeurs) :")
print(surfaces_triees[:10])

#Etape 1.3 - Visualisation loi rang-taille
print("\n" + "-"*60)
print("Étape 1.3 — Visualisation loi rang–taille")
print("-"*60)

rangs = list(range(1, len(surfaces_triees) + 1))

plt.figure(figsize=(8,5))
plt.plot(rangs, surfaces_triees)
plt.title("Loi rang–taille (échelle classique)")
plt.xlabel("Rang")
plt.ylabel("Surface (km²)")
plt.tight_layout()
plt.savefig("rang_taille_classique.png", dpi=200)
plt.close()

print("Image générée : rang_taille_classique.png")

#Etape 1.4 - Conversion logarithmique données
print("\n" + "-"*60)
print("Étape 1.4 — Conversion logarithmique des axes")
print("-"*60)

log_rangs = conversionLog(rangs)
log_surfaces = conversionLog(surfaces_triees)

plt.figure(figsize=(8,5))
plt.plot(log_rangs, log_surfaces)
plt.title("Loi rang–taille (axe logarithmique)")
plt.xlabel("log(rang)")
plt.ylabel("log(surface)")
plt.tight_layout()
plt.savefig("rang_taille_log.png", dpi=200)
plt.close()

print("Image générée : rang_taille_log.png")

#Etape 1.5 Test statistique possible ? 
# Non. Les rangs ne sont pas des variables aléatoires : ce sont des valeurs
# déterministes obtenues après un tri. Ils ne suivent donc pas une distribution
# probabiliste permettant d’appliquer un test statistique (normalité, KS, etc.)
# On ne peut tester que les valeurs (surfaces), jamais les rangs eux-mêmes.

print("\n" + "-"*60)
print("Fin de la partie 1 — Les images ont été générées et la conclusion est en commentaire.")
print("-"*60 + "\n")


print("\n" + "="*80)
print("                 Partie 2 — POPULATIONS DU MONDE (RANGS ET CORRÉLATIONS)")
print("="*80 + "\n")

# Étape 2.0 — Chargement du fichier populations
print("\n" + "-"*60)
print("Étape 2.0 — Importation du fichier Le-Monde-HS-Etats-du-monde-2007-2025.csv")
print("-"*60)

monde = pd.DataFrame(ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv"))
print("\nFichier chargé avec succès :")
print(monde.head())

#Etape 2.1 - Isolation colonnes pertinentes 
print("\n" + "-"*60)
print("Étape 2.1 — Colonnes à analyser : État, Pop 2007, Pop 2025, Densité 2007, Densité 2025")
print("-"*60)

colonnes_analyse = ["État", "Pop 2007", "Pop 2025", "Densité 2007", "Densité 2025"]
donnees = monde[colonnes_analyse]

etats = list(donnees["État"])
pop2007 = [float(x) for x in donnees["Pop 2007"]]
pop2025 = [float(x) for x in donnees["Pop 2025"]]
dens2007 = [float(x) for x in donnees["Densité 2007"]]
dens2025 = [float(x) for x in donnees["Densité 2025"]]

print(f"Nombre d'États : {len(etats)}")

#Etape 2.2 - Classement décroissant populations et densités 
print("\n" + "-"*60)
print("Étape 2.2 — Classement décroissant des populations et densités")
print("-"*60)

ordre_pop2007 = ordrePopulation(pop2007, etats)
ordre_pop2025 = ordrePopulation(pop2025, etats)
ordre_dens2007 = ordrePopulation(dens2007, etats)
ordre_dens2025 = ordrePopulation(dens2025, etats)

print("Extrait classement Pop 2007 (5 premiers) :", ordre_pop2007[:5])
print("Extrait classement Densité 2007 (5 premiers) :", ordre_dens2007[:5])

#Etape 2.3 - Préparation comparaison classement pays
print("\n" + "-"*60)
print("Étape 2.3 — Préparation de la comparaison des classements")
print("-"*60)

comparaison_pop_dens = classementPays(ordre_pop2007, ordre_dens2007)
comparaison_pop_dens.sort()  # tri par rapport au classement de 2007

#Etape 2.4 - Isolation deux colonnes pour corrélation 
print("\n" + "-"*60)
print("Étape 2.4 — Isolation des rangs Pop 2007 et Densité 2007")
print("-"*60)

rangs_pop = []
rangs_dens = []

for element in comparaison_pop_dens:
    rangs_pop.append(element[0])
    rangs_dens.append(element[1])

print("Extrait rangs Pop 2007 :", rangs_pop[:10])
print("Extrait rangs Densité 2007 :", rangs_dens[:10])

#Etape 2.5 - Calcul corrélations rang
print("\n" + "-"*60)
print("Étape 2.5 — Corrélation de rang (Spearman) et concordance (Kendall)")
print("-"*60)

from scipy.stats import spearmanr, kendalltau

spearman_coef, spearman_p = spearmanr(rangs_pop, rangs_dens)
kendall_coef, kendall_p = kendalltau(rangs_pop, rangs_dens)

print(f"Coefficient de corrélation de rang Spearman : {spearman_coef:.4f} (p-value = {spearman_p:.4f})")
print(f"Coefficient de concordance de rang Kendall : {kendall_coef:.4f} (p-value = {kendall_p:.4f})")

print("\n# Commentaire :")
print("# Ces coefficients indiquent le degré de similarité entre le classement par population et le classement par densité.")
print("# Valeurs proches de 1 => forte concordance ; proches de 0 => classement indépendant ; valeurs négatives => classement inverse.")


print("\n" + "="*80)
print("                                 BONUS — ANALYSE DES RANGS")
print("="*80 + "\n")

