import json
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://admin:Xtwj6YuW9fAYr2P@cluster0.r4oec.mongodb.net/db_TT?retryWrites=true&w=majority')
db = cluster['db_TT']

coll_kardex = db['Kardex']

kardex = coll_kardex.find()

periodos = []

# Esto es para sacar los periodos
for k in kardex:
    if k['kardex'] is not None:
        for s in k['kardex']:
            for p in k['kardex'][s]:
                periodos.append(p)

periodos = sorted(list(set(periodos)))
print(periodos)

aprobacion_por_periodo = {p:{'aprobado': [] , 'reprobado' : []} for p in periodos}

for k in kardex:
    if k['kardex'] is not None:
        for s in k['kardex']:
            for p in k['kardex'][s]:
                for m in k['kardex'][s][p]:
                    if int(k['kardex'][s][p][m]['calificacion']) < 6 or \
                        k['kardex'][s][p][m]['evaluacion'] == 'ETS':
                            aprobacion_por_periodo[p]['reprobado'].append(k['id'])
                            break
                    else:
                        aprobacion_por_periodo[p]['aprobado'].append(k['id'])

# Ahora volvemos sets las listas de aprobacion_por_periodo
