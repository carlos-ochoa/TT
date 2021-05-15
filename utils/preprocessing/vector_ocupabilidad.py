import pandas as pd
import numpy as np

path_json = 'utils\preprocessing\info_ocupabilidad.txt'
periodos = ['20212','20211','20202','20192','20191','20182','20181','20172','20171','20162','20161','20152'
'20151','20142','20141','20132','20131','20122','20121','20112','20111','20102','20101','20092','20091']

def vectorizacion():
    df = pd.read_json(path_json)
    df[['periodo','grupo','clave_materia','materia']]=df[['periodo','grupo','clave_materia','materia']].astype(str)
    print(df.dtypes)

    for i in df.index:
        periodo=df['periodo'][i]
        tamano=len(periodo)
        ano=periodo[:-1]
        fecha=''
        if periodo[tamano-1]=='1':
            fecha=ano+'-01'
        else:
            fecha=ano+'-08'
        df['periodo'][i]=fecha

    df['periodo'] = pd.to_datetime(df['periodo'], format='%Y-%m')
    df=df[['periodo', 'materia','cupo','inscritos']]
    df=df.groupby(['periodo', 'materia'],as_index=False).sum()
    return df

def vector_materia(df,materia):
    materias=df.groupby('materia')
    materia_cursada=materias.get_group(materia)
    materia_cursada.index=materia_cursada['periodo']
    print(materia_cursada.head())
    return materia_cursada