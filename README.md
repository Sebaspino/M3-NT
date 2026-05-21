# README.md

# 🌱 README — Dashboards de Nuevas Tecnologías

## 🚀 Demo en vivo

👉 **[https://m3-ntgit-jqgpibpemn2cvsaxytzn8f.streamlit.app/](https://m3-ntgit-jqgpibpemn2cvsaxytzn8f.streamlit.app/)**

---

## 📌 Descripción General

Este módulo corresponde al desarrollo de los dashboards analíticos construidos para el proyecto integrador, enfocados en:

- 🌱 **Dashboard de Laboratorio de Suelos**
- 🧪 **Dashboard SerenityLab Analytics**

La solución fue desarrollada utilizando tecnologías modernas orientadas a visualización de datos, analítica interactiva y exploración avanzada de información.

El objetivo principal de este componente fue transformar datos técnicos y operativos en información visual, dinámica y comprensible para apoyar la toma de decisiones.

---

# 🧠 Tecnologías Utilizadas

## Backend Analítico

| Tecnología | Uso Principal |
|---|---|
| Python | Lenguaje principal del proyecto |
| Pandas | Procesamiento y manipulación de datos |
| NumPy | Operaciones numéricas y estadísticas |
| SciPy | Procesamiento científico y estadístico |
| Statsmodels | Modelado y análisis estadístico |

---

## Visualización y Dashboards

| Tecnología | Función |
|---|---|
| Streamlit | Framework principal para dashboards interactivos |
| Plotly | Gráficos interactivos avanzados |
| Altair | Visualizaciones declarativas |
| Seaborn | Análisis estadístico visual |
| Matplotlib | Gráficos complementarios |

---

## Comunicación y APIs

| Tecnología | Función |
|---|---|
| Requests | Consumo de APIs REST |
| JSON | Intercambio de datos entre servicios |

---

# 📂 Estructura del Proyecto

```bash
NuevasTecnologias/
│
├── Inicio.py
├── data.csv
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 1_Análisis Exploratorio de Datos (EDA).py
│   ├── 2_Resultados (EDA).py
│   ├── 3_Graficos de laboratorio.py
│   └── 4_SerenityLab_Analitica.py
│
└── .streamlit/
    └── config.toml
```

---

# 🌱 Dashboard de Laboratorio de Suelos

## 📖 Descripción

Este dashboard fue diseñado para analizar información fisicoquímica de muestras de suelo agrícola en Colombia.

El sistema permite realizar:

- Exploración de datos (EDA)
- Limpieza y validación de información
- Identificación de patrones
- Comparación de variables químicas
- Análisis estadístico descriptivo
- Visualización geográfica y comparativa
- Detección de anomalías

---

# 📊 Funcionalidades Implementadas

## 🔍 Exploración de Datos (EDA)

Se desarrolló un módulo completo de análisis exploratorio que permite:

- Identificar valores nulos
- Revisar tipos de datos
- Detectar inconsistencias
- Analizar distribuciones
- Obtener métricas descriptivas
- Validar calidad de datos

### Librerías utilizadas

- Pandas
- NumPy
- Streamlit

---

## 📈 Visualizaciones Interactivas

El dashboard incluye múltiples tipos de gráficos avanzados:

| Visualización | Tecnología |
|---|---|
| Histogramas | Plotly |
| Scatter Plots | Plotly |
| Boxplots | Plotly |
| Radar Charts | Plotly |
| Heatmaps | Seaborn |
| Barras Dinámicas | Altair |
| Donut Charts | Altair |
| Series Temporales | Plotly |
| Tablas Interactivas | Streamlit |

---

## 🧪 Variables Analizadas

Entre las variables del laboratorio se incluyen:

- pH
- Materia orgánica
- Fósforo
- Azufre
- Calcio
- Magnesio
- Potasio
- Sodio
- Conductividad eléctrica
- CIC (Capacidad de Intercambio Catiónico)
- Micronutrientes

---

## 🎛️ Sistema de Filtros

El dashboard cuenta con filtros dinámicos que permiten:

- Filtrar por cultivo
- Filtrar por departamento
- Seleccionar variables X/Y
- Ajustar Top N de cultivos
- Segmentar información estadística

Todos los componentes se actualizan en tiempo real.

---

## 🎨 Diseño UI/UX

Se implementó una interfaz moderna utilizando:

- Paletas de colores personalizadas
- Sidebar estilizado
- Tema claro optimizado
- Distribución responsive
- Métricas visuales
- Componentes visuales dinámicos

---

# 🧪 Dashboard SerenityLab Analytics

## 📖 Descripción

El dashboard SerenityLab Analytics fue desarrollado como una plataforma analítica orientada a visualización de métricas clínicas y operativas.

Este módulo consume información desde un backend mediante API REST y presenta los datos en tiempo real utilizando componentes visuales modernos.

---

# 🔌 Integración con Backend

La aplicación utiliza comunicación HTTP mediante:

```python
requests
```

Conexión principal:

```python
BASE_URL = "http://localhost:8080"
```

Esto permite:

- Obtener información en tiempo real
- Consultar endpoints dinámicos
- Consumir métricas analíticas
- Integrar servicios externos

---

# 📊 Funcionalidades SerenityLab

## 📈 Métricas Analíticas

El dashboard presenta:

- Indicadores operativos
- Estadísticas generales
- Métricas clínicas
- Análisis comparativos
- Tendencias
- KPIs visuales

---

## 📉 Visualización Avanzada

Se desarrollaron componentes visuales utilizando:

- Plotly Graph Objects
- Indicadores personalizados
- Tarjetas métricas
- Gráficos dinámicos
- Layouts interactivos

---

## 🎨 Sistema de Diseño SerenityLab

Se creó una identidad visual personalizada basada en:

- Paleta rosa/púrpura
- Componentes translúcidos
- Bordes suaves
- Dashboard responsive
- Experiencia visual moderna

Colores principales:

```python
S_DARK  = "#831843"
S_MED   = "#be185d"
S_BASE  = "#ec4899"
S_LIGHT = "#f472b6"
```

---

# ⚙️ Configuración del Entorno

## 📦 Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## 📥 Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ▶️ Ejecución del Proyecto

## Ejecutar Streamlit

```bash
streamlit run Inicio.py
```

La aplicación se ejecutará normalmente en:

```bash
http://localhost:8501
```

---

# 📦 Dependencias Principales

```txt
streamlit>=1.35.0
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
altair>=5.2.0
seaborn>=0.13.0
matplotlib>=3.8.0
scipy>=1.11.0
statsmodels>=0.14.0
```

---

# 🏗️ Arquitectura General

## Flujo de Datos

```text
Dataset / API
      ↓
Procesamiento con Pandas
      ↓
Análisis Estadístico
      ↓
Visualizaciones Interactivas
      ↓
Dashboard Streamlit
```

---

# 🔥 Características Técnicas Destacadas

## ✅ Modularidad

El proyecto fue dividido en páginas independientes para facilitar:

- Escalabilidad
- Mantenimiento
- Reutilización
- Integración de nuevas funcionalidades

---

## ✅ Interactividad

Todos los dashboards fueron desarrollados con componentes dinámicos:

- Filtros en tiempo real
- Componentes reactivos
- Actualización automática
- Navegación intuitiva

---

## ✅ Escalabilidad

La arquitectura permite integrar:

- Modelos predictivos
- Machine Learning
- Nuevos datasets
- APIs externas
- Bases de datos

---

# 📚 Aprendizajes y Tecnologías Aplicadas

Durante el desarrollo se trabajó con:

- Analítica de datos
- Diseño de dashboards
- Visualización avanzada
- Arquitectura modular
- Integración frontend/backend
- Consumo de APIs
- Estadística aplicada
- UI/UX para analítica

---

# 👥 Equipo de Desarrollo

| Integrante | Rol |
|---|---|
| Sebastián Pino | Líder Analista de Datos |
| Jefferson Suaza | Desarrollador de Datos |
| Luisa Yepez | Desarrolladora de Soluciones |

---

# 🚀 Posibles Mejoras Futuras

- Integración con bases de datos SQL
- Autenticación de usuarios
- Despliegue en la nube
- Integración con IA predictiva
- Dashboards en tiempo real
- Exportación de reportes PDF/Excel
- Machine Learning para predicción
- Automatización de análisis

---

# 📌 Conclusión

El módulo de Nuevas Tecnologías representa la capa analítica e interactiva del proyecto integrador.

A través de Streamlit y herramientas modernas de visualización, se construyeron dashboards profesionales orientados a transformar datos complejos en información clara, visual y útil para la toma de decisiones.

El proyecto demuestra la integración efectiva entre:

- Ciencia de datos
- Desarrollo de software
- Visualización interactiva
- Diseño de experiencia de usuario
- Analítica aplicada

---

# 🛠️ Tecnologías Clave del Proyecto

```text
Python
Streamlit
Plotly
Pandas
NumPy
Altair
Seaborn
Matplotlib
SciPy
Statsmodels
Requests
```