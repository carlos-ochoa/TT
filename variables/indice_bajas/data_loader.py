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
    trayectorias = coll_trayectorias.find({
        '$and' : [
            {'materias_cursadas' : {'$gte' : 45}}, 
            {'materias_cursadas' : {'$lte' : 51}}
        ]
    })
except CursorNotFound as c:
    sys.exit(c)

materias = []
materias_unicas = []
i = 0
for trayectoria in trayectorias:
    i += 1
    materias.append(trayectoria['materias_cursadas'])

print(i)
print(set(materias))
print(max(set(materias)))
