import numpy as np
from collections import Counter
from pymongo.errors import ConnectionFailure, CursorNotFound
from utils.data import MongoConnection


def generar_vectores(trayectorias_reprobacion, mapa_curricular):
    data_source = MongoConnection()
    data_source.connect()
    for m in mapa_curricular:
      mapa_curricular_materias = dict(m['materias'])
    materias_obligatorias = [materia for materia,tipo in mapa_curricular_materias.items() if tipo == 'OBLIGATORIA']
    vectores_totales = []
    for alumno in trayectorias_reprobacion:
        vectores = []
        vector = [0 for i in range(51)]
        dictamen = data_source.get_dictamen(alumno['_id'])
        for dic in dictamen:
            if(dic['tiene_dictamen'] == "si"):
                vector[0] = 1
            else:
                vector[0] = 0
        vector[49] = 0
        for materia in alumno['materias']:
            if materia in materias_obligatorias:
                index = materias_obligatorias.index(materia)
            else:
                index = 47
                vector[index+1] = 1
        vectores.append(vector)
        vectores_totales.extend(vectores)
    return np.array(vectores_totales)

def generar_distribucion(predicciones):
    distribucion = []
    c = dict(Counter(predicciones))
    print(c)
    try:
        for value,count in c.items():
            if value == 0:
                distribucion.append({'value' : count, 'name' : 'Aprobado'})
            else:
                distribucion.append({'value' : count, 'name' : 'Reprobado'})
    except:
        pass
    if 0 in c.keys():
        indice = 1 - (c[0] / sum(c.values()))
    else:
        indice = 1
    return distribucion, indice
