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

#Obtención de las variables necesarias para la AVM (CÓDIGO POSTAL, SUPERFICIE, ANTIGÜEDAD)
url_catastro = "http://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/"
provincia=''
municipio=''
params_cat = {"Provincia": provincia, "Municipio": municipio, "RC": rc}
url = url_catastro + "OVCCallejero.asmx/Consulta_DNPRC"
response_catastro = requests.get(url, params=params_cat)
###print(response_catastro.content)
datos_xml=xmltodict.parse(response_catastro.content, process_namespaces=False, xml_attribs=False)
###imprimir todos los datos: print(datos_xml)
###imprimir la antigüedad: print('Año',datos_xml['consulta_dnp']['bico']['bi']['debi']['ant'])
###convertir el archivo xml a json: json_cat = json.dumps(datos_xml)
###imprimir el archivo: pprint.pprint(json_cat)
ant = 2020-int(datos_xml['consulta_dnp']['bico']['bi']['debi']['ant'])
sup = float(datos_xml['consulta_dnp']['bico']['bi']['debi']['sfc'])
cp = int(datos_xml['consulta_dnp']['bico']['bi']['dt']['locs']['lous']['lourb']['dp'])
st.write('Código postal', cp)
st.write('Superficie', sup)
st.write('Antigüedad', ant)
#Obtención de las coordenas longitud y latitud
srs='EPSG:4258'
rc_matriz= rc[0:14]
params_coord = {"Provincia": provincia, "Municipio": municipio, "SRS":srs, "RC": rc_matriz}
url_coord = url_catastro + "OVCCoordenadas.asmx/Consulta_CPMRC"
response_coord = requests.get(url_coord, params=params_coord)
datos_xml_coord=xmltodict.parse(response_coord.content, process_namespaces=False, xml_attribs=False)
###imprimir todos los datos: print(datos_xml_coord)
long = float(datos_xml_coord['consulta_coordenadas']['coordenadas']['coord']['geo']['xcen'])
lat = float(datos_xml_coord['consulta_coordenadas']['coordenadas']['coord']['geo']['ycen'])
st.write('Longitud', long)
st.write('Latitud', lat)

# Crear mapa
point = {'latitude':[lat],'longitude':[long]}
df_map = pd.DataFrame(data=point)
st.map(df_map)

# Crear foto
url_imagen = "http://ovc.catastro.meh.es/OVCServWeb/OVCWcfLibres/OVCFotoFachada.svc/RecuperarFotoFachadaGet?ReferenciaCatastral="+rc # El link de la imagen
st.image(url_imagen)
