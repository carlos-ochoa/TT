from fpdf import FPDF
import base64
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import os

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

def  create_plotPNG(distribucion,nombre):
    nombres = []
    data = []
    for i in distribucion:
        nombres.append(i['name'])
        data.append(i['value'])
    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, labels = nombres,autopct='%1.1f%%')
    plt.title("Distribución de "+nombre,bbox={'facecolor':'0.8','pad':5})
    path = "utils/pdfCreation/images/" + nombre +".png"
    plt.savefig(path,dpi=300)
    print(os.getcwd())
    print('png creado')

def create_plotPNG_line(vector, nombre, materia):

    indexes = []
    values = []
    plt.figure(figsize=(10, 7), dpi=70)
    for index, value in vector.items():
    #    print(f"Index : {index}, Value : {value}")
        indexes.append(index)
        values.append(value)
    plt.plot(indexes, values)
    plt.title(nombre + materia)
    plt.xlabel('Año')
    plt.ylabel('Porcentaje ' + materia)
    path = "utils/pdfCreation/images/" + nombre +".png"
    plt.savefig(path)
    print('png creado')

def create_general_report(distribucion_reprobacion, distribucion_bajas,distribucion_eficiencia, distribucion_dictamenes, materia_vectores, ocupabilidad_materia, materia,materia_ocupabilidad):
    ancho = 210
    alto = 297
    create_plotPNG(distribucion_reprobacion,"reprobacion")
    create_plotPNG(distribucion_bajas,"bajas")
    create_plotPNG(distribucion_eficiencia,"eficienciaTerminal")
    create_plotPNG(distribucion_dictamenes,"dictamen")
    create_plotPNG_line(materia_vectores, "reprobacionMateria", materia)
    create_plotPNG_line(ocupabilidad_materia, "ocupabilidadMateria", materia_ocupabilidad)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.set_text_color(r =17, g = 193, b = 244)
    pdf.ln(15)
    c = ''
    numero = 0
    while numero <= 30:
        c = c + '\t'
        numero = numero + 1
    pdf.write(5,c + 'Reporte de identificación de riesgos')
    pdf.ln(30)
    pdf.set_font('Arial','',10)
    pdf.set_text_color(r =0, g = 0, b = 0)
    pdf.write(5,'Distribución de bajas: Este indice explica el porcentaje de alumnos que pueden caer en situacion de desercion durante el semestre en curso. Se pueden elegir los niveles de analisis para identificar los grupos semestrales en mayor riesgo.')
    pdf.ln(10)
    pdf.write(5,'Distribución de dictaminados: Este indice explica el indice esperado de alumnos dictaminados que cumpliran su materia.')
    pdf.ln(90)
    pdf.write(5,'Distribución de eficiencia terminal: Este indice explica el porcentaje de alumnos que terminaran su carrera satisfactoriamente aportando a la eficiencia terminal semestral')
    pdf.ln(10)
    pdf.write(5,'Distribución de reprobación: Este indice explica el porcentaje de alumnos que pueden caer en situacion de reprobación de almenos una materia durante el nivel en curso. Se pueden elegir los niveles de analisis para identificar los grupos semestrales en mayor riesgo.')
    pdf.image("utils/pdfCreation/images/escudoIPN.jpg",5,10,50,40)
    pdf.image("utils/pdfCreation/images/escudoESCA.png",160,10,40,40)
    pdf.image("utils/pdfCreation/images/bajas.png",5,80,ancho/2-5)
    pdf.image("utils/pdfCreation/images/dictamen.png",ancho/2+5,80,ancho/2-5)
    pdf.image("utils/pdfCreation/images/eficienciaTerminal.png",5,220,ancho/2-5)
    pdf.image("utils/pdfCreation/images/reprobacion.png",ancho/2+5,220,ancho/2-5)
    pdf.add_page()
    pdf.ln(25)
    pdf.write(5,'Índice de ocupabilidad: Este indice determina la cantidad de alumnos que cursarán cada materia el siguiente periodo.')
    pdf.ln(10)
    pdf.write(5,'Índice de reprobación: Este indice explica el porcentaje de alumnos que reprobarán cada materia por semestre')
    pdf.image("utils/pdfCreation/images/ocupabilidadMateria.png",5,50,ancho/2-5)
    pdf.image("utils/pdfCreation/images/reprobacionMateria.png",ancho/2+5,50,ancho/2-5)
    pdf.set_text_color(r =0, g = 0, b = 0)
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), 'Riesgos generales')
    st.markdown(html, unsafe_allow_html=True)


