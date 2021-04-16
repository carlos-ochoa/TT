import joblib
import streamlit as st
from utils.data import MongoConnection
from utils.preprocessing import bajas, vector_bajas
from utils.visualizations import indices
from streamlit_echarts import st_echarts

data_source = MongoConnection()
data_source.connect()
trayectorias_bajas = data_source.get_tray_bajas()


# Inicializacion de modelos
bajas_model = joblib.load('modelos/dt_bajas_model.pkl')

nivel_analisis = st.sidebar.radio('Nivel de analisis',['Datos generales','Datos por alumno'])

st.title('Prototipo de sistema de AA para la identificacion de riesgos para el IPN')

if nivel_analisis == 'Datos generales':

    st.header('Indice de reprobacion')
    st.header('Indice de desercion')

    bajas_expander = st.beta_expander(
        'Descripcion'
    )

    bajas_expander.write('Este indice explica el porcentaje de alumnos que pueden caer en situacion de desercion durante el semestre en curso. \n Se pueden \
            elegir los niveles de analisis para identificar los grupos semestrales en mayor riesgo.')

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

elif nivel_analisis == 'Datos por alumno':
    st.header('Busqueda por alumno')
    boleta = st.text_input('Boleta')