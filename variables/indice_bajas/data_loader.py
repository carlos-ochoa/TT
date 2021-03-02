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
ruta = pathlib.Path(os.path.abspath(os.getcwd())).parent.parent.absolute()
pass_file = 'keys.txt'
conn_info = open(os.path.join(ruta,pass_file))
mongo_conn_info = conn_info.readlines()[0]

try:
    cluster = MongoClient(mongo_conn_info)
    db = cluster['db_TT']
    coll_trayectorias = db['Trayectorias']
    coll_carreras = db['Carreras']
except ConnectionFailure as c: 
    sys.exit(c)

try:
    trayectorias = coll_trayectorias.find()
    carreras = coll_carreras.find()
except CursorNotFound as c:
    sys.exit(c)

materias = []
materias_unicas = []
materias_por_alumno = []
i = 0
for trayectoria in trayectorias:
    i += 1
    for periodo in trayectoria['trayectoria']:
        for materia in trayectoria['trayectoria'][periodo]:
            materias_unicas.append(materia['nombre'])
    materias_por_alumno.append(sorted(materias_unicas.copy()))
    materias_unicas.clear()

i = 0

a = set(['COMUNICACION ORAL Y ESCRITA', 'SEMINARIO DE INVESTIGACIÓN'])
for carrera in carreras:
    if a.issubset(set(carrera['materias'])):
        print(carrera['nombre'])
        sys.exit()

for mapa in materias_por_alumno:
    print(json.dumps(mapa, indent = 2))
    print(set(mapa))
    for carrera in carreras: 
        if set(mapa).issubset(set(carrera['materias'])):
            print(set(carrera['materias']))
            print(carrera['nombre'])
            i += 1
    input()

print(i)
print(len(materias_por_alumno))