def create_individual_report(boleta,reprobacion, baja,dictamen ,materia_dictamen ):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.set_text_color(r =17, g = 193, b = 244)
    pdf.ln(15)
    c = ''
    numero = 0
    while numero <= 30:
        c = c + '\t'
        numero = numero + 1
    pdf.write(5,c + 'Reporte de identificación de riesgos')
    pdf.ln(30)
    pdf.set_text_color(r =0, g = 0, b = 0)
    pdf.set_font('Arial', 'B', 13)
    pdf.write(5,'Resultados del alumno: ' + boleta)
    pdf.ln(10)

    ####
    pdf.set_font('Arial','B',12)
    pdf.write(5,'Dictamen: ')
    pdf.set_font('Arial','',11)
    #resultado_dictamen = 'Cumple' if prediccion_dictamen[0] == 1 else 'No cumple'
    if dictamen == 2:
        pdf.write(5,'El alumno no tuvo dictamen')#No hubo dictamen
    if dictamen == 0:
        pdf.write(5,'Dictamen activo: ')
        pdf.write(5,materia_dictamen)
        pdf.ln(5)
        pdf.write(5,'El alumno no cumplirá su dictamen')
        ##No Cumple
    if dictamen == 1:
        pdf.write(5,'Dictamen activo: ')
        pdf.write(5,materia_dictamen)
        pdf.ln(5)
        pdf.write(5,'El alumno cumplirá su dictamen')
        #si cumple
    pdf.ln(10)
    ####
    pdf.set_font('Arial','B',12)
    pdf.write(5,'Reprobación: ')
    pdf.set_font('Arial','',11)
    if reprobacion == 1:
        pdf.write(5,'El alumno es propenso a reprobar')
    else :
        pdf.write(5,'El alumno no es propenso a reprobar')
    pdf.ln(10)

    ###
    pdf.set_font('Arial','B',12)
    pdf.write(5,'Baja: ')
    pdf.set_font('Arial','',11)

    if baja == 1:
        pdf.write(5,'El alumno es propenso a darse de baja')
    else :
        pdf.write(5,'El alumno no es propenso a darse de baja')
    pdf.ln(10)


    ####
    pdf.set_font('Arial','B',13)
    pdf.write(5,'Indice de reprobación')
    pdf.ln(10)
    pdf.set_font('Arial','',10)
    pdf.write(4,'Este modelo nos permite predecir si es que el alumno esta en riesgo de reprobar alguna de las materias que inscribió en su nuevo curso.')
    pdf.ln(10)
    ####
    pdf.set_font('Arial','B',13)
    pdf.write(5,'Dictamen')
    pdf.ln(10)
    pdf.set_font('Arial','',10)
    pdf.write(4,'Este modelo nos permite predecir si es que el alumno esta en riesgo de no cumplir su dictamen.')
    pdf.ln(10)

    ###
    pdf.set_font('Arial','B',13)
    pdf.write(5,'Indice de baja')
    pdf.ln(10)
    pdf.set_font('Arial','',10)
    pdf.write(4,'Este modelo nos permite predecir si es que el alumno esta en riesgo de darse de baja.')
    pdf.ln(10)
    ###


    pdf.image("utils/pdfCreation/images/escudoIPN.jpg",5,10,50,40)
    pdf.image("utils/pdfCreation/images/escudoESCA.png",160,10,40,40)

    pdf.output('test.pdf','F')
    nombre = 'reporte de ' + boleta
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), nombre)
    st.markdown(html, unsafe_allow_html=True)
