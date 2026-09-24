import os
import json
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
from PIL import Image
import io

def analizar_recibo(imagen_bytes: bytes, api_key: str = None) -> dict:
    """
    Analiza una imagen de un recibo utilizando modelos Gemini (3.8 Flash / 3.5 Flash-Lite / 2.5 Flash)
    y retorna un diccionario JSON estandarizado con los campos extraídos.
    """
    api_key_to_use = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key_to_use:
        raise ValueError("No se proporcionó una API Key de Gemini. Configúrala en las variables de entorno o en la app.")

    client = genai.Client(api_key=api_key_to_use)
    image = Image.open(io.BytesIO(imagen_bytes))

    prompt = """
    Analiza la imagen de este recibo de pago o factura y extrae la información requerida.
    Debes responder ÚNICAMENTE con un objeto JSON válido sin bloques de código markdown extraños y con el siguiente esquema exacto:
    {
      "fecha_pago": "YYYY-MM-DD o formato original legible si no se identifica año",
      "nombre_cliente": "Nombre del cliente o pagador",
      "monto_total": "Monto numérico o total pagado",
      "concepto_pago": "Descripción corta o concepto del pago",
      "numero_referencia": "Número de transacción, folio o referencia (si existe, sino N/A)"
    }
    """

    # Probar con modelos disponibles (del más reciente al más antiguo)
    modelos = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-2.5-flash"]
    last_error = None

    for model_name in modelos:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[image, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                )
            )
            raw_text = response.text.strip()
            # Limpiar markdown si el modelo lo incluye
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            
            return json.loads(raw_text.strip())
        except Exception as e:
            last_error = e

    raise RuntimeError(f"Error al analizar el recibo con Gemini API: {last_error}")
