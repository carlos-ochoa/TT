import json
import os 
import pathlib
import sys
from pickle import load
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
    coll_carreras = db['Carreras']
except ConnectionFailure as c: 
    sys.exit(c)

with open('carreras.pkl','rb') as carreras_file:
    carreras = load(carreras_file)

for carrera in carreras:
    carrera['materias'] = {k.replace('.',''):v for k,v in sorted(carrera['materias'].items())}

try:
    coll_carreras.insert_many(carreras, ordered = False)
except BulkWriteError as b:
    sys.exit(b)

