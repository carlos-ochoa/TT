import random

ruta = pathlib.Path(os.path.abspath(os.getcwd())).parent.absolute()
pass_file = 'keys.txt'
conn_info = open(os.path.join(ruta,pass_file))
mongo_conn_info = conn_info.readlines()[0]

try:
    cluster = MongoClient(mongo_conn_info)
    db = cluster['db_TT']
    coll_curso_actual = db['curso_actual']
except ConnectionFailure as c:
    sys.exit(c)
try:
    curso_actual = coll_curso_actual.find({})
except CursorNotFound as c:
    sys.exit(c)

def generar_trayectoria(boleta):
    registro = {}
    registro['_id'] = boleta
    limit = random.randint(1,11)
    dictamen_estado = ['no','si']
    estados = ['no cursado','aprobado','reprobado']
    periodos = ['no cursado' for i in range(11)]
    # Inscritas totales
    for i in range(limit):
        periodos[i] = estados[random.randint(1,2)]
    materias = random.randint(4,7)
    dictamen = dictamen_estado[random.randint(0,1)]
    registro['trayectoria'] = periodos
    registro['materias_inscritas'] = materias
    registro['periodos_cursados'] = limit 
    registro['tiene_dictamen'] = dictamen
    return registro

alumnos = []
registro = {}
for alumno in curso_actual:
    registro = generar_trayectoria(alumno['_id'])    
    alumnos.append(registro)

coll_curso_actual.insert_many(alumnos)