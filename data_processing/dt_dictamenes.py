from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CursorNotFound
import dns
import random

# Obtenemos la ruta donde se encuentra el archivo de claves de conexion
# Para evitar el hardcode de la información de acceso

try:
    cluster = MongoClient("mongodb+srv://admin:Xtwj6YuW9fAYr2P@cluster0.r4oec.mongodb.net/db_TT?retryWrites=true&w=majority")
    db = cluster['db_TT']
    coll_boletas = db['curso_actual']
    coll_carreras = db['Carreras']
    coll_dictamenes = db['Dictamenes']
    coll_curso_actual = db['curso_actual_dictamenes']
except ConnectionFailure as c: 
    sys.exit(c)

try:
    boletas = coll_boletas.find({})
    dictamenes = coll_dictamenes.find({})
    pipeline = [
                {'$lookup': 
                  {'from' : 'indice_bajas',
                  'localField' : '_id',
                  'foreignField' : '_id',
                  'as' : 'dictamenes_contador'
                  }
                }
                ]
    dictamenes = coll_dictamenes.aggregate(pipeline)
    dictamenes = list(dictamenes)
    mapa_curricular = coll_carreras.find({'nombre' : 'CONTADOR PUBLICO'})
except CursorNotFound as c:
    sys.exit(c)

dataset_dictamenes = []

def convertir_periodo(periodo):
  periodo = periodo[2:]
  periodo_convertido = periodo[:2] + '/' + periodo[-1]
  return periodo_convertido

def obtener_boletas():
    boletas_data = []
    boletas_finales = []
    for alumno in boletas:
        boletas_data.append(alumno['_id'])
    for i in range(119):
        boleta = boletas_data[random.randint(0,len(boletas_data)-1)]
        boletas_finales.append(boleta)
    return boletas_finales

periodos_permitidos = ['10/1','10/2', '11/1', '11/2', '12/1', '12/2', '13/1',
                       '13/2', '14/1', '14/2', '15/1', '15/2', '16/1', '16/2', 
                       '17/1', '17/2', '18/1', '18/2', '19/1', '19/2','20/1','20/2']
i = 0
boletas_finales = obtener_boletas()
for reg in dictamenes:
  for dic in reg['dictamenes_contador']:
    if len(dic) > 0 and dic['periodo_de_ingreso'] in periodos_permitidos and dic['tiene_dictamen'] == 'si':
      for dictamen in reg['dictamenes']:
        dictamen_individual = {}
        dictamen_individual['boleta'] = boletas_finales[i]
        dictamen_individual['materia'] = dictamen['materia']
        dictamen_individual['inicio'] = convertir_periodo(dictamen['inicio'])
        dictamen_individual['periodo_de_ingreso'] = dic['periodo_de_ingreso']
        dictamen_individual['materias_cursadas'] = dic['materias_cursadas']
        dictamen_individual['cumplio'] = dictamen['cumplio']
        dataset_dictamenes.append(dictamen_individual.copy())
        i += 1
      #print(reg)
      #print(dic)
      #input()

coll_curso_actual.insert_many(dataset_dictamenes)