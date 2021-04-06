import json
import os
import pathlib
import sys
from collections import defaultdict
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CursorNotFound, BulkWriteError
from bson.objectid import ObjectId
import random

# Obtenemos la ruta donde se encuentra el archivo de claves de conexion
# Para evitar el hardcode de la información de acceso
ruta = pathlib.Path(os.path.abspath(os.getcwd())).parent.absolute()
pass_file = 'keys.txt'
conn_info = open(os.path.join(ruta,pass_file))
mongo_conn_info = conn_info.readlines()[0]

try:
    cluster = MongoClient(mongo_conn_info)
    db = cluster['db_TT']
    coll_trayectorias = db['indice_bajas']
    coll_carreras = db['Carreras']
    coll_curso_actual = db['curso_actual']
except ConnectionFailure as c:
    sys.exit(c)
try:
    trayectorias = coll_trayectorias.find({'tipo_baja' : {'$exists' : True}})
    mapa_curricular = coll_carreras.find({'nombre' : 'CONTADOR PUBLICO'})

except CursorNotFound as c:
    sys.exit(c)

for m in mapa_curricular:
  mapa_curricular_materias = dict(m['materias'])
materias_obligatorias = [materia for materia,tipo in mapa_curricular_materias.items() if tipo == 'OBLIGATORIA']
materias_obligatorias.append('OTRA')

#print(materias_obligatorias )
#Se creo esta parte para generar datos no vistos por el modelo y ver resultados en la parte del índice de reprobacion
def crear_trayectoria(boleta,cantidadMaterias):
    materias=[]
    materiasCursadas = materias_cursadas(boleta)
    i=0
    nivel = 0
    j=random.randrange(4, 10)
    #print(cantidadMaterias)
    if cantidadMaterias+j>12:
        nivel = 2
        if cantidadMaterias+j>22:
            nivel = 3
            if cantidadMaterias+j>32:
                nivel = 4
                if cantidadMaterias+j>41:
                    nivel =5
                else:
                    nivel =1
    while i<j:
        materia = random.choice(materias_obligatorias)
        materiasDisponibles = set(materias_obligatorias) - set(materiasCursadas)
        if materia not in materiasDisponibles:
            materias.append(materia)
            i+=1



    trayectoria={"_id":boleta,"materias":materias,"nivel":nivel}
    print(trayectoria)
    return trayectoria

#Ayuda a tener la lista de materias que ya curso un alumno para que no sea repetidas
def materias_cursadas(boleta):
    trayectorias = coll_trayectorias.find({'_id' : boleta})
    materiasCursadas = []
    for alumno in trayectorias:
        for periodo in alumno['trayectoria']:
            for materia in alumno['trayectoria'][periodo]:
                #print(materia['nombre'])
                if materia not in materiasCursadas:
                    materiasCursadas.append(materia['nombre'])
    return materiasCursadas

alumnos = []

for boleta in trayectorias:
    if boleta['materias_cursadas']<=40:
        alumnos.append(crear_trayectoria(boleta['_id'],boleta['materias_cursadas']))
        #materias_cursadas(boleta['_id'])
coll_curso_actual.insert_many(alumnos)
