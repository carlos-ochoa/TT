import streamlit as st
import hashlib
import subprocess
from utils.data import MongoConnection
from PIL import Image

import requests

from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

data_source = MongoConnection()
data_source.connect()

def main():
    col1,col2 = st.beta_columns([1,3])
    image = Image.open('utils/pdfCreation/images/escudoIPN.jpg')
    col1.image(image)
    col2.subheader('Prototipo de sistema de AA para la identificacion de riesgos para el IPN')
    st.subheader("Inicio de Sesión")
    form = st.form(key='Login')
    email = form.text_input("E-mail")
    password = form.text_input("Password",type='password')
    submit = form.form_submit_button('Login')
    lottie_url = "https://assets1.lottiefiles.com/packages/lf20_9kZ5Pz.json"
    lottie_json = load_lottieurl(lottie_url)
    st_lottie(lottie_json)
    if submit:
        hashed_password =  hashlib.sha256(str.encode(password)).hexdigest()
        usuario = data_source.get_usuario(email)
        if usuario is not None:
            if usuario['password'] == hashed_password:
                print('Correcto')
                st.success("Bienvenido")
                subprocess.Popen(["streamlit", "run", "app.py"])
            else:
                print('Password Incorrecto')
                st.error("Password Incorrecto")
        else:
            print('Correo no registrado')
            st.error("Correo no registrado")

if __name__ == '__main__':
	main()