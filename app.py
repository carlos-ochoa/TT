import time
import joblib
import streamlit as st
import hashlib
import secrets
import string
import utils.send as mail
from utils.data import MongoConnection
from utils.models import arima_adeudos
from utils.preprocessing import bajas, vector_bajas, vector_reprobacion, vector_eficiencia, vector_adeudos, vector_dictamenes, vector_ocupabilidad
from utils.visualizations import indices
from streamlit_echarts import st_echarts
from utils.pdfCreation import pdf
import pandas as pd
from st_aggrid import AgGrid
import requests
from PIL import Image

from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

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
    col1,col2 = st.beta_columns([1,3])
    st.balloons()
    st.subheader("Home")
    nivel_analisis = st.sidebar.radio('Nivel de analisis',['Datos generales','Datos por alumno'])
    image = Image.open('utils/pdfCreation/images/escudoIPN.jpg')
    col1.image(image)
    col2.subheader('Prototipo de sistema de AA para la identificacion de riesgos para el IPN')

    if nivel_analisis == 'Datos generales':

        ################## Reprobracion
        st.header('Indice de reprobacion')

        reprobacion_expander = st.beta_expander(
            'Descripcion'
        )

        reprobacion_expander.write('Este indice explica el porcentaje de alumnos que pueden caer en situacion de reprobación de almenos una materia durante el nivel en curso. \n Se pueden \
                elegir los niveles de analisis para identificar los grupos semestrales en mayor riesgo.')

        nivel = st.selectbox('Nivel a analizar',
        ('Total', '1', '2','3','4','5'))

        dataset_trayectorias_reprobacion = vector_reprobacion.generar_vectores(trayectorias_reprobacion, trayectorias, nivel)
        predicciones_reprobacion = reprobacion_model.predict(dataset_trayectorias_reprobacion)
        distribucion_reprobacion, indice_reprobacion = vector_reprobacion.generar_distribucion(predicciones_reprobacion)
        if len(distribucion_reprobacion) != 0:
            pie = indices.graficar_indice('Alumnos que reprobaran', distribucion_reprobacion,'Estado de reprobacion',"#c23531")
            print(distribucion_reprobacion)
            st_echarts(options = pie)
            st.text(f'El indice de reprobacion esperado para este semestre es: {indice_reprobacion*100}%')
        else:
            st.text(f'No hay informacion disponible')


        ################### desercion

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
            pie = indices.graficar_indice('Alumnos que daran baja', distribucion_bajas,'Estado de baja',"#4A73D1")
            st_echarts(options = pie)
            st.text(f'El indice de bajas esperado para este semestre es: {indice_bajas*100}%')
            print(distribucion_bajas)
        else:
            st.text(f'No hay informacion disponible')

        st.header('Indice de eficiencia terminal')

        eficiencia_expander = st.beta_expander(
            'Descripcion'
        )

        ################### eficiencia terminal

        eficiencia_expander.write('Este indice explica el porcentaje de alumnos que terminaran su carrera satisfactoriamente aportando a la eficiencia terminal semestral')

        #dataset_trayectorias_reprobacion = vector_reprobacion.generar_vectores(trayectorias_reprobacion, trayectorias[1])
        #predicciones_reprobacion = reprobacion_model.predict(dataset_trayectorias_reprobacion)

        #dataset_trayectorias_bajas = vector_bajas.generar_vectores(trayectorias_bajas)
        # Predicciones de modelos
        #predicciones_bajas = bajas_model.predict(dataset_trayectorias_bajas)

        predicciones_egresados = vector_eficiencia.generar_vectores(dataset_trayectorias_reprobacion, dataset_trayectorias_bajas, predicciones_reprobacion, predicciones_bajas)

        distribucion_eficiencia, indice_eficiencia = vector_eficiencia.generar_distribucion(predicciones_egresados)
        if len(distribucion_eficiencia) != 0:
            pie = indices.graficar_indice('Alumnos que egresaran', distribucion_eficiencia,'Egresa','#D98A2B')
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
        prediccion=arima_adeudos.modelo_materia(materia_vectores['reprobados'])
        valor_prediccion=prediccion[0]
        st.line_chart(materia_vectores['reprobados'])
        #########
        print('uwu')
        print(materia_vectores['reprobados'])

        #############

        st.text(f'El porcentaje de reprobados  esperado  para esta materia  en este semestre es: {valor_prediccion*100}%')

        # Seccion para la variable de Ocupabilidad
        st.header('Ocupabilidad')
        ocupabilidad_expander = st.beta_expander(
            'Descripcion'
        )

        ocupabilidad_expander.write('Este indice determina la cantidad de alumnos que cursarán cada materia el siguiente periodo')
        materia_ocupabilidad = st.selectbox('Materia a analizar' ,materias_obligatorias
        , key = "selectOcupabilidad")

        ocupabilidad_vectores=vector_ocupabilidad.vectorizacion()
        ocupabilidad_materia=vector_ocupabilidad.vector_materia(ocupabilidad_vectores,materia_ocupabilidad)
        st.line_chart(ocupabilidad_materia['inscritos'])

        print('XDDDDDDDD')
        print(ocupabilidad_materia['inscritos'])


        prediccion_ocupabilidad=arima_adeudos.modelo_materia(ocupabilidad_materia['inscritos'])
        valor_prediccion_ocupabilidad=prediccion_ocupabilidad[0]

        st.text(f'El número de  alumnos que cursarán  esta materia  es de : {valor_prediccion_ocupabilidad}')

        # SECCION PARA VARIABLE DE CUMPLIMIENTO DE DICTAMEN

        st.header('Cumplimiento de dictamenes')

        dictamen_expander = st.beta_expander(
            'Descripcion'
        )

        dictamen_expander.write('Este indice explica el indice esperado de alumnos dictaminados que cumpliran su materia')

        materias_dictamen = vector_dictamenes.get_materias(dictamenes)
        materia_dictamen = st.selectbox('Materia a analizar' ,materias_dictamen)

        if materia_dictamen == 'Total':
            vectores_dictamenes = vector_dictamenes.generar_vectores(dictamenes, materias_obligatorias)
        else:
            vectores_dictamenes = vector_dictamenes.generar_vectores_filtrado(dictamenes, materias_obligatorias, materia_dictamen)
        predicciones = dictamenes_model.predict(vectores_dictamenes)

        distribucion_dictamenes, indice_dictamenes = vector_dictamenes.generar_distribucion(predicciones)
        if len(distribucion_dictamenes) != 0:
            pie = indices.graficar_indice('Cumplimiento de dictamen', distribucion_dictamenes,'Cumplimiento','#9C2BD9')
            print(distribucion_dictamenes)
            st_echarts(options = pie)
            st.text(f'El indice de cumplimiento de dictamenes esperado para este semestre es: {indice_dictamenes*100}%')


        ###Reporte###
        reportes = st.button("Generar reportes")
        if reportes:
            #variables: boletas,predicciones_reprobacion[0], predicciones_baja[0],dictamen,nombredictamen
            pdf.create_general_report(distribucion_reprobacion, distribucion_bajas,distribucion_eficiencia,distribucion_dictamenes,materia_vectores['reprobados'],ocupabilidad_materia['inscritos'], materia,materia_ocupabilidad)



    elif nivel_analisis == 'Datos por alumno':
        st.header('Busqueda por alumno')
        boleta = st.text_input('Boleta')
        buscar = st.checkbox('Buscar')
        with st.spinner('Cargando datos...'):
            if buscar and len(boleta) > 0:
                
                # Seccion para determinar la posibilidad de baja
                alumno = data_source.get_tray_baja_boleta(boleta)
                mi = alumno[0]['materias_inscritas']
                pc = alumno[0]['periodos_cursados']
                st.header('Información de historial académico')
                st.markdown(f'Materias inscritas hasta el momento: **_{mi}_**')
                st.markdown(f'Periodos cursados: **_{pc}_** ')
                df = pd.DataFrame(alumno[0]['trayectoria'], columns = ['RESULTADO DEL SEMESTRE'])
                df.index = df.index + 1
                st.table(df)
                alumnor = data_source.get_tray_baja_boleta_reprobacion(boleta)
                st.header('Materias inscritas en el periodo actual')
                df2 = pd.DataFrame(alumnor['materias'], columns = ['NOMBRE DE LA ASIGNATURA'])
                df2.index = df2.index + 1
                st.table(df2)
                dictamen_alumno = data_source.get_dictamen_alumno(boleta)
                if len(list(alumno)) != 0:
                    dataset_tray_alumno = vector_bajas.generar_vectores(alumno)
                    prediccion_bajas = bajas_model.predict(dataset_tray_alumno)
                    dataset_trayectorias_reprobacion = vector_reprobacion.generar_vector_individual(alumnor, trayectorias)
                    predicciones_reprobacion = reprobacion_model.predict(dataset_trayectorias_reprobacion)
                    st.header('Diagnóstico de la trayectoria del estudiante')
                    if len(dictamen_alumno) > 0:
                        vector_dictamen = vector_dictamenes.generar_vectores(dictamen_alumno, materias_obligatorias)
                        prediccion_dictamen = dictamenes_model.predict(vector_dictamen)
                        dalumno = dict(dictamen_alumno[0])
                        m = dalumno['materia']
                        st.markdown(f'Dictamen activo: **_{m}_**')
                        resultado_dictamen = 'Cumple' if prediccion_dictamen[0] == 1 else 'No cumple'
                        st.markdown(f'Probable resultado del dictamen: **_{resultado_dictamen}_**')
                    else :
                        m = 'ninguna'
                        prediccion_dictamen[0] = 2
                    if prediccion_bajas[0] == 1:
                        st.markdown('El estudiante es **_propenso a darse de baja_** este semestre')
                    else:
                        st.markdown('El estudiante **_no se daria de baja_** este semestre')
                    if predicciones_reprobacion[0] == 1:
                        st.markdown('El estudiante es **_propenso a reprobar_** este semestre')
                    else:
                        st.markdown('El estudiante **_no reprobará_** este semestre')
                    reportes = st.button("Generar reportes")
                    if reportes:
                        #variables: boletas,predicciones_reprobacion[0], predicciones_baja[0],dictamen,nombredictamen
                        pdf.create_individual_report(boleta,predicciones_reprobacion[0],prediccion_bajas[0],prediccion_dictamen[0],m)
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
    #password = form.text_input("Password",type='password')
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    print(password)
    password_hash= hashlib.sha256(str.encode(password)).hexdigest()
    submit = form.form_submit_button('Submit')
    nombre_completo=nombre +' '+ paterno + ' ' + materno
    if submit:
        data_source.insertar_usuario(email,nombre,paterno,materno,password_hash)
        mail.send(email,password)
        st.write(f'Se te ha dado de alta con exito {nombre_completo}')
    lottie_url = "https://assets10.lottiefiles.com/packages/lf20_q5pk6p1k.json"
    lottie_json = load_lottieurl(lottie_url)
    st_lottie(lottie_json)
