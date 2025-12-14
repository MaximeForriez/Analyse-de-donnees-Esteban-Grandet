import pandas as pd
import matplotlib.pyplot as plt
import os

with open("data/resultats-elections-presidentielles-2022-1er-tour.csv", "r", encoding="utf-8") as fichier:
	contenu = pd.read_csv(fichier, sep=",")

# 5. Affichage du DataFrame
print("\n===== Contenu du fichier =====")
print(contenu)

# 6. Nombre de lignes et colonnes
nb_lignes = len(contenu)
nb_colonnes = len(contenu.columns)

print("\n===== Dimensions =====")
print("Nombre de lignes :", nb_lignes)
print("Nombre de colonnes :", nb_colonnes)


# 7. Nature statistique des variables
print("\n===== Types des colonnes =====")
types = {col: str(contenu[col].dtype) for col in contenu.columns}
for col, t in types.items():
    print(f"{col} : {t}")

# 8. Afficher noms des colonnes avec head()
print("\n===== Noms des colonnes =====")
print(contenu.head(1))

# 9. Sélection du nombre des inscrits
print("\n===== Colonne Inscrits =====")
print(contenu["Inscrits"])

# 10. Somme des colonnes quantitatives uniquement
print("\n===== Sommes des colonnes quantitatives =====")
somme_quantitatives = []

for col in contenu.columns:
    if contenu[col].dtype in ("int64", "float64"):
        somme_quantitatives.append((col, contenu[col].sum()))

for nom, valeur in somme_quantitatives:
    print(f"{nom} : {valeur}")

# 11. Diagrammes en barres (Inscrits / Votants)
os.makedirs("images/barres", exist_ok=True)

print("\n===== Génération des diagrammes en barres =====")

for i in range(len(contenu)):
    dept = contenu.iloc[i]["Libellé du département"]

    plt.figure()
    plt.bar(["Inscrits", "Votants"], [
        contenu.iloc[i]["Inscrits"],
        contenu.iloc[i]["Votants"]
    ])
    plt.title(f"Inscrits / Votants — {dept}")
    plt.xlabel("Catégorie")
    plt.ylabel("Nombre")
    plt.tight_layout()
    plt.savefig(f"images/barres/{dept}.png")
    plt.close()

print("→ Diagrammes en barres créés dans images/barres/")

# 12. Diagrammes circulaires (blancs, nuls, exprimés, abstentions)
os.makedirs("images/camemberts", exist_ok=True)

print("\n===== Génération des diagrammes circulaires =====")

for i in range(len(contenu)):
    dept = contenu.iloc[i]["Libellé du département"]

    valeurs = [
        contenu.iloc[i]["Blancs"],
        contenu.iloc[i]["Nuls"],
        contenu.iloc[i]["Exprimés"],
        contenu.iloc[i]["Abstentions"],
    ]
    labels = ["Blancs", "Nuls", "Exprimés", "Abstentions"]

    plt.figure()
    plt.pie(valeurs, labels=labels, autopct="%1.1f%%")
    plt.title(f"Répartition des votes — {dept}")
    plt.tight_layout()
    plt.savefig(f"images/camemberts/{dept}.png")
    plt.close()

print("→ Diagrammes circulaires créés dans images/camemberts/")

# 13. Histogramme de la distribution des inscrits
os.makedirs("images", exist_ok=True)

print("\n===== Génération de l'histogramme =====")

plt.figure()
plt.hist(contenu["Inscrits"], bins=10, density=True)
plt.title("Distribution des inscrits")
plt.xlabel("Inscrits")
plt.ylabel("Densité")
plt.tight_layout()
plt.savefig("images/histogramme_inscrits.png")
plt.close()

print("→ Histogramme créé : images/histogramme_inscrits.png")

# 14. Diagrammes circulaires : voix par candidat
os.makedirs("images/voix_candidats", exist_ok=True)

print("\n===== Génération des diagrammes circulaires par candidat =====")

# Récupération des colonnes correspondant aux candidats (tout sauf les colonnes déjà utilisées)
colonnes_candidates = [col for col in contenu.columns if col not in [
    "Département", "Libellé du département", "Inscrits", "Votants",
    "Blancs", "Nuls", "Exprimés", "Abstentions", "Nom de la commune", "Code commune"
]]

# 14. Diagrammes circulaires : voix par candidat
os.makedirs("images/voix_candidats", exist_ok=True)

print("\n===== Génération des diagrammes circulaires par candidat =====")

# Colonnes candidates : toutes les colonnes numériques sauf celles déjà utilisées
colonnes_non_candidates = [
    "Département", "Libellé du département", "Inscrits", "Votants",
    "Blancs", "Nuls", "Exprimés", "Abstentions", "Nom de la commune", "Code commune"
]

colonnes_candidates = [
    col for col in contenu.columns 
    if col not in colonnes_non_candidates and pd.api.types.is_numeric_dtype(contenu[col])
]

# --- Par département ---
departements = contenu["Libellé du département"].unique()

for dept in departements:
    df_dept = contenu[contenu["Libellé du département"] == dept]
    
    # Somme des voix par candidat dans le département, conversion en float
    voix_par_candidat = df_dept[colonnes_candidates].apply(pd.to_numeric, errors='coerce').sum().fillna(0)
    
    if voix_par_candidat.sum() == 0:
        continue  # Ignorer les départements sans votes numériques valides
    
    plt.figure(figsize=(6,6))
    plt.pie(voix_par_candidat, labels=voix_par_candidat.index, autopct="%1.1f%%", startangle=90)
    plt.title(f"Voix par candidat — Département {dept}")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(f"images/voix_candidats/{dept}.png")
    plt.close()

# --- Pour la France entière ---
voix_france = contenu[colonnes_candidates].apply(pd.to_numeric, errors='coerce').sum().fillna(0)

plt.figure(figsize=(8,8))
plt.pie(voix_france, labels=voix_france.index, autopct="%1.1f%%", startangle=90)
plt.title("Voix par candidat — France entière")
plt.axis("equal")
plt.tight_layout()
plt.savefig("images/voix_candidats/france_entière.png")
plt.close()

print("→ Diagrammes circulaires des voix par candidat créés dans images/voix_candidats/")



print("\n===== Travail terminé ! =====")

