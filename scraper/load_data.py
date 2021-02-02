import json
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import random
#from scraper import Alumno, Materia, Adeudo, Dictamen, Baja

cluster = MongoClient('mongodb+srv://admin:Xtwj6YuW9fAYr2P@cluster0.r4oec.mongodb.net/db_TT?retryWrites=true&w=majority')
db = cluster['db_TT']
coll_students = db['Alumnos']
coll_kardex = db['Kardex']
coll_dicts = db['Dictamenes']
coll_drops = db['Bajas']
coll_debts = db['Adeudos']

new_kardex, new_subjects, new_debts, new_students, new_dicts, new_drops = [],[],[],[],[],[]

with open('info_saes.txt', encoding = 'UTF-8') as info:
    text = info.read()
    json_info = json.loads(text)
    for k,v in json_info.items():
        if isinstance(v,dict):
            #json_form_str = json.dumps(json_info[k], indent = 2)
            #print(json_form_str)
            if 'genero' in v.keys():
                student = {'_id':v['boleta'], 'genero':v['genero'], 'promedio':v['promedio'], 'avance':v['avance']}
            else:
                student = {'_id':v['boleta'], 'genero':None, 'promedio':None, 'avance':None}
            new_students.append(student)
            # Subjects
            if 'kardex' in v.keys():
                subjects = {'_id':v['boleta'],'kardex':v['kardex']}
            else:
                subjects = {'_id':v['boleta'],'kardex':None}
            new_subjects.append(subjects)
            # Debts
            debt = {'_id':v['boleta'], 'adeudos':v['adeudos']}
            new_debts.append(debt)
            # Dict
            debt = {'_id':v['boleta'], 'dictamenes':v['dictamenes']}
            new_dicts.append(debt)
            # Drops
            debt = {'_id':v['boleta'], 'bajas':v['bajas']}
            new_drops.append(debt)
            #input()
    try:
        '''coll_students.delete_many({})
        coll_kardex.delete_many({})
        coll_debts.delete_many({})
        coll_dicts.delete_many({})
        coll_drops.delete_many({})'''
        coll_students.insert_many(new_students, ordered = False)
        coll_kardex.insert_many(new_subjects, ordered = False)
        coll_debts.insert_many(new_debts, ordered = False)
        coll_dicts.insert_many(new_dicts, ordered = False)
        coll_drops.insert_many(new_drops, ordered = False)
    except BulkWriteError as e:
        print(e.details)
