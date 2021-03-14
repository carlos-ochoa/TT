import json
import os 
import pathlib
import sys
from collections import defaultdict
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CursorNotFound, BulkWriteError
from bson.objectid import ObjectId

# Obtenemos la ruta donde se encuentra el archivo de claves de conexion
# Para evitar el hardcode de la información de acceso
ruta = pathlib.Path(os.path.abspath(os.getcwd())).parent.parent.parent.absolute()
pass_file = 'keys.txt'
conn_info = open(os.path.join(ruta,pass_file))
mongo_conn_info = conn_info.readlines()[0]

try:
    cluster = MongoClient(mongo_conn_info)
    db = cluster['db_TT']
    coll_trayectorias = db['Trayectorias']
    coll_indice_bajas = db['indice_bajas']
except ConnectionFailure as c: 
    sys.exit(c)

try:
    trayectorias = coll_trayectorias.find({'carrera' : 'CONTADOR PUBLICO'})
except CursorNotFound as c:
    sys.exit(c)

periodos_permitidos = ['10/2', '11/1', '11/2', '12/1', '12/2', '13/1', '13/2', 
                        '14/1', '14/2', '15/1', '15/2', '16/1', '16/2', 
                        '17/1', '17/2', '18/1', '18/2', '19/1', '19/2',
                         '20/1', '20/2','21/1']
trayectorias_filtradas = []
# En la siguientes lineas de código se va a etiquetar cada ejemplo para mandarlo a una nueva colección especial para esta variable

def encontrar_periodos_consecutivos(periodo_inicio,periodos_alumno):
    es_consecutivo = True
    indice_inicio = periodos_permitidos.index(periodo_inicio)
    subconjunto_periodos = periodos_permitidos[indice_inicio:]
    for indice,periodo in enumerate(periodos_alumno):
        if not subconjunto_periodos[indice] == periodo:
            es_consecutivo = False
            break
    return es_consecutivo

def encontrar_periodos_cursados(trayectoria):
    periodos = []
    for periodo in trayectoria:
        periodos.append(periodo)
    return sorted(periodos)

def filtrarPeriodo(trayectoria):
    if trayectoria['periodo_de_ingreso'] in periodos_permitidos:
        return True
    else:
        return False

def filtrarMateriasAcabadas(trayectoria):
    if trayectoria['materias_cursadas'] >= 49:
        return True
    else:
        return False

def filtrarMateriasInacabadas(trayectoria):
    if trayectoria['materias_cursadas'] >= 49:
        return False
    else:
        return True

trayectorias_filtradas = list(filter(filtrarPeriodo, trayectorias))


materias_cursadas = []
for trayectoria in trayectorias_filtradas:
    materias_cursadas.append(trayectoria['materias_cursadas'])

trayectorias_terminadas = list(filter(filtrarMateriasAcabadas, trayectorias_filtradas))
trayectorias_sin_terminar = list(filter(filtrarMateriasInacabadas, trayectorias_filtradas))

# Revisamos que cada trayectoria haya estado inscrita en periodos consecutivos
# De lo contrario es candidata a ser etiquetada como baja
bajas_registros = defaultdict(dict)
bajas_permanentes = defaultdict(dict)
sin_bajas = defaultdict(dict)
for trayectoria in trayectorias_sin_terminar:
    periodo_inicio = trayectoria['periodo_de_ingreso']
    ultimo_periodo = trayectoria['ultimo_periodo']
    periodos_cursados = encontrar_periodos_cursados(trayectoria['trayectoria'])
    diferencia = periodos_permitidos.index('21/1') - periodos_permitidos.index(ultimo_periodo)
    es_consecutivo = encontrar_periodos_consecutivos(periodo_inicio, periodos_cursados)
    # HAY UN CASO MAS; SI EL ULTIMO PERIODO ES 21/1 Y ES CONSECUTIVO NO HAY BAJA
    if diferencia >= 2:
        bajas_registros[trayectoria['_id']] = 'permanente'
    elif ultimo_periodo == '21/1' and es_consecutivo:
        bajas_registros[trayectoria['_id']] = 'sin baja'
    else:
        bajas_registros[trayectoria['_id']] = 'temporal'

# Con las trayectorias terminadas pueden ocurrir dos casos, una baja temporal o no haberse dado de baja nunca
for trayectoria in trayectorias_terminadas:
    # Si todos sus periodos son consecutivos se considera no baja, de lo contrario es temporal
    periodo_inicio = trayectoria['periodo_de_ingreso']
    periodos = encontrar_periodos_cursados(trayectoria['trayectoria'])
    es_consecutivo = encontrar_periodos_consecutivos(periodo_inicio,periodos)
    bajas_registros[trayectoria['_id']] = 'sin baja' if es_consecutivo else 'temporal'

# A partir de aquí tenemos que actualizar el nuevo campo en el dataset
trayectorias.rewind()
for trayectoria in trayectorias:
    coll_indice_bajas.insert_one(trayectoria)

trayectorias.rewind()
for k,v in bajas_registros.items():
    coll_indice_bajas.update_one({'_id' : k},{'$set' : {'tipo_baja' : v}})