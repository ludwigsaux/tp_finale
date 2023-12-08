
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import json
import warnings
import pynsee

from pynsee.download import download_file

# Ignorer les FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Import your functions here (after converting them from the notebook script)
# from your_converted_script import departement_function, region_function, ...
url_energie = 'https://opendata.agenceore.fr/explore/dataset/conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-commune/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false'
url_departement = 'https://france-geojson.gregoiredavid.fr/repo/departements.geojson'
url_data_departement = 'https://storage.googleapis.com/kagglesdsdata/datasets/4132742/7156188/donnees_departements.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20231208%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20231208T164929Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=3f39ee51130207e5d9074c9378644f612b09755cbac7b7503e5d2cee72924ee0964a113e68c2afa62253e691f6d07af90a42f6dea46cd0e9310d268ab7219c9eec387e29be4ef15856ac37bb43f6cbaf3118cd409da513b529bb6270cf988e53667ed135e65f6c6d649710a1e53f47000e570667094ab31c1b3e877f493866d2c0d65c1c0e154937f4271563cbea43a6983e643e7b6e9cce5bd0a4f58c02f4ee05a28e3d6c1a698903a638799f7b846303f6ed70fb128b1d1fbcae1e8bb24746c0e9cb7e2560df44a1cf7ffa9c42bbb7a23550420cfe3b5f8f83698663fcdc4e37e00c46f2455c995f1529f68b31781ad1a7c6fac44d6961d38c28ff26107ad1'

# Chemin vers le répertoire des fichiers CSV temporaires
temp_csv_dir = 'temp_csv_parts'

# Liste des noms de fichiers CSV temporaires
csv_files = [os.path.join(temp_csv_dir, f) for f in os.listdir(temp_csv_dir) if f.endswith('.csv')]

# Reconstituez le DataFrame en concaténant les fichiers CSV temporaires
df_energie = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

df_departement = pd.read_csv(url_data_departement, sep=';')
departements_geo_data = gpd.read_file(url_departement)

filosofi = download_file("FILOSOFI_COM_2016")

# Function placeholders for each page (replace these with actual functions from your script)
def departement_page():
    st.write("Contenu de la page Département.")

def region_page():
    st.write("Contenu de la page Région.")

def communes_page():
    st.write("Contenu de la page Communes.")

def secteur_page():
    st.write("Contenu de la page Secteur.")

def tendances_page():
    st.write("Contenu de la page Tendances.")

def filosofi_page():
    st.write("Contenu de la page Filosofi.")

def visualiser_consommation_departement():
    # Les données de consommation sont des strings, au besoin ajoutez des zéros à gauche pour avoir deux caractères
    df_energie['code_departement'] = df_energie['code_departement'].astype(str).str.zfill(2)

    # Convertir les données GeoPandas en projection EPSG:4326 si nécessaire
    departements_geo_data = departements_geo_data.to_crs(epsg=4326)

    # Préparation des données de consommation d'énergie par département
    data_departement = df_energie.groupby('code_departement').agg({'consototale': 'sum'}).reset_index()

    # Fusion des données GeoPandas avec les données de consommation
    merged_departement_data = departements_geo_data.merge(data_departement, left_on='code', right_on='code_departement')

    # Convertir le GeoDataFrame fusionné en GeoJSON pour l'utiliser dans Plotly
    geojson = json.loads(merged_departement_data.to_json())

    # La partie importante ici est d'assurer que l'argument 'featureidkey' est correctement défini pour correspondre aux propriétés de l'objet GeoJSON
    fig_departements = px.choropleth_mapbox(merged_departement_data, 
                                            geojson=geojson, 
                                            locations='code_departement',
                                            color='consototale',
                                            featureidkey="properties.code",
                                            mapbox_style="carto-positron",
                                            zoom=5, 
                                            center={"lat": 46.2276, "lon": 2.2137},
                                            title='Consommation d\'Énergie par Département en France',
                                            labels={'consototale': 'Consommation Totale (MWh)', 'code_departement': 'Département'},
                                            color_continuous_scale='Blues')

    fig_departements.update_layout(height=850, width=1000)
    st.plotly_chart(fig_departements)

# Streamlit application layout
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Choisir une page:", 
                              ["Département", "Région", "Communes", "Secteur", "Tendances", "Filosofi"])

    if choice == "Département":
        st.header("Département")
        visualiser_consommation_departement()
    elif choice == "Région":
        st.header("Région")
        region_page()
    elif choice == "Communes":
        st.header("Communes")
        communes_page()
    elif choice == "Secteur":
        st.header("Secteur")
        secteur_page()
    elif choice == "Tendances":
        st.header("Tendances")
        tendances_page()
    elif choice == "Filosofi":
        st.header("Filosofi")
        filosofi_page()

if __name__ == "__main__":
    main()
    

