import streamlit as st
import pandas as pd
import plotly.express as px
from auth import check_login
from db import query

# --- Autenticación ---
check_login()

# --- Título ---
st.title("📊 Dashboard de Ventas Globales - Superstore")

# --- Cargar datos desde la base de datos ---
df = query("SELECT * FROM ventas")

# --- Filtros avanzados ---
st.sidebar.header("Filtros")

years = sorted(df["Order Date"].str[:4].unique())
year_filter = st.sidebar.multiselect("Año", years, default=years)

categories = df["Category"].unique()
category_filter = st.sidebar.multiselect("Categoría", categories, default=categories)

regions = df["Region"].unique()
region_filter = st.sidebar.multiselect("Región", regions, default=regions)

df_filtered = df[
    df["Order Date"].str[:4].isin(year_filter) &
    df["Category"].isin(category_filter) &
    df["Region"].isin(region_filter)
]

# --- Métricas ---
col1, col2, col3 = st.columns(3)

col1.metric("Ventas Totales", f"{df_filtered['Sales'].sum():,.2f} €")
col2.metric("Beneficio Total", f"{df_filtered['Profit'].sum():,.2f} €")
col3.metric("Pedidos", f"{len(df_filtered)}")

# --- Gráfico 1: Ventas por mes ---
df_filtered["Order Date"] = pd.to_datetime(df_filtered["Order Date"])
df_filtered["Mes"] = df_filtered["Order Date"].dt.to_period("M").astype(str)

fig1 = px.line(
    df_filtered.groupby("Mes")["Sales"].sum().reset_index(),
    x="Mes", y="Sales",
    title="📈 Ventas por Mes",
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico 2: Ventas por Categoría ---
fig2 = px.bar(
    df_filtered.groupby("Category")["Sales"].sum().reset_index(),
    x="Category", y="Sales",
    title="📊 Ventas por Categoría",
    color="Category"
)
st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: Mapa de ventas por estado ---
if "State" in df_filtered.columns:
    fig3 = px.choropleth(
        df_filtered,
        locations="State",
        locationmode="USA-states",
        color="Sales",
        scope="usa",
        title="🗺️ Ventas por Estado"
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- Tabla final ---
st.subheader("📄 Datos filtrados")
st.dataframe(df_filtered)
