import numpy as np
import numpy as np
from collections import Counter
from pymongo.errors import ConnectionFailure, CursorNotFound
from utils.data import MongoConnection

def generar_vectores(vectores_reprobacion, vectores_bajas, pred_rep, pred_baja):
    # De 0 a 47 se controlan las materias en el vector de reprobacion
    # En 11 se controla la cantidad total de materias en vector_bajas
    egresa_a_tiempo = 0
    vectores_eficiencia = []
    total_materias = 48
    for rep,baj,p_rep,p_baj in zip(vectores_reprobacion, vectores_bajas, pred_rep, pred_baja):
        materias_inscritas = 0
        for materia in rep[:48]:
            if materia != 0:
                materias_inscritas += 1
        # Si con estas materias termina su trayectoria...
        if total_materias - baj[11] + materias_inscritas <= 0:
            if p_rep == 1:
                egresa_a_tiempo = 0
            else:
                if p_baj == 1:
                    egresa_a_tiempo = 0
                else:
                    egresa_a_tiempo = 1
            vectores_eficiencia.append(egresa_a_tiempo)
    return vectores_eficiencia


def generar_distribucion(predicciones):
    distribucion = []
    c = dict(Counter(predicciones))
    print(c)
    try:
        for value,count in c.items():
            if value == 0:
                distribucion.append({'value' : count, 'name' : 'No egresado'})
            else:
                distribucion.append({'value' : count, 'name' : 'Egresado'})
    except:
        pass
    if 0 in c.keys():
        indice = 1 - (c[0] / sum(c.values()))
    else:
        indice = 1
    return distribucion, indice