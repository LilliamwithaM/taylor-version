import streamlit as st

def saludo(nombre):
    mymensaje = "bienvenido /a/e " + nombre
    return mymensaje

myname = st.text_input("nombre: ")
if (myname):
    mensaje = saludo(myname)
    st.write(f"Result: {mensaje}")