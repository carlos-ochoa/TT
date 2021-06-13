import numpy as np
from collections import Counter

def generar_vectores(trayectorias):
    vectores = []
    for trayectoria in trayectorias:
        vector = [0 for i in range(14)]
        for index,periodo in enumerate(trayectoria['trayectoria']):
            if periodo == 'aprobado':
                vector[index] = 1
            elif periodo == 'reprobado':
                vector[index] = 2
        vector[11] = trayectoria['materias_inscritas']
        vector[12] = trayectoria['periodos_cursados']
        vector[13] = 1 if trayectoria['tiene_dictamen'] == 'si' else 0
        vectores.append(vector.copy())
    return np.array(vectores)

def obtener_rose_distribution(vectores,predicciones):
    p = []
    for v in vectores:
        p.append(v[12]+1)
    periodos = sorted(list(set(p)))
    distribucion = {str(pe):0 for pe in periodos}
    for i,v in enumerate(vectores):
        if predicciones[i] == 1:
            distribucion[str(v[12]+1)] += 1
    d = [{"value" : v, "name" : k} for k,v in distribucion.items()]
    return d

def filtrar_vectores(vectores, predicciones, semestre = 'Total'):
    vectores_filtrados, predicciones_filtradas = [], []
    if semestre == 'Total':
        return vectores, predicciones
    for vector,prediccion in zip(vectores,predicciones):
        if int(semestre) == vector[12]+1:
            print(semestre,vector[12]+1,prediccion,vector)
            vectores_filtrados.append(vector.copy())
            predicciones_filtradas.append(prediccion)
    print(len(vectores_filtrados))
    return np.array(vectores_filtrados), predicciones_filtradas

def generar_distribucion(predicciones):
    distribucion = []
    c = dict(Counter(predicciones))
    print(c)
    try:
        for value,count in c.items():
            if value == 0:
                distribucion.append({'value' : count, 'name' : 'Sin baja'})
            else:
                distribucion.append({'value' : count, 'name' : 'Con baja'})
    except:
        pass
    if 0 in c.keys():
        indice = 1 - (c[0] / sum(c.values()))
    else:
        indice = 1
    return distribucion, indice

