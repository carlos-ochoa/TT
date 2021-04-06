import joblib
import streamlit as st
from utils.data import MongoConnection
from utils.preprocessing import bajas
from utils.visualizations import indices
from streamlit_echarts import st_echarts

data_source = MongoConnection()
data_source.connect()
trayectorias,mapa_curricular = data_source.get_trayectorias()
dataset_trayectorias = bajas.generar_vector_con_reprobacion(trayectorias)
dataset_trayectorias = bajas.procesar_dataframe(dataset_trayectorias)

distribuciones = [
    {"value": 235, "name": "Baja"},
    {"value": 274, "name": "No baja"}
]

st.title('Prototipo de sistema de AA para la identificacion de riesgos para el IPN')

st.header('Indice de reprobacion')
st.header('Indice de desercion')

pie = indices.graficar_indice('Alumnos que daran baja', distribuciones)
st_echarts(options=pie)

st.header('Indice de eficiencia terminal')