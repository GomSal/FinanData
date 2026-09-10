import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generar_comprobante_pdf(datos_json: dict, output_path: str = None) -> bytes:
    """
    Genera un recibo/comprobante de pago profesional en PDF usando ReportLab.
    Retorna los bytes del archivo generado o guarda el archivo si se especifica output_path.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        output_path if output_path else buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1, # Centrado
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4B5563'),
        alignment=1,
        spaceAfter=25
    )

    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor('#1F2937')
    )

    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor('#374151')
    )

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#6B7280'),
        alignment=1,
        spaceBefore=30
    )

    # Título y encabezado
    story.append(Paragraph("COMPROBANTE DE PAGO", title_style))
    story.append(Paragraph("Documento Digital de Confirmación Financiera", subtitle_style))
    story.append(Spacer(1, 10))

    # Preparar tabla con la información del recibo
    fecha = datos_json.get("fecha_pago", "N/A")
    cliente = datos_json.get("nombre_cliente", "N/A")
    monto = datos_json.get("monto_total", "0.00")
    concepto = datos_json.get("concepto_pago", "N/A")
    referencia = datos_json.get("numero_referencia", "N/A")

    table_data = [
        [Paragraph("Fecha de Pago:", label_style), Paragraph(str(fecha), value_style)],
        [Paragraph("Cliente / Pagador:", label_style), Paragraph(str(cliente), value_style)],
        [Paragraph("Monto Total:", label_style), Paragraph(f"${monto}", value_style)],
        [Paragraph("Concepto de Pago:", label_style), Paragraph(str(concepto), value_style)],
        [Paragraph("No. de Referencia:", label_style), Paragraph(str(referencia), value_style)],
    ]

    t = Table(table_data, colWidths=[2.2 * inch, 4.5 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1F2937')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F3F4F6')),
    ]))

    story.append(t)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Este comprobante ha sido generado automáticamente por el Escáner de Recibos y es válido como registro de operación.", footer_style))

    doc.build(story)

    if output_path:
        return None

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
