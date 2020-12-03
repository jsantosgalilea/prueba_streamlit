import streamlit as st
import requests
import xmltodict
import folium
import json
import pprint
import pandas as pd
import numpy as np
import webbrowser
import time
from geopy.geocoders import ArcGIS

st.title("BUCADOR CATASTRAL")
st.header("Localiza datos catastrales")
st.subheader("Introduce la referencia catastral")
st.write("Esto seria un st.write")

add_selectbox = st.sidebar.selectbox(
    "Ejemplo de selector en lateral",
    ("Opción 1", "Opción 2", "Opción 3")
)
rc = st.text_input('Referencia Catastral', '3342401VK4384D0001UB')
tipoInm = st.selectbox(
    "Tipo de inmueble",
    ("VPT", "VUT", "PZT", "TRT")
)
ej = st.text_input('Direccion', 'Calle Redecilla del Camino 2 28050 Madrid')
temp = ArcGIS().geocode(ej)
st.write('Dirección normalizada: ', temp.raw)
st.write('Longitud dirección: ', temp.latitude, 'Longitud dirección: ', temp.longitude)

# Crear mapa
point = {'latitude':[lat],'longitude':[long]}
df_map = pd.DataFrame(data=point)
st.map(df_map)

# Crear foto
url_imagen = "http://ovc.catastro.meh.es/OVCServWeb/OVCWcfLibres/OVCFotoFachada.svc/RecuperarFotoFachadaGet?ReferenciaCatastral="+rc # El link de la imagen
st.image(url_imagen)
