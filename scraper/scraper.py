from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
import json
from pickle import load, dump

# Vamos a crear nuestra estructura que almacenará la información que obtenga el scraper y luego será enviada a un json
class Alumno:
    boleta = None
    genero = None
    promedio = None
    avance = None
    kardex = {}
    adeudos = None
    dictamenes = None
    bajas = None

    def __init__(self, boleta):
        self.boleta = boleta

class Materia:
    periodo = None
    nombre = None
    evaluacion = None
    calificacion = None

    def __init__(self, periodo, nombre, evaluacion, calificacion):
        self.periodo = periodo
        self.nombre = nombre
        self.evaluacion = evaluacion
        self.calificacion = calificacion

class Adeudo:
    semestre = None
    materia = None
    estatus = None
    periodo = None

    def __init__(self, semestre, materia, estatus, periodo):
        self.semstre = semestre
        self.materia = materia
        self.estatus = estatus
        self.periodo = periodo

class Dictamen:
    materia = None
    fecha = None
    evaluacion = None
    inicio = None
    limite = None
    cumplio = None

    def __init__(self, materia, fecha, evaluacion, inicio, limite, cumplio):
        self.materia = materia
        self.fecha = fecha
        self.evaluacion = evaluacion
        self.inicio = inicio
        self.limite = limite
        self.cumplio = cumplio

class Baja:
    inicio = None
    regreso = None
    periodos_baja = None
    fecha_solicitud = None
    tipo = None
    cumplio = None
    motivo = None

    def __init__(self, inicio, regreso, periodos_baja, fecha_solicitud, tipo, cumplio, motivo):
        self.inicio = inicio
        self.regreso = regreso
        self.periodos_baja = periodos_baja
        self.fecha_solicitud = fecha_solicitud
        self.cumplio = cumplio
        self.tipo = tipo
        self.motivo = motivo


driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
driver.get('https://www.saes.escasto.ipn.mx/EJECUTIVO/default.aspx')
with open('boletas.txt','r') as archivo_boletas:
    boletas = archivo_boletas.read().splitlines()
#alumnos = {boleta:None for boleta in boletas[1223:5000]}
with open('dict_saes.pkl','rb') as diccionario_saes:
    alumnos = load(diccionario_saes)
