import streamlit as st
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import json
import os

url_energie = 'https://opendata.agenceore.fr/explore/dataset/conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-commune/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false'

# Chemin vers le répertoire des fichiers CSV temporaires
temp_csv_dir = 'temp_csv_parts'

# Liste des noms de fichiers CSV temporaires
csv_files = [os.path.join(temp_csv_dir, f) for f in os.listdir(temp_csv_dir) if f.endswith('.csv')]

# Reconstituez le DataFrame en concaténant les fichiers CSV temporaires
data = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Page d'accueil
if st.button("Accueil"):
    # Titre de l'application
    st.title('Bienvenue sur le TP final de Ludwig SAUX')
    

# Page Région
if st.button("Région"):
    st.title('Consommation d\'Énergie par Région en France')
    # Ajoutez ici votre code pour afficher la carte par région

# Page Département
if st.button("Département"):
    st.title('Consommation d\'Énergie par Département en France')

    # Assurez-vous que les codes de département dans les données de consommation sont des strings
    data['code_departement'] = data['code_departement'].astype(str).str.zfill(2)

    # Chargement du fichier GeoJSON pour les départements
    # Remarque : Assurez-vous que le fichier est disponible dans l'environnement de Streamlit
    departements_geojson_path = 'departements.geojson'
    departements_geo_data = gpd.read_file(departements_geojson_path)

    # Convertir les données GeoPandas en projection EPSG:4326 si nécessaire
    departements_geo_data = departements_geo_data.to_crs(epsg=4326)

    # Préparation des données de consommation d'énergie par département
    data_departement = data.groupby('code_departement').agg({'consototale': 'sum'}).reset_index()

    # Fusion des données GeoPandas avec les données de consommation
    merged_departement_data = departements_geo_data.merge(data_departement, left_on='code', right_on='code_departement')

    # Convertir le GeoDataFrame fusionné en GeoJSON pour l'utiliser dans Plotly
    geojson = json.loads(merged_departement_data.to_json())

    # Création du premier graphique (Carte choroplèthe)
    fig_departements = px.choropleth_mapbox(merged_departement_data, 
                                            geojson=geojson, 
                                            locations='code_departement',
                                            color='consototale',
                                            featureidkey="properties.code",
                                            mapbox_style="carto-positron",
                                            zoom=5, 
                                            center={"lat": 46.2276, "lon": 2.2137},
                                            labels={'consototale': 'Consommation Totale (MWh)', 'code_departement': 'Département'},
                                            color_continuous_scale='Blues')

    fig_departements.update_layout(height=450, width=600)
    
    # Création du deuxième graphique (Histogramme)
    plt.figure(figsize=(10, 6))
    sns.histplot(data_departement['consototale'], bins=20, kde=True, color='blue')
    plt.title('Distribution de la Consommation Totale par Département')
    plt.xlabel('Consommation Totale (MWh)')
    plt.ylabel('Fréquence')

    # Afficher les deux graphiques avec Streamlit
    col1, col2 = st.beta_columns(2)
    with col1:
        st.plotly_chart(fig_departements)
    with col2:
        st.pyplot()

# Page Ville
if st.button("Ville"):
    # Sélectionner uniquement les 10 communes avec la consommation la plus élevée

    # Grouper les données par commune et calculer la consommation totale
    grouped_df_energie = data.groupby('libelle_commune')['consototale'].sum().reset_index()

    # Sélectionner les 10 communes avec la consommation la plus élevée
    top_10_consumption_communes = grouped_df_energie.nlargest(8, 'consototale')

    # Étiqueter les communes comme 'High'
    top_10_consumption_communes['Type'] = 'High'

    # Créer un graphique en barres pour les communes avec les hautes consommations
    plt.figure(figsize=(12, 8))
    sns.barplot(x='consototale', y='libelle_commune', data=top_10_consumption_communes, color='red')
    plt.title('Top 10 Communes par Consommation')
    plt.xlabel('Consommation Totale (MWh)')
    plt.ylabel('Commune')

    # Afficher le graphique avec Streamlit
    st.pyplot()
