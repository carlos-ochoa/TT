import joblib
import streamlit as st
from utils.data import MongoConnection
from utils.preprocessing import bajas, vector_bajas, vector_reprobacion
from utils.visualizations import indices
from streamlit_echarts import st_echarts

data_source = MongoConnection()
data_source.connect()

trayectorias_bajas = data_source.get_tray_bajas()
trayectorias_reprobacion = data_source.get_tray_reprobacion()
trayectorias = data_source.get_trayectorias()

# Inicializacion de modelos
bajas_model = joblib.load('modelos/dt_bajas_model.pkl')
reprobacion_model = joblib.load('modelos/ClasificadorKnnIndiceReprobacion.pkl')



st.title('Prototipo de sistema de AA para la identificacion de riesgos para el IPN')

st.header('Indice de reprobacion')

nivel = st.selectbox('Nivel a analizar',
('Total', '1', '2','3','4','5'))


dataset_trayectorias_reprobacion = vector_reprobacion.generar_vectores(trayectorias_reprobacion, trayectorias[1])
predicciones_reprobacion = reprobacion_model.predict(dataset_trayectorias_reprobacion)
distribucion_reprobacion, indice_reprobacion = vector_reprobacion.generar_distribucion(predicciones_reprobacion)
if len(distribucion_reprobacion) != 0:
    pie = indices.graficar_indice('Alumnos que reprobaran', distribucion_reprobacion)
    print(distribucion_reprobacion)
    st_echarts(options = pie)
    st.text(f'El indice de reprobacion esperado para este semestre es: {indice_reprobacion*100}%')
else:
    st.text(f'No hay informacion disponible')

st.header('Indice de desercion')

semestre = st.selectbox(
    'Semestre a analizar',
     ('Total', '1', '2','3','4','5','6','7','8','9','10','11','12'))



dataset_trayectorias_bajas = vector_bajas.generar_vectores(trayectorias_bajas)
# Predicciones de modelos
predicciones_bajas = bajas_model.predict(dataset_trayectorias_bajas)
dataset_trayectorias_bajas, predicciones_bajas = vector_bajas.filtrar_vectores(dataset_trayectorias_bajas, predicciones_bajas, semestre)
distribucion_bajas, indice_bajas = vector_bajas.generar_distribucion(predicciones_bajas)

if len(distribucion_bajas) != 0:
    pie = indices.graficar_indice('Alumnos que daran baja', distribucion_bajas)
    st_echarts(options = pie)
    st.text(f'El indice de bajas esperado para este semestre es: {indice_bajas*100}%')
else:
    st.text(f'No hay informacion disponible')
st.header('Indice de eficiencia terminal')
