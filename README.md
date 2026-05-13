# 🌱 Dashboard Análisis de Suelos – Colombia

Dashboard interactivo de análisis fisicoquímico de suelos colombianos,
construido con **Streamlit**, **Plotly**, **Altair** y **Seaborn**.

## 📦 Instalación

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Ejecutar

```bash
# Asegúrate de que data.csv está en la misma carpeta que app.py
streamlit run app.py
```

El dashboard se abre automáticamente en `http://localhost:8501`

## 📁 Estructura

```
dashboard_suelos/
├── app.py            ← Aplicación principal Streamlit
├── data.csv          ← Dataset (Análisis Lab. Suelos Colombia)
├── requirements.txt  ← Dependencias Python
└── README.md
```

## 📊 Visualizaciones incluidas

| Tipo          | Librería  | Descripción                                      |
|---------------|-----------|--------------------------------------------------|
| Histograma    | Plotly    | Distribución del pH con zonas de referencia      |
| Scatter plot  | Plotly    | Correlación entre dos variables fisicoquímicas   |
| Box plot      | Plotly    | Distribución por cultivo (Top N)                 |
| Radar chart   | Plotly    | Perfil fisicoquímico comparativo por cultivo     |
| Heatmap       | Seaborn   | Matriz de correlación entre propiedades          |
| Bar chart     | Altair    | Variables por departamento                       |
| Donut chart   | Altair    | Distribución de categorías de pH                 |
| Serie temporal| Plotly    | Evolución de variables a lo largo del tiempo     |
| Tabla         | Streamlit | Estadísticas descriptivas completas              |

## 🎛️ Filtros del sidebar

- **Cultivo** – Filtra todos los gráficos por cultivo específico
- **Departamento** – Filtra por región geográfica
- **Variable X / Y** – Elige las variables fisicoquímicas a comparar
- **Top N cultivos** – Ajusta el número de cultivos en rankings

## 🧪 Variables fisicoquímicas

- pH (agua:suelo)
- Materia Orgánica (%)
- Fósforo Bray II (mg/kg)
- Azufre (mg/kg)
- Calcio, Magnesio, Potasio, Sodio intercambiables
- Capacidad de Intercambio Catiónico – CIC (cmol+/kg)
- Conductividad Eléctrica
- Micronutrientes: Fe, Cu, Mn, Zn, B disponibles
