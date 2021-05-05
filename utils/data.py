import os
import dns
import time
import pathlib
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure, CursorNotFound, BulkWriteError

class MongoConnection(object):

    def __init__(self):
        self.db = None
        self.coll_trayectorias = None
        self.coll_indice_bajas = None

    def connect(self):
        # Obtenemos la ruta donde se encuentra el archivo de claves de conexion
        # Para evitar el hardcode de la información de acceso
        ruta = pathlib.Path(os.path.abspath(os.getcwd())).absolute()
        pass_file = 'keys.txt'
        conn_info = open(os.path.join(ruta,pass_file))
        mongo_conn_info = conn_info.readlines()[0]

        try:
            cluster = MongoClient(mongo_conn_info)
            self.db = cluster['db_TT']
            self.coll_trayectorias = self.db['Trayectorias']
            self.coll_indice_bajas = self.db['indice_bajas']
            self.coll_carreras = self.db['Carreras']
            self.coll_curso_actual_bajas = self.db['curso_actual_para_bajas']
            self.coll_curso_actual = self.db['curso_actual']
            self.coll_dictamenes = self.db['curso_actual_dictamenes']
            self.coll_usuarios=self.db['usuarios']
        except ConnectionFailure as c:
            sys.exit(c)
        return

    def get_trayectorias(self):
        try:
            trayectorias = self.coll_indice_bajas.find({'tipo_baja' : {'$exists' : True}})
            mapa_curricular = self.coll_carreras.find({'nombre' : 'CONTADOR PUBLICO'})
        except CursorNotFound as c:
            sys.exit(c)
        return trayectorias,mapa_curricular

    def get_tray_bajas(self):
        try:
            curso_actual_bajas = self.coll_curso_actual_bajas.find({})
        except CursorNotFound as c:
            sys.exit(c)
        return curso_actual_bajas

    def get_tray_reprobacion(self):
        pipeline = [
            { '$lookup':
                {
                   'from': "indice_bajas",
                   'localField': "_id",
                   'foreignField': "_id",
                   'as': "curso_a"
                }
            }
        ]
        try:
            curso_actual = self.db['curso_actual'].aggregate(pipeline)
            curso_actual = list(curso_actual)
        except CursorNotFound as c:
            sys.exit(c)
        return curso_actual

    def get_dictamen(self,id):
        try:
            dictamen = self.coll_indice_bajas.find({'_id' : id})
        except CursorNotFound as c:
            sys.exit(c)
        return dictamen

    def get_tray_baja_boleta(self, boleta):
        try:
            alumno = self.coll_curso_actual_bajas.find({'_id' : boleta})
            alumno = list(alumno)
            return alumno
        except CursorNotFound as c:
            sys.exit(c)
        #return alumno

    def get_materias(self):
        try:
             mapa_curricular = self.coll_carreras.find({'nombre' : 'CONTADOR PUBLICO'})
             for materia in mapa_curricular:
                 mapa_curricular_materias = dict(materia['materias'])
                 materias_obligatorias = [materia for materia,tipo in mapa_curricular_materias.items() if tipo == 'OBLIGATORIA']
        except CursorNotFound as c:
            sys.exit(c)
        return materias_obligatorias

    def get_dictamenes(self):
        try:
            dictamenes = self.coll_dictamenes.find({})
        except CursorNotFound as c:
            sys.exit(c)
        return dictamenes

    def get_trayectorias_adeudos(self):
        try:
            periodos_permitidos = ['10/1','10/2', '11/1', '11/2', '12/1', '12/2', '13/1', '13/2',
                                   '14/1', '14/2', '15/1', '15/2', '16/1', '16/2',
                                    '17/1', '17/2', '18/1', '18/2', '19/1', '19/2',
                                    '20/1']
            trayectorias = self.coll_indice_bajas.find({'periodo_de_ingreso' :{'$in': periodos_permitidos}})
        except CursorNotFound as c:
            sys.exit(c)
        return trayectorias

    def get_tray_baja_boleta_reprobacion(self, boleta):
        pipeline = [
            { '$lookup':
                {
                   'from': "indice_bajas",
                   'localField': "_id",
                   'foreignField': "_id",
                   'as': "curso_a"
                }
            }
        ]
        try:
            curso_actual = self.db['curso_actual'].aggregate(pipeline)
            curso_actual = list(curso_actual)
            for reg in curso_actual:
                if reg['_id'] == boleta:
                    return reg
        except CursorNotFound as c:
            sys.exit(c)

    def insertar_usuario(self, email,nombre,paterno,materno, password):
        try:
            query = { "_id": email, "nombre": nombre,"paterno":paterno, "materno":materno, "password":password}
            self.coll_usuarios.insert_one(query)
        except CursorNotFound as c:
            sys.exit(c)

    def get_usuario(self,email):
        try:
            usuario= self.coll_usuarios.find_one({ "_id":email })
            return usuario
        except CursorNotFound as c:
            sys.exit(c)
