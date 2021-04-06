import streamlit  as st
import pandas as pd
import numpy as np
import joblib
from utils.data import MongoConnection

data_source = MongoConnection()
data_source.connect()
trayectorias = data_source.get_trayectorias()

st.title('Indice de reprobación.')

prediccion = {0 : 'aprobado', 1 : 'reprobado'}

valores =  ['Semestrales','Boletas']


df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})




option = st.selectbox(
    'Ver resultados semestrales o por boleta',
     valores)

'You selected: ', option

if option == 'Semestrales':
    df
else :
    st.write('Aun no')

modeloIndiceReprobacion = joblib.load('modelos/ClasificadorKnnIndiceReprobacion.pkl')
a = modeloIndiceReprobacion.predict([[0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	1,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	1,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]])

st.subheader('Prediction')
st.write(prediccion[a[0]])
