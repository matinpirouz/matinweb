from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import mm
import arabic_reshaper
from bidi.algorithm import get_display

def en_to_fa_numbers(text):
    en_digits = "0123456789"
    fa_digits = "۰۱۲۳۴۵۶۷۸۹"
    for en, fa in zip(en_digits, fa_digits):
        text = text.replace(en, fa)
    return text

def rtl_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def wrap_text(text, max_width, canvas_obj, font_name="Vazir", font_size=11):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if canvas_obj.stringWidth(test_line, font_name, font_size) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines



def create_invoice_pdf(
    filename,
    invoice_number,
    customer_name,
    date,
    items,
    discription,
    shop_name,
    shop_phone_number,
    invoice_type,
    discount=0,
    previous_debt=0

    ):
    
    c = canvas.Canvas('media/' + filename, pagesize=portrait(A4))
    pdfmetrics.registerFont(TTFont('Vazir', 'Vazir.ttf'))
    c.setFont('Vazir', 14)

    width, height = portrait(A4)
    margin = 5 * mm
    
    
    # اطلاعات مشتری
    customer_info_data = [
        [rtl_text(f"شماره: {en_to_fa_numbers(str(invoice_number))}")],
        [rtl_text(f"تاریخ: {en_to_fa_numbers(date)}")],
        [rtl_text(f"تلفن: {en_to_fa_numbers(shop_phone_number)}"), rtl_text(f"صورت حساب آقای/خانم: {customer_name}")],
    ]
    row_height = 25
    col_widths_info = [100, 450]
    table_top_info = height - margin + 8
    x_info = width - margin - sum(col_widths_info)
    y_info = table_top_info
    c.setFont('Vazir', 12)
    for row in customer_info_data:
        for i, cell in enumerate(row):
            width_cell = col_widths_info[i]
            c.setFillColor(colors.black)
            c.drawRightString(x_info + sum(col_widths_info[:i + 1]) - 5, y_info - row_height + 7, cell)
        y_info -= row_height

    # عنوان‌ها
    c.setFont('Vazir', 17)
    c.drawCentredString(width / 2, height - margin - 20, rtl_text(shop_name))
    c.drawCentredString(width / 2, height - margin - 50, rtl_text(invoice_type))


    # جدول
    c.setFont('Vazir', 11)
    table_top = height - margin - 80
    row_height = 25
    headers = ["ردیف", "نام کالا", "سایز", "نوع خدمات", "تعداد", "مبلغ کل"]
    col_widths = [30, 240, 35, 140, 35, 85]

    x = width - margin
    for i, header in enumerate(headers):
        c.setFillColor(colors.white)
        c.rect(x - col_widths[i], table_top - row_height, col_widths[i], row_height, stroke=1, fill=1)
        c.setFillColor(colors.black)
        c.drawCentredString(x - col_widths[i] / 2, table_top - row_height + 7, rtl_text(header))
        x -= col_widths[i]
    c.setFillColor(colors.black)

    total = 0
    y = table_top - row_height
    c.setFont('Vazir', 11)

    for i, item in enumerate(items):
        if y - row_height < margin:
            c.showPage()
            pdfmetrics.registerFont(TTFont('Vazir', 'Vazir.ttf'))
            c.setFont('Vazir', 11)
            y = height - margin

            # دوباره رسم هدر جدول
            x = width - margin
            for i_header, header in enumerate(headers):
                c.setFillColor(colors.white)
                c.rect(x - col_widths[i_header], y - row_height, col_widths[i_header], row_height, stroke=1, fill=1)
                c.setFillColor(colors.black)
                c.drawCentredString(x - col_widths[i_header] / 2, y - row_height + 7, rtl_text(header))
                x -= col_widths[i_header]
            c.setFillColor(colors.black)
            y -= row_height

        y -= row_height
        x = width - margin


        c.setFillColor(colors.black)

        price = int(item.get("price", 0)) if item.get("price") != '' else 0
        total += price

        values = [
            en_to_fa_numbers(str(i + 1)),
            rtl_text(item["name"]),
            en_to_fa_numbers(str(item.get("size", "-"))),
            rtl_text(item["type"]),
            en_to_fa_numbers(str(item.get('qty'))),
            en_to_fa_numbers(f"{rtl_text('ریال')} {price:11,}"),
        ]

        for j in range(len(col_widths)):
            if i % 2 == 0:
                c.setFillColorRGB(0.85, 0.85, 0.85)
            else:
                c.setFillColor(colors.white)
            c.rect(x - col_widths[j], y, col_widths[j], row_height, stroke=1, fill=1)
            c.setFillColor(colors.black)
            c.drawCentredString(x - col_widths[j] / 2, y + 7, values[j])
            x -= col_widths[j]

    rows = [("جمع کل", total)]

    if discount > 0:
        rows.append(("تخفیف", discount))

    if previous_debt > 0:
        rows.append(("بدهی قبلی", previous_debt))

    payable = total - discount + previous_debt
    
    if previous_debt > 0 and discount > 0:
        rows.append(("مبلغ قابل پرداخت", payable))

        # جمع کل
    box_width = 240
    line_height = 22
    padding = 10

    box_height = line_height * len(rows) + padding * 2

    box_x = width - margin - box_width
    box_y = y - 10

    # پس‌زمینه کادر
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(box_x, box_y - box_height, box_width, box_height, stroke=1, fill=1)

    # متن داخل کادر
    current_y = box_y - padding - 12
    c.setFillColor(colors.black)

    for label, value in rows:
        c.setFont('Vazir', 13)

        c.drawRightString(
            box_x + box_width - padding,
            current_y,
            rtl_text(f"{label}: {en_to_fa_numbers(f'{value:,}')} ریال")
        )

        current_y -= line_height

    y = box_y - box_height - 20

    if discription != '':
        c.drawRightString(width - margin, y - 23, rtl_text("توضیحات: " + discription))
    else:
        discription = None
        
#    c.drawRightString(width - margin - 100 , y - 53 + (0 if discription else 30), rtl_text("مهر و امضا خریدار"))
#    c.drawRightString(margin + 180, y - 53 + (0 if discription else 30), rtl_text("مهر و امضا فروشنده"))
    c.drawCentredString(width / 2, y - 53 + (0 if discription else 30), rtl_text(f"خواهشمند است مبلغ فاکتور را به شماره کارت {en_to_fa_numbers('3904-1825-2910-5022')} نزد بانک پاسارگاد به نام"))
    c.drawCentredString(width / 2, y - 83 + (0 if discription else 30), rtl_text(f"مسعود پیروز واریز و رسید آن را برای شماره {en_to_fa_numbers(shop_phone_number)} در پیام‌رسان واتساپ یا بله ارسال نمایید."))
    c.save()
    
    return c
