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
@st.cache_resource(ttl=300)
def get_cached_connection():
    return get_databricks_connection()

# Función para ejecutar queries y devolver un DataFrame
@st.cache_data(ttl=600)  # Cache de 10 minutos
def load_table(table_name, query_condition=""):
    """Carga una tabla. Acepta una condición WHERE opcional."""
    query = f"SELECT * FROM {table_name} {query_condition}"
    try:
        # Intenta usar la conexión que está en caché
        conn = get_cached_connection()
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=columns)
    except Exception as e:
        # Si falla (por ejemplo, conexión cerrada), limpia la caché de la conexión
        st.cache_resource.clear()
        
        # Vuelve a intentar con una conexión nueva
        try:
            conn = get_cached_connection()
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(result, columns=columns)
        except Exception as retry_error:
            # Si el segundo intento también falla, muestra el error
            st.error(f"Error al conectar con Databricks después de reintentar: {retry_error}")
            st.stop()

# --- Barra Lateral (Filtros) ---
st.sidebar.header("Filtros")

# --- Carga de datos ---# Cargamos todas las fechas disponibles en el resumen
try:
    df_fechas = load_table("gold_market_summary")
    df_fechas['ingestion_date'] = pd.to_datetime(df_fechas['ingestion_date']).dt.date
    fechas_disponibles = sorted(df_fechas['ingestion_date'].unique(), reverse=True)
except Exception as e:
    st.error(f"Error al cargar fechas: {e}")
    st.stop()

# Selector de fecha en la barra lateral (por defecto, la más reciente)
fecha_seleccionada = st.sidebar.selectbox(
    "Seleccioná una fecha:",
    options=fechas_disponibles,
    index=0
)

# --- Carga de datos filtrados por la fecha seleccionada ---
# Usamos la condición WHERE para traer solo el día elegido
condicion = f"WHERE ingestion_date = '{fecha_seleccionada}'"

try:
    df_summary = load_table("gold_market_summary", condicion)
    df_top10 = load_table("gold_top_10_market_cap", condicion).sort_values("market_cap_rank")
    df_gainers = load_table("gold_top_gainers", condicion).sort_values("price_change_pct_24h", ascending=False)
    df_losers = load_table("gold_top_losers", condicion).sort_values("price_change_pct_24h", ascending=True)
    
     #1. Extraemos dinámicamente los nombres de las 5 primeras monedas (las de mayor market cap hoy)
    # df_top10 ya está ordenado por market_cap_rank
    top_5_names = df_top10.head(5)['name'].tolist()
    
    # 2. Armamos el string para el SQL. Ej: "'Bitcoin', 'Ethereum', 'Tether', 'BNB', 'Solana'"
    top_5_names_str = ", ".join([f"'{name}'" for name in top_5_names])
    
    # 3. Hacemos la consulta a Silver usando ese string dinámico
    query_history = f"WHERE name IN ({top_5_names_str})"
    df_history = load_table("silver_coingecko_market", query_history)
    df_history['ingestion_date'] = pd.to_datetime(df_history['ingestion_date'])
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# --- KPIs Principales ---
st.subheader(f"Resumen del Mercado - {fecha_seleccionada}")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Monedas", f"{df_summary['total_monedas'][0]:,}")
col2.metric("Capitalización Total", f"${df_summary['capitalizacion_total_usd'][0]:,.0f}")
col3.metric("Volumen 24h", f"${df_summary['volumen_total_24h_usd'][0]:,.0f}")
col4.metric("Variación Promedio 24h", f"{df_summary['variacion_promedio_24h'][0]:.2f}%")

st.divider()

# --- Gráfico Histórico (NUEVO) ---
st.subheader("Evolución Histórica (Top 5 Monedas)")
fig_history = px.line(
    df_history, 
    x="ingestion_date", 
    y="current_price_usd", 
    color="name",
    markers=True,
    title="Precio en USD (Últimos días)",
    labels={"ingestion_date": "Fecha", "current_price_usd": "Precio (USD)", "name": "Moneda"}
)
st.plotly_chart(fig_history, use_container_width=True)

st.divider()

# --- Top 10 por Capitalización ---
st.subheader(f"Top 10 Monedas por Capitalización - {fecha_seleccionada}")
fig_top10 = px.bar(df_top10, x="name", y="market_cap_usd", 
                   title="Capitalización de Mercado (USD)",
                   labels={"name": "Moneda", "market_cap_usd": "Market Cap (USD)"},
                   color="price_change_pct_24h", color_continuous_scale="RdYlGn")
st.plotly_chart(fig_top10, use_container_width=True)

# --- Ganadoras y Perdedoras (24h) ---
col_g, col_l = st.columns(2)

with col_g:
    st.subheader("🚀 Top 5 Ganadoras (24h)")
    st.dataframe(df_gainers[['name', 'symbol', 'current_price_usd', 'price_change_pct_24h']], use_container_width=True, hide_index=True)

with col_l:
    st.subheader("📉 Top 5 Perdedoras (24h)")
    st.dataframe(df_losers[['name', 'symbol', 'current_price_usd', 'price_change_pct_24h']], use_container_width=True, hide_index=True)