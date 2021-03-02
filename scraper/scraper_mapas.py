from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
import json
from collections import defaultdict
from pickle import load, dump

class Carrera(object):
    def __init__(self, nombre):
        self.nombre = nombre
        self.materias = defaultdict(dict)

carreras = ['ADMINISTRACION Y DESARROLLO EMPRESARIAL', 
            'CONTADOR PUBLICO', 'COMERCIO INTERNACIONAL',
            'NEGOCIOS INTERNACIONALES','RELACIONES COMERCIALES']

mapas_curriculares = []

driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
driver.get('https://www.saes.escasto.ipn.mx/EJECUTIVO/default.aspx')

foo = input()

for carrera in carreras:
    info_carrera = Carrera(carrera)
    while True:
        tabla = driver.find_element_by_id('ctl00_mainCopy_GridView1').find_elements_by_tag_name('tbody')
        tabla_tr = tabla[0].find_elements_by_tag_name('tr')
        for tr in tabla_tr[1:]:
            tabla_td = tr.find_elements_by_tag_name('td')
            info_carrera.materias[tabla_td[2].text] = tabla_td[3].text
            print(tabla_td[2].text)
        respuesta = input('¿Cambiar al siguiente periodo?')
        if respuesta == 'n':
            break
    mapas_curriculares.append(info_carrera.__dict__)
    with open('carreras.pkl','wb') as carreras_info:
        dump(mapas_curriculares,carreras_info)
    input('Cambia de carrera')   

print(mapas_curriculares) 