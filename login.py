import streamlit as st
import hashlib
import subprocess
from utils.data import MongoConnection
data_source = MongoConnection()
data_source.connect()

def main():
    st.title("Prototipo de sistema de AA para la identificacion de riesgos para el IPN")
    st.subheader("Inicio de Sesión")
    form = st.form(key='Login')
    email = form.text_input("E-mail")
    password = form.text_input("Password",type='password')
    submit = form.form_submit_button('Login')
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