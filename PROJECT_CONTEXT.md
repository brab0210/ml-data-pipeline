# Proyecto: Data Engineering Portfolio - Mercado Libre API

##  Objetivo General
Construir un pipeline ETL (Bronze → Silver → Gold) con Databricks (Free Edition), consumiendo la API de Mercado Libre, y visualizar los resultados en un dashboard (Streamlit o Looker Studio).

##  Arquitectura y Stack
- **Fuente:** API Mercado Libre (endpoint `/sites/MLA/search`)
- **Ingesta:** Python (requests) → Databricks
- **Almacenamiento:** Delta Lake (Tablas Bronze, Silver, Gold)
- **Orquestación:** Databricks Workflows (Free Edition)
- **Dashboard:** Streamlit Community Cloud (o Looker Studio)
- **Control de versiones:** GitHub

##  Estado Actual (Actualizar al final de cada sesión)
- **Etapa actual:** Semana 1 - Exploración de API y creación de la capa Bronze.
- **Última tarea completada:** [Ej: Autenticación exitosa con la API y prueba de extracción de 100 ítems.]
- **Próxima tarea a realizar:** [Ej: Escribir el notebook de ingesta y guardar los datos crudos en una tabla Delta Bronze.]
- **Decisiones tomadas:** Se usará Streamlit para el dashboard por afinidad con Python/Web.
