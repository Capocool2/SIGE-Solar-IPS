"""
ETL Motor - SIGE-Solar IPS
Procesamiento y Estandarización de Consumos Eléctricos 2018
Red Pública Hospitalaria de Barranquilla (MiRed IPS)
"""

import os
import re
import unicodedata
import pandas as pd
import numpy as np


def clean_number(val):
    """
    Convierte valores numéricos con formatos variados (strings con $, comas, barras, etc.)
    a float de manera segura.
    """
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace('$', '').replace(' ', '')
    if '/' in s:
        return 0.0
    if ',' in s and '.' in s:
        if s.find(',') < s.find('.'):
            s = s.replace(',', '')
        else:
            s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        s = s.replace(',', '.')
    try:
        return float(s)
    except Exception:
        return 0.0


def standardize_text(s):
    """
    Normaliza texto eliminando acrónimos con puntos (C.A.M.I.N.O. -> CAMINO, P.A.S.O. -> PASO),
    corrigiendo caracteres dañados de codificación y estandarizando espaciado.
    """
    if not isinstance(s, str):
        return ''
    s = s.strip()
    # Reemplazo de puntos en acrónimos
    s = re.sub(r'C\.A\.M\.I\.N\.O\.?', 'CAMINO', s, flags=re.IGNORECASE)
    s = re.sub(r'P\.A\.S\.O\.?', 'PASO', s, flags=re.IGNORECASE)
    s = re.sub(r'\bCamino\b', 'CAMINO', s)
    s = re.sub(r'\bPaso\b', 'PASO', s)
    
    # Corrección de posibles caracteres con errores de codificación
    corrections = {
        'Mara': 'María',
        'Mara': 'María',
        'Simn': 'Simón',
        'Simn': 'Simón',
        'Lpez': 'López',
        'Lpez': 'López',
        'Galn': 'Galán',
        'Galn': 'Galán',
        'Jos': 'José',
        'Jos': 'José'
    }
    for bad, good in corrections.items():
        s = s.replace(bad, good)
        
    # Corrección adicional si hay codepoints especiales
    s = s.replace('\ufffd', 'ó') # En caso de que persista caracter de sustitución
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def consolidate_ips(sede_clean):
    """
    Consolida múltiples medidores y sedes satélite en una sola institución agrupada.
    """
    s = sede_clean
    if re.search(r'Adelita de Char', s, re.IGNORECASE):
        return 'CAMINO Adelita de Char'
    if re.search(r'Hospital General de Barranquilla', s, re.IGNORECASE):
        return 'Hospital General de Barranquilla'
    if re.search(r'Hospital Nazareth', s, re.IGNORECASE):
        return 'Hospital Nazareth'
    if re.search(r'La Luz.*Chinita', s, re.IGNORECASE) or re.search(r'Chinita.*La Luz', s, re.IGNORECASE):
        return 'CAMINO La Luz - Chinita'
    if re.search(r'Carlos Meisel', s, re.IGNORECASE):
        return 'PASO Carlos Meisel'
    if re.search(r'Esmeralda Lipaya', s, re.IGNORECASE):
        return 'PASO Esmeralda Lipaya'
    if re.search(r'Las Flores', s, re.IGNORECASE):
        return 'PASO Las Flores'
    if re.search(r'Nueva Colombia', s, re.IGNORECASE):
        return 'PASO Nueva Colombia'
    if re.search(r'Villa San Pablo', s, re.IGNORECASE):
        return 'PASO Villa San Pablo'
        
    # Eliminar sufijos numéricos o de medidor como ' 1', ' 2', ' I', ' II'
    s_group = re.sub(r'\s+\d+$', '', s)
    s_group = re.sub(r'\s+[I|V|X]+$', '', s_group)
    return s_group.strip()


def classify_tipologia(name):
    """
    Clasifica la sede en 'Hospital', 'CAMINO' o 'PASO'.
    """
    u = name.upper()
    if 'HOSPITAL' in u:
        return 'Hospital'
    elif 'CAMINO' in u:
        return 'CAMINO'
    elif 'PASO' in u or 'CENTRO' in u or 'PUESTO' in u:
        return 'PASO'
    return 'CAMINO'


