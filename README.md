# Escáner de Recibos y Gestión Financiera (Costo $0)

Aplicación web desarrollada en Streamlit para el escaneo, extracción inteligente de datos con Gemini AI, almacenamiento acumulativo en Excel y generación de comprobantes digitales en PDF.

## 🚀 Características
- **Captura desde Celular/Cámara:** Widget directo `st.camera_input`.
- **Visión Artificial con Gemini AI:** Extrae fecha, cliente, monto total, concepto y referencia en formato JSON.
- **Registro Acumulativo en Excel:** Guardado automático mediante Pandas y `openpyxl`.
- **Generador de Comprobantes PDF:** Documentos profesionales generados con `reportlab`.

## 🛠️ Instalación y Uso Local

1. Clonar el repositorio.
2. Crear un entorno virtual e instalar las dependencias:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # En Windows
   pip install -r requirements.txt
   ```
3. Iniciar la aplicación Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Ingresa tu `GEMINI_API_KEY` en el menú lateral o agrégala a un archivo `.env`.

## ☁️ Despliegue en Streamlit Community Cloud
1. Sube este código a GitHub.
2. Conecta el repositorio en [Streamlit Community Cloud](https://share.streamlit.io/).
3. En **Advanced Settings**, agrega el secret:
   ```toml
   GEMINI_API_KEY = "tu_api_key_aqui"
   ```
4. Despliega y listo.
