#  Crypto Data Pipeline & Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Databricks](https://img.shields.io/badge/Databricks-Free_Tier-orange.svg)
![SQL](https://img.shields.io/badge/SQL-Spark_SQL-lightgrey.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Pipeline de datos end-to-end (ETL) diseñado para extraer información del mercado de criptomonedas en tiempo real, procesarla utilizando la **Arquitectura Medallion** en Databricks, y visualizar los resultados en un dashboard interactivo.

 [![Ver Dashboard](https://img.shields.io/badge/_Ver_Dashboard_en_Vivo-Streamlit-red?style=for-the-badge)](https://ml-data-pipeline-jrp6rdenslzbvz2imfj5pf.streamlit.app/)

---

##  Arquitectura del Proyecto

El pipeline sigue la Arquitectura Medallion, garantizando la calidad y trazabilidad de los datos de principio a fin:

```text
API CoinGecko (JSON) 
   │
   ▼
[ Capa Bronze] ──> Ingesta cruda (Python/PySpark). Datos guardados como String para evitar conflictos de esquema.
   │
   ▼
[ Capa Silver] ──> Limpieza y Tipado (SQL). Casteo de datos a Double/Int, redondeo y deduplicación.
   │
   ▼
[ Capa Gold]   ──> Agregaciones de Negocio (SQL). Tablas listas para KPIs y visualizaciones.
   │
   ▼
[ Streamlit]   ──> Dashboard interactivo conectado en tiempo real vía databricks-sql-connector.
```
##  Tecnologías Utilizadas

*   **Procesamiento y Almacenamiento:** Databricks, PySpark, Spark SQL, Delta Lake.
*   **Ingesta:** Python (`requests`).
*   **Orquestación:** Databricks Workflows (Jobs con dependencias diarias).
*   **Visualización:** Streamlit (Community Cloud), Plotly, Pandas.
*   **Lenguajes:** Python y SQL.

##  Tablas Generadas (Capa Gold)

*   `gold_market_summary`: KPIs generales del mercado (Capitalización total, volumen operado 24h, etc.).
*   `gold_top_10_market_cap`: Ranking de las 10 principales monedas por capitalización.
*   `gold_top_gainers`: Las 5 monedas con mayor suba porcentual en las últimas 24 horas.
*   `gold_top_losers`: Las 5 monedas con mayor caída porcentual en las últimas 24 horas.

##  Características Técnicas Destacadas

*   **Automatización total:** Un Job en Databricks orquesta la ingesta y transformación diaria (Tarea Bronze ➔ Tarea Silver ➔ Tarea Gold).
*   **Manejo robusto de conexiones:** La app de Streamlit implementa un sistema de reintentos y TTL (Time-To-Live) para evitar caídas por inactividad del SQL Warehouse.
*   **Seguridad:** Las credenciales de Databricks (Host, HTTP Path, Token PAT) se manejan a través de secretos en Streamlit, nunca expuestas en el código.
*   **Calidad de Datos (Data Quality):** El pipeline incluye una tarea final de validación con PySpark que verifica que no haya precios nulos, valores negativos o registros duplicados antes de dar por exitosa la ejecución.
