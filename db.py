import sqlite3
import pandas as pd
import streamlit as st
import os

@st.cache_resource
def init_db():
    """
    Carga el CSV desde el repositorio y crea una base de datos SQLite en memoria.
    Compatible con Streamlit Cloud.
    """

    # Ruta absoluta dentro del contenedor de Streamlit Cloud
    csv_path = os.path.join("data", "superstore.csv")

    if not os.path.exists(csv_path):
        st.error(f"No se encontró el archivo CSV en: {csv_path}")
        st.stop()

    # Intento de lectura con varios encodings
    encodings = ["utf-8", "latin1", "utf-8-sig"]

    for enc in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        st.error("No se pudo leer el CSV con ningún encoding conocido.")
        st.stop()

    # Crear base de datos en memoria
    conn = sqlite3.connect(":memory:")
    df.to_sql("ventas", conn, if_exists="replace", index=False)

    return conn


def query(sql):
    """
    Ejecuta una consulta SQL sobre la base de datos en memoria.
    """
    conn = init_db()
    return pd.read_sql(sql, conn)
