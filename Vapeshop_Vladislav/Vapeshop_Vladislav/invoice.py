

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
from reportlab.lib import colors
from django.http import HttpResponse
from goods.models import Line

def generate_invoice(order, order_items):
    pdfmetrics.registerFont(TTFont('Times New Roman', 'static/fonts/times.ttf'))
    pdfmetrics.registerFont(TTFont('Times New Roman Bold', 'static/fonts/times_bold.ttf'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Order_{order.order_number}.pdf"'
    c = SimpleDocTemplate(response, pagesize=A4,)
    elements = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TimesNewRomanBold', fontName='Times New Roman Bold', fontSize=14, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Center', fontName='Times New Roman', fontSize=12, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Left14', fontName='Times New Roman', fontSize=14))
    styles.add(ParagraphStyle(name='Left12', fontName='Times New Roman', fontSize=12))
    styles.add(ParagraphStyle(name='Link', fontName='Times New Roman', fontSize=12, textColor=colors.blue, underline=False))
    elements.append(Paragraph(f"Заказ покупателя №{order.order_number} от {order.created_at.date()}", styles['TimesNewRomanBold']))
    elements.append(Spacer(1, 12))
    telegram_link = 'https://t.me/kotiq212'
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f'Менеджер: <a href="{telegram_link}" color=blue>@kotiq212</a>', styles['Left12']))
    elements.append(Spacer(1, 12))

    data = [
        [Paragraph('N п.п.', styles['Center']), Paragraph('Наименование', styles['Center']), Paragraph('Количество (Шт)', styles['Center']), Paragraph('Цена (BYN)', styles['Center']), Paragraph('Сумма (BYN)', styles['Center'])]
    ]

    value = 0
    lines = Line.objects.all()
    for line in lines:
        count = 1
        for i in order_items:
            if i.product.line == line:
                if count == 1:
                    data.append(['', Paragraph(str(line), styles['TimesNewRomanBold'])])
                data.append([Paragraph(str(count), styles['Center']), Paragraph(str(f'{i.product.line}-{i.product.taste} ({i.product.stronghold})'), styles['Left12']), Paragraph(str(i.quantity), styles['Center']), Paragraph(str(float(i.price)), styles['Center']), Paragraph(str(float(i.price) * float(i.quantity)), styles['Center'])])
                count +=1
                value += i.quantity
    col_widths = [40, 300, 60, 60, 60]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
                               ('FONTSIZE', (0, 0), (-1, -1), 14),
                               ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('TOPPADDING', (0, 0), (-1, -1), 3),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black),]))
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(
        Paragraph(f"Общее количество позиций заказа: {value} штук", styles['Left14']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Итоговая стоимоть заказа (с учетом возможных скидок): {order.total_price} BYN", styles['Left14']))
    c.build(elements)
    return response
