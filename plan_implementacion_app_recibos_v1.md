# Plan de Implementación: Escáner de Recibos y Gestión Financiera (Costo $0)

Este documento contiene las especificaciones detalladas y las instrucciones exactas que debes entregarle a un agente de programación (o LLM) para que genere todo el código de la aplicación de manera estructurada y sin errores. 

La arquitectura recomendada utiliza herramientas de despliegue rápido y análisis de datos en Python, ideales para integrarse con repositorios de GitHub y entornos locales (como VS Code en Windows o Ubuntu).

---

## Arquitectura del Proyecto (Stack Tecnológico)
*   **Frontend (Interfaz Móvil):** Streamlit (usando el widget `st.camera_input`).
*   **Backend & Lógica:** Python.
*   **Motor de Visión Artificial (OCR):** Gemini 2.5 Flash / 1.5 Flash API (Tier gratuito vía Google AI Studio). SDK: `google-genai`.
*   **Base de Datos / Registro:** Pandas para estructuración de datos y `openpyxl` para escritura en Excel (`.xlsx`).
*   **Generador de Comprobantes:** ReportLab (creación de `.pdf` formales).
*   **Despliegue:** Streamlit Community Cloud (Alojamiento web 100% gratuito vinculado a Git).

---

## Fase 1: Configuración del Entorno y Dependencias
**Objetivo:** Preparar el entorno virtual y asegurar que las librerías necesarias estén instaladas.

**Instrucción para el Agente de IA:**
> "Actúa como un ingeniero de software experto en Python. Crea el archivo `requirements.txt` para un proyecto que utilizará Streamlit para la interfaz, el SDK `google-genai` (SDK unificado de Google AI) para visión artificial, `pandas` y `openpyxl` para manejar registros en Excel, `reportlab` para generar PDFs, `pillow` para procesamiento de imágenes, y `python-dotenv` para gestión de variables de entorno. El archivo debe listar solo dependencias directas con versiones mínimas (sin pin exacto), para compatibilidad con Streamlit Community Cloud."

---

## Fase 2: Módulo de Visión Artificial (Extracción de Datos)
**Objetivo:** Conectar la imagen capturada con el LLM multimodal para estructurar el texto del recibo en formato JSON.

**Instrucción para el Agente de IA:**
> "Escribe un módulo en Python usando el SDK `google-genai` (`from google import genai`). Crea una función llamada `analizar_recibo(imagen_bytes, api_key)` que reciba la imagen escaneada de un recibo como bytes y una API key opcional. Usa `genai.Client` y prueba los modelos `gemini-2.5-flash` y `gemini-1.5-flash` en ese orden (fallback). El prompt interno debe obligar al modelo a devolver ÚNICAMENTE un objeto JSON válido con las claves: `fecha_pago`, `nombre_cliente`, `monto_total`, `concepto_pago` y `numero_referencia`. Usa `response_mime_type='application/json'` en la configuración. Maneja errores de conexión, formato JSON inválido y limpieza de bloques markdown en la respuesta."

---

## Fase 3: Procesamiento de Datos y Registro en Excel
**Objetivo:** Tomar el JSON extraído y agregarlo como una nueva fila en un archivo de Excel acumulativo, validando que los datos sean correctos.

**Instrucción para el Agente de IA:**
> "Escribe un módulo en Python usando `pandas` que tome el diccionario JSON devuelto por la API de IA y lo agregue a un archivo local llamado `registro_pagos.xlsx`. Si el archivo no existe, el script debe crearlo con los encabezados adecuados. Asegúrate de limpiar los datos (ej. quitar símbolos de moneda del monto para dejarlo numérico) antes de guardar. Usa `openpyxl` como motor de Pandas para evitar problemas de compatibilidad."

---

## Fase 4: Generación del Documento Financiero (PDF)
**Objetivo:** Crear un recibo digital oficial en PDF que sirva como comprobante para el cliente y la entidad financiera.

**Instrucción para el Agente de IA:**
> "Escribe un script en Python utilizando la librería `reportlab`. Crea una función `generar_comprobante_pdf(datos_json)` que reciba el JSON extraído en el paso anterior y genere un archivo `.pdf`. El PDF debe tener un diseño limpio y profesional: un título centrado, un recuadro o tabla estilizada con la información del cliente, monto, fecha, concepto y referencia, y un texto en el pie de página indicando que es un comprobante válido. Devuelve la ruta del archivo generado."

---

## Fase 5: Interfaz de Usuario e Integración (Frontend con Streamlit)
**Objetivo:** Unir todos los módulos en una aplicación interactiva que se pueda usar desde el navegador de un teléfono móvil.

**Instrucción para el Agente de IA:**
> "Crea el archivo principal `app.py` utilizando Streamlit. La aplicación debe tener:
> 1. Un título y una descripción de uso.
> 2. El widget `st.camera_input` para permitir al usuario tomar una foto del recibo físico desde el celular.
> 3. Al capturar la foto, mostrar un *spinner* de carga (`st.spinner`).
> 4. Invocar la función de visión artificial para extraer los datos.
> 5. Mostrar los datos extraídos en pantalla para que el usuario los revise (opcionalmente editables).
> 6. Invocar las funciones para actualizar el archivo de Excel y generar el PDF.
> 7. Mostrar un botón de descarga (`st.download_button`) para que el usuario pueda bajar el PDF generado y otro para el Excel."

---

## Fase 6: Despliegue a Producción (Costo $0)
**Pasos a realizar manualmente (No requiere código de IA):**
1. Sube tu código (archivos `.py`, `.md`, `.gitignore` y `requirements.txt`) a un repositorio público o privado en **GitHub**. 
2. Ingresa a **Streamlit Community Cloud** (share.streamlit.io).
3. Conecta tu cuenta de GitHub.
4. Selecciona tu repositorio y apunta al archivo `app.py`.
5. En la sección "Advanced Settings" de Streamlit, configura tus variables de entorno (Secrets) agregando tu API Key: `GEMINI_API_KEY = "tu_clave_aqui"`.
6. Haz clic en "Deploy". Obtendrás una URL pública que puedes abrir desde el navegador de tu dispositivo móvil y usar tu cámara de inmediato.
