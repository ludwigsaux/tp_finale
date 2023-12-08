
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

url_energie = 'https://opendata.agenceore.fr/explore/dataset/conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-commune/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false'
url_departement = 'https://france-geojson.gregoiredavid.fr/repo/departements.geojson'
url_data_departement = 'https://storage.googleapis.com/kagglesdsdata/datasets/4132742/7156188/donnees_departements.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20231208%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20231208T164929Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=3f39ee51130207e5d9074c9378644f612b09755cbac7b7503e5d2cee72924ee0964a113e68c2afa62253e691f6d07af90a42f6dea46cd0e9310d268ab7219c9eec387e29be4ef15856ac37bb43f6cbaf3118cd409da513b529bb6270cf988e53667ed135e65f6c6d649710a1e53f47000e570667094ab31c1b3e877f493866d2c0d65c1c0e154937f4271563cbea43a6983e643e7b6e9cce5bd0a4f58c02f4ee05a28e3d6c1a698903a638799f7b846303f6ed70fb128b1d1fbcae1e8bb24746c0e9cb7e2560df44a1cf7ffa9c42bbb7a23550420cfe3b5f8f83698663fcdc4e37e00c46f2455c995f1529f68b31781ad1a7c6fac44d6961d38c28ff26107ad1'


# Function placeholders (replace these with actual functions from your script)
def function1():
    st.write("Function 1 content goes here.")

def function2():
    st.write("Function 2 content goes here.")

# Streamlit application layout
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Choose a page:", ["Département", "Région"])

    if choice == "Page 1":
        st.header("Page 1")
        function1()
    elif choice == "Page 2":
        st.header("Page 2")
        function2()

if __name__ == "__main__":
    main()
