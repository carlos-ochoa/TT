from fpdf import FPDF
import base64
import streamlit as st


def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

def create_individual_report(boleta,reprobacion, baja,dictamen ,materia_dictamen ):
    ancho = 210
    alto = 297
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
    pdf.write(4,'Este modelo nos permite predecir si es que el alumno esta en riesgo de reprobar alguna de las materias que inscribió en su nuevo curso.')
    pdf.ln(10)

    ###
    pdf.set_font('Arial','B',13)
    pdf.write(5,'Indice de baja')
    pdf.ln(10)
    pdf.set_font('Arial','',10)
    pdf.write(4,'Este modelo nos permite predecir si es que el alumno esta en riesgo de reprobar alguna de las materias que inscribió en su nuevo curso.')
    pdf.ln(10)
    ###


    pdf.image("utils/pdfCreation/escudoIPN.jpg",5,10,50,40)
    pdf.image("utils/pdfCreation/escudoESCOM.jpg",160,10,40,40)

    pdf.output('test.pdf','F')
    nombre = 'reporte de ' + boleta
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), nombre)
    st.markdown(html, unsafe_allow_html=True)
