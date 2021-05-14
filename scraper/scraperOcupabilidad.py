from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
import json
from pickle import load, dump

class Ocupabilidad:
    periodo = None
    grupo= None
    clave_materia = None
    materia= None
    semestre = None
    cupo = None
    inscritos = None

    def __init__(self, periodo,grupo, clave_materia,materia, semestre, cupo, inscritos):
        self.periodo=periodo
        self.grupo = grupo
        self.clave_materia = clave_materia
        self.materia=materia
        self.semestre = semestre
        self.cupo = cupo
        self.inscritos = inscritos

registros=[]
options = Options()
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
driver = webdriver.Chrome(chrome_options = options, executable_path=r'chromedriver_win.exe')
driver.maximize_window()
driver.get('https://www.saes.escasto.ipn.mx')
anos = ['20212','20211','20202','20192','20191','20182','20181','20172','20171','20162','20161','20152'
'20151','20142','20141','20132','20131','20122','20121','20112','20111','20102','20101','20092','20091']
foo = input()
driver.find_element_by_id('ctl00_mainCopy_rblEsquema_1').click()
driver.find_element_by_id('ctl00_mainCopy_dpdcarrera').send_keys('CONTADOR PÚBLICO')
for ano in anos:
    driver.find_element_by_id('ctl00_mainCopy_dpdPeriodoEscolarHist').send_keys(ano)
    tabla = driver.find_element_by_id('ctl00_mainCopy_GrvOcupabilidad').find_element_by_tag_name('tbody')
    lista_tr = tabla.find_elements_by_tag_name('tr')
    for tr in lista_tr[1:]:
        lista_td = tr.find_elements_by_tag_name('td')
        ocupabilidad = Ocupabilidad(ano, lista_td[0].text,lista_td[1].text, lista_td[2].text, lista_td[3].text,lista_td[4].text,lista_td[5].text)
        registros.append(ocupabilidad.__dict__)

with open('info_ocupabilidad.txt','w') as archivo:
    json.dump(registros,archivo)
