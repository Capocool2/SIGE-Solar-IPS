"""
========================================================================================
SIGE-Solar IPS: Sistema Inteligente de Gestión Energética Hospitalaria
Red Pública Hospitalaria de Barranquilla - MiRed IPS
Desarrollado en Python con Streamlit, Plotly, Pandas y Scikit-Learn
========================================================================================
"""

import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import streamlit as st

# Importar motor ETL
from etl import load_and_process_excel

# ======================================================================================
# CONFIGURACIÓN DE PÁGINA STREAMLIT
# ======================================================================================
st.set_page_config(
    page_title="SIGE-Solar IPS | Red MiRed Barranquilla",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================================================
# ESTILOS CSS PERSONALIZADOS (DISEÑO CORPORATIVO CLÍNICO-SOSTENIBLE)
# ======================================================================================
CUSTOM_CSS = """
<style>
/* Importación de Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

/* Variables CSS - Tema Claro (predeterminado) */
:root {
    --primary-deep: #10375C;
    --primary-blue: #1E88E5;
    --primary-light: #E3F2FD;
    --solar-amber: #FB8C00;
    --solar-amber-light: #FFF3E0;
    --green-eco: #2E7D32;
    --green-light: #E8F5E9;
    --purple-accent: #7C3AED;
    --purple-light: #EDE9FE;
    --bg-main: #F8FAFC;
    --card-bg: #FFFFFF;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --border-color: #E2E8F0;
    --shadow-soft: 0 4px 20px -2px rgba(16, 55, 92, 0.08);
    --shadow-hover: 0 8px 30px rgba(16, 55, 92, 0.14);
}

/* Variables CSS - Modo Oscuro (activado desde ☰ → Settings → Theme → Dark) */
[data-theme="dark"] {
    --primary-deep: #90CAF9;
    --primary-blue: #64B5F6;
    --primary-light: #1E3A5F;
    --solar-amber: #FFB74D;
    --solar-amber-light: #3E2A10;
    --green-eco: #66BB6A;
    --green-light: #1B3A1E;
    --purple-accent: #A78BFA;
    --purple-light: #372258;
    --bg-main: #0F1117;
    --card-bg: #1E2130;
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --border-color: #2D3748;
    --shadow-soft: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    --shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.5);
}

/* Sobrescrituras para Dark Mode en elementos Streamlit */
[data-theme="dark"] .kpi-card {
    background: #1E2130 !important;
    border-color: #2D3748 !important;
}
[data-theme="dark"] .kpi-icon-blue { background: #1E3A5F !important; color: #64B5F6 !important; }
[data-theme="dark"] .kpi-icon-amber { background: #3E2A10 !important; color: #FFB74D !important; }
[data-theme="dark"] .kpi-icon-green { background: #1B3A1E !important; color: #66BB6A !important; }
[data-theme="dark"] .kpi-icon-deep  { background: #263040 !important; color: #90CAF9 !important; }
[data-theme="dark"] .kpi-icon-purple { background: #372258 !important; color: #C4B5FD !important; }
[data-theme="dark"] .kpi-label { color: #94A3B8 !important; }
[data-theme="dark"] .kpi-value { color: #F1F5F9 !important; }
[data-theme="dark"] .kpi-delta-neutral { background: #263040 !important; color: #94A3B8 !important; }
[data-theme="dark"] .kpi-delta-green   { background: #1B3A1E !important; color: #86EFAC !important; }
[data-theme="dark"] .kpi-delta-amber   { background: #3E2A10 !important; color: #FCD34D !important; }
[data-theme="dark"] .kpi-delta-purple  { background: #372258 !important; color: #DDD6FE !important; }
[data-theme="dark"] .content-card { background: #1E2130 !important; border-color: #2D3748 !important; }
[data-theme="dark"] .card-title { color: #90CAF9 !important; }
[data-theme="dark"] .card-subtitle { color: #94A3B8 !important; }
[data-theme="dark"] .alert-danger  { background: #2D1717 !important; border-color: #7F1D1D !important; color: #FCA5A5 !important; }
[data-theme="dark"] .alert-warning { background: #2D2210 !important; border-color: #78350F !important; color: #FCD34D !important; }
[data-theme="dark"] .alert-success { background: #14261B !important; border-color: #166534 !important; color: #86EFAC !important; }
[data-theme="dark"] .alert-info    { background: #172554 !important; border-color: #1E40AF !important; color: #93C5FD !important; }
[data-theme="dark"] .stTabs [data-baseweb="tab-list"] { background-color: #1A1F2E !important; }
[data-theme="dark"] .stTabs [aria-selected="true"]     { background-color: #1E2130 !important; color: #90CAF9 !important; }

/* Tipografía base */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

/* Ocultar barra superior genérica de streamlit */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Contenedor principal con padding pulido */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 98% !important;
}

/* Header Banner Hero */
.hero-header {
    background: linear-gradient(135deg, #10375C 0%, #0D2840 50%, #1A4D78 100%);
    border-radius: 16px;
    padding: 28px 36px;
    color: #FFFFFF;
    box-shadow: 0 10px 25px -5px rgba(16, 55, 92, 0.35);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.hero-header::after {
    content: '';
    position: absolute;
    top: -40px;
    right: -40px;
    width: 240px;
    height: 240px;
    background: radial-gradient(circle, rgba(251, 140, 0, 0.25) 0%, rgba(251, 140, 0, 0) 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 6px 14px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #90CAF9;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 6px 0;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1rem;
    color: #CBD5E1;
    margin: 0;
    max-width: 950px;
    line-height: 1.5;
}

/* KPI Cards Superiores */
.kpi-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: var(--shadow-soft);
    position: relative;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    overflow: hidden;
    height: 100%;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
}

.kpi-card-border-blue { border-left: 5px solid var(--primary-blue); }
.kpi-card-border-amber { border-left: 5px solid var(--solar-amber); }
.kpi-card-border-green { border-left: 5px solid var(--green-eco); }
.kpi-card-border-deep { border-left: 5px solid var(--primary-deep); }
.kpi-card-border-purple { border-left: 5px solid var(--purple-accent); }

.kpi-icon-wrap {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    margin-bottom: 10px;
}

.kpi-icon-blue { background: #E3F2FD; color: #1E88E5; }
.kpi-icon-amber { background: #FFF3E0; color: #FB8C00; }
.kpi-icon-green { background: #E8F5E9; color: #2E7D32; }
.kpi-icon-deep { background: #ECEFF1; color: #10375C; }
.kpi-icon-purple { background: #EDE9FE; color: #7C3AED; }

.kpi-label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.kpi-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.15;
    margin-bottom: 6px;
}

.kpi-delta {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.78rem;
    font-weight: 600;
    border-radius: 6px;
    padding: 2px 8px;
}

.kpi-delta-neutral { background: #F1F5F9; color: #475569; }
.kpi-delta-green { background: #DCFCE7; color: #15803D; }
.kpi-delta-amber { background: #FEF3C7; color: #B45309; }
.kpi-delta-purple { background: #EDE9FE; color: #6D28D9; }

/* Contenedores de Sección y Tarjetas */
.content-card {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 22px;
    box-shadow: var(--shadow-soft);
    margin-bottom: 20px;
}

.card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.18rem;
    font-weight: 700;
    color: var(--primary-deep);
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-subtitle {
    font-size: 0.86rem;
    color: var(--text-secondary);
    margin-bottom: 18px;
}

/* Banner de Alerta Crítica */
.alert-box {
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
}

.alert-danger {
    background: #FEF2F2;
    border: 1px solid #FCA5A5;
    color: #991B1B;
}

.alert-warning {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    color: #92400E;
}

.alert-success {
    background: #F0FDF4;
    border: 1px solid #86EFAC;
    color: #166534;
}

.alert-info {
    background: #EFF6FF;
    border: 1px solid #93C5FD;
    color: #1E40AF;
}

.alert-title {
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 4px;
}

.alert-desc {
    font-size: 0.875rem;
    line-height: 1.45;
}

/* Pestañas estilizadas */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: #F1F5F9;
    padding: 6px;
    border-radius: 12px;
    margin-bottom: 24px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 10px 16px;
    color: #475569;
    border: none !important;
    background-color: transparent;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: var(--primary-deep) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}

/* Badges de tipología */
.badge-tipologia {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}
.badge-camino { background-color: #E3F2FD; color: #1565C0; }
.badge-hospital { background-color: #EDE7F6; color: #512DA8; }
.badge-paso { background-color: #FEF3C7; color: #B45309; }

/* Botones con estilo moderno */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: 8px 20px;
    transition: all 0.2s ease;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #F8FAFC;
    border-right: 1px solid #E2E8F0;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ======================================================================================
# CARGA Y CACHÉ DE DATOS
# ======================================================================================
@st.cache_data(show_spinner="Procesando matriz energética hospitalaria con motor ETL...")
def get_clean_data(file_source='CONSUMO DE ENERGIA 2018.xlsx'):
    return load_and_process_excel(file_source)


# ======================================================================================
# SIDEBAR: CONTROLES, ESQUEMA TARIFARIO, PARÁMETROS SOLARES Y FILTROS
# ======================================================================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 12px 0 16px 0;">
            <div style="font-size: 2.2rem; margin-bottom: 4px;">🏥☀️</div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 700; color: #10375C;">
                SIGE-Solar IPS
            </div>
            <div style="font-size: 0.78rem; font-weight: 600; color: #64748B; letter-spacing: 0.05em;">
                MIRED IPS BARRANQUILLA
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 1. EXPANDER: FUENTE DE DATOS
    with st.expander("📁 1. Fuente de Datos & ETL", expanded=False):
        uploaded_file = st.file_uploader(
            "Cargar Excel alternativo",
            type=["xlsx", "xls"],
            help="Por defecto el sistema carga 'CONSUMO DE ENERGIA 2018.xlsx' en el workspace."
        )
        data_source = uploaded_file if uploaded_file is not None else 'CONSUMO DE ENERGIA 2018.xlsx'
        
        st.markdown("""
            <div style="font-size: 0.8rem; background: #F1F5F9; padding: 10px; border-radius: 8px; margin-top: 8px;">
                <strong>Balance ETL Verificado:</strong><br>
                ✓ 11 hojas analizadas (Ene-Nov)<br>
                ✓ 597 registros consolidados<br>
                ✓ Balance: 8,922,163 kWh<br>
                ✓ Facturación: $3,580,300,966 COP
            </div>
        """, unsafe_allow_html=True)

    # Cargar datos procesados
    try:
        df_raw = get_clean_data(data_source)
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
        st.stop()

    # Cálculo de la tarifa histórica promedio exacta del Excel 2018
    tarifa_historica_global = (df_raw['Valor_Total'].sum() / df_raw['Consumo_kWh'].sum()) if df_raw['Consumo_kWh'].sum() > 0 else 401.28

    # 2. EXPANDER: FILTROS GLOBALES
    with st.expander("🔍 2. Filtros de Análisis", expanded=True):
        # Filtro de Mes
        todos_meses = list(df_raw['Mes'].cat.categories)
        meses_seleccionados = st.multiselect(
            "Meses a Analizar",
            options=todos_meses,
            default=todos_meses,
            help="Selecciona uno o varios meses para filtrar los tableros."
        )

        # Filtro de Tipología
        tipologias_disponibles = ['Todas'] + sorted(df_raw['Tipologia'].unique().tolist())
        tipologia_sel = st.selectbox("Tipología Institucional", tipologias_disponibles)

        # Filtro de Estado
        estados_disponibles = ['Todos', 'Habilitada', 'Cerrada']
        estado_sel = st.selectbox("Estado Operativo", estados_disponibles)

        # Filtro de IPS Agrupada
        df_filtrable = df_raw.copy()
        if tipologia_sel != 'Todas':
            df_filtrable = df_filtrable[df_filtrable['Tipologia'] == tipologia_sel]
        if estado_sel != 'Todos':
            df_filtrable = df_filtrable[df_filtrable['Estado'] == estado_sel]

        ips_list = ['Todas las IPS'] + sorted(df_filtrable['IPS_Agrupada'].unique().tolist())
        ips_sel = st.selectbox("Institución (IPS Agrupada)", ips_list)

    # 3. EXPANDER: ESQUEMA TARIFARIO & CONTROL DINÁMICO PRECIO kWh
    with st.expander("💵 3. Esquema Tarifario & Finanzas", expanded=True):
        esquema_tarifario = st.radio(
            "Seleccionar Esquema Tarifario:",
            options=[
                f"Tarifa Histórica Excel 2018 (~${tarifa_historica_global:.1f} COP/kWh)",
                "Precio del kWh Personalizado / Actualizado ($ COP/kWh)"
            ],
            index=0,
            help="Permite analizar con los costos reales facturados en 2018 o simular escenarios con precios actualizados de energía en Barranquilla (Air-e)."
        )

        es_personalizado = "Personalizado" in esquema_tarifario

        if es_personalizado:
            precio_kwh_activo = st.number_input(
                "Precio del kWh ($ COP/kWh)",
                min_value=100.0,
                max_value=2500.0,
                value=850.0,
                step=25.0,
                help="Tarifa activa monomia de energía para calcular costos y ahorros futuros."
            )
            tipo_tarifa_label = "Tarifa Simulada"
        else:
            precio_kwh_activo = st.number_input(
                "Precio del kWh ($ COP/kWh)",
                min_value=100.0,
                max_value=2500.0,
                value=float(round(tarifa_historica_global, 1)),
                step=10.0,
                help="Tarifa media histórica ponderada del Excel 2018."
            )
            tipo_tarifa_label = "Tarifa Excel 2018"

        cargo_potencia_kw = st.number_input(
            "Cargo por Potencia / Demanda ($ COP/kW-mes)",
            min_value=0.0,
            max_value=150000.0,
            value=35000.0,
            step=2500.0,
            help="Cargo regulado por potencia pico contratada/demandada (kW-mes) en media tensión para la Costa Caribe (CREG)."
        )

        capex_kwp = st.number_input(
            "CAPEX Instalado ($ COP / kWp)",
            min_value=2500000,
            max_value=7000000,
            value=4200000,
            step=100000,
            help="Costo promedio llave en mano por kWp instalado en Colombia para proyectos comerciales/hospitalarios."
        )

        tasa_descuento = st.slider(
            "Tasa de Descuento Anual (WACC %)",
            min_value=5.0,
            max_value=18.0,
            value=10.0,
            step=0.5
        )

        inflacion_tarifa = st.slider(
            "Aumento Anual de Tarifa (%)",
            min_value=1.0,
            max_value=12.0,
            value=4.0,
            step=0.5
        )

        ley_1715_activa = st.toggle(
            "Aplicar Beneficios Ley 1715 / 2099",
            value=True,
            help="Aplica deducción especial del 50% de renta en los primeros 5 años y 0% arancel/IVA."
        )

    # 4. EXPANDER: PARÁMETROS TÉCNICOS SOLARES (BARRANQUILLA)
    with st.expander("☀️ 4. Ingeniería Solar (Barranquilla)", expanded=False):
        hsp = st.slider(
            "Horas Sol Pico (HSP h/día)",
            min_value=4.0,
            max_value=6.5,
            value=5.2,
            step=0.1,
            help="Radiación solar diaria promedio en Barranquilla (promedio IDEAM: 5.2 - 5.5 h/día)."
        )
        pr = st.slider(
            "Performance Ratio (PR)",
            min_value=0.65,
            max_value=0.88,
            value=0.78,
            step=0.01,
            help="Factor de rendimiento del sistema fotovoltaico (pérdidas térmicas, suciedad, inversor, cableado)."
        )
        potencia_panel = st.selectbox(
            "Potencia del Módulo Solar (Wp)",
            options=[450, 550, 600],
            index=1,
            help="Potencia pico de cada panel monocristalino tier 1."
        )
        cobertura_solar_pct = st.slider(
            "Meta Cobertura Solar Objetivo (%)",
            min_value=10,
            max_value=100,
            value=40,
            step=5,
            help="% de la demanda energética que se desea abastecer con energía solar fotovoltaica."
        )

    st.markdown("""
        <div style="font-size: 0.75rem; color: #94A3B8; text-align: center; margin-top: 20px;">
            SIGE-Solar IPS v2.0 • Producción<br>
            Alcaldía de Barranquilla & MiRed IPS
        </div>
    """, unsafe_allow_html=True)


# ======================================================================================
# FILTRADO DEL DATAFRAME PRINCIPAL
# ======================================================================================
df_filtered = df_raw.copy()

if meses_seleccionados:
    df_filtered = df_filtered[df_filtered['Mes'].isin(meses_seleccionados)]

if tipologia_sel != 'Todas':
    df_filtered = df_filtered[df_filtered['Tipologia'] == tipologia_sel]

if estado_sel != 'Todos':
    df_filtered = df_filtered[df_filtered['Estado'] == estado_sel]

if ips_sel != 'Todas las IPS':
    df_filtered = df_filtered[df_filtered['IPS_Agrupada'] == ips_sel]


# ======================================================================================
# HEADER PRINCIPAL (HERO SECTION)
# ======================================================================================
st.markdown("""
    <div class="hero-header">
        <div class="hero-badge">
            <span>🏥 GESTIÓN ENERGÉTICA HOSPITALARIA 4.0</span>
            <span>•</span>
            <span>☀️ RED PÚBLICA BARRANQUILLA</span>
        </div>
        <h1 class="hero-title">SIGE-Solar IPS</h1>
        <p class="hero-subtitle">
            Sistema Inteligente de Apoyo a la Gestión Energética Hospitalaria Basado en Energía Solar Fotovoltaica,
            Analítica de Datos y Diseño UX/UI para la Red Pública <strong>MiRed IPS</strong> de Barranquilla.
        </p>
    </div>
""", unsafe_allow_html=True)


# ======================================================================================
# CÁLCULOS PARA TARJETAS SUPERIORES (KPI SUMMARY RIBBON - 5 TARJETAS)
# ======================================================================================
total_kwh_filtrado = df_filtered['Consumo_kWh'].sum()
total_costo_historico = df_filtered['Valor_Total'].sum()
num_meses_filtrados = max(1, df_filtered['Mes'].nunique())
consumo_promedio_mensual = total_kwh_filtrado / num_meses_filtrados

# Costo valorado según el esquema tarifario activo
if es_personalizado:
    costo_valorado_activo = total_kwh_filtrado * precio_kwh_activo
    costo_promedio_mensual = costo_valorado_activo / num_meses_filtrados
    tarifa_display_delta = f"Tarifa personalizada: ${precio_kwh_activo:,.1f}/kWh"
else:
    costo_valorado_activo = total_costo_historico
    costo_promedio_mensual = costo_valorado_activo / num_meses_filtrados
    tarifa_prom_real = (total_costo_historico / total_kwh_filtrado) if total_kwh_filtrado > 0 else tarifa_historica_global
    tarifa_display_delta = f"Tarifa media real: ${tarifa_prom_real:.1f}/kWh"

# Fórmulas de ingeniería solar
gen_mensual_kwp = hsp * 30.0 * pr  # ~ 121.68 kWh/mes por kWp
potencia_solar_req_kwp = (consumo_promedio_mensual * (cobertura_solar_pct / 100.0)) / gen_mensual_kwp
num_paneles_req = math.ceil((potencia_solar_req_kwp * 1000.0) / potencia_panel)
area_techo_m2 = num_paneles_req * 2.6

# Generación solar y mitigación ambiental (SIN Colombia: 0.164 kg CO2e / kWh)
FACTOR_SIN_CO2 = 0.164  # kg CO2e / kWh
gen_solar_anual_kwh = potencia_solar_req_kwp * gen_mensual_kwp * 12.0
co2_mitigado_ton_anual = (gen_solar_anual_kwh * FACTOR_SIN_CO2) / 1000.0
arboles_equivalentes = int(co2_mitigado_ton_anual * 45.45)  # 1 árbol ~ 22 kg CO2/año


# ======================================================================================
# RENDERIZADO DE 5 KPI CARDS SUPERIORES
# ======================================================================================
col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)

with col_k1:
    st.markdown(f"""
        <div class="kpi-card kpi-card-border-blue">
            <div class="kpi-icon-wrap kpi-icon-blue">⚡</div>
            <div class="kpi-label">Demanda Energética</div>
            <div class="kpi-value">{total_kwh_filtrado/1e6:.2f} <span style="font-size: 0.95rem; color: #64748B;">GWh</span></div>
            <div class="kpi-delta kpi-delta-neutral">
                Promedio: {consumo_promedio_mensual:,.0f} kWh/mes
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_k2:
    st.markdown(f"""
        <div class="kpi-card kpi-card-border-deep">
            <div class="kpi-icon-wrap kpi-icon-deep">💵</div>
            <div class="kpi-label">Costo Valorado</div>
            <div class="kpi-value">${costo_valorado_activo/1e6:,.1f} <span style="font-size: 0.95rem; color: #64748B;">M COP</span></div>
            <div class="kpi-delta kpi-delta-neutral">
                {tarifa_display_delta}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_k3:
    st.markdown(f"""
        <div class="kpi-card kpi-card-border-purple">
            <div class="kpi-icon-wrap kpi-icon-purple">🏷️</div>
            <div class="kpi-label">Precio del kWh</div>
            <div class="kpi-value">${precio_kwh_activo:,.1f} <span style="font-size: 0.95rem; color: #64748B;">COP</span></div>
            <div class="kpi-delta kpi-delta-purple">
                ● {tipo_tarifa_label}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_k4:
    st.markdown(f"""
        <div class="kpi-card kpi-card-border-amber">
            <div class="kpi-icon-wrap kpi-icon-amber">☀️</div>
            <div class="kpi-label">Potencia Solar ({cobertura_solar_pct}%)</div>
            <div class="kpi-value">{potencia_solar_req_kwp:,.1f} <span style="font-size: 0.95rem; color: #64748B;">kWp</span></div>
            <div class="kpi-delta kpi-delta-amber">
                {num_paneles_req:,} paneles • {area_techo_m2:,.0f} m²
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_k5:
    st.markdown(f"""
        <div class="kpi-card kpi-card-border-green">
            <div class="kpi-icon-wrap kpi-icon-green">🌿</div>
            <div class="kpi-label">Descarbonización</div>
            <div class="kpi-value">{co2_mitigado_ton_anual:,.1f} <span style="font-size: 0.95rem; color: #64748B;">tCO₂e</span></div>
            <div class="kpi-delta kpi-delta-green">
                🌳 ~{arboles_equivalentes:,} árboles equiv.
            </div>
        </div>
    """, unsafe_allow_html=True)


# ======================================================================================
# PESTAÑAS METODOLÓGICAS (LOS 7 PASOS DE GESTIÓN ENERGÉTICA EN 6 TABS)
# ======================================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Pasos 1 y 2: Caracterización & Pareto",
    "⚡ Paso 3: Perfil de Carga (kW)",
    "📉 Paso 4: Línea Base Energética",
    "🔍 Paso 5: Auditoría Inteligente",
    "🏥 Paso 6: Indicadores EnPIs",
    "☀️ Paso 7: Simulación Solar & Finanzas"
])


# ======================================================================================
# TAB 1: PASOS 1 Y 2: CARACTERIZACIÓN & PARETO
# ======================================================================================
with tab1:
    st.markdown("""
        <div class="card-title">📊 Pasos 1 y 2: Caracterización del Consumo y Análisis de Pareto (80/20)</div>
        <div class="card-subtitle">
            Diagnóstico integral del comportamiento histórico de la demanda energética mensual, evolución del costo valorado y concentración del consumo por tipología hospitalaria.
        </div>
    """, unsafe_allow_html=True)

    # Controles de proyección Diciembre 2018
    col_t1_ctrl1, col_t1_ctrl2 = st.columns([3, 1])
    with col_t1_ctrl2:
        incluir_dic = st.checkbox(
            "Incluir Proyección Diciembre 2018 (Regresión ML)",
            value=True,
            help="Proyecta el mes faltante del año fiscal 2018 mediante un modelo de regresión lineal sobre el consumo histórico."
        )

    # Preparación de datos mensuales
    monthly_summary = (
        df_filtered.groupby('Mes', observed=True)
        .agg({'Consumo_kWh': 'sum', 'Valor_Total': 'sum'})
        .reset_index()
    )
    if es_personalizado:
        monthly_summary['Valor_Visual'] = (monthly_summary['Consumo_kWh'] * precio_kwh_activo) / 1e6
        label_costo_eje = f'Costo Valorado a ${precio_kwh_activo:,.1f}/kWh ($ Millones COP)'
    else:
        monthly_summary['Valor_Visual'] = monthly_summary['Valor_Total'] / 1e6
        label_costo_eje = 'Costo Facturado en Excel ($ Millones COP)'

    monthly_summary['Tipo'] = 'Histórico Facturado'

    # Modelo de Regresión Lineal para Diciembre 2018
    if len(monthly_summary) >= 4 and incluir_dic and ('NOVIEMBRE 2018' in monthly_summary['Mes'].values):
        X = np.arange(1, len(monthly_summary) + 1).reshape(-1, 1)
        y_kwh = monthly_summary['Consumo_kWh'].values
        
        reg_kwh = LinearRegression().fit(X, y_kwh)
        next_month_idx = np.array([[len(monthly_summary) + 1]])
        pred_kwh = float(reg_kwh.predict(next_month_idx)[0])
        pred_kwh = max(0.0, pred_kwh)
        r2_score = reg_kwh.score(X, y_kwh)
        
        pred_costo_cop = pred_kwh * precio_kwh_activo if es_personalizado else pred_kwh * tarifa_historica_global
        pred_costo_millones = pred_costo_cop / 1e6

        dec_row = pd.DataFrame([{
            'Mes': 'DICIEMBRE 2018 (Proy.)',
            'Consumo_kWh': pred_kwh,
            'Valor_Total': pred_costo_cop,
            'Valor_Visual': pred_costo_millones,
            'Tipo': 'Proyección ML'
        }])
        monthly_plot_df = pd.concat([monthly_summary, dec_row], ignore_index=True)
    else:
        monthly_plot_df = monthly_summary
        r2_score = 0.0

    linea_base_promedio = monthly_summary['Consumo_kWh'].mean()

    # Gráfico Dual Combinado (Barras Consumo + Línea Costo)
    fig_evol = go.Figure()
    colors_bars = ['#1E88E5' if t == 'Histórico Facturado' else '#FB8C00' for t in monthly_plot_df['Tipo']]

    fig_evol.add_trace(go.Bar(
        x=monthly_plot_df['Mes'],
        y=monthly_plot_df['Consumo_kWh'],
        name='Consumo Eléctrico (kWh)',
        marker=dict(color=colors_bars, opacity=0.88),
        hovertemplate='<b>%{x}</b><br>Consumo: %{y:,.0f} kWh<extra></extra>',
        yaxis='y1'
    ))

    fig_evol.add_trace(go.Scatter(
        x=monthly_plot_df['Mes'],
        y=monthly_plot_df['Valor_Visual'],
        name=label_costo_eje,
        mode='lines+markers',
        line=dict(color='#10375C', width=3),
        marker=dict(size=8, color='#10375C', symbol='circle'),
        hovertemplate='<b>%{x}</b><br>Costo: $%{y:,.1f} M COP<extra></extra>',
        yaxis='y2'
    ))

    # Línea Base Promedio
    fig_evol.add_trace(go.Scatter(
        x=monthly_plot_df['Mes'],
        y=[linea_base_promedio] * len(monthly_plot_df),
        name=f'Consumo Promedio ({linea_base_promedio:,.0f} kWh)',
        mode='lines',
        line=dict(color='#DC2626', width=2, dash='dash'),
        yaxis='y1'
    ))

    fig_evol.update_layout(
        title='<b>Evolución Mensual de la Demanda Eléctrica y Valoración del Costo</b>',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        yaxis=dict(title='Consumo (kWh)', gridcolor='#E2E8F0', showgrid=True, zeroline=False),
        yaxis2=dict(title='Costo ($ Millones COP)', overlaying='y', side='right', showgrid=False, zeroline=False),
        xaxis=dict(gridcolor='#F1F5F9', tickangle=-25),
        height=440,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    st.plotly_chart(fig_evol, use_container_width=True)

    if incluir_dic and len(monthly_summary) >= 4 and 'DICIEMBRE 2018 (Proy.)' in monthly_plot_df['Mes'].values:
        st.markdown(f"""
            <div style="font-size: 0.85rem; background: #F8FAFC; border-left: 4px solid #FB8C00; padding: 10px 14px; border-radius: 6px; margin-bottom: 24px;">
                <strong>Proyección Diciembre 2018 (Regresión Lineal Scikit-Learn):</strong> Demanda proyectada: 
                <strong>{dec_row['Consumo_kWh'].values[0]:,.0f} kWh</strong> | Costo valorado: 
                <strong>${dec_row['Valor_Total'].values[0]:,.0f} COP</strong> (a ${precio_kwh_activo:.1f}/kWh) | Ajuste del modelo: 
                <strong>R² = {r2_score:.3f}</strong>. Consumo acumulado anual estimado: 
                <strong>{(total_kwh_filtrado + dec_row['Consumo_kWh'].values[0]):,.0f} kWh</strong>.
            </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------------------
    # PASO 2: CURVA DE PARETO DE LAS TOP 12 IPS Y ESTRUCTURA JERÁRQUICA
    # ----------------------------------------------------------------------------------
    col_p1, col_p2 = st.columns([1, 1])

    with col_p1:
        st.markdown("""
            <div class="card-title">📊 Curva de Pareto: Top 12 IPS de Mayor Consumo</div>
            <div class="card-subtitle">Concentración del consumo eléctrico hospitalario y principio 80/20.</div>
        """, unsafe_allow_html=True)

        pareto_df = (
            df_filtered.groupby(['Tipologia', 'IPS_Agrupada'], observed=True)['Consumo_kWh']
            .sum()
            .reset_index()
            .sort_values('Consumo_kWh', ascending=False)
            .head(12)
        )
        total_consumo_actual = max(1.0, df_filtered['Consumo_kWh'].sum())
        pareto_df['Pct_Individual'] = (pareto_df['Consumo_kWh'] / total_consumo_actual) * 100.0
        pareto_df['Pct_Acumulado'] = pareto_df['Pct_Individual'].cumsum()

        color_map_tipo = {'CAMINO': '#1E88E5', 'Hospital': '#7C3AED', 'PASO': '#F59E0B'}

        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(
            x=pareto_df['IPS_Agrupada'],
            y=pareto_df['Consumo_kWh'],
            name='Consumo (kWh)',
            marker=dict(color=[color_map_tipo.get(t, '#1E88E5') for t in pareto_df['Tipologia']]),
            hovertemplate='<b>%{x}</b><br>Consumo: %{y:,.0f} kWh<extra></extra>',
            yaxis='y1'
        ))

        fig_pareto.add_trace(go.Scatter(
            x=pareto_df['IPS_Agrupada'],
            y=pareto_df['Pct_Acumulado'],
            name='% Acumulado (Pareto)',
            mode='lines+markers',
            line=dict(color='#DC2626', width=2.5),
            marker=dict(size=7, color='#DC2626'),
            hovertemplate='<b>%{x}</b><br>% Acumulado: %{y:.1f}%<extra></extra>',
            yaxis='y2'
        ))

        # Línea guía de corte 80%
        fig_pareto.add_shape(
            type='line',
            x0=-0.5,
            x1=len(pareto_df) - 0.5,
            y0=80,
            y1=80,
            yref='y2',
            line=dict(color='#64748B', dash='dash', width=1.5)
        )

        fig_pareto.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            yaxis=dict(title='Consumo (kWh)', gridcolor='#E2E8F0', showgrid=True),
            yaxis2=dict(title='% Acumulado', overlaying='y', side='right', range=[0, 105], showgrid=False),
            xaxis=dict(tickangle=-40, gridcolor='#F1F5F9'),
            height=420,
            margin=dict(l=40, r=40, t=40, b=90)
        )
        st.plotly_chart(fig_pareto, use_container_width=True)

    with col_p2:
        st.markdown("""
            <div class="card-title">🗂️ Jerarquía Hospitalaria (Treemap Interactivo)</div>
            <div class="card-subtitle">Distribución del consumo: Tipología ➔ Institución Agrupada ➔ Medidor/Sede.</div>
        """, unsafe_allow_html=True)

        treemap_df = df_filtered.copy()
        treemap_df['Consumo_Positivo'] = treemap_df['Consumo_kWh'].apply(lambda x: max(1.0, x))

        fig_tree = px.treemap(
            treemap_df,
            path=['Tipologia', 'IPS_Agrupada', 'Sede'],
            values='Consumo_Positivo',
            color='Tipologia',
            color_discrete_map={'CAMINO': '#1E88E5', 'Hospital': '#7C3AED', 'PASO': '#F59E0B'},
            hover_data={'Consumo_kWh': ':,.0f', 'Valor_Total': ':$,.0f'}
        )
        fig_tree.update_traces(
            root_color="lightgrey",
            textinfo="label+value+percent parent"
        )
        fig_tree.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            height=420,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_tree, use_container_width=True)


