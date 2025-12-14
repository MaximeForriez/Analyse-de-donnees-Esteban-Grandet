import requests
import pandas as pd

# -------------------------------
# 1. Construire l'URL API
# -------------------------------

def geturl(token, station_id, start, end, fmt="csv"):
    """
    Génère l'URL pour accéder à l'API Infoclimat.
    """
    base = "https://www.infoclimat.fr/opendata/?"
    url = (
        f"{base}"
        f"start={start}&"
        f"end={end}&"
        f"format={fmt}&"
        f"stations[]={station_id}&"
        f"method=export&"
        f"token={token}"
    )
    return url

# -------------------------------
# 2. Test connexion
# -------------------------------

def testConnexion(response):
    if response.status_code == 200:
        print("Connexion API OK ✅")
        return True
    else:
        print("Erreur API :", response.status_code)
        return False

# -------------------------------
# 3. Téléchargement CSV
# -------------------------------

def download_csv_data(url):
    response = requests.get(url)
    if not testConnexion(response):
        return None
    return response.text  # CSV brut

# -------------------------------
# 4. Extraction metadata / titres / données
# -------------------------------

def extract_sections(csv_text):
    lignes = csv_text.split("\n")
    metadata = []
    titre = []
    data2 = []

    for i, ligne in enumerate(lignes):
        if i in [0, 1, 2, 3, 4, 6]:
            metadata.append(ligne)
        elif i == 5:
            titre = ligne.split(";")
        else:
            if ligne.strip() != "":
                data2.append(ligne.split(";"))

    return metadata, titre, data2

# -------------------------------
# 5. Conversion en Pandas
# -------------------------------

def convert_to_pandas(metadata, titre, data2):
    df_data = pd.DataFrame(data2, columns=titre)
    df_metadata = pd.DataFrame({"metadata": metadata})
    return df_data, df_metadata

# -------------------------------
# 6. Téléchargement JSON (Bonus)
# -------------------------------

def download_json_data(token, station_id, start, end):
    url = geturl(token, station_id, start, end, fmt="json")
    response = requests.get(url)
    if not testConnexion(response):
        return None
    return response.json()

# -------------------------------
# 7. Programme principal
# -------------------------------

if __name__ == "__main__":

    # ⚠️ Remplace cette clé par ta clé réelle
    token = "b1B7IzrcLSzJaSUqQwk6uoCP4VP7p5O6TZ2ClHn3iG48aGMtGA"
    station_id = "ME099"  # LATMOS-PARIS
    start = "2025-10-01"
    end   = "2025-10-30"

    # --- CSV ---
    url_csv = geturl(token, station_id, start, end)
    print("URL CSV générée :", url_csv)

    csv_text = download_csv_data(url_csv)
    if csv_text:
        metadata, titre, data2 = extract_sections(csv_text)
        df_data, df_metadata = convert_to_pandas(metadata, titre, data2)

        # Enregistrement
        df_data.to_excel("donnees_meteo.xlsx", index=False)
        df_metadata.to_csv("metadonnees.csv", encoding="utf-8", index=False)
        print("✅ Fichiers CSV/Excel enregistrés.")

    # --- JSON (Bonus) ---
    json_data = download_json_data(token, station_id, start, end)
    if json_data:
        # Conversion en DataFrame
        if "data" in json_data:
            df_json = pd.DataFrame(json_data["data"])
            df_json.to_excel("donnees_meteo_json.xlsx", index=False)
            print("✅ Fichier JSON converti et enregistré.")

