# main.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Lecture du fichier CSV avec 'with'
csv_path = "data/island-index.csv"  # adapte ce chemin selon ton fichier
with open(csv_path, 'r', encoding='utf-8') as f:
    df = pd.read_csv(f)

# 2. Sélection des colonnes quantitatives
quant_cols = df.select_dtypes(include=[np.number]).columns
print("Colonnes quantitatives :", quant_cols.tolist())

# 3. Calcul des paramètres statistiques
stats = {}
for col in quant_cols:
    mean_val = df[col].mean().round(2)
    median_val = df[col].median().round(2)
    mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else np.nan
    std_val = df[col].std().round(2)
    mean_abs_dev = np.mean(np.abs(df[col] - mean_val)).round(2)
    col_range = (df[col].max() - df[col].min()).round(2)
    stats[col] = {
        "Moyenne": mean_val,
        "Médiane": median_val,
        "Mode": mode_val,
        "Ecart-type": std_val,
        "Ecart absolu à la moyenne": mean_abs_dev,
        "Etendue": col_range
    }

# 4. Affichage des statistiques
for col, param in stats.items():
    print(f"\nColonne : {col}")
    for k, v in param.items():
        print(f"{k} : {v}")

# 5. Distance interquartile et interdécile
iqd_idd = {}
for col in quant_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqd = (q3 - q1).round(2)
    
    d1 = df[col].quantile(0.1)
    d9 = df[col].quantile(0.9)
    idd = (d9 - d1).round(2)
    
    iqd_idd[col] = {"IQR": iqd, "Interdécile": idd}

print("\nDistance interquartile et interdécile :")
for col, val in iqd_idd.items():
    print(f"{col} -> IQR: {val['IQR']}, Interdécile: {val['Interdécile']}")

# 6. Boîtes à moustache (boxplots)
output_dir = "img"
os.makedirs(output_dir, exist_ok=True)

for col in quant_cols:
    plt.figure(figsize=(8,6))
    plt.boxplot(df[col].dropna())
    plt.title(f"Boîte à moustache de {col}")
    plt.ylabel(col)
    # Sauvegarde du graphique
    safe_col = col.replace("/", "_").replace("\\", "_")
    plt.savefig(f"{output_dir}/{safe_col}.png")
    plt.close()

print("\nBoîtes à moustache sauvegardées dans le dossier 'img'.")

#9 et 10
csv_path = "data/island-index.csv"
with open(csv_path, 'r', encoding='utf-8') as f:
    df = pd.read_csv(f)

df.columns = df.columns.str.strip()

surface = df['Surface (km²)']

# Définition des intervalles et catégories
bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, np.inf]
labels = ['0-10', '10-25', '25-50', '50-100', '100-2500', '2500-5000', '5000-10000', '>=10000']

categories = pd.cut(surface, bins=bins, labels=labels, right=True)
counts = categories.value_counts().sort_index()

print("Nombre d’îles par catégorie de surface :")
print(counts)