def load_and_process_excel(filepath='CONSUMO DE ENERGIA 2018.xlsx'):
    """
    Motor ETL principal. Procesa las 11 hojas del libro Excel, resuelve heterogeneidades
    de cabeceras, limpia registros, aplica reglas de negocio y genera un DataFrame estandarizado.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe en la ruta de trabajo.")

    xl = pd.ExcelFile(filepath)
    records = []

    # Meses ordenados cronológicamente
    ordered_months = [
        'ENERO 2018', 'FEBRERO 2018', 'MARZO 2018', 'ABRIL 2018', 'MAYO 2018', 'JUNIO 2018',
        'JULIO 2018', 'AGOSTO 2018', 'SEPTIEMBRE 2018', 'OCTUBRE 2018', 'NOVIEMBRE 2018'
    ]
    month_name_map = {m.strip().upper(): m for m in ordered_months}

    for sheet in xl.sheet_names:
        sheet_clean = sheet.strip()
        df_raw = xl.parse(sheet, header=None)

        # 1. Detección dinámica de la fila de encabezados
        header_idx = None
        for idx, row in df_raw.iterrows():
            val0 = str(row[0]).strip().upper() if pd.notna(row[0]) else ''
            if val0 in ['SEDES', 'SEDE']:
                header_idx = idx
                break

        if header_idx is None:
            continue

        header_row = [str(x).strip() if pd.notna(x) else '' for x in df_raw.iloc[header_idx].values]

        # 2. Mapeo dinámico de columnas
        col_sede = 0
        col_consumo = None
        col_total = None
        col_tarifa = None
        col_calculo = None

        for c_idx, col_name in enumerate(header_row):
            u_name = col_name.upper()
            if 'CONSUMO' in u_name and col_consumo is None:
                col_consumo = c_idx
            elif 'TOTAL' in u_name and 'DIAS' not in u_name and 'DÍAS' not in u_name and col_total is None:
                col_total = c_idx
            elif 'TARIFA' in u_name and col_tarifa is None:
                col_tarifa = c_idx
            elif 'CALCULO' in u_name or 'CÁLCULO' in u_name:
                col_calculo = c_idx

        # Omitir fila de subencabezado si existe '(kWh)' o 'Desde'
        start_r = header_idx + 1
        if start_r < len(df_raw):
            val_check = str(df_raw.iloc[start_r, col_consumo]).strip() if pd.notna(df_raw.iloc[start_r, col_consumo]) else ''
            row_str = ' '.join([str(x).upper() for x in df_raw.iloc[start_r].values if pd.notna(x)])
            if '(KWH)' in val_check.upper() or 'DESDE' in row_str:
                start_r += 1

        estado = 'Habilitada'
        prev_sede = None

        for r in range(start_r, len(df_raw)):
            row = df_raw.iloc[r]
            val0 = row[col_sede]
            str0 = str(val0).strip() if pd.notna(val0) else ''
            u0 = str0.upper()

            # Evitar cabeceras duplicadas
            if u0 in ['SEDES', 'SEDE']:
                continue

            # Detección de bloque 'SEDES CERRADAS'
            if 'SEDES CERRADAS' in u0 or any('SEDES CERRADAS' in str(c).upper() for c in row.values if pd.notna(c)):
                estado = 'Cerrada'
                continue

            # Filtro de filas de totales, firmas y notas
            ignored_keywords = [
                'TOTAL', 'SUBTOTAL', 'ACLARACI', 'OBSERV', 'REVIS', 'GESTI',
                'CARLOS ALBERTO', 'ANA MILENA', 'TOTALES'
            ]
            if any(kw in u0 for kw in ignored_keywords):
                continue

            consumo_val = clean_number(row[col_consumo]) if col_consumo is not None else 0.0
            total_val = clean_number(row[col_total]) if col_total is not None else 0.0

            # Descartar filas con el total mensual global (>= 500,000 kWh)
            if consumo_val >= 500000:
                continue

            # Herencia de sede previa para el caso de Julio (Hospital General de Barranquilla 2 con sede NaN)
            sede_name = str0
            if (not sede_name or sede_name.lower() == 'nan') and 0 < consumo_val < 500000 and prev_sede:
                sede_name = prev_sede

            if not sede_name or sede_name.lower() == 'nan':
                continue

            prev_sede = sede_name

            # Limpieza y corrección de tarifas
            tarifa_val = clean_number(row[col_tarifa]) if col_tarifa is not None else 0.0
            if tarifa_val > 2000:
                tarifa_val = tarifa_val / 100.0

            # Clasificación del cálculo (Medición Real vs Estimado)
            calculo_raw = str(row[col_calculo]).strip() if col_calculo is not None and pd.notna(row[col_calculo]) else ''
            if sheet_clean == 'ENERO 2018':
                calculo_val = 'Real'
            else:
                u_calc = calculo_raw.upper()
                if 'ESTIMAD' in u_calc or 'PROMEDIO' in u_calc:
                    calculo_val = 'Estimado'
                elif 'MEDIC' in u_calc or 'REAL' in u_calc:
                    calculo_val = 'Real'
                else:
                    calculo_val = 'Real'

            sede_cleaned = standardize_text(sede_name)
            ips_agrupada = consolidate_ips(sede_cleaned)
            tipologia = classify_tipologia(sede_cleaned)

            # Estandarizar nombre del mes sin espacios residuales
            mes_std = month_name_map.get(sheet_clean.upper(), sheet_clean)

            records.append({
                'Mes': mes_std,
                'Sede_Original': sede_name,
                'Sede': sede_cleaned,
                'IPS_Agrupada': ips_agrupada,
                'Tipologia': tipologia,
                'Consumo_kWh': consumo_val,
                'Valor_Total': total_val,
                'Tarifa': tarifa_val,
                'Calculo': calculo_val,
                'Estado': estado
            })

    df = pd.DataFrame(records)

    # Ordenar meses cronológicamente como categoría
    month_order = [
        'ENERO 2018', 'FEBRERO 2018', 'MARZO 2018', 'ABRIL 2018', 'MAYO 2018', 'JUNIO 2018',
        'JULIO 2018', 'AGOSTO 2018', 'SEPTIEMBRE 2018', 'OCTUBRE 2018', 'NOVIEMBRE 2018'
    ]
    df['Mes'] = pd.Categorical(df['Mes'], categories=month_order, ordered=True)
    df = df.sort_values(['Mes', 'Tipologia', 'IPS_Agrupada']).reset_index(drop=True)

    return df


if __name__ == '__main__':
    df = load_and_process_excel()
    print("=== CONTROL DE CALIDAD ETL ===")
    print(f"Total registros: {len(df)}")
    print(f"Consumo Total: {df['Consumo_kWh'].sum():,.2f} kWh (Esperado: 8,922,163.00)")
    print(f"Costo Total: ${df['Valor_Total'].sum():,.2f} COP (Esperado: $3,580,300,966.00)")
    assert round(df['Consumo_kWh'].sum(), 2) == 8922163.00, "Error en validación de Consumo kWh"
    assert round(df['Valor_Total'].sum(), 2) == 3580300966.00, "Error en validación de Costo COP"
    print("VALIDACIÓN EXITOSA: Consumo y costo coinciden exactamente al 100%.")
