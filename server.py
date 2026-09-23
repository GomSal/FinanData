from mcp.server.fastmcp import FastMCP
import pandas as pd

# 1. Inicializamos el servidor MCP
mcp = FastMCP("Streamlit_Data_Helper")

# 2. Exponemos una herramienta al agente de Antigravity
@mcp.tool()
def generar_resumen_dataframe(ruta_csv: str) -> str:
    """
    Lee un archivo de datos (CSV) local y devuelve un resumen estadístico 
    para que el agente decida qué gráficos de Plotly recomendar.
    """
    try:
        df = pd.read_csv(ruta_csv)
        info = f"Columnas: {list(df.columns)}\nFilas: {len(df)}\n"
        resumen = df.describe().to_string()
        return f"Info del Dataset:\n{info}\nResumen:\n{resumen}"
    except Exception as e:
        return f"Error leyendo el archivo: {str(e)}"

if __name__ == "__main__":
    # 3. El servidor escucha por la entrada estándar (stdio)
    mcp.run()