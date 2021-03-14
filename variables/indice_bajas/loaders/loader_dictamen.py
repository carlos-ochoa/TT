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
    coll_dictamenes = db['Dictamenes']
except ConnectionFailure as c: 
    sys.exit(c)

try:
    trayectorias = coll_trayectorias.find()
except CursorNotFound as c:
    sys.exit(c)


for trayectoria in trayectorias:
    dictamen = coll_dictamenes.find({'_id' : trayectoria['_id']})
    for campo in dictamen:
        materia_dictamen = campo['dictamenes'][0] if len(campo['dictamenes']) else None
        if materia_dictamen is not None:
            nombre_materia = materia_dictamen['materia']
            tiene_dictamen = 'si' if len(nombre_materia) > 2 else 'no'
            coll_trayectorias.update_one({'_id' : trayectoria['_id']}, {'$set' : {'tiene_dictamen' : tiene_dictamen}})



coll_trayectorias.update_many(
    {
        'tiene_dictamen' : {'$exists' : False},
    },
    {
        '$set' : {'tiene_dictamen' : 'no'}
    }
)