"""
pdf_gen.py — Generador de presupuestos PDF para KIUSO / Seguridad Reina S.A.
"""
import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas

AZUL  = colors.HexColor('#1a2a4a')
ROJO  = colors.HexColor('#cc0000')
GRIS  = colors.HexColor('#f5f5f5')
BORDE = colors.HexColor('#dddddd')
BLANC = colors.white
NEGRO = colors.black
LOGO  = os.path.join(os.path.dirname(__file__), 'logo.png')

def wrap_text(text, max_width, font="Helvetica", size=8.5):
    """Divide el texto en líneas que caben en max_width."""
    words = str(text).split(' ')
    lines, line = [], ''
    for word in words:
        test = (line + ' ' + word).strip()
        if stringWidth(test, font, size) <= max_width:
            line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines or ['']

def fmt(v):
    if v == 0:
        return "0,00 €"
    e = int(abs(v))
    d = round((abs(v) - e) * 100)
    return f"{e:,}".replace(",", ".") + f",{d:02d} €"

def generar_pdf(path, lineas, cliente, descuento_extra=0, descuento_extra_label="",
                comision=0, comision_label="", comision_suma=True, opciones=None, mostrar_dto=True):
    """
    lineas: lista de dicts {desc, ud, precio_u, total}
    cliente: dict {nombre, telefono, email, direccion, cp, ciudad}
    descuento_extra: % adicional sobre total tras PPP (0 = no aplica)
    comision: % adicional (0 = no aplica), comision_suma: True=suma, False=resta
    """
    c = pdfcanvas.Canvas(path, pagesize=A4)
    w, h = A4
    ml = 20*mm; mr = 20*mm
    cw = w - ml - mr
    y = h - 15*mm

    # Encabezado
    if os.path.exists(LOGO):
        c.drawImage(LOGO, ml, y-18*mm, width=18*mm, height=18*mm,
                    mask='auto', preserveAspectRatio=True)
    tx = ml + 23*mm
    c.setFont("Helvetica-Bold", 11); c.setFillColor(AZUL)
    c.drawString(tx, y-5*mm,  "PUERTAS ACORAZADAS")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(tx, y-10*mm, "SEGURIDAD REINA, S.A.")
    c.setFont("Helvetica", 8); c.setFillColor(NEGRO)
    c.drawString(tx, y-15*mm, "C/ Brinell, 14 · 28906 Getafe (Madrid)")
    c.drawString(tx, y-19*mm, "Tfno.: 91.665.24.76 / Fax: 91.695.81.53  ·  www.puertaskiuso.com")
    y -= 25*mm

    # Línea
    c.setStrokeColor(AZUL); c.setLineWidth(1.5)
    c.line(ml, y, w-mr, y); y -= 8*mm

    # Título
    c.setFillColor(AZUL)
    c.rect(ml, y-8*mm, cw, 10*mm, fill=1, stroke=0)
    c.setFillColor(BLANC); c.setFont("Helvetica-Bold", 13)
    c.drawString(ml+5*mm, y-5.5*mm, "PRESUPUESTO ORIENTATIVO")
    y -= 16*mm

    # Datos cliente
    campos = []
    if cliente.get('nombre'):   campos.append(("CLIENTE",    cliente['nombre']))
    if cliente.get('telefono'): campos.append(("TELÉFONO",   cliente['telefono']))
    if cliente.get('email'):    campos.append(("EMAIL",      cliente['email']))
    if cliente.get('direccion'):campos.append(("DIRECCIÓN",  cliente['direccion']))
    if cliente.get('cp') or cliente.get('ciudad'):
        campos.append(("C.P. / CIUDAD", f"{cliente.get('cp','')} {cliente.get('ciudad','')}".strip()))
    campos.append(("FECHA", date.today().strftime("%d de %B de %Y")
                   .replace("January","enero").replace("February","febrero")
                   .replace("March","marzo").replace("April","abril")
                   .replace("May","mayo").replace("June","junio")
                   .replace("July","julio").replace("August","agosto")
                   .replace("September","septiembre").replace("October","octubre")
                   .replace("November","noviembre").replace("December","diciembre")))

    h_caja = len(campos) * 6*mm + 4*mm
    c.setFillColor(GRIS); c.setStrokeColor(BORDE)
    c.rect(ml, y-h_caja, cw, h_caja+2*mm, fill=1, stroke=1)
    for i, (label, valor) in enumerate(campos):
        yy = y - 5*mm - i*6*mm
        c.setFillColor(AZUL); c.setFont("Helvetica-Bold", 8)
        c.drawString(ml+3*mm, yy, label)
        c.setFillColor(NEGRO); c.setFont("Helvetica", 8)
        c.drawString(ml+28*mm, yy, str(valor))
    y -= h_caja + 8*mm

    # Cabecera tabla
    cols = [cw*0.60, cw*0.06, cw*0.17, cw*0.17]
    c.setFillColor(AZUL)
    c.rect(ml, y-7*mm, cw, 8*mm, fill=1, stroke=0)
    c.setFillColor(BLANC); c.setFont("Helvetica-Bold", 8.5)
    c.drawString(ml+3*mm, y-4.5*mm, "DESCRIPCIÓN")
    c.drawCentredString(ml+cols[0]+cols[1]/2, y-4.5*mm, "Ud.")
    c.drawRightString(ml+cols[0]+cols[1]+cols[2]-3*mm, y-4.5*mm, "Precio unit.")
    c.drawRightString(w-mr-3*mm, y-4.5*mm, "Total")
    y -= 7*mm

    # Columnas: descripcion mas ancha, resto mas estrecho
    cols = [cw*0.60, cw*0.06, cw*0.17, cw*0.17]
    desc_max_w = cols[0] - 6*mm
    LINE_H = 4.5*mm

    for i, ln in enumerate(lineas):
        incluido = ln.get('incluido', False)
        desc_lines = wrap_text(str(ln['desc']), desc_max_w)
        n_lines = len(desc_lines)
        text_block_h = n_lines * LINE_H
        rh = max(8*mm, text_block_h + 4*mm)

        c.setFillColor(BLANC if i%2==0 else GRIS)
        c.setStrokeColor(BORDE)
        c.rect(ml, y-rh, cw, rh, fill=1, stroke=1)

        # Centro vertical de la fila
        mid_y = y - rh/2

        # Centrado vertical correcto:
        # - mid_y es el centro exacto de la fila
        # - Para Helvetica 8.5pt: ascender=6.10pt, descender=1.76pt
        # - center_offset = ascender - (ascender+descender)/2 = 2.17pt = 0.77mm
        # - Para N líneas: primera baseline sube (N-1)*LINE_H/2 para centrar el bloque
        CENTER_OFF = 0.77*mm  # corrección baseline Helvetica 8.5pt
        first_baseline = mid_y + ((n_lines - 1) * LINE_H / 2) - CENTER_OFF
        c.setFillColor(NEGRO); c.setFont("Helvetica", 8.5)
        for li, dl in enumerate(desc_lines):
            c.drawString(ml+3*mm, first_baseline - li*LINE_H, dl)

        # Ud, precio y total — mismo punto de referencia que la descripción (1 línea)
        num_y = mid_y - CENTER_OFF
        c.drawCentredString(ml+cols[0]+cols[1]/2, num_y, str(ln['ud']))

        if incluido:
            c.setFillColor(colors.HexColor('#2a6e3f'))
            c.setFont("Helvetica-Oblique", 7.5)
            c.drawRightString(ml+cols[0]+cols[1]+cols[2]-3*mm, num_y, "Incl. puerta")
            c.drawRightString(w-mr-3*mm, num_y, "Incl. puerta")
        else:
            c.setFillColor(NEGRO); c.setFont("Helvetica", 8.5)
            c.drawRightString(ml+cols[0]+cols[1]+cols[2]-3*mm, num_y, fmt(ln['precio_u']))
            c.drawRightString(w-mr-3*mm, num_y, fmt(ln['total']))
        c.setFillColor(NEGRO)
        y -= rh

    y -= 4*mm

    # Subtotal
    subtotal = sum(ln['total'] for ln in lineas)
    dto_ppp  = round(subtotal * 0.05, 2) if mostrar_dto else 0
    base     = round(subtotal - dto_ppp, 2)

    c.setFont("Helvetica-Bold", 9); c.setFillColor(NEGRO)
    c.drawRightString(w-mr-3*mm-cols[3], y-5*mm, "Subtotal")
    c.drawRightString(w-mr-3*mm, y-5*mm, fmt(subtotal))
    y -= 8*mm

    if mostrar_dto:
        c.setFillColor(ROJO); c.setFont("Helvetica-Bold", 9)
        c.drawRightString(w-mr-3*mm-cols[3], y-5*mm, "Dto. 5% PPP")
        c.drawRightString(w-mr-3*mm, y-5*mm, f"- {fmt(dto_ppp)}")
        y -= 8*mm

    total = base

    # Descuento extra
    if descuento_extra > 0:
        importe_dto = round(base * descuento_extra / 100, 2)
        total = round(total - importe_dto, 2)
        c.setFillColor(ROJO); c.setFont("Helvetica-Bold", 9)
        lbl = descuento_extra_label or f"Dto. {descuento_extra}%"
        c.drawRightString(w-mr-3*mm-cols[3], y-5*mm, lbl)
        c.drawRightString(w-mr-3*mm, y-5*mm, f"- {fmt(importe_dto)}")
        y -= 8*mm

    # Comisión
    if comision > 0:
        importe_com = round(total * comision / 100, 2)
        lbl = comision_label or f"Comisión {comision}%"
        if comision_suma:
            total = round(total + importe_com, 2)
            c.setFillColor(NEGRO); c.setFont("Helvetica-Bold", 9)
            c.drawRightString(w-mr-3*mm-cols[3], y-5*mm, lbl)
            c.drawRightString(w-mr-3*mm, y-5*mm, f"+ {fmt(importe_com)}")
        else:
            total = round(total - importe_com, 2)
            c.setFillColor(ROJO); c.setFont("Helvetica-Bold", 9)
            c.drawRightString(w-mr-3*mm-cols[3], y-5*mm, lbl)
            c.drawRightString(w-mr-3*mm, y-5*mm, f"- {fmt(importe_com)}")
        y -= 8*mm

    y -= 2*mm

    # Total
    c.setStrokeColor(AZUL); c.setLineWidth(1)
    c.line(ml, y, w-mr, y); y -= 2*mm
    c.setFillColor(AZUL)
    c.rect(ml, y-10*mm, cw, 12*mm, fill=1, stroke=0)
    c.setFillColor(BLANC); c.setFont("Helvetica-Bold", 11)
    c.drawString(ml+5*mm, y-6.5*mm, "TOTAL (IVA incluido)")
    c.setFont("Helvetica-Bold", 13)
    c.drawRightString(w-mr-5*mm, y-6.5*mm, fmt(total))
    y -= 18*mm

    # Notas
    notas = [
        "• Precios con IVA incluido.",
        "• Instalación incluida en el precio.",
        "• Presupuesto válido por 30 días desde la fecha de emisión.",
    ]
    if mostrar_dto:
        notas.append("• El descuento del 5% será válido exclusivamente para pedidos confirmados dentro de los 10 días siguientes a la entrega del presupuesto final.")
    for nota in notas:
        c.setFont("Helvetica", 7.5); c.setFillColor(NEGRO)
        c.drawString(ml, y, nota); y -= 5*mm

    y -= 4*mm
    c.setStrokeColor(BORDE); c.setFillColor(GRIS)
    c.rect(ml, y-8*mm, cw, 9*mm, fill=1, stroke=1)
    c.setFont("Helvetica-Oblique", 7.5); c.setFillColor(NEGRO)
    c.drawString(ml+3*mm, y-5*mm,
        "*Este presupuesto es orientativo, no quedará cerrado hasta que el comercial no haga la medición de la puerta.")

    # ── OPCIONES ADICIONALES ─────────────────────────────────────────────
    if opciones:
        y -= 6*mm
        c.setStrokeColor(AZUL); c.setLineWidth(0.8)
        c.line(ml, y, w-mr, y); y -= 7*mm

        c.setFillColor(colors.HexColor('#e8ecf2'))
        c.rect(ml, y-7*mm, cw, 8*mm, fill=1, stroke=0)
        c.setFillColor(AZUL); c.setFont("Helvetica-Bold", 9)
        c.drawString(ml+4*mm, y-4.8*mm, "OPCIONES ADICIONALES — no incluidas en el presupuesto")
        y -= 10*mm

        c.setFont("Helvetica", 7.5); c.setFillColor(colors.HexColor('#555555'))
        c.drawString(ml, y, "Puede ampliar su equipamiento con los siguientes extras. Consúltenos si desea incluirlos.")
        y -= 8*mm

        for i, (nom, pre) in enumerate(opciones):
            bg = BLANC if i % 2 == 0 else GRIS
            c.setFillColor(bg); c.setStrokeColor(BORDE)
            c.rect(ml, y-7*mm, cw, 7*mm, fill=1, stroke=1)
            c.setFont("Helvetica", 8.5); c.setFillColor(NEGRO)
            c.drawString(ml+3*mm, y-4.8*mm, nom)
            c.setFont("Helvetica-Bold", 8.5)
            c.drawRightString(w-mr-3*mm, y-4.8*mm, fmt(pre))
            y -= 7*mm

    # Pie
    c.setStrokeColor(AZUL); c.setLineWidth(0.5)
    c.line(ml, 15*mm, w-mr, 15*mm)
    c.setFont("Helvetica", 7); c.setFillColor(colors.HexColor('#666666'))
    c.drawCentredString(w/2, 10*mm,
        "Puertas Acorazadas · Seguridad Reina, S.A. · C/ Brinell, 14 · 28906 Getafe (Madrid) · www.puertaskiuso.com")

    c.save()
    return total
