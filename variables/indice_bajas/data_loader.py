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
except ConnectionFailure as c: 
    sys.exit(c)

try:
    trayectorias = coll_trayectorias.find()
except CursorNotFound as c:
    sys.exit(c)

print(trayectorias['2010400953']['10/1'])
sys.exit()

total_materias = []
total_materias_por_alumno = 0
saltar_id = True
for trayectoria in trayectorias:
    for campo in trayectoria:
        if saltar_id:
            saltar_id = False
            continue
        else:
            total_materias_por_alumno += len(campo)
    total_materias.append(total_materias_por_alumno)
    total_materias_por_alumno = 0
    saltar_id = True

print(total_materias)
print(max(total_materias))
