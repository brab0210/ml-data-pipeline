#  Crypto Data Pipeline & Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Databricks](https://img.shields.io/badge/Databricks-Free_Tier-orange.svg)
![SQL](https://img.shields.io/badge/SQL-Spark_SQL-lightgrey.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Pipeline de datos end-to-end (ETL) diseñado para extraer información del mercado de criptomonedas en tiempo real, procesarla utilizando la **Arquitectura Medallion** en Databricks, y visualizar los resultados en un dashboard interactivo.

 **[Ver Dashboard en Vivo](https://ml-data-pipeline-jrp6rdenslzbvz2imfj5pf.streamlit.app/)**

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
