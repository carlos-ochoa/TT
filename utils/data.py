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
        except ConnectionFailure as c: 
            sys.exit(c)
        return

    def get_trayectorias(self):
        try:
            trayectorias = self.coll_trayectorias.find({'carrera' : 'CONTADOR PUBLICO'})
        except CursorNotFound as c:
            sys.exit(c)
        return trayectorias