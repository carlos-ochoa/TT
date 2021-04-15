import os
import dns
import pathlib
from pymongo import MongoClient
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
