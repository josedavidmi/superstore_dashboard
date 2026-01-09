import sqlite3
import pandas as pd

def init_db(csv_path="data/superstore.csv"):
    conn = sqlite3.connect("superstore.db")
    df = pd.read_csv(csv_path)
    df.to_sql("ventas", conn, if_exists="replace", index=False)
    conn.close()

def query(sql):
    conn = sqlite3.connect("superstore.db")
    df = pd.read_sql(sql, conn)
    conn.close()
    return df
