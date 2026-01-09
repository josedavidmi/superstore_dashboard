import sqlite3
import pandas as pd
import streamlit as st

@st.cache_resource
def init_db(csv_path="data/superstore.csv"):
    conn = sqlite3.connect(":memory:")  # Base de datos en memoria
    df = pd.read_csv(csv_path)
    df.to_sql("ventas", conn, if_exists="replace", index=False)
    return conn

def query(sql):
    conn = init_db()
    return pd.read_sql(sql, conn)
