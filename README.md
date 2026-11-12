# Proyecto Integrador — Big Data 2026-2

**Universidad Santo Tomas — Seccional Tunja**
Ingenieria de Sistemas — Big Data 2026-2

## Integrantes

- Ferney Morales
- Julian Guerra
- Nicolas Samaca

## Problematica

Se analiza el dataset publico de Olist (e-commerce brasileno) para entender los factores que afectan la logistica de entregas, la satisfaccion del cliente y el comportamiento de ventas por categoria y metodo de pago. El objetivo es responder preguntas de negocio concretas usando tecnicas de Big Data.

## Dataset

**Brazilian E-Commerce Public Dataset by Olist** — disponible en Kaggle:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

- 98,666+ registros reales de pedidos
- 9 archivos CSV relacionados (orders, items, customers, payments, reviews, products, sellers, geolocation, traduccion de categorias)

## Tematicas

1. **PySpark (Batch):** carga, limpieza, consultas SQL y pruebas de integracion con Spark
2. **Streaming:** simulacion de micro-batches con Structured Streaming sobre los datos de Olist
3. **Visualizacion:** graficas con matplotlib, seaborn y plotly respondiendo 4 preguntas de negocio

## Preguntas de negocio

1. Cuales estados tienen mayor porcentaje de entregas tardias respecto al tiempo estimado?
2. Como se relaciona el tiempo de entrega y el valor de flete con la calificacion del cliente?
3. Cuales son las categorias con mayor ingreso y cual es el ticket promedio por categoria?
4. Cual es el volumen por metodo de pago y su relacion con el riesgo de no entrega?

## Estructura del repositorio

```
proyecto-integrador-bigdata/
├── archive/                  # CSVs originales de Olist
├── notebook_integrador_limpio.ipynb   # Notebook con las 3 tematicas
├── app.py                    # Dashboard interactivo (Streamlit + Plotly)
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo
```

## Como ejecutar

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el notebook

Abrir `notebook_integrador_limpio.ipynb` en Jupyter o VS Code y ejecutar todas las celdas.

Requisitos: Java 17+, HADOOP_HOME configurado con winutils.exe (para PySpark en Windows).

### 3. Ejecutar el dashboard

```bash
streamlit run app.py
```

Se abre en el navegador con filtros interactivos y graficas de Plotly.

## Declaracion de uso de IA

Se utilizo asistencia de IA (OpenAI Codex) como apoyo en la estructuracion del codigo y depuracion de errores. Todo el analisis, las preguntas de negocio y las conclusiones fueron elaborados por los integrantes del equipo.
