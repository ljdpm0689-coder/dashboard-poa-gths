import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard POA GTHS 2026", layout="wide", page_icon="📈")

# 2. Estilo CSS para un look moderno
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

# 3. Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv('POA_2026_Con_Resultados.csv')

df = load_data()

# 4. Título y Filtros
st.title("📈 Dashboard de Ejecución POA 2026")
st.markdown("### Dirección de Talento Humano y Servicios")

with st.sidebar:
    st.header("⚙️ Configuración")
    eje_selec = st.multiselect("Filtrar por Eje:", df['Eje Estratégico'].unique(), default=df['Eje Estratégico'].unique())
    
df_filt = df[df['Eje Estratégico'].isin(eje_selec)]

# 5. KPIs de Impacto
promedio_ejecucion = df_filt['% Ejecución'].mean()
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Indicadores", len(df_filt))
col2.metric("Meta Total", f"{df_filt['Meta Anual'].sum():,.0f}")
col3.metric("Ejecución Real", f"{df_filt['Ejecución Real'].sum():,.1f}")
col4.metric("% Avance Promedio", f"{promedio_ejecucion:.1f}%", delta=f"{promedio_ejecucion-100:.1f}%")

st.divider()

# 6. Visualizaciones Interactivas
c1, c2 = st.columns([1.5, 1])

with c1:
    st.subheader("📊 Comparativa: Meta vs. Real")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_filt['Indicador Asociado'], y=df_filt['Meta Anual'], name='Meta Anual', marker_color='#D3D3D3'))
    fig.add_trace(go.Bar(x=df_filt['Indicador Asociado'], y=df_filt['Ejecución Real'], name='Ejecución Real', marker_color='#1f77b4'))
    fig.update_layout(barmode='group', xaxis_tickangle=-45, height=450, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🎯 Cumplimiento por Eje")
    fig_sun = px.sunburst(df_filt, path=['Eje Estratégico', 'Producto'], values='% Ejecución',
                          color='% Ejecución', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_sun, use_container_width=True)

# 7. Tabla Interactiva con Barra de Progreso
st.subheader("📝 Listado de Indicadores y Porcentaje de Cumplimiento")

# Usamos st.column_config para mostrar una barra de progreso real dentro de la tabla
st.dataframe(
    df_filt[['Indicador Asociado', 'Meta Anual', 'Ejecución Real', '% Ejecución']],
    column_config={
        "% Ejecución": st.column_config.ProgressColumn(
            "Progreso de Meta",
            help="Porcentaje de cumplimiento de la meta anual",
            format="%.1f%%",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True,
    use_container_width=True
)
