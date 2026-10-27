# Proyecto: Data Engineering Portfolio - CoinGecko API

##  Objetivo General
Construir un pipeline ETL end-to-end (Bronze → Silver → Gold) utilizando Databricks Free Edition, consumiendo la API pública de CoinGecko, y visualizar los resultados en un dashboard interactivo (Streamlit).

##  Arquitectura y Stack
- **Fuente de Datos:** API pública de CoinGecko (`/coins/markets`), sin autenticación (top 50 monedas).
- **Ingesta (Bronze):** Python (requests, PySpark) → Tabla Delta `bronze_coingecko_market` (datos crudos como string).
- **Limpieza (Silver):** SQL en Databricks → Tabla Delta `silver_coingecko_market` (casteo de tipos, limpieza de nulos, redondeo).
- **Negocio (Gold):** SQL en Databricks → Tablas Delta agregadas (`gold_market_summary`, `gold_top_10_market_cap`, `gold_top_gainers`, `gold_top_losers`).
- **Orquestación:** Databricks Workflows (Free Edition).
- **Dashboard:** Streamlit Community Cloud (gratuito).
- **Control de versiones:** GitHub (integrado con Databricks Git folders).

##  Estado Actual
- **Etapa actual:** Dashboard funcional y desplegado - Finalizado.
- **Última tarea completada:** Conexión de Streamlit a Databricks mediante `databricks-sql-connector` y despliegue en Streamlit Community Cloud.
- **Próxima tarea a realizar:** (Opcional) Implementar una barra lateral con filtros interactivos o añadir más visualizaciones.
- **Decisiones tomadas:** Se optó por la Opción A (conexión en tiempo real vía PAT) en lugar de exportar CSVs.

##  Notas para el próximo chat / IA
- El usuario tiene bases de desarrollo web, lo cual es ideal para personalizar el frontend en Streamlit.
- Todo el desarrollo se hace bajo el paradigma "Free Tier" (Databricks Free, Streamlit Cloud, GitHub).
