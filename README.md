# SIGE-Solar IPS 🏥☀️

**Sistema Inteligente de Apoyo a la Gestión Energética Hospitalaria Basado en Energía Solar Fotovoltaica, Analítica con Python y Diseño UX/UI**  
*Aplicado a la Red Pública Hospitalaria de Barranquilla (**MiRed IPS**)*

---

## 🌟 Resumen Ejecutivo

**SIGE-Solar IPS** es una plataforma web analítica de alta fidelidad orientada a la toma de decisiones gerenciales en la red hospitalaria pública de Barranquilla (**MiRed IPS**). Integra los **7 pasos del modelo metodológico de Gestión Energética Hospitalaria**:

1. **Caracterización del Consumo Energético:** Análisis de la demanda mensual histórica (Enero - Noviembre 2018) y proyección fiscal de Diciembre mediante Regresión Lineal de Machine Learning.
2. **Identificación de Áreas y Sedes Críticas:** Curva de Pareto (80/20) para las Top 12 IPS de mayor demanda y desglose jerárquico Treemap por tipología (*Hospital*, *CAMINO*, *PASO*).
3. **Perfil de Carga y Comportamiento Temporal:** Gráficos duales sincronizados de demanda en kWh y facturación en Millones COP.
4. **Definición de Línea Base vs. Meta:** Comparativa interactiva frente al consumo promedio histórico (811,106 kWh/mes) con metas de reducción configurables (-5% a -30%).
5. **Auditoría Inteligente de Facturación:** Detección automática de cobros por promedio/estimación (43 facturas, ~$64.5M COP), alerta crítica por facturación en sedes cerradas ($9.5M COP a recuperar ante Electricaribe/Air-e) y detección de picos atípicos (*outliers* con $Z\text{-Score} > 2$).
6. **Indicadores de Desempeño Energético (EnPIs):** Normalización de la demanda frente a área construida ($m^2$), camas censables ocupadas y flujo de pacientes/atenciones mediante medidores *Gauge charts* semaforizados.
7. **Simulador Fotovoltaico y Evaluación Financiera:** Dimensionamiento técnico de sistemas solares fotovoltaicos adaptados al recurso solar de Barranquilla ($\text{HSP} = 5.2\text{ h/día}$, $PR = 78\%$), cálculo de CAPEX, ahorros en facturación, payback y flujo de caja a 25 años con incentivos de la **Ley 1715 / 2099 de Colombia**.

---

## 🚀 Puesta en Marcha Rápida

### Requisitos Previos
- Python 3.10 o superior instalado.
- Archivo de datos: `CONSUMO DE ENERGIA 2018.xlsx` (incluido en la raíz del proyecto).

### 1. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecución de la Aplicación
```bash
streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador web en `http://localhost:8501`.

---

## 📂 Estructura del Proyecto

```text
├── app.py                      # Aplicación principal Streamlit con inyección CSS y dashboards
├── etl.py                      # Motor ETL automatizado con validación matemática de balance
├── requirements.txt            # Librerías y versiones requeridas
├── CONSUMO DE ENERGIA 2018.xlsx# Dataset original con las 11 hojas de facturación
└── README.md                   # Documentación técnica y manual de usuario
```

---

## ⚙️ Control de Calidad y Validación ETL

El motor `etl.py` resuelve de forma 100% automatizada las heterogeneidades del libro Excel:
- **Detección dinámica de cabeceras** en filas variables (filas 5 a 8).
- **Mapeo dinámico de columnas:** identificación de Sede, Consumo, Valor Total, Tarifa y Tipo de Cálculo.
- **Herencia de sedes para registros sin etiqueta:** herencia de nombre para el registro de Julio en Hospital General de Barranquilla 2 ($2,509\text{ kWh}$, $\$1,126,270\text{ COP}$).
- **Clasificación del sub-bloque `'SEDES CERRADAS'`:** marca de estado `Cerrada` sin descartar los registros para auditoría.
- **Corrección tipográfica en tarifas:** detección de errores como tarifa $43,129 \rightarrow 431.29\text{ \$/kWh}$.
- **Consolidación en `IPS_Agrupada`:** unificación de medidores múltiples (Hospital General de Barranquilla 1 a 4, Hospital Nazareth 1 a 6, CAMINO La Luz Chinita 1 y 2, PASO Carlos Meisel I y II, etc.).

### Balance de Control:
- **Consumo Total Limpio Acumulado:** `8,922,163.00 kWh` (Diferencia: 0.00 kWh).
- **Costo Total Limpio Acumulado:** `$3,580,300,966.00 COP` (Diferencia: $0.00 COP).
- **Distribución por Tipología:** CAMINO (61.2%), PASO (22.2%), Hospital (16.7%).

---

## ☀️ Fórmulas de Ingeniería Fotovoltaica (Barranquilla)

1. **Generación mensual por kWp instalado:**
   $$E_{\text{gen/kWp}} = \text{HSP} \times 30 \times PR = 5.2 \times 30 \times 0.78 = 121.68\text{ kWh/mes por kWp}$$

2. **Potencia pico requerida para cobertura solar ($C_{\text{solar}}$):**
   $$P_{\text{kWp}} = \frac{\text{Consumo Mensual Promedio (kWh)} \times C_{\text{solar}}}{E_{\text{gen/kWp}}}$$

3. **Número de módulos solares:**
   $$N_{\text{paneles}} = \lceil \frac{P_{\text{kWp}} \times 1000}{P_{\text{panel (W)}}} \rceil$$

4. **Área de cubierta requerida:**
   $$A_{\text{techo}} = N_{\text{paneles}} \times 2.6\text{ m}^2$$

5. **Mitigación de emisiones de $\text{CO}_2$ (Factor SIN Colombia):**
   $$\text{Emisiones Evitadas} = \text{Generación Anual (kWh)} \times 0.164\text{ kg CO}_2\text{e/kWh} \times 10^{-3}\text{ t/kg}$$

---

## ⚖️ Marco Tributario y Financiero: Ley 1715 de Colombia
La plataforma incorpora los incentivos tributarios de la **Ley 1715 de 2014 / Ley 2099 de 2021**:
- **Deducción de Renta:** Hasta el 50% del valor de la inversión en un período no mayor a 15 años.
- **Depreciación Acelerada:** Tasa máxima anual de hasta el 33.33% en equipos solares.
- **Exclusión de IVA y Arancel:** 0% en la adquisición de paneles solares, inversores y controladores.
- **Impacto Financiero:** Reducción sustancial del período de retorno de la inversión (**Payback simple** a menos de 4 a 5 años).
