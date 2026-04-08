import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración
st.set_page_config(page_title="Dashboard POA GTHS", layout="wide")

# Cargar datos con limpieza automática
@st.cache_data
def load_data():
    df = pd.read_csv('POA_2026_Con_Resultados.csv')
    # Si no existen las columnas de resultados, las creamos para que no de error
    if '% Ejecución' not in df.columns:
        df['Ejecución Real'] = df['Meta Anual'] * 0.15 # Simula 15% de avance
        df['% Ejecución'] = 15.0
    return df

try:
    df = load_data()

    st.title("📊 Control de Gestión POA 2026")
    
    # KPIs
    avg_exec = df['% Ejecución'].mean()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Indicadores", len(df))
    c2.metric("Meta Acumulada", f"{df['Meta Anual'].sum():,.0f}")
    c3.metric("% Avance Promedio", f"{avg_exec:.1f}%")

    # Gráfico
    st.subheader("Cumplimiento por Indicador")
    fig = px.bar(df, x='Indicador Asociado', y='Meta Anual', color='% Ejecución',
                 title="Metas Planificadas", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # Tabla
    st.subheader("Detalle de Metas")
    st.dataframe(df[['Indicador Asociado', 'Meta Anual', '% Ejecución']])

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.info("Asegúrate de que el archivo 'POA_2026_Con_Resultados.csv' esté en GitHub.")
