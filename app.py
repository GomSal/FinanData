import os
import io
import pandas as pd
# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from ocr_module import analizar_recibo
from data_module import registrar_pago
from pdf_module import generar_comprobante_pdf

st.set_page_config(
    page_title="Escáner de Recibos y Gestión Financiera",
    page_icon="🧾",
    layout="centered"
)

st.title("🧾 Escáner de Recibos y Registro Financiero")
st.markdown("Captura o sube la foto de tu recibo físico para extraer automáticamente la información, registrarla en Excel y generar un comprobante PDF.")

# Configuración de API Key en Sidebar o Entorno
st.sidebar.header("⚙️ Configuración")
api_key_env = os.environ.get("GEMINI_API_KEY", "")
api_key_input = st.sidebar.text_input("Gemini API Key", value=api_key_env, type="password")

if not api_key_input:
    st.sidebar.warning("⚠️ Ingresa tu GEMINI_API_KEY para habilitar la visión artificial.")

# Pestañas para Captura con Cámara o Subir Archivo
tab1, tab2 = st.tabs(["📷 Cámara Móvil", "📁 Cargar Imagen"])
imagen_bytes = None

with tab1:
    foto = st.camera_input("Toma una foto limpia del recibo")
    if foto:
        imagen_bytes = foto.getvalue()

with tab2:
    archivo_subido = st.file_uploader("Subir imagen de recibo (JPG, PNG)", type=["jpg", "jpeg", "png"])
    if archivo_subido:
        imagen_bytes = archivo_subido.getvalue()

EXCEL_PATH = "registro_pagos.xlsx"

if imagen_bytes:
    st.subheader("1. Procesamiento y Extracción por IA")
    st.image(imagen_bytes, caption="Imagen del recibo", use_container_width=True)

    if st.button("🔍 Analizar Recibo con Gemini", type="primary"):
        if not api_key_input:
            st.error("Por favor proporciona una Gemini API Key válida en el menú lateral.")
        else:
            with st.spinner("Procesando recibo con visión artificial..."):
                try:
                    datos = analizar_recibo(imagen_bytes, api_key=api_key_input)
                    st.session_state["datos_recibo"] = datos
                    st.success("¡Datos extraídos correctamente!")
                except Exception as e:
                    st.error(f"Error al analizar el recibo: {str(e)}")

# Si hay datos extraídos en sesión, mostrarlos y permitir edición
if "datos_recibo" in st.session_state:
    st.subheader("2. Revisión y Edición de Datos")
    datos = st.session_state["datos_recibo"]

    with st.form("form_recibo"):
        col1, col2 = st.columns(2)
        with col1:
            fecha_pago = st.text_input("Fecha de Pago", value=str(datos.get("fecha_pago", "")))
            nombre_cliente = st.text_input("Nombre de Cliente / Pagador", value=str(datos.get("nombre_cliente", "")))
            monto_total = st.text_input("Monto Total", value=str(datos.get("monto_total", "")))
        with col2:
            concepto_pago = st.text_input("Concepto de Pago", value=str(datos.get("concepto_pago", "")))
            numero_referencia = st.text_input("Número de Referencia", value=str(datos.get("numero_referencia", "")))

        guardar_btn = st.form_submit_button("💾 Confirmar y Registrar Pago")

        if guardar_btn:
            datos_actualizados = {
                "fecha_pago": fecha_pago,
                "nombre_cliente": nombre_cliente,
                "monto_total": monto_total,
                "concepto_pago": concepto_pago,
                "numero_referencia": numero_referencia
            }
            # Guardar en Excel
            df_actualizado = registrar_pago(datos_actualizados, excel_path=EXCEL_PATH)
            st.session_state["datos_recibo"] = datos_actualizados
            st.success("¡Registro de pago guardado exitosamente en Excel!")

    st.subheader("3. Descarga de Comprobante PDF y Registro")

    datos_finales = st.session_state["datos_recibo"]
    pdf_data = generar_comprobante_pdf(datos_finales)

    col_a, col_b = st.columns(2)

    with col_a:
        st.download_button(
            label="📄 Descargar Comprobante PDF",
            data=pdf_data,
            file_name=f"Comprobante_{datos_finales.get('numero_referencia', 'pago')}.pdf",
            mime="application/pdf"
        )

    with col_b:
        if os.path.exists(EXCEL_PATH):
            with open(EXCEL_PATH, "rb") as f:
                excel_bytes = f.read()
            st.download_button(
                label="📊 Descargar Registro de Pagos (Excel)",
                data=excel_bytes,
                file_name="registro_pagos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Mostrar tabla acumulativa de Excel si existe
if os.path.exists(EXCEL_PATH):
    st.divider()
    st.subheader("📈 Historico de Pagos Registrados")
    try:
        df_hist = pd.read_excel(EXCEL_PATH, engine="openpyxl")
        st.dataframe(df_hist, use_container_width=True)
    except Exception as e:
        st.warning(f"No se pudo cargar el historial: {e}")
