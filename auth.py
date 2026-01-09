import streamlit as st

def login():
    st.sidebar.header("Acceso al Dashboard")
    user = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    login_btn = st.sidebar.button("Entrar")

    if login_btn:
        if user == "admin" and password == "1234":
            st.session_state["logged"] = True
        else:
            st.sidebar.error("Credenciales incorrectas")

def check_login():
    if "logged" not in st.session_state or not st.session_state["logged"]:
        login()
        st.stop()
