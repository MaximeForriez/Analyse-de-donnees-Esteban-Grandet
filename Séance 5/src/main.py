#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats

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

#----------------------------------------------------------------------------------------------------
print("Résultat sur le calcul d'un intervalle de fluctuation")
donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

#Etape 1.0 - Théorie de l'échantillonnage
print("\n" + "-"*60)
print("Partie 1 — Théorie de l'échantillonnage (intervalles de fluctuation)")
print("-"*60 + "\n")

#Etape 1.1 - Calcul des moyennes par colonnes
moyennes = donnees.mean().round(0) 
print("\nMoyennes observées sur 100 échantillons :\n", moyennes)

#Etape 1.2 - Calcul des fréquences observées dans échantillons
somme_moyennes = moyennes.sum()
frequences_echant = (moyennes / somme_moyennes).round(2)
print("\nFréquences observées dans les échantillons :\n", frequences_echant)

#Etape 1.3 - Fréquences réelle population mère
pop_totale = 2185
pop_pour, pop_contre, pop_sans = 852, 911, 422
frequences_reelles = pd.Series({
    "Pour": round(pop_pour / pop_totale, 2),
    "Contre": round(pop_contre / pop_totale, 2),
    "Sans opinion": round(pop_sans / pop_totale, 2)
})
print("\nFréquences réelles de la population mère :\n", frequences_reelles)

#Etape 1.4 - Calcul intervalles fluctuation 
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

#Etape 1.5 - Comparaison fréquences observée et réelles 
print("\nComparaison avec les valeurs réelles :\n")
for cat in frequences_reelles.index:
    fr_real = frequences_reelles[cat]
    inf, sup = intervalle_fluctuation[cat]
    if inf <= fr_real <= sup:
        conclusion = "La fréquence réelle est comprise dans l’intervalle"
    else:
        conclusion = "La fréquence réelle est en dehors de l’intervalle"
    print(f"{cat} : fréquence réelle = {fr_real} → {conclusion}")

#---------------------------------------------------------------------------------
#Etape 2.0 - Théorie de l'estimation 
print("\n" + "-"*60)
print("Partie 2 — Théorie de l'estimation (intervalles de confiance)")
print("-"*60 + "\n")

#Etape 2.1 - Sélection 1er échantillon
premier_ech = donnees.iloc[0]
ligne = list(premier_ech.astype(int))
colonnes = list(donnees.columns)
print("Premier échantillon (ligne 0) :")
for nom, val in zip(colonnes, ligne):
    print(f"{nom} : {val}")

#Etape 2.2 - Calcul taille échantillon et fréquences 
n = sum(ligne)
print(f"\nEffectif total de l’échantillon : n = {n}")

frequences = {nom: round(val / n, 2) for nom, val in zip(colonnes, ligne)}
print("\nFréquences observées sur cet échantillon :")
for nom, freq in frequences.items():
    print(f"{nom} : {freq}")

#Etape 2.3 - Calcul intervalle de confiance 
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

#Etape 2.4 - Comparaison fréquences réelles et intervalles 
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

#Etape 2.5 - Verification plusieurs lignes 
print("\nAnalyse rapide sur les 5 premiers échantillons (IC 95 %) :")

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


#----------------------------------------------------------------------------
#Etape 3.0 - Théorie de la décision 
print("\n" + "-"*60)
print("Partie 3 — Théorie de la décision (test de Shapiro-Wilk)")
print("-"*60 + "\n")

import scipy.stats as stats

#Etape 3.1 - changement fichier CSV
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

#Etape 3.2 - Test de Shapiro-Wilks
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

#Etape 3.3 - Interprétation 
print("\nInterprétation :")
print("Le test de Shapiro-Wilk vérifie si l'échantillon suit une loi normale.")
print("- Si p-value > 0.05 : la distribution peut être considérée comme normale.")
print("- Si p-value ≤ 0.05 : la distribution ne suit pas la loi normale.")
print("Ces résultats permettront de décider quel test statistique utiliser pour l’analyse ultérieure.\n")