# Esperamos hasta loguearnos y movernos a la página correcta para hacer la búsqueda
foo = input()
# Buscamos los elementos necesarios para consultar el kárdex de un alumno
for boleta in boletas[4524:5000]:
    print(boleta)
    time.sleep(1)
    periodos_usados = []
    alumno = Alumno(boleta)
    driver.find_element_by_id('ctl00_mainCopy_Txbx_Busqueda').send_keys(boleta)
    divs = driver.find_elements_by_tag_name('div')
    buscar = driver.find_element_by_id('ctl00_mainCopy_Btn_Buscar').click()
    time.sleep(random.randint(1,3))
    # Aquí damos click a la boleta que requerimos para ver el historial
    referencia = f"a[href='BusquedaAlumnoRes.aspx?Boleta={boleta}&Tipo=Inscrito']"
    print(referencia)
    driver.find_element_by_css_selector(referencia).click()
    time.sleep(1)
    # Buscamos si podemos obtener algunos datos de su trayectoria, en caso de no existir solo bajamos el kárdex
    try:
        span_info = driver.find_element_by_id('ctl00_mainCopy_Lbl_Alumno')
        # Cuando no hay información disponible el texto en el span lo indica explícitamente, por lo que buscaremos este texto para comprobarlo
        if span_info.text != 'Información no disponible.':
            tabla = span_info.find_element_by_tag_name('table')
            tabla = tabla.find_element_by_tag_name('tbody')
            lista_tr = tabla.find_elements_by_tag_name('tr')
            # Nos interesan solo la fila que contiene el género y la que contiene promedio y % de avance en la carrera
            alumno.genero = lista_tr[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('b').text
            alumno.promedio = lista_tr[4].find_element_by_tag_name('td').find_elements_by_tag_name('b')[0].text
            alumno.avance = lista_tr[4].find_element_by_tag_name('td').find_elements_by_tag_name('b')[1].text
    except NoSuchElementException:
        pass
    # Scrapeamos el kárdex
    # Elegimos el div que contiene el iframe con la información del kardex
    try:
        div_kardex = driver.find_element_by_id('ctl00_mainCopy_TabContainer1').find_element_by_id('ctl00_mainCopy_TabContainer1_body').find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel6')
        frame_kardex = div_kardex.find_element_by_tag_name('iframe')
        # Cambiamos el driver a navegar dentro del iframe
        driver.switch_to.frame(frame_kardex)
        # Localizamos las tablas y el semestre que representan
        sems_totales, periodos = {},{}
        materias = []
        semestres = driver.find_element_by_id('Lbl_Kardex').find_elements_by_tag_name('center')
        for semestre in semestres:
            tabla_semestre = semestre.find_element_by_tag_name('table').find_element_by_tag_name('tbody')
            lista_tr = tabla_semestre.find_elements_by_tag_name('tr')
            # Obtenemos el semestre del que estamos leyendo la información
            sem = lista_tr[0].find_element_by_tag_name('td').text
            for tr in lista_tr[2:]:
                lista_td = tr.find_elements_by_tag_name('td')
                periodo = lista_td[3].text
                materia = Materia(periodo, lista_td[1].text, lista_td[4].text, lista_td[5].text).__dict__
                #materias.append(materia)
                if periodo not in periodos_usados:
                    periodos_usados.append(periodo)
                    periodos[periodo] = []
                try:
                    periodos[periodo].append(materia)
                except:
                    periodos[periodo] = []
                    periodos[periodo].append(materia)
            sems_totales[sem] = periodos.copy()
            periodos = {}
        # Una vez recorridos todos los semestres del Kardex lo añadimos a nuestra instancia de Alumno
        alumno.kardex = sems_totales.copy()
        # Retornamos al html original
        driver.switch_to.default_content()
    except NoSuchElementException:
        pass
    try:
        # Ahora vamos a revisar los adeudos y materias sin cursar
        adeudos = []
        adeudos_span = driver.find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel2_tab')
        adeudos_span.click()
        div_adeudos = driver.find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel2')

        tabla_adeudos = div_adeudos.find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel2_GV_RepAdeu').find_element_by_tag_name('tbody')
        lista_tr = tabla_adeudos.find_elements_by_tag_name('tr')
        for tr in lista_tr[1:]:
            lista_td = tr.find_elements_by_tag_name('td')
            if len(lista_td) > 3:
                adeudo = Adeudo(lista_td[0].text,lista_td[1].text,lista_td[2].text,lista_td[3].text).__dict__
            else:
                adeudo = Adeudo(lista_td[0].text,lista_td[1].text,lista_td[2].text,None).__dict__
            adeudos.append(adeudo)
    except NoSuchElementException:
        pass
    alumno.adeudos = adeudos.copy()
    # Ahora vamos a revisar los dictámenes, en caso de existir
    try:
        dictamenes = []
        div_dictamenes = driver.find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel3')
        dictamenes_span = driver.find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel3_tab')
        dictamenes_span.click()
        tabla_dictamenes = div_dictamenes.find_elements_by_tag_name('div')[1].find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel3_GV_Dictamenes').find_element_by_tag_name('tbody')
        lista_tr = tabla_dictamenes.find_elements_by_tag_name('tr')
        for tr in lista_tr[1:]:
            lista_td = tr.find_elements_by_tag_name('td')
            dictamen = Dictamen(lista_td[4].text,lista_td[5].text,lista_td[6].text,lista_td[7].text,lista_td[8].text,lista_td[9].text).__dict__
            dictamenes.append(dictamen)
    except NoSuchElementException:
        pass
    alumno.dictamenes = dictamenes.copy()
    # Ahora vamos a revisar las bajas
    try:
        bajas = []
        div_bajas = driver.find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel4')
        bajas_span = driver.find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel4_tab')
        bajas_span.click()
        len_div_bajas = len(div_bajas.find_elements_by_tag_name('div'))
        if len_div_bajas > 1:
            tabla_bajas = div_bajas.find_elements_by_tag_name('div')[1].find_element_by_id('ctl00_mainCopy_TabContainer1_TabPanel4_GV_Bajas').find_element_by_tag_name('tbody')
            lista_tr = tabla_bajas.find_elements_by_tag_name('tr')
            for tr in lista_tr[1:]:
                lista_td = tr.find_elements_by_tag_name('td')
                baja = Baja(lista_td[2].text,lista_td[3].text,lista_td[4].text,lista_td[5].text,lista_td[6].text,lista_td[7].text,lista_td[8].text).__dict__
                bajas.append(baja)
    except NoSuchElementException:
        pass
    alumno.bajas = bajas.copy()
    alumnos[boleta] = alumno.__dict__
    # Finalmente damos click de regreso para hacer lo mismo con otro alumno
    try:
        driver.find_element_by_id('ctl00_mainCopy_Lnk').click()
    except NoSuchElementException:
        # Retornamos con la flechita del navegador
        driver.back()

    with open('dict_saes.pkl','wb') as diccionario_saes:
        dump(alumnos,diccionario_saes)

    with open('info_saes_prueba.txt','w') as archivo:
        json.dump(alumnos,archivo)
