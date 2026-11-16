# Proyecto Integrador Big Data - E-Commerce Olist

Proyecto académico orientado a la **optimización logística, el análisis de
ventas y la evaluación del nivel de servicio** de la plataforma brasileña
Olist. El análisis integra procesamiento con PySpark, simulación de streaming,
visualización avanzada y un dashboard interactivo desarrollado con Streamlit.

## 1. Contextualización

Olist conecta comercios y compradores dentro del comercio electrónico
brasileño. El proyecto analiza demoras logísticas entre estados, diferencias en
los costos de transporte, cancelaciones, pedidos no entregados y calificaciones
de los compradores.

El problema afecta principalmente a:

- gerentes de logística y operaciones;
- vendedores afiliados cuya reputación puede verse afectada;
- clientes que reciben pedidos tarde o no los reciben;
- responsables comerciales que necesitan conocer las categorías y medios de
  pago más importantes.

El análisis responde cuatro preguntas de negocio:

1. ¿Qué estados presentan mayores retrasos y qué porcentaje de pedidos llega
   después de la fecha estimada?
2. ¿Cómo se relacionan el tiempo de entrega y el valor del flete con la
   calificación del cliente?
3. ¿Qué categorías generan mayores ingresos y cuáles tienen el ticket promedio
   más alto?
4. ¿Qué medios de pago concentran mayor volumen y cuál presenta mayor tasa de
   cancelación o pedidos no entregados?

## 2. Dataset

Se utiliza el
[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce),
un conjunto de datos públicos y reales publicado en Kaggle.

El repositorio incluye `data/olist_analitico_limpio.csv`, una tabla depurada con
una fila por pedido, utilizada directamente por el dashboard. También incluye
las nueve tablas fuente en `data/raw`, por lo que el notebook puede ejecutarse
completo después de clonar el repositorio sin modificar rutas ni descargar
archivos adicionales.

## 3. Componentes del proyecto

- **PySpark batch:** lectura distribuida, transformaciones, agregaciones,
  `groupBy`, joins y consultas con Spark SQL.
- **Structured Streaming:** simulación de micro-lotes y actualización de
  métricas acumuladas.
- **NumPy:** cálculo vectorizado de métricas logísticas y comerciales.
- **Matplotlib y Seaborn:** histogramas y análisis de correlación.
- **Plotly:** gráficos interactivos.
- **Streamlit:** dashboard con cuatro KPIs, seis gráficos y tres filtros.

## 4. Estructura del repositorio

```text
ProyectoFinal_BigData/
|-- app.py
|-- notebook.ipynb
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- data/
|   |-- olist_analitico_limpio.csv
|   `-- raw/
|       |-- olist_customers_dataset.csv
|       |-- olist_geolocation_dataset.csv
|       |-- olist_order_items_dataset.csv
|       |-- olist_order_payments_dataset.csv
|       |-- olist_order_reviews_dataset.csv
|       |-- olist_orders_dataset.csv
|       |-- olist_products_dataset.csv
|       |-- olist_sellers_dataset.csv
|       `-- product_category_name_translation.csv
`-- tools/
    `-- hadoop/
        `-- bin/
            |-- hadoop.dll
            `-- winutils.exe
```

## 5. Requisitos previos

- Python 3.11 o 3.12.
- Java 17 para las secciones de PySpark.
- Git, si se desea clonar el repositorio.
- VS Code con las extensiones **Python** y **Jupyter**, o Jupyter Notebook.

## 6. Instructivo de instalación y ejecución

### Paso 1. Descargar el proyecto

La forma recomendada es clonar el repositorio:

```powershell
git clone https://github.com/jguerra-max/ProyectoFinal_BigData.git
cd ProyectoFinal_BigData
```

También puede utilizarse **Code > Download ZIP** desde GitHub y extraer el ZIP
en una carpeta local.

### Paso 2. Crear un entorno virtual

Este paso es recomendado para evitar conflictos con otras instalaciones de
Python:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell muestra el prefijo `(.venv)`, el entorno quedó activado.

### Paso 3. Instalar `requirements.txt`

El archivo no se ejecuta ni se abre manualmente. Se utiliza con `pip` para
instalar todas las librerías del notebook y del dashboard:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

La instalación incluye Pandas, NumPy, Matplotlib, Seaborn, Plotly, PySpark,
Jupyter y Streamlit.

### Paso 4. Verificar el dataset incluido

No es necesario descargar archivos adicionales. Antes de ejecutar, confirmar
que existan:

```text
data/olist_analitico_limpio.csv
data/raw/olist_orders_dataset.csv
```

El notebook localiza automáticamente la raíz del repositorio y utiliza
`data/raw`. El dashboard utiliza `data/olist_analitico_limpio.csv`.

### Paso 5. Registrar y seleccionar el kernel

Con el entorno virtual activado:

```powershell
python -m ipykernel install --user --name olist_bigdata --display-name "Python (Olist BigData)"
```

Después, en VS Code:

1. Abrir `notebook.ipynb`.
2. Pulsar **Select Kernel** en la esquina superior derecha.
3. Seleccionar **Jupyter Kernel**.
4. Elegir **Python (Olist BigData)**.

Para comprobar el kernel:

```python
import sys
print(sys.executable)
```

La ruta mostrada debe terminar en `.venv\Scripts\python.exe`.

### Paso 6. Ejecutar el notebook

Abrir `notebook.ipynb` y seleccionar **Run All**. Las celdas están organizadas
en el siguiente orden:

1. configuración e importación de librerías;
2. auditoría y depuración del dataset;
3. construcción de la tabla analítica;
4. métricas vectorizadas con NumPy;
5. visualizaciones con Matplotlib, Seaborn y Plotly;
6. procesamiento batch con PySpark;
7. simulación con Structured Streaming;
8. conclusiones por pregunta de negocio y conclusión general.

La primera ejecución puede tardar varios minutos, especialmente en las etapas
de PySpark y Streaming.

### Paso 7. Ejecutar el dashboard

Desde la raíz del repositorio y con el entorno virtual activado:

```powershell
python -m streamlit run app.py
```

Streamlit abrirá el dashboard en el navegador. Si no se abre automáticamente,
visitar:

```text
http://localhost:8501
```

El dashboard permite filtrar por:

- estados del cliente;
- categoría del producto;
- medio de pago.

Los KPIs y los seis gráficos se recalculan automáticamente al cambiar los
filtros.

### Paso 8. Detener Streamlit

Regresar a la terminal donde se está ejecutando Streamlit y pulsar:

```text
Ctrl + C
```

## 7. Solución de errores frecuentes

### `ModuleNotFoundError`

El notebook está utilizando un kernel distinto del entorno donde se instalaron
las librerías. Seleccionar **Python (Olist BigData)** y reiniciar el kernel.

También puede comprobarse la instalación con:

```powershell
python -m pip install -r requirements.txt
```

### No se encuentran las tablas Olist

Verificar que `data/raw` exista dentro de la carpeta clonada y contenga los
nueve archivos CSV. No es necesario editar `DATA_DIR` ni escribir una ruta
absoluta del computador.

### PySpark no inicia

Comprobar la instalación de Java:

```powershell
java -version
```

Se recomienda utilizar Java 17 y reiniciar VS Code después de instalarlo.

### Streamlit no encuentra el dataset

Verificar la existencia de:

```text
data/olist_analitico_limpio.csv
```

El archivo debe conservar exactamente ese nombre y ubicación.

## 8. Integrantes

- Ferney Morales
- Julián Guerra
- Nicolás Samacá
