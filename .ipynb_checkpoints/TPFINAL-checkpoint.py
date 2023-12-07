import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import json

# Titre de l'application
st.title('Consommation d\'Énergie par Département en France')

# Chargement des données de consommation d'énergie
# Remarque : Assurez-vous que le fichier est disponible dans l'environnement de Streamlit
data = pd.read_csv('conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-commune.csv', sep=';')

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

# Création du graphique
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

fig_departements.update_layout(height=850)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig_departements)
