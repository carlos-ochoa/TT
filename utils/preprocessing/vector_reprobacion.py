import numpy as np
from collections import Counter

def generar_vectores(trayectorias_reprobacion, trayectorias,nivel):
    mapa_curricular = trayectorias[1]
    dictamen = trayectorias[0]
    for m in mapa_curricular:
      mapa_curricular_materias = dict(m['materias'])
    materias_obligatorias = [materia for materia,tipo in mapa_curricular_materias.items() if tipo == 'OBLIGATORIA']
    vectores_totales = []
    vectores_rose = []
    for alumno in trayectorias_reprobacion:
        if nivel == 'Total' or int(nivel) == alumno['nivel']:
            vectores = []
            vector = [0 for i in range(51)]
            vector_rose = [alumno['nivel']]
            vectores_rose.append(vector_rose.copy())
            for dic in alumno['curso_a']:
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
    return np.array(vectores_totales),vectores_rose

def obtener_rose_distribution(vectores,predicciones):
    p = []
    for v in vectores:
        p.append(v[0])
    periodos = sorted(list(set(p)))
    distribucion = {str(pe):0 for pe in periodos}
    for i,v in enumerate(vectores):
        if predicciones[i] == 1:
            distribucion[str(v[0])] += 1
    d = [{"value" : v, "name" : k} for k,v in distribucion.items()]
    return d

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

def generar_vector_individual(alumno, trayectorias):
    mapa_curricular = trayectorias[1]
    dictamen = trayectorias[0]
    for m in mapa_curricular:
      mapa_curricular_materias = dict(m['materias'])
    materias_obligatorias = [materia for materia,tipo in mapa_curricular_materias.items() if tipo == 'OBLIGATORIA']
    vectores = []
    vector = [0 for i in range(51)]
    print(alumno['curso_a'])
    for dic in alumno['curso_a']:
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
    return np.array(vectores)
