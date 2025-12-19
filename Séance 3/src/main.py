import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# Configuration des dossiers
# =============================
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR = os.path.join(BASE_DIR, "img")

os.makedirs(IMG_DIR, exist_ok=True)

# =============================
# 1. Lecture du fichier CSV (élections)
# =============================
file_elections = os.path.join(DATA_DIR, "resultats-elections-presidentielles-2022-1er-tour.csv")

with open(file_elections, "r", encoding="utf-8") as f:
    df = pd.read_csv(f, low_memory=False)

# Conversion propre des colonnes numériques
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="ignore")

# =============================
# 2. Sélection des colonnes quantitatives
# =============================
quantitative_cols = df.select_dtypes(include=[np.number])

# =============================
# 3. Calcul des paramètres statistiques
# =============================
means = quantitative_cols.mean().round(2)
medians = quantitative_cols.median().round(2)
modes = quantitative_cols.mode().iloc[0].round(2)
stds = quantitative_cols.std().round(2)

abs_dev_mean = quantitative_cols.sub(means).abs().mean().round(2)

ranges = (quantitative_cols.max() - quantitative_cols.min()).round(2)

# =============================
# 4. Affichage des résultats
# =============================
print("Moyennes :", means.tolist())
print("Médianes :", medians.tolist())
print("Modes :", modes.tolist())
print("Écarts-types :", stds.tolist())
print("Écart absolu moyen :", abs_dev_mean.tolist())
print("Étendues :", ranges.tolist())

# =============================
# 5. Distance interquartile et interdécile
# =============================
q1 = quantitative_cols.quantile(0.25)
q3 = quantitative_cols.quantile(0.75)
interquartile = (q3 - q1).round(2)

d1 = quantitative_cols.quantile(0.1)
d9 = quantitative_cols.quantile(0.9)
interdecile = (d9 - d1).round(2)

print("Distance interquartile :", interquartile.tolist())
print("Distance interdécile :", interdecile.tolist())

# =============================
# 6. Boîtes à moustaches
# =============================
for col in quantitative_cols.columns:
    plt.figure()
    plt.boxplot(quantitative_cols[col].dropna())
    plt.title(f"Boîte à moustaches – {col}")
    plt.ylabel(col)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, f"boxplot_{col}.png"))
    plt.close()

# =============================
# 7. Lecture du fichier island-index.csv
# =============================
file_islands = os.path.join(DATA_DIR, "island-index.csv")

with open(file_islands, "r", encoding="utf-8") as f:
    df_islands = pd.read_csv(f)

# Nettoyage des noms de colonnes
df_islands.columns = df_islands.columns.str.strip()

# =============================
# 8. Catégorisation des surfaces
# =============================
# Adapter ici si le nom exact diffère
surface = df_islands["Surface (km²)"]

bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, np.inf]
labels = [
    "]0,10]",
    "]10,25]",
    "]25,50]",
    "]50,100]",
    "]100,2500]",
    "]2500,5000]",
    "]5000,10000]",
    "]10000,+∞["
]

categories = pd.cut(surface, bins=bins, labels=labels, right=True)
counts = categories.value_counts().sort_index()

print("Répartition des îles par surface :")
print(counts)

# =============================
# 9. Bonus : export CSV et Excel
# =============================
results_df = pd.DataFrame({
    "Moyenne": means,
    "Médiane": medians,
    "Mode": modes,
    "Écart-type": stds,
    "Écart absolu moyen": abs_dev_mean,
    "Étendue": ranges,
    "Interquartile": interquartile,
    "Interdécile": interdecile
})

results_df.to_csv(os.path.join(BASE_DIR, "statistiques_elections.csv"))
results_df.to_excel(os.path.join(BASE_DIR, "statistiques_elections.xlsx"))


