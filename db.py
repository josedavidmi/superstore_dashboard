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

    csv_path = os.path.join("data", "superstore.csv")

    if not os.path.exists(csv_path):
        st.error(f"No se encontró el archivo CSV en: {csv_path}")
        st.stop()

    # Lector robusto que ignora caracteres inválidos
    try:
        df = pd.read_csv(
            csv_path,
            encoding="latin1",
            engine="python",
            on_bad_lines="skip"   # ignora líneas corruptas
        )
    except Exception as e:
        st.error(f"Error leyendo el CSV: {e}")
        st.stop()

    # Limpieza de caracteres invisibles como 0xA0
    df = df.applymap(
        lambda x: x.replace("\xa0", " ") if isinstance(x, str) else x
    )

    # Crear base de datos en memoria
    conn = sqlite3.connect(":memory:")
    df.to_sql("ventas", conn, if_exists="replace", index=False)

    return conn


def query(sql):
    conn = init_db()
    return pd.read_sql(sql, conn)