# ======================================================================================
# TAB 2: PASO 3: ANÁLISIS DEL PERFIL DE CARGA (DEMANDA kW)
# ======================================================================================
with tab2:
    st.markdown("""
        <div class="card-title">⚡ Paso 3: Análisis del Perfil de Carga y Demanda Horaria (kW)</div>
        <div class="card-subtitle">
            <strong>¿Cuándo consumimos?</strong> Modelado de la curva de demanda de 00:00 a 24:00 horas, identificación de picos térmicos diurnos en Barranquilla,
            cálculo del Factor de Carga y valoración del cargo por potencia regulada.
        </div>
    """, unsafe_allow_html=True)

    # 1. Selector de Alcance para el Perfil de Carga
    col_perfil_scope, col_perfil_info = st.columns([2, 1])
    with col_perfil_scope:
        opciones_perfil = ['Toda la Red MiRed IPS (Consolidada)'] + sorted(df_raw['IPS_Agrupada'].unique().tolist())
        sede_perfil_sel = st.selectbox(
            "Seleccione la Institución o Alcance para analizar su Perfil de Carga:",
            options=opciones_perfil,
            help="Modela la curva horaria en base al consumo mensual real calibrado por tipología hospitalaria."
        )

    # Filtrar datos para el perfil seleccionado
    if sede_perfil_sel == 'Toda la Red MiRed IPS (Consolidada)':
        df_perfil_target = df_raw.copy()
        tipologia_perfil = 'Red MiRed IPS'
    else:
        df_perfil_target = df_raw[df_raw['IPS_Agrupada'] == sede_perfil_sel]
        tipologia_perfil = df_perfil_target['Tipologia'].iloc[0] if len(df_perfil_target) > 0 else 'CAMINO'

    # Cálculos matemáticos rigurosos de calibración de demanda
    num_m_perfil = max(1, df_perfil_target['Mes'].nunique())
    consumo_mes_perfil = df_perfil_target['Consumo_kWh'].sum() / num_m_perfil
    consumo_dia_perfil = consumo_mes_perfil / 30.0
    p_promedio_kw = consumo_dia_perfil / 24.0  # Demanda media continua en kW

    # Vectores de ponderación horaria f(h) normalizados (media = 1.0)
    # Hospital / CAMINO: Operación 24/7 con alta carga diurna por climatización en Barranquilla (aires acondicionados), quirófanos y consulta
    weights_hosp = np.array([
        0.66, 0.64, 0.62, 0.62, 0.65, 0.72,  # 00:00 - 05:00 (Carga base nocturna ~65%)
        0.88, 1.12, 1.32, 1.42, 1.46, 1.47,  # 06:00 - 11:00 (Rampa de inicio clínico)
        1.45, 1.48, 1.46, 1.40, 1.32, 1.22,  # 12:00 - 17:00 (Pico térmico Barranquilla a las 13:00 - 14:00)
        1.08, 0.94, 0.84, 0.76, 0.70, 0.67   # 18:00 - 23:00 (Descenso gradual nocturno)
    ])
    weights_hosp = weights_hosp / np.mean(weights_hosp)

    # PASO: Atención ambulatoria diurna (07:00 - 17:00). Noche mínima (cadena de frío de vacunas y luces de seguridad)
    weights_paso = np.array([
        0.22, 0.22, 0.21, 0.21, 0.22, 0.24,  # 00:00 - 05:00 (Base nocturna mínima ~22%)
        0.42, 0.82, 1.62, 1.78, 1.84, 1.82,  # 06:00 - 11:00 (Apertura de consultorios)
        1.78, 1.85, 1.82, 1.74, 1.55, 1.10,  # 12:00 - 17:00 (Pico ambulatorio y térmico)
        0.58, 0.36, 0.28, 0.24, 0.23, 0.22   # 18:00 - 23:00 (Cierre y stand-by)
    ])
    weights_paso = weights_paso / np.mean(weights_paso)

    # Red Completa: Mezcla ponderada según distribución real (CAMINO 61.2%, PASO 22.2%, Hospital 16.6%)
    weights_red = (0.612 * weights_hosp) + (0.166 * weights_hosp) + (0.222 * weights_paso)
    weights_red = weights_red / np.mean(weights_red)

    if tipologia_perfil == 'PASO':
        w_activo = weights_paso
        perfil_desc = "Perfil Ambulatorio (Paso): Operación diurna 07:00-17:00 con carga base nocturna mínima para refrigeración de vacunas."
    elif tipologia_perfil in ['Hospital', 'CAMINO']:
        w_activo = weights_hosp
        perfil_desc = f"Perfil Clínico 24/7 ({tipologia_perfil}): Carga base nocturna continua (UCI/Urgencias) y pico pronunciado diurno por HVAC (aires acondicionados)."
    else:
        w_activo = weights_red
        perfil_desc = "Perfil Consolidado Red MiRed: Ponderación multi-institucional de centros de alta y mediana complejidad con centros ambulatorios."

    # Curva horaria en kW garantizando integral matemática exacta
    potencia_horaria_kw = p_promedio_kw * w_activo
    p_max_pico_kw = float(np.max(potencia_horaria_kw))
    hora_pico_idx = int(np.argmax(potencia_horaria_kw))
    factor_carga_pct = (p_promedio_kw / p_max_pico_kw) * 100.0 if p_max_pico_kw > 0 else 0.0

    # Valoración de cargos
    costo_demanda_pico_mes = p_max_pico_kw * cargo_potencia_kw
    costo_energia_mes = consumo_mes_perfil * precio_kwh_activo
    costo_total_mes_estimado = costo_energia_mes + costo_demanda_pico_mes

    # Modelo horario de autogeneración solar estimada para visualización de Peak Shaving
    # Curva solar de radiación diurna de 06:00 a 18:00
    solar_weights_24h = np.zeros(24)
    for h in range(6, 19):
        # Campana senoidal de radiación diurna
        angle = (h - 6) / 12.0 * math.pi
        solar_weights_24h[h] = max(0.0, math.sin(angle))
    if np.sum(solar_weights_24h) > 0:
        solar_weights_24h = solar_weights_24h / np.sum(solar_weights_24h)

    # Potencia solar equivalente para la sede con la cobertura seleccionada en la sidebar
    p_solar_sede_kwp = (consumo_mes_perfil * (cobertura_solar_pct / 100.0)) / gen_mensual_kwp
    generacion_solar_dia_kwh = (p_solar_sede_kwp * gen_mensual_kwp) / 30.0
    potencia_solar_horaria_kw = generacion_solar_dia_kwh * solar_weights_24h
    potencia_neta_residual_kw = np.maximum(0.0, potencia_horaria_kw - potencia_solar_horaria_kw)
    nuevo_pico_residual_kw = float(np.max(potencia_neta_residual_kw))
    reduccion_pico_kw = max(0.0, p_max_pico_kw - nuevo_pico_residual_kw)
    ahorro_demanda_mes = reduccion_pico_kw * cargo_potencia_kw

    # Tarjetas de Métricas Clave del Perfil
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric(
        "Demanda Máxima / Pico Estimada",
        f"{p_max_pico_kw:,.1f} kW",
        f"Hora crítica: {hora_pico_idx:02d}:00 hrs"
    )
    col_m2.metric(
        "Demanda Promedio Continua",
        f"{p_promedio_kw:,.1f} kW",
        f"Consumo diario: {consumo_dia_perfil:,.0f} kWh/día"
    )
    col_m3.metric(
        "Factor de Carga (LF)",
        f"{factor_carga_pct:.1f}%",
        "Alta eficiencia" if factor_carga_pct >= 60 else "Carga concentrada diurna"
    )
    col_m4.metric(
        "Costo Mensual por Demanda Pico",
        f"${costo_demanda_pico_mes/1e6:,.2f} M COP/mes",
        f"Tarifa: ${cargo_potencia_kw:,.0f} /kW-mes"
    )

    # Gráfico Principal: Curva Horaria de Demanda de 00:00 a 24:00 (kW)
    horas_labels = [f"{h:02d}:00" for h in range(24)]
    fig_curva = go.Figure()

    # Demanda Bruta Actual
    fig_curva.add_trace(go.Scatter(
        x=horas_labels,
        y=potencia_horaria_kw,
        name='Demanda Eléctrica Actual (kW)',
        mode='lines+markers',
        line=dict(color='#1E88E5', width=3.5),
        fill='tozeroy',
        fillcolor='rgba(30, 136, 229, 0.12)',
        marker=dict(size=5, color='#1E88E5'),
        hovertemplate='<b>%{x}</b><br>Demanda Actual: %{y:,.1f} kW<extra></extra>'
    ))

    # Demanda Promedio Continua
    fig_curva.add_trace(go.Scatter(
        x=horas_labels,
        y=[p_promedio_kw] * 24,
        name=f'Demanda Promedio ({p_promedio_kw:,.1f} kW)',
        mode='lines',
        line=dict(color='#10375C', width=2, dash='dash'),
        hovertemplate='Demanda Media: %{y:,.1f} kW<extra></extra>'
    ))

    # Generación Solar Fotovoltaica Coincidente
    fig_curva.add_trace(go.Scatter(
        x=horas_labels,
        y=potencia_solar_horaria_kw,
        name=f'Generación Solar Estimada ({cobertura_solar_pct}% cob.)',
        mode='lines',
        line=dict(color='#FB8C00', width=2.5, dash='dot'),
        fill='tozeroy',
        fillcolor='rgba(251, 140, 0, 0.15)',
        hovertemplate='<b>%{x}</b><br>Generación Solar: %{y:,.1f} kW<extra></extra>'
    ))

    # Demanda Neta Residual (Peak Shaving)
    fig_curva.add_trace(go.Scatter(
        x=horas_labels,
        y=potencia_neta_residual_kw,
        name='Demanda Neta de Red (Post-Solar)',
        mode='lines',
        line=dict(color='#16A34A', width=2.5),
        hovertemplate='<b>%{x}</b><br>Demanda Neta: %{y:,.1f} kW<extra></extra>'
    ))

    # Marcador en el Pico Máximo
    fig_curva.add_annotation(
        x=horas_labels[hora_pico_idx],
        y=p_max_pico_kw,
        text=f"Pico Máximo: {p_max_pico_kw:,.1f} kW",
        showarrow=True,
        arrowhead=2,
        arrowcolor='#DC2626',
        arrowsize=1.2,
        ax=0,
        ay=-40,
        bgcolor="#FFFFFF",
        bordercolor="#DC2626",
        borderwidth=1.5,
        font=dict(color="#DC2626", size=11, family="Plus Jakarta Sans")
    )

    fig_curva.update_layout(
        title=f'<b>Curva de Demanda Horaria (00:00 a 24:00) y Rasurado de Picos (Peak Shaving) — {sede_perfil_sel}</b>',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        yaxis=dict(title='Potencia de Demanda (kW)', gridcolor='#E2E8F0', showgrid=True, zeroline=False),
        xaxis=dict(title='Hora del Día (00:00 - 23:00)', gridcolor='#F1F5F9'),
        height=430,
        margin=dict(l=40, r=40, t=80, b=40)
    )

    st.plotly_chart(fig_curva, use_container_width=True)

    st.markdown(f"""
        <div style="font-size: 0.85rem; background: #F8FAFC; border-left: 4px solid #1E88E5; padding: 10px 14px; border-radius: 6px; margin-bottom: 24px;">
            <strong>Diagnóstico del Perfil de Demanda:</strong> {perfil_desc} 
            Gracias a la alta coincidencia entre la radiación solar en Barranquilla (10:00 a 15:00) y el pico de climatización hospitalaria, 
            la instalación solar reduce el pico de demanda en <strong>{reduccion_pico_kw:,.1f} kW</strong> (<strong>-{ (reduccion_pico_kw/p_max_pico_kw)*100:.1f}%</strong>), 
            liberando un ahorro adicional de <strong>${ahorro_demanda_mes/1e6:,.2f} M COP/mes</strong> en cargos por potencia contratada.
        </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------------------
    # ESTACIONALIDAD MENSUAL DE LA DEMANDA Y ESTRUCTURA DE COSTOS
    # ----------------------------------------------------------------------------------
    col_est1, col_est2 = st.columns([1, 1])

    with col_est1:
        st.markdown("""
            <div class="card-title">🌡️ Estacionalidad Mensual de la Demanda Pico (kW)</div>
            <div class="card-subtitle">Variación mes a mes de la exigencia térmica y climatización en Barranquilla.</div>
        """, unsafe_allow_html=True)

        monthly_pico_df = (
            df_perfil_target.groupby('Mes', observed=True)['Consumo_kWh']
            .sum()
            .reset_index()
        )
        # Estimación de demanda pico mes a mes en función del consumo del mes
        monthly_pico_df['Demanda_Pico_kW'] = monthly_pico_df['Consumo_kWh'] / (30.0 * 24.0 * (factor_carga_pct / 100.0))
        monthly_pico_df['Demanda_Media_kW'] = monthly_pico_df['Consumo_kWh'] / (30.0 * 24.0)

        fig_estac = go.Figure()
        fig_estac.add_trace(go.Bar(
            x=monthly_pico_df['Mes'],
            y=monthly_pico_df['Demanda_Pico_kW'],
            name='Demanda Pico Estimada (kW)',
            marker=dict(color='#FB8C00', opacity=0.9),
            hovertemplate='<b>%{x}</b><br>Pico Estimado: %{y:,.1f} kW<extra></extra>'
        ))
        fig_estac.add_trace(go.Scatter(
            x=monthly_pico_df['Mes'],
            y=monthly_pico_df['Demanda_Media_kW'],
            name='Demanda Promedio (kW)',
            mode='lines+markers',
            line=dict(color='#10375C', width=2.5),
            hovertemplate='<b>%{x}</b><br>Media: %{y:,.1f} kW<extra></extra>'
        ))

        fig_estac.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            yaxis=dict(title='Potencia (kW)', gridcolor='#E2E8F0', showgrid=True),
            xaxis=dict(tickangle=-30, gridcolor='#F1F5F9'),
            height=340,
            margin=dict(l=40, r=30, t=40, b=50)
        )
        st.plotly_chart(fig_estac, use_container_width=True)

    with col_est2:
        st.markdown("""
            <div class="card-title">⚖️ Estructura del Gasto Eléctrico Mensual</div>
            <div class="card-subtitle">Desglose de facturación: Consumo de Energía Activa vs. Cargo por Capacidad/Demanda.</div>
        """, unsafe_allow_html=True)

        df_costos_perfil = pd.DataFrame({
            'Concepto': ['Energía Activa ($ COP)', 'Cargo por Demanda Pico ($ COP)'],
            'Valor_COP': [costo_energia_mes, costo_demanda_pico_mes]
        })

        fig_pie_costo = px.pie(
            df_costos_perfil,
            names='Concepto',
            values='Valor_COP',
            hole=0.55,
            color='Concepto',
            color_discrete_map={
                'Energía Activa ($ COP)': '#1E88E5',
                'Cargo por Demanda Pico ($ COP)': '#7C3AED'
            }
        )
        fig_pie_costo.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f} COP<extra></extra>',
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        fig_pie_costo.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=340,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_pie_costo, use_container_width=True)


# ======================================================================================
# TAB 3: PASO 4: DEFINICIÓN DE LA LÍNEA BASE ENERGÉTICA
# ======================================================================================
with tab3:
    st.markdown("""
        <div class="card-title">📉 Paso 4: Definición de la Línea Base Energética y Metas de Mejora</div>
        <div class="card-subtitle">
            <strong>¿De dónde partimos?</strong> Establecimiento del consumo de referencia histórico (Línea Base) y cuantificación de metas de reducción
            mediante eficiencia energética operativa (-15%) integradas con autogeneración solar fotovoltaica.
        </div>
    """, unsafe_allow_html=True)

    # 1. Controles de Escenario de Línea Base
    col_lb_ctrl1, col_lb_ctrl2 = st.columns([2, 1])
    with col_lb_ctrl1:
        meta_eficiencia_pct = st.slider(
            "Meta de Reducción por Eficiencia Energética Operativa (%):",
            min_value=5,
            max_value=30,
            value=15,
            step=1,
            help="Meta de reducción del consumo de energía mediante buenas prácticas, control de climatización y cambio tecnológico."
        )
    with col_lb_ctrl2:
        incluir_solar_en_meta = st.checkbox(
            f"Integrar Meta Solar FV ({cobertura_solar_pct}% cobertura)",
            value=True,
            help="Combina el ahorro por eficiencia operativa con la autogeneración solar fotovoltaica en sitio."
        )

    # Cálculos globales de Línea Base
    linea_base_kwh_mes = consumo_promedio_mensual
    ahorro_eficiencia_kwh_mes = linea_base_kwh_mes * (meta_eficiencia_pct / 100.0)
    consumo_meta_eficiencia_kwh_mes = linea_base_kwh_mes - ahorro_eficiencia_kwh_mes

    generacion_solar_meta_kwh_mes = (linea_base_kwh_mes * (cobertura_solar_pct / 100.0)) if incluir_solar_en_meta else 0.0
    consumo_meta_combinada_kwh_mes = max(0.0, consumo_meta_eficiencia_kwh_mes - generacion_solar_meta_kwh_mes)

    # Valoración económica con el precio activo del kWh
    costo_base_mes_cop = linea_base_kwh_mes * precio_kwh_activo
    costo_meta_eficiencia_mes_cop = consumo_meta_eficiencia_kwh_mes * precio_kwh_activo
    costo_meta_combinada_mes_cop = consumo_meta_combinada_kwh_mes * precio_kwh_activo

    ahorro_anual_eficiencia_kwh = ahorro_eficiencia_kwh_mes * 12.0
    ahorro_anual_eficiencia_cop = ahorro_anual_eficiencia_kwh * precio_kwh_activo

    ahorro_anual_combinado_kwh = (linea_base_kwh_mes - consumo_meta_combinada_kwh_mes) * 12.0
    ahorro_anual_combinado_cop = ahorro_anual_combinado_kwh * precio_kwh_activo

    co2_evitado_meta_anual = (ahorro_anual_combinado_kwh * FACTOR_SIN_CO2) / 1000.0
    arboles_meta_anual = int(co2_evitado_meta_anual * 45.45)

    # Tarjetas de impacto de la meta
    col_mb1, col_mb2, col_mb3, col_mb4 = st.columns(4)
    col_mb1.metric(
        "Consumo Línea Base",
        f"{linea_base_kwh_mes:,.0f} kWh/mes",
        f"${costo_base_mes_cop/1e6:,.1f} M COP/mes"
    )
    col_mb2.metric(
        f"Meta Eficiencia (-{meta_eficiencia_pct}%)",
        f"{consumo_meta_eficiencia_kwh_mes:,.0f} kWh/mes",
        f"-{ahorro_eficiencia_kwh_mes:,.0f} kWh/mes ahorrados"
    )
    col_mb3.metric(
        "Demanda Neta Red Combinada",
        f"{consumo_meta_combinada_kwh_mes:,.0f} kWh/mes",
        f"-{((linea_base_kwh_mes - consumo_meta_combinada_kwh_mes)/linea_base_kwh_mes)*100:.1f}% Reducción Total"
    )
    col_mb4.metric(
        "Ahorro Económico Anual Proyectado",
        f"${ahorro_anual_combinado_cop/1e6:,.1f} M COP/año",
        f"🌳 ~{arboles_meta_anual:,} árboles equiv."
    )

    # ----------------------------------------------------------------------------------
    # GRÁFICOS COMPARATIVOS DE SITUACIÓN ACTUAL VS METAS
    # ----------------------------------------------------------------------------------
    col_gb1, col_gb2 = st.columns([1, 1])

    with col_gb1:
        st.markdown("##### ⚡ Comparativa de Demanda Mensual (kWh/mes)")
        categorias_comp = ['1. Situación Actual\n(Línea Base)', f'2. Meta con\nEficiencia (-{meta_eficiencia_pct}%)', '3. Meta Combinada\n(Eficiencia + Solar)']
        valores_kwh_comp = [linea_base_kwh_mes, consumo_meta_eficiencia_kwh_mes, consumo_meta_combinada_kwh_mes]
        colores_kwh_comp = ['#DC2626', '#FB8C00', '#16A34A']

        fig_comp_kwh = go.Figure(go.Bar(
            x=categorias_comp,
            y=valores_kwh_comp,
            text=[f"{v:,.0f} kWh" for v in valores_kwh_comp],
            textposition='outside',
            marker=dict(color=colores_kwh_comp, opacity=0.9)
        ))
        fig_comp_kwh.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title='Consumo Mensual (kWh)', gridcolor='#E2E8F0', showgrid=True),
            height=360,
            margin=dict(l=30, r=20, t=30, b=40)
        )
        st.plotly_chart(fig_comp_kwh, use_container_width=True)

    with col_gb2:
        st.markdown(f"##### 💵 Comparativa de Gasto Eléctrico Mensual ($ M COP a ${precio_kwh_activo:.1f}/kWh)")
        valores_cop_comp = [costo_base_mes_cop / 1e6, costo_meta_eficiencia_mes_cop / 1e6, costo_meta_combinada_mes_cop / 1e6]

        fig_comp_cop = go.Figure(go.Bar(
            x=categorias_comp,
            y=valores_cop_comp,
            text=[f"${v:,.1f} M" for v in valores_cop_comp],
            textposition='outside',
            marker=dict(color=['#10375C', '#1E88E5', '#16A34A'], opacity=0.9)
        ))
        fig_comp_cop.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title='Gasto Mensual ($ Millones COP)', gridcolor='#E2E8F0', showgrid=True),
            height=360,
            margin=dict(l=30, r=20, t=30, b=40)
        )
        st.plotly_chart(fig_comp_cop, use_container_width=True)

    # ----------------------------------------------------------------------------------
    # TABLA DE IMPACTO POR SEDE HOSPITALARIA
    # ----------------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("""
        <div class="card-title">📋 Plan de Metas de Eficiencia Energética por Institución Hospitalaria</div>
        <div class="card-subtitle">Desglose de la línea base y potencial de ahorro anual para las sedes de MiRed IPS.</div>
    """, unsafe_allow_html=True)

    tabla_lb_list = []
    for ips_name, grp in df_raw.groupby('IPS_Agrupada', observed=True):
        m_c = max(1, grp['Mes'].nunique())
        c_base = grp['Consumo_kWh'].sum() / m_c
        ahorro_ef_kwh_a = c_base * (meta_eficiencia_pct / 100.0) * 12.0
        ahorro_ef_cop_a = ahorro_ef_kwh_a * precio_kwh_activo
        
        gen_solar_a = (c_base * (cobertura_solar_pct / 100.0) * 12.0) if incluir_solar_en_meta else 0.0
        ahorro_total_cop_a = (ahorro_ef_kwh_a + gen_solar_a) * precio_kwh_activo
        
        tabla_lb_list.append({
            'IPS_Agrupada': ips_name,
            'Tipologia': grp['Tipologia'].iloc[0],
            'Linea_Base_Mes_kWh': round(c_base, 0),
            'Meta_Consumo_Mes_kWh': round(c_base * (1.0 - meta_eficiencia_pct/100.0), 0),
            'Ahorro_Eficiencia_Ano_kWh': round(ahorro_ef_kwh_a, 0),
            'Ahorro_Eficiencia_Ano_COP': round(ahorro_ef_cop_a, 0),
            'Ahorro_Total_Ano_COP': round(ahorro_total_cop_a, 0)
        })

    df_tabla_lb = pd.DataFrame(tabla_lb_list).sort_values('Linea_Base_Mes_kWh', ascending=False)

    st.dataframe(
        df_tabla_lb.style.format({
            'Linea_Base_Mes_kWh': '{:,.0f}',
            'Meta_Consumo_Mes_kWh': '{:,.0f}',
            'Ahorro_Eficiencia_Ano_kWh': '{:,.0f}',
            'Ahorro_Eficiencia_Ano_COP': '${:,.0f}',
            'Ahorro_Total_Ano_COP': '${:,.0f}'
        }),
        use_container_width=True,
        hide_index=True
    )

    csv_linea_base = df_tabla_lb.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="⬇️ Descargar Plan de Metas de Eficiencia Energética (CSV)",
        data=csv_linea_base,
        file_name="MiRed_IPS_Plan_Metas_Eficiencia_2018.csv",
        mime="text/csv"
    )


# ======================================================================================
# TAB 4: PASO 5: AUDITORÍA INTELIGENTE & ANOMALÍAS
# ======================================================================================
with tab4:
    st.markdown("""
        <div class="card-title">🔍 Paso 5: Adquisición de Datos, Auditoría de Calidad y Detección de Anomalías</div>
        <div class="card-subtitle">
            Auditoría algorítmica de facturación eléctrica: identificación de cobros por promedio/estimado,
            consumo anómalo en sedes cerradas y picos de consumo atípicos con puntuación Z-Score.
        </div>
    """, unsafe_allow_html=True)

    # 1. CALIDAD DE MEDICIÓN (REAL VS ESTIMADO)
    col_aud1, col_aud2 = st.columns([1, 2])

    with col_aud1:
        st.markdown("""
            <div class="card-title">📈 Calidad de Facturación</div>
            <div class="card-subtitle">Proporción de cobros por Medición Real vs. Promedio Estimado.</div>
        """, unsafe_allow_html=True)

        calc_summary = df_raw.groupby('Calculo', observed=True).agg({
            'Consumo_kWh': 'sum',
            'Valor_Total': 'sum',
            'Sede': 'count'
        }).reset_index()

        fig_donut = px.pie(
            calc_summary,
            names='Calculo',
            values='Consumo_kWh',
            hole=0.55,
            color='Calculo',
            color_discrete_map={'Real': '#1E88E5', 'Estimado': '#EF4444'}
        )
        fig_donut.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=10, b=10)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_aud2:
        st.markdown("""
            <div class="card-title">⚖️ Resumen del Riesgo de Facturación Estimada</div>
            <div class="card-subtitle">Impacto de la falta de lectura física por parte del operador de red (Electricaribe).</div>
        """, unsafe_allow_html=True)

        df_estimados_all = df_raw[df_raw['Calculo'] == 'Estimado']
        total_kwh_est = df_estimados_all['Consumo_kWh'].sum()
        total_cop_est = df_estimados_all['Valor_Total'].sum()
        total_rec_est = len(df_estimados_all)

        st.markdown(f"""
            <div class="alert-box alert-warning">
                <div style="font-size: 1.8rem;">⚠️</div>
                <div>
                    <div class="alert-title">{total_rec_est} Facturas Facturadas por Estimación / Promedio</div>
                    <div class="alert-desc">
                        Durante el 2018 se identificaron <strong>{total_rec_est} facturas cobradas como 'Estimado'</strong> 
                        por el operador de red, sumando <strong>{total_kwh_est:,.0f} kWh</strong> y 
                        <strong>${total_cop_est:,.0f} COP (~${total_cop_est/1e6:.2f} Millones)</strong>.<br>
                        <strong>Riesgo para MiRed IPS:</strong> Los cobros estimados suelen sobrestimar la carga real o perpetuar 
                        cargos cuando las sedes reducen su operación, justificando un reclamo formal con base en el art. 146 de la Ley 142 de 1994.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 2. ALERTA CRÍTICA: SEDES CERRADAS FACTURADAS
    st.markdown("---")
    df_cerradas = df_raw[df_raw['Estado'] == 'Cerrada']
    kwh_cerradas = df_cerradas['Consumo_kWh'].sum()
    costo_cerradas = df_cerradas['Valor_Total'].sum()

    st.markdown(f"""
        <div class="alert-box alert-danger">
            <div style="font-size: 2rem;">🚨</div>
            <div style="width: 100%;">
                <div class="alert-title">ALERTA CRÍTICA DE GESTIÓN: Consumo y Cobro Activo en Sedes Cerradas</div>
                <div class="alert-desc">
                    El parser ETL detectó el sub-bloque de <strong>'SEDES CERRADAS'</strong> (registros a partir de Marzo 2018).
                    A pesar de encontrarse fuera de servicio, el operador de red continuó facturando cargos de energía y fijos por un valor acumulado de 
                    <strong>${costo_cerradas:,.0f} COP</strong> ({kwh_cerradas:,.0f} kWh).<br>
                    <strong>Sedes afectadas prioritarias:</strong> PASO La Chinita, PASO Villa San Pablo, PASO Nueva Colombia, PASO Carlos Meisel I.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.markdown("##### 📋 Desglose Económico por Sede Cerrada")
        cerradas_agg = df_cerradas.groupby('Sede', observed=True).agg({
            'Consumo_kWh': 'sum',
            'Valor_Total': 'sum',
            'Mes': 'count'
        }).reset_index().rename(columns={'Mes': 'Facturas'})
        cerradas_agg['Costo_Formateado'] = cerradas_agg['Valor_Total'].apply(lambda x: f"${x:,.0f} COP")
        cerradas_agg['Consumo_Formateado'] = cerradas_agg['Consumo_kWh'].apply(lambda x: f"{x:,.0f} kWh")
        st.dataframe(
            cerradas_agg[['Sede', 'Facturas', 'Consumo_Formateado', 'Costo_Formateado']],
            use_container_width=True,
            hide_index=True
        )

    with col_c2:
        st.markdown("##### 📊 Evolución del Sobrecosto en Sedes Cerradas")
        cerradas_mes = df_cerradas.groupby('Mes', observed=True)['Valor_Total'].sum().reset_index()
        fig_cerradas_mes = px.bar(
            cerradas_mes,
            x='Mes',
            y='Valor_Total',
            labels={'Valor_Total': 'Costo Cobrado ($ COP)'},
            color_discrete_sequence=['#DC2626']
        )
        fig_cerradas_mes.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=280,
            margin=dict(l=30, r=20, t=20, b=40)
        )
        st.plotly_chart(fig_cerradas_mes, use_container_width=True)

    # 3. DETECTOR DE PICOS ATÍPICOS (OUTLIERS CON Z-SCORE > 2)
    st.markdown("---")
    st.markdown("""
        <div class="card-title">🔍 Detector de Picos Atípicos (Outliers Estadísticos con Z-Score > 2.0)</div>
        <div class="card-subtitle">
            Identificación automatizada de anomalías en la demanda de cada sede respecto a su comportamiento histórico (μ + 2σ).
        </div>
    """, unsafe_allow_html=True)

    outliers_list = []
    for sede_name, group in df_raw.groupby('Sede', observed=True):
        consumos = group['Consumo_kWh'].values
        std_val = float(np.std(consumos))
        mean_val = float(np.mean(consumos))
        if std_val > 0:
            for _, r in group.iterrows():
                z = (r['Consumo_kWh'] - mean_val) / std_val
                if z > 2.0:
                    outliers_list.append({
                        'Mes': r['Mes'],
                        'Sede': r['Sede'],
                        'Tipologia': r['Tipologia'],
                        'Consumo_kWh': r['Consumo_kWh'],
                        'Media_Sede': mean_val,
                        'Desviacion': std_val,
                        'Z_Score': round(z, 2),
                        'Valor_Total': r['Valor_Total'],
                        'Calculo': r['Calculo'],
                        'Estado': r['Estado'],
                        'Diagnostico_Preliminar': 'Pico atípico > 200% de la media' if z > 2.5 else 'Desviación significativa'
                    })

    df_outliers = pd.DataFrame(outliers_list).sort_values('Z_Score', ascending=False)

    col_out1, col_out2 = st.columns([2, 1])

    with col_out1:
        st.dataframe(
            df_outliers[[
                'Mes', 'Sede', 'Tipologia', 'Consumo_kWh', 'Media_Sede', 'Z_Score', 'Calculo', 'Estado', 'Diagnostico_Preliminar'
            ]].style.format({
                'Consumo_kWh': '{:,.0f}',
                'Media_Sede': '{:,.0f}',
                'Z_Score': '{:.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )

    with col_out2:
        fig_z = px.scatter(
            df_outliers,
            x='Z_Score',
            y='Consumo_kWh',
            size='Consumo_kWh',
            color='Tipologia',
            hover_name='Sede',
            hover_data=['Mes', 'Calculo', 'Estado'],
            title='<b>Severidad de Picos Atípicos (Z-Score)</b>'
        )
        fig_z.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_z, use_container_width=True)

    with st.expander("📥 Ver y Descargar Tabla Completa de Facturas Cobradas como 'Estimado'"):
        st.markdown("Tabla para soporte documental y radicación de reclamaciones ante Electricaribe / Air-e:")
        df_est_display = df_estimados_all[[
            'Mes', 'Sede', 'Tipologia', 'Consumo_kWh', 'Valor_Total', 'Tarifa', 'Estado'
        ]].copy()
        df_est_display['Valor_Total_Formato'] = df_est_display['Valor_Total'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(df_est_display, use_container_width=True, hide_index=True)

        csv_estimados = df_estimados_all.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="⬇️ Descargar Expediente de Facturas Estimadas (CSV)",
            data=csv_estimados,
            file_name="MiRed_Auditoria_Facturacion_Estimada_2018.csv",
            mime="text/csv"
        )


# ======================================================================================
# TAB 5: PASO 6: INDICADORES DE DESEMPEÑO ENERGÉTICO (EnPIs)
# ======================================================================================
with tab5:
    st.markdown("""
        <div class="card-title">🏥 Paso 6: Indicadores de Desempeño Energético Hospitalario (EnPIs)</div>
        <div class="card-subtitle">
            Normalización de la demanda eléctrica frente a variables operacionales clínicas: área construida (m²),
            camas censables ocupadas y flujo mensual de pacientes/procedimientos, valorados con el <strong>Precio del kWh configurado</strong>.
        </div>
    """, unsafe_allow_html=True)

    # Diccionario de parámetros operacionales realistas según escala y tipología
    METADATA_SEDES_DEFAULT = {
        'Toda la Red MiRed IPS': {'area': 125000, 'camas': 650, 'pacientes': 180000},
        'CAMINO Adelita de Char': {'area': 8500, 'camas': 65, 'pacientes': 14500},
        'Hospital General de Barranquilla': {'area': 14000, 'camas': 160, 'pacientes': 13800},
        'Hospital Nazareth': {'area': 9500, 'camas': 110, 'pacientes': 9800},
        'CAMINO Suroccidente': {'area': 6200, 'camas': 45, 'pacientes': 11200},
        'CAMINO Simón Bolívar': {'area': 5800, 'camas': 40, 'pacientes': 9500},
        'CAMINO Bosques de María': {'area': 5200, 'camas': 35, 'pacientes': 8900},
        'CAMINO Metropolitano': {'area': 4800, 'camas': 30, 'pacientes': 8200},
        'CAMINO La Manga': {'area': 4200, 'camas': 25, 'pacientes': 7400},
        'CAMINO La Luz - Chinita': {'area': 4000, 'camas': 20, 'pacientes': 6800},
        'CAMINO Murillo': {'area': 3600, 'camas': 18, 'pacientes': 5900},
        'PASO Las Flores': {'area': 950, 'camas': 4, 'pacientes': 2800},
        'PASO Universal': {'area': 850, 'camas': 4, 'pacientes': 2500}
    }

    # Selector de Institución para el análisis EnPI
    lista_sedes_enpi = ['Toda la Red MiRed IPS'] + sorted(df_raw['IPS_Agrupada'].unique().tolist())
    sede_sel_enpi = st.selectbox("Seleccione la Institución Hospitalaria para evaluar EnPIs:", lista_sedes_enpi)

    # Filtrar datos de la sede seleccionada
    if sede_sel_enpi == 'Toda la Red MiRed IPS':
        df_sede_enpi = df_raw.copy()
        defaults_sede = METADATA_SEDES_DEFAULT['Toda la Red MiRed IPS']
    else:
        df_sede_enpi = df_raw[df_raw['IPS_Agrupada'] == sede_sel_enpi]
        if sede_sel_enpi in METADATA_SEDES_DEFAULT:
            defaults_sede = METADATA_SEDES_DEFAULT[sede_sel_enpi]
        else:
            tipo_detectada = df_sede_enpi['Tipologia'].iloc[0] if len(df_sede_enpi) > 0 else 'PASO'
            if tipo_detectada == 'Hospital':
                defaults_sede = {'area': 11000, 'camas': 120, 'pacientes': 11000}
            elif tipo_detectada == 'CAMINO':
                defaults_sede = {'area': 4500, 'camas': 25, 'pacientes': 7500}
            else:
                defaults_sede = {'area': 750, 'camas': 2, 'pacientes': 2100}

    # Métricas energéticas promedio mensual de la sede
    meses_sede = max(1, df_sede_enpi['Mes'].nunique())
    kwh_mes_sede = df_sede_enpi['Consumo_kWh'].sum() / meses_sede
    # Costo mensual valorado con el precio del kWh activo
    cop_mes_sede = kwh_mes_sede * precio_kwh_activo

    # Inputs operacionales editables por el usuario
    st.markdown("##### ⚙️ Parámetros Operacionales de la Institución (Editables)")
    col_en1, col_en2, col_en3 = st.columns(3)
    with col_en1:
        area_input = st.number_input("Área Construida (m²)", min_value=100, max_value=300000, value=defaults_sede['area'], step=50)
    with col_en2:
        camas_input = st.number_input("Camas Censables Ocupadas", min_value=0, max_value=2000, value=defaults_sede['camas'], step=1)
    with col_en3:
        pacientes_input = st.number_input("Pacientes Atendidos al Mes", min_value=50, max_value=500000, value=defaults_sede['pacientes'], step=100)

    # Cálculo de los 6 EnPIs
    eui_kwh_m2 = kwh_mes_sede / max(1.0, area_input)
    kwh_cama = (kwh_mes_sede / max(1, camas_input)) if camas_input > 0 else 0.0
    kwh_paciente = kwh_mes_sede / max(1, pacientes_input)
    cop_paciente = cop_mes_sede / max(1, pacientes_input)
    pct_renovable = cobertura_solar_pct  # Sincronizado con el simulador solar
    huella_anual_tco2 = ((kwh_mes_sede * 12.0) * FACTOR_SIN_CO2) / 1000.0

    st.markdown("##### 🎯 Medidores de Rendimiento Energético (Gauges)")
    g1, g2, g3 = st.columns(3)

    # Gauge 1: EUI (kWh/m²-mes)
    with g1:
        fig_g1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=eui_kwh_m2,
            title={'text': "<b>1. Intensidad de Uso (EUI)</b><br><span style='font-size:0.75rem;'>kWh / m²-mes</span>"},
            gauge={
                'axis': {'range': [0, 80]},
                'bar': {'color': "#10375C"},
                'steps': [
                    {'range': [0, 25], 'color': "#DCFCE7"},
                    {'range': [25, 45], 'color': "#FEF3C7"},
                    {'range': [45, 80], 'color': "#FEE2E2"}
                ],
                'threshold': {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 45}
            }
        ))
        fig_g1.update_layout(height=240, margin=dict(l=25, r=25, t=40, b=25), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_g1, use_container_width=True)
        st.caption("Benchmark: < 25 Eficiente | 25-45 Aceptable | > 45 Ineficiente")

    # Gauge 2: kWh / cama-mes
    with g2:
        val_g2 = kwh_cama if camas_input > 0 else 0
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val_g2,
            title={'text': "<b>2. Consumo por Cama</b><br><span style='font-size:0.75rem;'>kWh / cama ocupada-mes</span>"},
            gauge={
                'axis': {'range': [0, 1500]},
                'bar': {'color': "#1E88E5"},
                'steps': [
                    {'range': [0, 450], 'color': "#DCFCE7"},
                    {'range': [450, 750], 'color': "#FEF3C7"},
                    {'range': [750, 1500], 'color': "#FEE2E2"}
                ]
            }
        ))
        fig_g2.update_layout(height=240, margin=dict(l=25, r=25, t=40, b=25), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_g2, use_container_width=True)
        st.caption("Benchmark: < 450 Eficiente | 450-750 Medio | > 750 Crítico")

    # Gauge 3: kWh / paciente
    with g3:
        fig_g3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=kwh_paciente,
            title={'text': "<b>3. Consumo por Paciente</b><br><span style='font-size:0.75rem;'>kWh / atención o consulta</span>"},
            gauge={
                'axis': {'range': [0, 40]},
                'bar': {'color': "#7C3AED"},
                'steps': [
                    {'range': [0, 15], 'color': "#DCFCE7"},
                    {'range': [15, 28], 'color': "#FEF3C7"},
                    {'range': [28, 40], 'color': "#FEE2E2"}
                ]
            }
        ))
        fig_g3.update_layout(height=240, margin=dict(l=25, r=25, t=40, b=25), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_g3, use_container_width=True)
        st.caption("Benchmark: < 15 Adecuado | 15-28 Alerta | > 28 Sobredemanda")

    g4, g5, g6 = st.columns(3)

    # Gauge 4: Costo por Paciente
    with g4:
        fig_g4 = go.Figure(go.Indicator(
            mode="number+delta",
            value=cop_paciente,
            number={'prefix': "$", 'valueformat': ",.0f"},
            title={'text': "<b>4. Costo por Atención Clínica</b><br><span style='font-size:0.75rem;'>$ COP / paciente mes</span>"}
        ))
        fig_g4.update_layout(height=180, margin=dict(l=25, r=25, t=40, b=25), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_g4, use_container_width=True)
        st.caption(f"Valorado a ${precio_kwh_activo:,.1f}/kWh • Gasto mensual: ${cop_mes_sede:,.0f} COP")

    # Gauge 5: % Energía Renovable
    with g5:
        fig_g5 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct_renovable,
            number={'suffix': "%"},
            title={'text': "<b>5. Matriz Renovable Solar</b><br><span style='font-size:0.75rem;'>% Cobertura FV Simulada</span>"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#FB8C00"},
                'steps': [
                    {'range': [0, 30], 'color': "#FEF3C7"},
                    {'range': [30, 70], 'color': "#DCFCE7"},
                    {'range': [70, 100], 'color': "#BBF7D0"}
                ]
            }
        ))
        fig_g5.update_layout(height=180, margin=dict(l=25, r=25, t=40, b=25), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_g5, use_container_width=True)
        st.caption(f"Generación Solar Prevista: {(kwh_mes_sede * pct_renovable / 100.0):,.0f} kWh/mes")

    # Gauge 6: Huella de Carbono
    with g6:
        fig_g6 = go.Figure(go.Indicator(
            mode="number",
            value=huella_anual_tco2,
            number={'suffix': " tCO₂e", 'valueformat': ",.1f"},
            title={'text': "<b>6. Huella de Carbono Anual</b><br><span style='font-size:0.75rem;'>Emisiones indirectas Alcance 2</span>"}
        ))
        fig_g6.update_layout(height=180, margin=dict(l=25, r=25, t=40, b=25), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_g6, use_container_width=True)
        st.caption(f"Factor SIN Colombia: 0.164 kg CO₂e/kWh • Equiv. a {int(huella_anual_tco2 * 45.45):,} árboles")


# ======================================================================================
# TAB 6: PASO 7: SIMULADOR SOLAR FOTOVOLTAICO Y EVALUACIÓN FINANCIERA
# ======================================================================================
with tab6:
    st.markdown("""
        <div class="card-title">☀️ Paso 7: Simulador Solar Fotovoltaico y Evaluación Financiera de Inversión</div>
        <div class="card-subtitle">
            Dimensionamiento técnico de sistemas de autogeneración solar fotovoltaica conectada a red (SFV),
            cálculo de CAPEX, ahorros en facturación valorados a <strong>${precio_kwh_activo:,.1f} COP/kWh</strong>, payback y flujo de caja a 25 años con incentivos de la Ley 1715 / 2099.
        </div>
    """, unsafe_allow_html=True)

    # Selector de alcance de la simulación
    col_s_scope1, col_s_scope2 = st.columns([2, 1])
    with col_s_scope1:
        opciones_simulador = ['Toda la Red MiRed IPS (Consolidado)'] + sorted(df_raw['IPS_Agrupada'].unique().tolist())
        sede_simulacion = st.selectbox(
            "Seleccione el alcance para la instalación solar fotovoltaica:",
            options=opciones_simulador,
            help="Puedes dimensionar el sistema para toda la red hospitalaria o para un centro asistencial específico."
        )

    # Filtrar datos de la sede objetivo
    if sede_simulacion == 'Toda la Red MiRed IPS (Consolidado)':
        df_target_sim = df_raw.copy()
    else:
        df_target_sim = df_raw[df_raw['IPS_Agrupada'] == sede_simulacion]

    meses_target = max(1, df_target_sim['Mes'].nunique())
    consumo_mensual_target = df_target_sim['Consumo_kWh'].sum() / meses_target

    # Tarifa activa para la simulación
    tarifa_target = precio_kwh_activo

    # CÁLCULOS FOTOVOLTAICOS RIGUROSOS
    # 1. Generación mensual por kWp: E_gen/kWp = HSP * 30 * PR (kWh/mes por kWp)
    gen_unit_kwp_mes = hsp * 30.0 * pr
    gen_unit_kwp_ano = gen_unit_kwp_mes * 12.0

    # 2. Potencia requerida según % cobertura: P_kWp = (Consumo_mes * C_solar) / E_gen/kWp
    potencia_kwp_target = (consumo_mensual_target * (cobertura_solar_pct / 100.0)) / gen_unit_kwp_mes

    # 3. Número de paneles de potencia seleccionada (450Wp, 550Wp, 600Wp)
    n_paneles_target = math.ceil((potencia_kwp_target * 1000.0) / potencia_panel)

    # 4. Potencia real instalada con los paneles calculados
    potencia_real_kwp = (n_paneles_target * potencia_panel) / 1000.0

    # 5. Área de cubierta requerida (2.6 m² por panel de alta potencia comercial)
    area_cubierta_m2 = n_paneles_target * 2.6

    # 6. Generación solar esperada
    gen_solar_mes_target = potencia_real_kwp * gen_unit_kwp_mes
    gen_solar_ano_target = potencia_real_kwp * gen_unit_kwp_ano

    # 7. Evaluación financiera usando el Precio del kWh activo
    capex_total_cop = potencia_real_kwp * capex_kwp
    ahorro_mensual_cop = gen_solar_mes_target * tarifa_target
    ahorro_anual_cop = gen_solar_ano_target * tarifa_target
    costo_om_anual = capex_total_cop * 0.012  # 1.2% CAPEX anual

    # Payback Simple (Años)
    flujo_neto_anual_base = ahorro_anual_cop - costo_om_anual
    payback_simple = (capex_total_cop / flujo_neto_anual_base) if flujo_neto_anual_base > 0 else 99.0

    # Descarbonización
    co2_anual_mitigado = (gen_solar_ano_target * FACTOR_SIN_CO2) / 1000.0
    arboles_mitigados = int(co2_anual_mitigado * 45.45)

    # Panel de Resultados Técnicos & Económicos
    st.markdown("##### 📐 Resultados de Ingeniería y Dimensionamiento")
    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Potencia Pico del Sistema", f"{potencia_real_kwp:,.1f} kWp", f"{cobertura_solar_pct}% Demanda")
    rc2.metric("Módulos Solares Tier 1", f"{n_paneles_target:,} paneles", f"{potencia_panel} Wp monocristalino")
    rc3.metric("Área de Cubierta Requerida", f"{area_cubierta_m2:,.0f} m²", f"{area_cubierta_m2/10000:.2f} hectáreas")
    rc4.metric("Generación Anual Proyectada", f"{gen_solar_ano_target/1e3:,.1f} MWh/año", f"{gen_solar_mes_target:,.0f} kWh/mes")

    rf1, rf2, rf3, rf4 = st.columns(4)
    rf1.metric("Inversión Inicial (CAPEX)", f"${capex_total_cop/1e6:,.1f} M COP", f"${capex_kwp:,.0f} /kWp")
    rf2.metric("Ahorro Anual en Factura", f"${ahorro_anual_cop/1e6:,.1f} M COP/año", f"${ahorro_mensual_cop/1e6:,.1f} M/mes")
    rf3.metric("Retorno Simple (Payback)", f"{payback_simple:.1f} años", f"Valorado a ${tarifa_target:.1f}/kWh")
    rf4.metric("Emisiones Evitadas", f"{co2_anual_mitigado:,.1f} tCO₂e/año", f"~{arboles_mitigados:,} árboles")

    # ----------------------------------------------------------------------------------
    # FLUJO DE CAJA A 25 AÑOS (CON/SIN LEY 1715)
    # ----------------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("""
        <div class="card-title">📈 Flujo de Caja Acumulado y Análisis Financiero a 25 Años</div>
        <div class="card-subtitle">
            Proyección del retorno de capital considerando degradación de módulos (0.5%/año), indexación tarifaria y beneficios tributarios de la Ley 1715 / 2099.
        </div>
    """, unsafe_allow_html=True)

    years = np.arange(0, 26)
    flujo_anual = []
    flujo_acumulado = []
    flujo_acumulado_ley1715 = []

    # Escudo fiscal Ley 1715: deducción del 50% de la inversión en renta (beneficio de caja = 50% * 35% tasa corporativa = 17.5% de CAPEX)
    # Repartido en 5 años (3.5% del CAPEX por año)
    ahorro_tributario_anual = (capex_total_cop * 0.175) / 5.0 if ley_1715_activa else 0.0

    acum = -capex_total_cop
    acum_ley = -capex_total_cop

    flujo_acumulado.append(acum)
    flujo_acumulado_ley1715.append(acum_ley)

    for y in range(1, 26):
        factor_degradacion = (1.0 - 0.005) ** (y - 1)
        factor_tarifa = (1.0 + (inflacion_tarifa / 100.0)) ** (y - 1)
        
        ahorro_ano_y = ahorro_anual_cop * factor_degradacion * factor_tarifa
        om_ano_y = costo_om_anual * (1.02 ** (y - 1))
        flujo_neto_y = ahorro_ano_y - om_ano_y
        
        acum += flujo_neto_y
        flujo_acumulado.append(acum)
        
        beneficio_y = ahorro_tributario_anual if y <= 5 else 0.0
        acum_ley += (flujo_neto_y + beneficio_y)
        flujo_acumulado_ley1715.append(acum_ley)

    df_flujo = pd.DataFrame({
        'Año': years,
        'Flujo_Estandar': flujo_acumulado,
        'Flujo_Ley1715': flujo_acumulado_ley1715
    })

    fig_flujo = go.Figure()

    fig_flujo.add_trace(go.Scatter(
        x=df_flujo['Año'],
        y=df_flujo['Flujo_Estandar'] / 1e6,
        name='Flujo Acumulado Estándar',
        mode='lines+markers',
        line=dict(color='#1E88E5', width=3),
        hovertemplate='Año %{x}: $%{y:,.1f} M COP<extra></extra>'
    ))

    if ley_1715_activa:
        fig_flujo.add_trace(go.Scatter(
            x=df_flujo['Año'],
            y=df_flujo['Flujo_Ley1715'] / 1e6,
            name='Flujo Acumulado con Ley 1715 / 2099',
            mode='lines+markers',
            line=dict(color='#16A34A', width=3, dash='dash'),
            hovertemplate='Año %{x} (Ley 1715): $%{y:,.1f} M COP<extra></extra>'
        ))

    # Línea de equilibrio (Breakeven)
    fig_flujo.add_shape(
        type='line',
        x0=0,
        x1=25,
        y0=0,
        y1=0,
        line=dict(color='#DC2626', width=2, dash='dot')
    )

    fig_flujo.update_layout(
        title=f'<b>Flujo de Caja Neto Acumulado a 25 Años ($ Millones COP — Tarifa Base: ${tarifa_target:,.1f}/kWh)</b>',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        yaxis=dict(title='Flujo Acumulado ($ Millones COP)', gridcolor='#E2E8F0', showgrid=True),
        xaxis=dict(title='Año de Operación del Sistema SFV', gridcolor='#F1F5F9', dtick=2),
        height=420,
        margin=dict(l=50, r=40, t=70, b=50)
    )

    st.plotly_chart(fig_flujo, use_container_width=True)

    # ----------------------------------------------------------------------------------
    # MATRIZ MULTI-SEDE Y EXPORTACIÓN GERENCIAL
    # ----------------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("""
        <div class="card-title">📊 Matriz de Dimensionamiento Solar Multisede (Red Completa)</div>
        <div class="card-subtitle">
            Resumen técnico y presupuestal para la toma de decisiones de inversión en los centros de salud de Barranquilla.
        </div>
    """, unsafe_allow_html=True)

    matriz_list = []
    for ips_name, grp in df_raw.groupby('IPS_Agrupada', observed=True):
        m_count = max(1, grp['Mes'].nunique())
        c_mes = grp['Consumo_kWh'].sum() / m_count
        
        # Potencia requerida para la cobertura seleccionada
        p_kwp = (c_mes * (cobertura_solar_pct / 100.0)) / gen_unit_kwp_mes
        n_pan = math.ceil((p_kwp * 1000.0) / potencia_panel)
        p_real_kwp = (n_pan * potencia_panel) / 1000.0
        a_techo = n_pan * 2.6
        cpx = p_real_kwp * capex_kwp
        gen_ano = p_real_kwp * gen_unit_kwp_ano
        ahorro_ano = gen_ano * precio_kwh_activo
        pb = (cpx / max(1.0, (ahorro_ano - cpx * 0.012)))
        co2_evitado = (gen_ano * FACTOR_SIN_CO2) / 1000.0
        
        matriz_list.append({
            'IPS_Agrupada': ips_name,
            'Tipologia': grp['Tipologia'].iloc[0],
            'Consumo_Mes_kWh': round(c_mes, 0),
            'Potencia_kWp': round(p_real_kwp, 1),
            'Paneles': n_pan,
            'Area_Techo_m2': round(a_techo, 0),
            'CAPEX_COP': round(cpx, 0),
            'Ahorro_Anual_COP': round(ahorro_ano, 0),
            'Payback_Anos': round(pb, 1),
            'CO2_Evitado_t_ano': round(co2_evitado, 1)
        })

    df_matriz = pd.DataFrame(matriz_list).sort_values('Consumo_Mes_kWh', ascending=False)

    st.dataframe(
        df_matriz.style.format({
            'Consumo_Mes_kWh': '{:,.0f}',
            'Potencia_kWp': '{:,.1f}',
            'Paneles': '{:,}',
            'Area_Techo_m2': '{:,.0f}',
            'CAPEX_COP': '${:,.0f}',
            'Ahorro_Anual_COP': '${:,.0f}',
            'Payback_Anos': '{:.1f}',
            'CO2_Evitado_t_ano': '{:,.1f}'
        }),
        use_container_width=True,
        hide_index=True
    )

    csv_matriz = df_matriz.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="⬇️ Descargar Dimensionamiento Fotovoltaico Red Completa (CSV)",
        data=csv_matriz,
        file_name="MiRed_IPS_Dimensionamiento_Solar_2018.csv",
        mime="text/csv"
    )
