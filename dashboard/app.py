import streamlit as st
import pandas as pd
import plotly.express as px
from databricks import sql

st.set_page_config(page_title="Crypto Dashboard", page_icon="🪙", layout="wide")

st.title("🪙 Crypto Market Dashboard")
st.markdown("Datos en tiempo real desde Databricks (Capa Gold).")

# --- Configuración de la conexión (lee los secretos de Streamlit) ---
def get_databricks_connection():
    return sql.connect(
        server_hostname=st.secrets["DATABRICKS_HOST"],
        http_path=st.secrets["DATABRICKS_HTTP_PATH"],
        access_token=st.secrets["DATABRICKS_TOKEN"]
    )

# Cache de la conexión para no reconectar en cada interacción
@st.cache_resource
def get_cached_connection():
    return get_databricks_connection()

# Función para ejecutar queries y devolver un DataFrame
@st.cache_data(ttl=600)  # Cache de 10 minutos
def load_table(table_name):
    with get_cached_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=columns)

# --- Carga de datos ---
try:
    df_summary = load_table("gold_market_summary")
    df_top10 = load_table("gold_top_10_market_cap")
    df_gainers = load_table("gold_top_gainers")
    df_losers = load_table("gold_top_losers")
except Exception as e:
    st.error(f"Error al conectar con Databricks: {e}")
    st.stop()

# --- KPIs Principales ---
st.subheader("Resumen del Mercado")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Monedas", f"{df_summary['total_monedas'][0]:,}")
col2.metric("Capitalización Total", f"${df_summary['capitalizacion_total_usd'][0]:,.0f}")
col3.metric("Volumen 24h", f"${df_summary['volumen_total_24h_usd'][0]:,.0f}")
col4.metric("Variación Promedio 24h", f"{df_summary['variacion_promedio_24h'][0]:.2f}%")

st.divider()

# --- Top 10 por Capitalización ---
st.subheader("Top 10 Monedas por Capitalización")
fig_top10 = px.bar(df_top10, x="name", y="market_cap_usd", 
                   title="Capitalización de Mercado (USD)",
                   labels={"name": "Moneda", "market_cap_usd": "Market Cap (USD)"},
                   color="price_change_pct_24h", color_continuous_scale="RdYlGn")
st.plotly_chart(fig_top10, use_container_width=True)

# --- Ganadoras y Perdedoras (24h) ---
col_g, col_l = st.columns(2)

with col_g:
    st.subheader("🚀 Top 5 Ganadoras (24h)")
    st.dataframe(df_gainers, use_container_width=True, hide_index=True)

with col_l:
    st.subheader("📉 Top 5 Perdedoras (24h)")
    st.dataframe(df_losers, use_container_width=True, hide_index=True)