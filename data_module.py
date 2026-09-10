import os
import re
import pandas as pd

def limpiar_monto(monto_val) -> float:
    """
    Limpia cadenas de texto para extraer únicamente el número decimal flotante.
    """
    if isinstance(monto_val, (int, float)):
        return float(monto_val)
    
    if not monto_val:
        return 0.0
    
    # Extraer dígitos, puntos y comas
    val_str = str(monto_val).strip()
    # Eliminar símbolos de moneda y caracteres no numéricos excepto comas y puntos
    cleaned = re.sub(r'[^\d.,]', '', val_str)
    
    # Manejar formatos como 1,234.56 o 1.234,56
    if ',' in cleaned and '.' in cleaned:
        if cleaned.rfind(',') > cleaned.rfind('.'):
            # Formato europeo: 1.234,56
            cleaned = cleaned.replace('.', '').replace(',', '.')
        else:
            # Formato americano: 1,234.56
            cleaned = cleaned.replace(',', '')
    elif ',' in cleaned:
        cleaned = cleaned.replace(',', '.')

    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def registrar_pago(datos_json: dict, excel_path: str = "registro_pagos.xlsx") -> pd.DataFrame:
    """
    Agrega un registro JSON formateado como una nueva fila en un archivo de Excel.
    Si el archivo no existe, lo crea con sus encabezados.
    """
    monto_num = limpiar_monto(datos_json.get("monto_total", 0))

    nuevo_registro = {
        "Fecha de Pago": datos_json.get("fecha_pago", "N/A"),
        "Nombre Cliente": datos_json.get("nombre_cliente", "N/A"),
        "Monto Total ($)": monto_num,
        "Concepto": datos_json.get("concepto_pago", "N/A"),
        "Número de Referencia": datos_json.get("numero_referencia", "N/A")
    }

    df_nuevo = pd.DataFrame([nuevo_registro])

    if os.path.exists(excel_path):
        try:
            df_existente = pd.read_excel(excel_path, engine="openpyxl")
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        except Exception:
            df_final = df_nuevo
    else:
        df_final = df_nuevo

    # Guardar en Excel con openpyxl
    df_final.to_excel(excel_path, index=False, engine="openpyxl")
    return df_final
