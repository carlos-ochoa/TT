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

boletas = []
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
    boletas.append(trayectoria['_id'])


carreras_nombres = ['ADMINISTRACION Y DESARROLLO EMPRESARIAL', 
            'CONTADOR PUBLICO', 'COMERCIO INTERNACIONAL',
            'NEGOCIOS INTERNACIONALES','RELACIONES COMERCIALES','NO IDENTIFICADO']

i = 0
encontrado = False
diferencias, intersecciones = [],{}
carreras_etiquetadas = {k:0 for k in carreras_nombres}

index = 0
for mapa in materias_por_alumno:
    #print(json.dumps(mapa, indent = 2))
    #print(set(mapa))
    for carrera in carreras:
        if set(mapa).issubset(set(carrera['materias'])):
            #print(set(carrera['materias']))
            print(carrera['nombre'])
            carreras_etiquetadas[carrera['nombre']] += 1
            encontrado = True
            mayor_interseccion = carrera['nombre']
            break
        else:
            intersecciones[carrera['nombre']] = len(set(mapa) & set(carrera['materias']))
        #    print('NO IDENTIFICADO')
    if not encontrado:
        mayor_interseccion = max(intersecciones.items(), key = lambda e : e[1])[0]
        carrera_de_interseccion = list(coll_carreras.find({'nombre' : mayor_interseccion}))
        materias_diferentes = set(mapa) - set(carrera_de_interseccion[0]['materias'])
        materias_admin_acento = set(['MATEMATICAS PARA NEGOCIOS','SEMINARIO DE INVESTIGACION'])
        if set(mapa) == materias_admin_acento:
            print(mayor_interseccion)
            carreras_etiquetadas[mayor_interseccion] += 1
        elif mayor_interseccion == 'RELACIONES COMERCIALES':
            print(mayor_interseccion)
            carreras_etiquetadas[mayor_interseccion] += 1
        elif mayor_interseccion == 'COMERCIO INTERNACIONAL':
            print(mayor_interseccion)
            carreras_etiquetadas[mayor_interseccion] += 1
        else:
            print('NO IDENTIFICADO')
            carreras_etiquetadas['NO IDENTIFICADO'] += 1
        #print(mayor_interseccion)
        #print(materias_diferentes)
        #print(json.dumps(set(mapa), indent = 2))
    encontrado = False
    carreras.rewind()
    # A continuación etiquetamos en la base al alumno con su carrera
    coll_trayectorias.update({'_id': boletas[index]}, {'$set':{'carrera' : mayor_interseccion}})
    # Revisamos la intersección más grande y calculamos la diferencia de los conjuntos, para ver qué materias son las que fallan
    #input()
    index += 1

print(json.dumps(carreras_etiquetadas, indent = 2))
print(len(materias_por_alumno))
