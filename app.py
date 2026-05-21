"""
app.py — Generador de Presupuestos KIUSO · Seguridad Reina S.A.
"""
import os, tempfile
import streamlit as st
from tarifas import *
from pdf_gen import generar_pdf, fmt

st.set_page_config(page_title="KIUSO · Presupuestos", page_icon="🔒",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif !important;
    font-size: 15px !important;
}
.stApp { background: #f5f3ef; }

/* Inputs más grandes */
[data-testid="stTextInput"] input {
    font-size: 15px !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    border: 1.5px solid #d8d3c9 !important;
    background: #fffefb !important;
}
[data-testid="stSelectbox"] > div > div {
    font-size: 15px !important;
    border-radius: 8px !important;
    border: 1.5px solid #d8d3c9 !important;
    background: #fffefb !important;
}
[data-testid="stNumberInput"] input {
    font-size: 15px !important;
    border-radius: 8px !important;
    border: 1.5px solid #d8d3c9 !important;
    background: #fffefb !important;
}
[data-testid="stCheckbox"] label p {
    font-size: 14px !important;
    font-weight: 400 !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #3a3530 !important;
}
[data-testid="stRadio"] label p { font-size: 14px !important; }

/* Sección */
.seccion {
    background: #fffefb;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 16px;
    border: 1.5px solid #e5e0d8;
    box-shadow: 0 2px 8px rgba(26,20,10,0.04);
}
.sec-titulo {
    font-family: 'Outfit', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #1a2a4a;
    border-bottom: 2px solid #1a2a4a;
    padding-bottom: 10px;
    margin-bottom: 18px;
}

/* Panel resumen */
.resumen-card {
    background: #1a2a4a;
    color: #f0ece4;
    border-radius: 14px;
    padding: 28px;
    position: sticky;
    top: 20px;
}
.resumen-titulo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
    font-weight: 600;
    color: white;
    margin: 0 0 20px 0;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    padding-bottom: 14px;
    letter-spacing: 0.5px;
}
.li {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    padding: 5px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    gap: 10px;
    line-height: 1.4;
}
.li span:first-child { opacity: .82; flex: 1; }
.li span:last-child  { font-weight: 500; white-space: nowrap; color: #d4cfc6; }
.li0 { opacity: .35 !important; font-style: italic; }
.subtotales {
    margin-top: 14px;
    border-top: 1px solid rgba(255,255,255,0.15);
    padding-top: 12px;
}
.dto {
    color: #f0866a;
    font-size: 13px;
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
}
.subtotal-row {
    color: rgba(255,255,255,0.7);
    font-size: 13px;
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
}
.total-box {
    background: white;
    color: #1a2a4a;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.total-lbl {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #666;
}
.total-imp {
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px;
    font-weight: 600;
    color: #1a2a4a;
    letter-spacing: -0.5px;
}

/* Botón */
.stButton > button {
    background: #1a2a4a !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    width: 100% !important;
    padding: 14px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #253d6e !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(26,42,74,0.3) !important;
}

/* Divisor de categoría en extras */
.cat-header {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #8a8070;
    margin: 14px 0 6px 0;
    padding-bottom: 4px;
    border-bottom: 1px solid #e5e0d8;
}

/* Info boxes */
[data-testid="stInfo"] {
    font-size: 14px !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
cl, ct = st.columns([1, 9])
with cl:
    if os.path.exists(logo_path):
        st.image(logo_path, width=72)
with ct:
    st.markdown("""
    <div style="padding-top:8px">
        <div style="font-family:'Cormorant Garamond',serif;font-size:30px;color:#1a2a4a;font-weight:600;letter-spacing:-0.5px;line-height:1.1">
            Generador de Presupuestos
        </div>
        <div style="font-family:'Outfit',sans-serif;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#9a9285;margin-top:5px">
            Puertas Acorazadas · Seguridad Reina S.A.
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
col_form, col_prev = st.columns([3, 2], gap="large")

# ════════════════════════════════════════════════════════════════════
#  FORMULARIO
# ════════════════════════════════════════════════════════════════════
with col_form:

    # CLIENTE
    st.markdown('<div class="seccion"><div class="sec-titulo">Datos del cliente</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    nombre    = r1.text_input("Nombre / Empresa", placeholder="Nombre completo")
    telefono  = r2.text_input("Teléfono",         placeholder="600 000 000")
    email     = r1.text_input("Email",             placeholder="correo@ejemplo.com")
    direccion = r2.text_input("Dirección",         placeholder="Calle, número, piso")
    rcp, rciu = st.columns(2)
    cp     = rcp.text_input("Código postal", placeholder="28000")
    ciudad = rciu.text_input("Ciudad", placeholder="Madrid")
    st.markdown('</div>', unsafe_allow_html=True)

    # PUERTA
    st.markdown('<div class="seccion"><div class="sec-titulo">Puerta</div>', unsafe_allow_html=True)
    modelo_sel    = st.selectbox("Modelo", list(MODELOS.keys()))
    escalas       = list(MODELOS[modelo_sel].keys())
    escala_sel    = st.selectbox("Escala / Medida", escalas)
    precio_puerta = MODELOS[modelo_sel][escala_sel]
    es_trastero   = modelo_sel in TRASTERO_MODELOS
    if es_trastero:
        st.info("Sin jambas ni embocadura · Cilindro Iseo R7 incluido · Ventilación e inversión sin coste.")
    st.markdown('</div>', unsafe_allow_html=True)

    # TABLEROS
    st.markdown('<div class="seccion"><div class="sec-titulo">Tableros</div>', unsafe_allow_html=True)
    t_labels = [t[0] for t in TABLEROS]
    tic, tec = st.columns(2)

    with tic:
        st.markdown("**Interior**")
        ti_sel  = st.selectbox("Tablero interior", t_labels, label_visibility="collapsed", key="ti")
        ti_data = next(t for t in TABLEROS if t[0] == ti_sel)
        ti_manual = 0
        if ti_data[2] == "manual":
            ti_manual = st.number_input("Precio interior (€)", min_value=0, value=0, step=1, key="ti_m")
        ti_mol_precio = 0
        if ti_data[2] == "madera":
            ti_mol = st.selectbox("Moldurado interior", [m[0] for m in MOLDURADOS], key="ti_mol")
            ti_mol_precio = next(m[1] for m in MOLDURADOS if m[0] == ti_mol)

    with tec:
        st.markdown("**Exterior**")
        te_sel  = st.selectbox("Tablero exterior", t_labels, label_visibility="collapsed", key="te")
        te_data = next(t for t in TABLEROS if t[0] == te_sel)
        te_manual = 0
        if te_data[2] == "manual":
            te_manual = st.number_input("Precio exterior (€)", min_value=0, value=0, step=1, key="te_m")
        te_mol_precio = 0
        if te_data[2] == "madera":
            te_mol = st.selectbox("Moldurado exterior", [m[0] for m in MOLDURADOS], key="te_mol")
            te_mol_precio = next(m[1] for m in MOLDURADOS if m[0] == te_mol)

    es_aluminio = te_data[2] in ("aluminio", "rustico")
    if es_aluminio:
        st.info("Tablero aluminio/rústico: 1 juego de jambas · Sin embocadura estándar · F1+29+68 automático.")
    st.markdown('</div>', unsafe_allow_html=True)

    # CILINDRO
    st.markdown('<div class="seccion"><div class="sec-titulo">Cilindro y cerradura</div>', unsafe_allow_html=True)
    doble = st.checkbox("Doble cerradura  (+219 €)")
    if not es_trastero:
        if doble:
            cil_d_sel  = st.selectbox("Cilindros amaestrados", [c[0] for c in CILINDROS_DOBLE])
            cil_precio = next(c[1] for c in CILINDROS_DOBLE if c[0] == cil_d_sel)
            st.caption("El Kaba Expert por defecto no se incluye — sustituido por los amaestrados.")
        else:
            cil_sel    = st.selectbox("Cilindro", [c[0] for c in CILINDROS])
            cil_precio = next(c[1] for c in CILINDROS if c[0] == cil_sel)
    else:
        cil_precio = 0; doble = False
        st.info("Cilindro Iseo R7 incluido en el precio de la puerta.")
    st.markdown('</div>', unsafe_allow_html=True)

    # JAMBAS Y EMBOCADURA
    if not es_trastero:
        st.markdown('<div class="seccion"><div class="sec-titulo">Jambas y embocadura</div>', unsafe_allow_html=True)
        jc1, jc2 = st.columns(2)
        n_jambas = jc1.number_input("Juegos de jambas", min_value=0, max_value=4,
                                     value=1 if es_aluminio else 2, step=1)
        emb_opts = [
            "Sin embocadura",
            "≤150 mm  (98 €)",
            ">150 mm  (112 €)",
            "MDA ≤150 mm  (158 €)",
            "MDA >150 mm  (197 €)",
            "Aluminio ≤150 mm  (181 €)",
            "Aluminio >150 mm  (217 €)",
        ]
        emb_sel = jc2.selectbox("Embocadura", emb_opts, index=0 if es_aluminio else 1)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        n_jambas = 0; emb_sel = "Sin embocadura"

    # FIJOS Y MONTANTES
    st.markdown('<div class="seccion"><div class="sec-titulo">Fijos y montantes</div>', unsafe_allow_html=True)
    fm_sel = []
    fmc = st.columns(2)
    for i, (nom, pre) in enumerate(FIJOS_MONTANTES):
        col = fmc[i % 2]
        if col.checkbox(f"{nom}  ({pre} €)", key=f"fm_{i}"):
            ud = col.number_input("Unidades", min_value=1, max_value=10, value=1, key=f"fmud_{i}")
            fm_sel.append((nom, pre, ud))
    st.markdown('</div>', unsafe_allow_html=True)

    # EXTRAS — por categorías
    st.markdown('<div class="seccion"><div class="sec-titulo">Extras y accesorios</div>', unsafe_allow_html=True)
    extras_sel = []

    # Categorías detectadas por prefijo
    CATS = [
        ("PUERTA",             [e for e in EXTRAS if e[0] in ["Extra Grado 4","Extra aislante lana de roca","Extra apertura invertida","Extra pintado / barnizado RAL","Extra Revólver antibala FB2","Extra Magnum antibala FB3","Incremento negro  (solo KXXI)","Express especial","Express muy especial","Precerco soldadura","Precerco Grado 5"]]),
        ("CERRAJERÍA",         [e for e in EXTRAS if e[0] in ["Cerradura eléctrica CISA","Cerradero eléctrico","Cerradura antipánico  (sin cilindro)","Cerradura emergencia + barra toallero","Muelle cierrapuertas RC3/RC4","Muelle cierrapuertas RC5/RF","Extra 3D Key","Extra 3D Key doble  (sin cilindro)","Electropistón","Contacto magnético","Protector imán"]]),
        ("CAMBIOS DE CERRADURA",[e for e in EXTRAS if e[0].startswith("Cambio") or e[0] == "Bloque MIA con 5 llaves"]),
        ("LLAVES",             [e for e in EXTRAS if e[0].startswith("Llave") or e[0] == "Porte envío de llaves"]),
        ("DOMÓTICA",           [e for e in EXTRAS if any(x in e[0] for x in ["Tedee","Danalock","X1R","Gateway"])]),
        ("TABLERO / CRISTAL",  [e for e in EXTRAS if any(x in e[0] for x in ["tablero","Cristal","Incrustaciones","decoración","Manipulación","Tachuelas"])]),
        ("REMATES Y ACABADOS", [e for e in EXTRAS if any(x in e[0] for x in ["Escalón","Cortavientos","Forro","Zócalo","Vierteaguas","F1","Media caña","Tratamiento","Pintura","Lacar","burlete"])]),
        ("HERRAJES",           [e for e in EXTRAS if any(x in e[0] for x in ["Protector THS","polvo","Mirilla","Tirador","manilla","Pomo","Manilla","capuchones"])]),
        ("CRISTAL EN HOJA",    [e for e in EXTRAS if "en hoja" in e[0]]),
        ("INSTALACIÓN",        [e for e in EXTRAS if any(x in e[0] for x in ["Mano de obra","Instalación","Desplazamiento","Desmontaje","Panel","Recuperar"])]),
    ]

    exc = st.columns(2)
    for cat_name, items in CATS:
        if not items:
            continue
        st.markdown(f'<div class="cat-header">{cat_name}</div>', unsafe_allow_html=True)
        for i_g, (nom, pre) in enumerate(items):
            global_key = f"ex_{nom[:20].replace(' ','_')}"
            col = exc[i_g % 2]
            if col.checkbox(f"{nom}  ({pre} €)", key=global_key):
                ud = 1
                if any(x in nom for x in ["THS","Tirador","Mirilla","Tedee","hora","metro","unidad","reja"]):
                    ud = col.number_input("Ud.", min_value=1, max_value=100, value=1, key=f"{global_key}_ud")
                extras_sel.append((nom, pre, ud))
    st.markdown('</div>', unsafe_allow_html=True)

    # DESCUENTOS / COMISIONES
    st.markdown('<div class="seccion"><div class="sec-titulo">Descuentos / Comisiones adicionales</div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    dto_pct = dc1.number_input("Descuento adicional (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    dto_lbl = dc1.text_input("Etiqueta descuento", placeholder="Dto. especial cliente")
    com_pct = dc2.number_input("Comisión (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    com_lbl = dc2.text_input("Etiqueta comisión", placeholder="Comisión comercial")
    com_op  = dc2.radio("La comisión...", ["Se resta", "Se suma"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  CALCULAR LÍNEAS
# ════════════════════════════════════════════════════════════════════
def precio_tab(data, manual, mol):
    if data[2] == "sapelly": return 0
    if data[2] == "manual":  return manual
    if data[2] in TABLEROS_SIN_MOLDURADO: return data[1] or 0
    return (data[1] or 0) + mol

def desc_tab(sel, data, mol):
    if data[2] == "madera" and mol > 0:
        mn = next((m[0].split("  ")[0] for m in MOLDURADOS if m[1] == mol), "")
        return f"{sel} {mn}"
    return sel

lineas = []
lineas.append({"desc": f"{modelo_sel} · {escala_sel}",
               "ud": 1, "precio_u": precio_puerta, "total": precio_puerta})

ti_p = precio_tab(ti_data, ti_manual, ti_mol_precio)
lineas.append({"desc": f"Tablero interior — {desc_tab(ti_sel, ti_data, ti_mol_precio)}",
               "ud": 1, "precio_u": ti_p, "total": ti_p})

te_p = precio_tab(te_data, te_manual, te_mol_precio)
lineas.append({"desc": f"Tablero exterior — {desc_tab(te_sel, te_data, te_mol_precio)}",
               "ud": 1, "precio_u": te_p, "total": te_p})

if es_aluminio:
    lineas.append({"desc": "F1+29+68 (aluminio)", "ud": 1, "precio_u": F1_29_68, "total": F1_29_68})

if doble:
    lineas.append({"desc": "Extra cerradura doble", "ud": 1, "precio_u": DOBLE_CERRADURA, "total": DOBLE_CERRADURA})
    lineas.append({"desc": cil_d_sel, "ud": 1, "precio_u": cil_precio, "total": cil_precio})
elif cil_precio > 0:
    lineas.append({"desc": cil_sel if not es_trastero else "Cilindro Iseo R7",
                   "ud": 1, "precio_u": cil_precio, "total": cil_precio})

if n_jambas > 0:
    lineas.append({"desc": f"Jambas — {n_jambas} juego{'s' if n_jambas>1 else ''}",
                   "ud": n_jambas, "precio_u": JAMBAS_PRECIO, "total": n_jambas * JAMBAS_PRECIO})

EMB_MAP = {
    "≤150 mm  (98 €)":           ("Embocadura ≤150 mm",              EMBOCADURA_150),
    ">150 mm  (112 €)":          ("Embocadura >150 mm",               EMBOCADURA_150P),
    "MDA ≤150 mm  (158 €)":      ("Embocadura MDA ≤150 mm",          EMBOCADURA_MDA_S),
    "MDA >150 mm  (197 €)":      ("Embocadura MDA >150 mm",          EMBOCADURA_MDA_L),
    "Aluminio ≤150 mm  (181 €)": ("Embocadura aluminio ≤150 mm",     EMBOCADURA_ALU_S),
    "Aluminio >150 mm  (217 €)": ("Embocadura aluminio >150 mm",     EMBOCADURA_ALU_L),
}
if emb_sel in EMB_MAP:
    ed, ep = EMB_MAP[emb_sel]
    lineas.append({"desc": ed, "ud": 1, "precio_u": ep, "total": ep})

for nom, pre, ud in fm_sel:
    lineas.append({"desc": nom, "ud": ud, "precio_u": pre, "total": pre * ud})
for nom, pre, ud in extras_sel:
    lineas.append({"desc": nom, "ud": ud, "precio_u": pre, "total": pre * ud})

subtotal = sum(ln['total'] for ln in lineas)
dto_ppp  = round(subtotal * 0.05, 2)
base     = round(subtotal - dto_ppp, 2)
total    = base
dto_imp = com_imp = 0
if dto_pct > 0:
    dto_imp = round(base * dto_pct / 100, 2)
    total   = round(total - dto_imp, 2)
if com_pct > 0:
    com_imp = round(total * com_pct / 100, 2)
    total   = round(total + com_imp if com_op == "Se suma" else total - com_imp, 2)


# ════════════════════════════════════════════════════════════════════
#  PANEL RESUMEN
# ════════════════════════════════════════════════════════════════════
with col_prev:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="resumen-card">', unsafe_allow_html=True)
    st.markdown('<div class="resumen-titulo">Resumen del presupuesto</div>', unsafe_allow_html=True)

    for ln in lineas:
        c0 = "li0" if ln['total'] == 0 else ""
        st.markdown(
            f'<div class="li"><span class="{c0}">{ln["desc"]}</span>'
            f'<span class="{c0}">{fmt(ln["total"])}</span></div>',
            unsafe_allow_html=True)

    st.markdown(f"""
    <div class="subtotales">
        <div class="subtotal-row"><span>Subtotal</span><span>{fmt(subtotal)}</span></div>
        <div class="dto"><span>Dto. 5% PPP</span><span>− {fmt(dto_ppp)}</span></div>
    """, unsafe_allow_html=True)

    if dto_pct > 0:
        lbl = dto_lbl or f"Dto. adicional {dto_pct}%"
        st.markdown(f'<div class="dto"><span>{lbl}</span><span>− {fmt(dto_imp)}</span></div>',
                    unsafe_allow_html=True)
    if com_pct > 0:
        lbl  = com_lbl or f"Comisión {com_pct}%"
        sign = "+" if com_op == "Se suma" else "−"
        color = "#f0866a" if com_op == "Se resta" else "#7ec8a0"
        st.markdown(f'<div class="dto" style="color:{color}"><span>{lbl}</span><span>{sign} {fmt(com_imp)}</span></div>',
                    unsafe_allow_html=True)

    st.markdown(f"""</div>
    <div class="total-box">
        <div>
            <div class="total-lbl">Total IVA incluido</div>
        </div>
        <div class="total-imp">{fmt(total)}</div>
    </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if st.button("⬇  Generar PDF"):
        cliente_dict = {"nombre": nombre, "telefono": telefono, "email": email,
                        "direccion": direccion, "cp": cp, "ciudad": ciudad}
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name
        generar_pdf(path=tmp_path, lineas=lineas, cliente=cliente_dict,
                    descuento_extra=dto_pct, descuento_extra_label=dto_lbl,
                    comision=com_pct, comision_label=com_lbl,
                    comision_suma=(com_op == "Se suma"))
        with open(tmp_path, "rb") as f:
            pdf_bytes = f.read()
        os.unlink(tmp_path)
        fname = f"presupuesto_{(nombre or 'kiuso').lower().replace(' ','_')}.pdf"
        st.download_button("📄  Descargar PDF", pdf_bytes, fname, "application/pdf")
