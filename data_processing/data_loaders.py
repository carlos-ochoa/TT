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
ruta = pathlib.Path(os.path.abspath(os.getcwd())).parent.absolute()
pass_file = 'keys.txt'
conn_info = open(os.path.join(ruta,pass_file))
mongo_conn_info = conn_info.readlines()[0]

try:
    cluster = MongoClient(mongo_conn_info)
    db = cluster['db_TT']
    coll_kardex = db['Kardex']
    coll_trayectorias = db['Trayectorias']
except ConnectionFailure as c: 
    sys.exit(c)

try:
    kardex = coll_kardex.find()
except CursorNotFound as c:
    sys.exit(c)

trayectorias = []
trayectoria = defaultdict(dict)

# Loader de trayectorias académicas

def contar_materias_cursadas(materias):
    materias_pasadas = 0
    for materia in materias:
        if int(materia['calificacion']) >= 6:
            materias_pasadas += 1
    return materias_pasadas

def eliminar_periodo(materia):
    del materia['periodo']
    return materia

for k in kardex:
    if k['kardex'] is not None:
        periodos_por_alumno = []
        trayectoria['_id'] = k['_id']
        trayectoria['materias_cursadas'] = 0
        for semestre in k['kardex']:
            for periodo in k['kardex'][semestre]:
                periodos_por_alumno.append(periodo)
                materias = k['kardex'][semestre][periodo]
                # Elimina el atributo periodo de cada materia, no es necesario
                materias = list(map(eliminar_periodo,materias))
                if len(list(trayectoria[periodo])) == 0:
                    trayectoria[periodo] = list(materias)
                else:
                    trayectoria[periodo].extend(materias)
                trayectoria['materias_cursadas'] += contar_materias_cursadas(materias)
        periodos_por_alumno = sorted(periodos_por_alumno)
        trayectoria['periodo_de_ingreso'] = periodos_por_alumno[0] if len(periodos_por_alumno) > 0 else 'ND'
        trayectoria['ultimo_periodo'] = periodos_por_alumno[-1] if len(periodos_por_alumno) > 0 else 'ND'
    trayectorias.append(trayectoria)
    trayectoria = defaultdict(dict)

try:
    coll_trayectorias.insert_many(trayectorias, ordered = False)
except BulkWriteError as b:
    sys.exit(b)
