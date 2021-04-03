import joblib
import streamlit as st
from utils.data import MongoConnection

data_source = MongoConnection()
data_source.connect()
trayectorias = data_source.get_trayectorias()

st.title('Prototipo de sistema de AA para la identificacion de riesgos para el IPN')

st.header('Indice de reprobacion')
st.header('Indice de desercion')
st.header('Indice de eficiencia terminal')