import unittest
import os
import pandas as pd
from data_module import limpiar_monto, registrar_pago
from pdf_module import generar_comprobante_pdf

class TestRecibos(unittest.TestCase):

    def test_limpiar_monto(self):
        self.assertEqual(limpiar_monto("$1,250.50"), 1250.50)
        self.assertEqual(limpiar_monto("1.250,50"), 1250.50)
        self.assertEqual(limpiar_monto("500"), 500.0)
        self.assertEqual(limpiar_monto(None), 0.0)

    def test_registrar_pago(self):
        test_excel = "test_registro.xlsx"
        if os.path.exists(test_excel):
            os.remove(test_excel)

        datos = {
            "fecha_pago": "2026-09-09",
            "nombre_cliente": "Juan Perez",
            "monto_total": "$150.00",
            "concepto_pago": "Servicios de Consultoria",
            "numero_referencia": "REF-9988"
        }

        df = registrar_pago(datos, excel_path=test_excel)
        self.assertTrue(os.path.exists(test_excel))
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Monto Total ($)"], 150.0)

        if os.path.exists(test_excel):
            os.remove(test_excel)

    def test_generar_pdf(self):
        datos = {
            "fecha_pago": "2026-09-09",
            "nombre_cliente": "Maria Lopez",
            "monto_total": "320.75",
            "concepto_pago": "Compra de Insumos",
            "numero_referencia": "REF-1122"
        }
        pdf_bytes = generar_comprobante_pdf(datos)
        self.assertIsNotNone(pdf_bytes)
        self.assertTrue(len(pdf_bytes) > 0)

if __name__ == "__main__":
    unittest.main()
