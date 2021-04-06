import pandas as pd

periodos_permitidos = ['10/1','10/2', '11/1', '11/2', '12/1', '12/2', '13/1', '13/2', 
                        '14/1', '14/2', '15/1', '15/2', '16/1', '16/2', 
                        '17/1', '17/2', '18/1', '18/2', '19/1', '19/2',
                         '20/1']

def calcular_periodos_inscrito(row):
  inicio = periodos_permitidos.index(row['ingreso'])
  fin = periodos_permitidos.index(row['ultimo'])
  return fin - inicio + 1

def convertir_dictamen(row):
  valor = 0
  if row['dictamen'] == 'si':
    valor = 1
  return valor

def obtener_clase(row):
  clase = 0
  if row['tipo_baja'] != 'sin baja':
    clase = 1
  return clase

def procesar_dataframe(data):
  periodos_inscrito = data.apply(lambda row : calcular_periodos_inscrito(row), axis = 1)
  tiene_dictamen = data.apply(lambda row : convertir_dictamen(row), axis = 1)
  baja = data.apply(lambda row : obtener_clase(row), axis = 1)
  data['periodos_inscrito'] = periodos_inscrito
  data['tiene_dictamen'] = tiene_dictamen
  data['baja'] = baja
  numeric_data = data.drop(labels = ['ingreso','ultimo','dictamen','tipo_baja'], axis = 1)
  numeric_data = numeric_data.apply(pd.to_numeric)
  return numeric_data

def encontrar_periodos_consecutivos(periodo_inicio,periodos_alumno):
    es_consecutivo = 1
    periodo_baja = None
    indice_inicio = periodos_permitidos.index(periodo_inicio)
    subconjunto_periodos = periodos_permitidos[indice_inicio:]
    for indice,periodo in enumerate(periodos_alumno):
        if not subconjunto_periodos[indice] == periodo:
            es_consecutivo = 0
            periodo_baja = subconjunto_periodos[indice-1]
            break
    return es_consecutivo, periodo_baja

def encontrar_periodos_cursados(trayectoria):
    periodos = []
    for periodo in trayectoria:
        periodos.append(periodo)
    periodos = sorted(periodos)
    try:
        del periodos[periodos.index('21/1')]
    except:
        pass
    try:
        del periodos[periodos.index('20/2')]
    except:
        pass
    return periodos

def generar_vector_con_reprobacion(trayectorias):
  dataset = []
  numeros = [str(n) for n in range(1,12)]
  columns = ['ingreso','ultimo','dictamen']
  columns.extend(numeros)
  columns.extend(['inscritas_totales','tipo_baja'])
  for alumno in trayectorias:
    vectores = []
    materias_inscritas = 0
    numero_periodo = 1
    vector = [0 for i in range(16)]
    vector[0] = alumno['periodo_de_ingreso']
    vector[1] = alumno['ultimo_periodo'] if alumno['ultimo_periodo'] != '21/1' or alumno['ultimo_periodo'] != '20/2' else '20/1'
    if vector[1] == '21/1' or vector[1] == '20/2':
      vector[1] = '20/1'
    vector[2] = alumno['tiene_dictamen']
    # Aqui indicamos si la trayectoria es continua o no 
    periodos_cursados = encontrar_periodos_cursados(alumno['trayectoria'])
    _,periodo_baja = encontrar_periodos_consecutivos(vector[0], periodos_cursados)
    vector[1] = periodo_baja if periodo_baja != None else vector[1]
    p = 3
    for periodo in alumno['trayectoria']:
      if periodo != '21/1' or periodo != '20/2':
        if periodo == periodo_baja:
          break
        else:
          for materia in alumno['trayectoria'][periodo]:
            if int(materia['calificacion']) > 6:
              resultado_periodo = 1 # cursado y aprobado
            else:
              resultado_periodo = 2 # cursado y reprobado
              break
            materias_inscritas += 1
          if p > 10:
            p = 11
          vector[p] = resultado_periodo
          numero_periodo += 1
      p += 1
    vector[14] = materias_inscritas
    vector[15] = alumno['tipo_baja']
    vectores.append(vector)
    dataset.extend(vectores)
  dataset = pd.DataFrame(dataset, columns = columns)
  return dataset

