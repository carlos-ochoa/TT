import pandas as pd
import numpy as np
from collections import Counter
from pymongo.errors import ConnectionFailure, CursorNotFound
from utils.data import MongoConnection

def generar_vector(alumno,materias_obligatorias):
    vectores=[]  
    for periodo in alumno['trayectoria']:
        for materia in alumno['trayectoria'][periodo]:
            if materia['nombre'] in materias_obligatorias:
                vector=[]
                vector.append(periodo)
                vector.append(materia['nombre'])
                vector.append(materia['evaluacion'])
                vector.append(materia['calificacion'])
                vectores.append(vector)
    return vectores

def generar_vectores(materias_obligatorias):
    data_source = MongoConnection()
    data_source.connect()
    trayectorias=data_source.get_trayectorias_adeudos()
    dataset = []
    columns = ['periodo','materia','evaluacion','calificacion']
    for trayectoria in trayectorias:
        vector_resultado=generar_vector(trayectoria,materias_obligatorias)
        dataset.extend(vector_resultado)

    dataset = np.array(dataset)
    df = pd.DataFrame(dataset, columns = columns)

    return df

def vectorizacion(materias_obligatorias):
    df=generar_vectores(materias_obligatorias)
    periodos_permitidos = ['10/1','10/2', '11/1', '11/2', '12/1', '12/2', '13/1', '13/2', 
                                   '14/1', '14/2', '15/1', '15/2', '16/1', '16/2', 
                                    '17/1', '17/2', '18/1', '18/2', '19/1', '19/2',
                                    '20/1']
    materias_por_periodo = df.groupby('periodo')
    nuevos_vectores=[]
    for periodo in periodos_permitidos:
        cursadas_periodo= materias_por_periodo.get_group(periodo)
        cursadas=cursadas_periodo.groupby('materia')
        for obligatoria in materias_obligatorias:
            if not cursadas_periodo[cursadas_periodo.materia.isin([obligatoria])].empty:
                nuevo_vector=[]
                nuevo_vector.append(periodo)
                nuevo_vector.append(obligatoria)
                materia_cursada=cursadas.get_group(obligatoria)
                materia_cursada['calificacion'] = materia_cursada['calificacion'].astype(int)
                values=[5,4,3,2,1,0]
                values_aprobatorios=[10,9,8,7,6]
                filtrado_abandono = materia_cursada[materia_cursada.calificacion.isin(values)]
                total_abandono=filtrado_abandono.shape[0]
                media = materia_cursada['calificacion'].mean()
                nuevo_vector.append(media)
                total_rows = materia_cursada.shape[0]
                nuevo_vector.append(total_rows)
                materia_cursada=materia_cursada[materia_cursada.calificacion.isin(values_aprobatorios)]
                total=materia_cursada['evaluacion'].value_counts().rename_axis('evaluacion').reset_index(name='total')
                ordinario=total[total.evaluacion.isin(['ORD'])]
                extraordinario=total[total.evaluacion.isin(['EXT'])]
                ets=total[total.evaluacion.isin(['ETS'])]
                recurse=total[total.evaluacion.isin(['REC'])]
                if(not ordinario.empty):
                    p_ordinario=ordinario.iloc[0]['total']/total_rows
                else:
                    p_ordinario=0.0
                if(not extraordinario.empty):
                    p_extraordinario=extraordinario.iloc[0]['total']/total_rows
                else:
                    p_extraordinario=0.0
                if( not ets.empty):
                    p_ets=ets.iloc[0]['total']/total_rows
                else:
                    p_ets=0.0
                if(not recurse.empty):
                    p_recurse=recurse.iloc[0]['total']/total_rows
                else:
                    p_recurse=0.0

                nuevo_vector.append(p_ordinario)
                nuevo_vector.append(p_extraordinario)
                nuevo_vector.append(p_ets)
                nuevo_vector.append(p_recurse)
                total_abandono=total_abandono/total_rows
                total_reprobados=p_extraordinario+p_ets+p_recurse+total_abandono
                nuevo_vector.append(total_abandono)
                nuevo_vector.append(total_reprobados)
                nuevos_vectores.append(nuevo_vector)
    columns_nuevas = ['periodo','materia','media','total_inscritos','ordinario','extraordinaro','ets','recurse','adeudos','reprobados']
    dataset_nuevo = np.array(nuevos_vectores)
    df_vectorizado = pd.DataFrame(nuevos_vectores, columns = columns_nuevas)
    
    for i in df_vectorizado.index:
        periodo=df_vectorizado['periodo'][i]
        df_vectorizado['periodo'][i]='20'+periodo
        fecha=df_vectorizado['periodo'][i]
        fecha=fecha.replace('/1','-01')
        fecha=fecha.replace('/2','-08')
        df_vectorizado['periodo'][i]=fecha
    df_vectorizado['periodo'] = pd.to_datetime(df_vectorizado['periodo'], format='%Y-%m')
    resultados_por_materia_periodo = df_vectorizado.groupby('materia')
    resultados_por_materia_periodo.index=resultados_por_materia_periodo['periodo']
    return resultados_por_materia_periodo

def vectores_materias(resultados_por_materia_periodo, materia):
    datos_agrupados=resultados_por_materia_periodo.get_group(materia)
    datos_agrupados.index=datos_agrupados['periodo']
    return datos_agrupados
