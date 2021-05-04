import random
import os
import pathlib
import sys
from collections import defaultdict
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CursorNotFound, BulkWriteError
from bson.objectid import ObjectId
import random

ruta = pathlib.Path(os.path.abspath(os.getcwd())).parent.absolute()
pass_file = 'keys.txt'
conn_info = open(os.path.join(ruta,pass_file))
mongo_conn_info = conn_info.readlines()[0]

try:
    cluster = MongoClient(mongo_conn_info)
    db = cluster['db_TT']
    coll_boletas = db['curso_actual']
    coll_dictamenes = db['Dictamenes']
    coll_curso_actual = db['curso_actual_dictamenes']
except ConnectionFailure as c:
    sys.exit(c)
try:
    boletas = coll_boletas.find({})
    curso_actual = coll_curso_actual.find({})
    dictamenes = coll_dictamenes.find({})
except CursorNotFound as c:
    sys.exit(c)

def obtener_boletas():
    boletas_data = []
    boletas_finales = []
    for alumno in boletas:
        boletas_data.append(alumno['_id'])
    for i in range(119):
        boleta = boletas_data[random.randint(0,len(boletas_data)-1)]
        while boleta not in boletas_finales:
            boletas_finales.append(boleta)
            boleta = boletas_data[random.randint(0,len(boletas_data)-1)]
    return boletas_finales

def generar_dictamenes():
    boletas_finales = obtener_boletas()
    #print(boletas_finales)
    dictamenes_finales = []
    i = 0
    for alumno in dictamenes:
        if i < len(boletas_finales):
            print(i)
            dictamenes_finales.append(alumno)
            dictamenes_finales[i]['_id'] = boletas_finales[i] 
            i += 1
        else:
            break
    return dictamenes_finales

dictamenes_data = generar_dictamenes()
print(dictamenes_data)

coll_curso_actual.insert_many(dictamenes_data)