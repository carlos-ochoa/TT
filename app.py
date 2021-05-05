import time
import joblib
import streamlit as st
import hashlib
import utils.send_mail as mail
from utils.data import MongoConnection
from utils.models import arima_adeudos
from utils.preprocessing import bajas, vector_bajas, vector_reprobacion, vector_eficiencia, vector_adeudos, vector_dictamenes
from utils.visualizations import indices
from streamlit_echarts import st_echarts

data_source = MongoConnection()
data_source.connect()

trayectorias_bajas = data_source.get_tray_bajas()
trayectorias_reprobacion = data_source.get_tray_reprobacion()
trayectorias = data_source.get_trayectorias()
materias_obligatorias = data_source.get_materias()
dictamenes = data_source.get_dictamenes()

# Inicializacion de modelos
bajas_model = joblib.load('modelos/dt_bajas_model.pkl')
reprobacion_model = joblib.load('modelos/ClasificadorKnnIndiceReprobacion.pkl')
dictamenes_model = joblib.load('modelos/DTDictamenes.pkl')

menu = ["Home","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.subheader("Home")
    nivel_analisis = st.sidebar.radio('Nivel de analisis',['Datos generales','Datos por alumno'])
    st.title('Prototipo de sistema de AA para la identificacion de riesgos para el IPN')

    if nivel_analisis == 'Datos generales':

        st.header('Indice de reprobacion')

        reprobacion_expander = st.beta_expander(
            'Descripcion'
        )

        reprobacion_expander.write('Este indice explica el porcentaje de alumnos que pueden caer en situacion de reprobación de almenos una materia durante el semestre en curso. \n Se pueden \
                elegir los niveles de analisis para identificar los grupos semestrales en mayor riesgo.')

        nivel = st.selectbox('Nivel a analizar',
        ('Total', '1', '2','3','4','5'))

        dataset_trayectorias_reprobacion = vector_reprobacion.generar_vectores(trayectorias_reprobacion, trayectorias, nivel)
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

        eficiencia_expander = st.beta_expander(
            'Descripcion'
        )

        eficiencia_expander.write('Este indice explica el porcentaje de alumnos que terminaran su carrera satisfactoriamente aportando a la eficiencia terminal semestral')

        #dataset_trayectorias_reprobacion = vector_reprobacion.generar_vectores(trayectorias_reprobacion, trayectorias[1])
        #predicciones_reprobacion = reprobacion_model.predict(dataset_trayectorias_reprobacion)

        #dataset_trayectorias_bajas = vector_bajas.generar_vectores(trayectorias_bajas)
        # Predicciones de modelos
        #predicciones_bajas = bajas_model.predict(dataset_trayectorias_bajas)

        predicciones_egresados = vector_eficiencia.generar_vectores(dataset_trayectorias_reprobacion, dataset_trayectorias_bajas, predicciones_reprobacion, predicciones_bajas)

        distribucion_eficiencia, indice_eficiencia = vector_eficiencia.generar_distribucion(predicciones_egresados)
        if len(distribucion_eficiencia) != 0:
            pie = indices.graficar_indice('Alumnos que egresaran', distribucion_eficiencia)
            print(distribucion_eficiencia)
            st_echarts(options = pie)
            st.text(f'El indice de eficiencia terminal esperado para este semestre es: {indice_eficiencia*100}%')
        else:
            st.text(f'No hay informacion disponible')

        #Seccion para la variable de procentaje de reprobación por materia

        st.header('Porcentaje de reprobación por materia')

        materia_expander = st.beta_expander(
            'Descripcion'
        )

        materia_expander.write('Este indice explica el porcentaje de alumnos que reprobarán cada materia por semestre')

        materia = st.selectbox('Materia a analizar' ,materias_obligatorias
        )

        vectores_adeudos_por_periodo=vector_adeudos.vectorizacion(materias_obligatorias)
        materia_vectores=vector_adeudos.vectores_materias(vectores_adeudos_por_periodo,materia)
        prediccion=arima_adeudos.modelo_materia(materia_vectores)
        valor_prediccion=prediccion[0]
        st.line_chart(materia_vectores['reprobados'])

        st.text(f'El porcentaje de reprobados  esperado  para esta materia  en este semestre es: {valor_prediccion*100}%')

        # SECCION PARA VARIABLE DE CUMPLIMIENTO DE DICTAMEN

        st.header('Cumplimiento de dictamenes')

        dictamen_expander = st.beta_expander(
            'Descripcion'
        )

        dictamen_expander.write('Este indice explica el indice esperado de alumnos dictaminados que cumpliran su materia')

        #materia = st.selectbox('Materia a analizar' ,materias_obligatorias)

        vectores_dictamenes = vector_dictamenes.generar_vectores(dictamenes, materias_obligatorias)
        predicciones = dictamenes_model.predict(vectores_dictamenes)

        distribucion_dictamenes, indice_dictamenes = vector_dictamenes.generar_distribucion(predicciones)
        if len(distribucion_dictamenes) != 0:
            pie = indices.graficar_indice('Cumplimiento de dictamen', distribucion_dictamenes)
            print(distribucion_dictamenes)
            st_echarts(options = pie)
            st.text(f'El indice de cumplimiento de dictamenes esperado para este semestre es: {indice_dictamenes*100}%')
        else:
            st.text(f'No hay informacion disponible')

    elif nivel_analisis == 'Datos por alumno':
        st.header('Busqueda por alumno')
        boleta = st.text_input('Boleta')
        if st.button('Buscar') and len(boleta) > 0:
            # Seccion para determinar la posibilidad de baja
            alumno = data_source.get_tray_baja_boleta(boleta)
            alumnor = data_source.get_tray_baja_boleta_reprobacion(boleta)
            if len(list(alumno)) != 0:
                dataset_tray_alumno = vector_bajas.generar_vectores(alumno)
                prediccion_bajas = bajas_model.predict(dataset_tray_alumno)
                dataset_trayectorias_reprobacion = vector_reprobacion.generar_vector_individual(alumnor, trayectorias)
                predicciones_reprobacion = reprobacion_model.predict(dataset_trayectorias_reprobacion)
                if prediccion_bajas[0] == 1:
                    st.text('El estudiante es propenso a darse de baja este semestre')
                else:
                    st.text('El estudiante no se daria de baja este semestre')
                if predicciones_reprobacion[0] == 1:
                    st.text('El estudiante es propenso a reprobar este semestre')
                else:
                    st.text('El estudiante no reprobará este semestre')
            else:
                st.text('Boleta no encontrada')
            # Seccion para n variable
elif choice == "SignUp":
    st.subheader("Crear nueva cuenta")
    form = st.form(key='SignUp')
    nombre = form.text_input("Nombre")
    paterno = form.text_input("Apellido Paterno")
    materno = form.text_input("Apellido Materno")
    email = form.text_input("E-mail")
    password = form.text_input("Password",type='password')
    password_hash= hashlib.sha256(str.encode(password)).hexdigest()
    submit = form.form_submit_button('Submit')
    nombre_completo=nombre +' '+ paterno + ' ' + materno
    if submit:
        data_source.insertar_usuario(email,nombre,paterno,materno,password_hash)
        mail.send(email,password)
        st.write(f'Se te ha dado de alta con exito {nombre_completo}')