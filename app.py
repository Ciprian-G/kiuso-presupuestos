"""
app.py — Generador de Presupuestos KIUSO
Seguridad Reina S.A.
"""
import os, tempfile
import streamlit as st
from tarifas import *
from pdf_gen import generar_pdf, fmt

# ── Configuración página ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="KIUSO · Presupuestos",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f8f7f4; }

.seccion {
    background: white;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 16px;
    border: 1px solid #e8e5e0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.sec-titulo {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #1a2a4a;
    border-bottom: 2px solid #1a2a4a;
    padding-bottom: 8px;
    margin-bottom: 16px;
}
.resumen-card {
    background: #1a2a4a;
    color: white;
    border-radius: 10px;
    padding: 24px;
    position: sticky;
    top: 20px;
}
.resumen-card h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 16px;
    margin: 0 0 20px 0;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    padding-bottom: 12px;
}
.linea-item {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    gap: 8px;
}
.linea-item span:first-child { opacity: 0.85; flex: 1; }
.linea-item span:last-child  { font-weight: 500; white-space: nowrap; }
.linea-cero { opacity: 0.45 !important; }
.total-box {
    background: white;
    color: #1a2a4a;
    border-radius: 8px;
    padding: 14px 16px;
    margin-top: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.total-box .label { font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
.total-box .importe { font-family: 'DM Serif Display', serif; font-size: 22px; }
.dto-linea { color: #ff6b6b; font-size: 12px; display: flex; justify-content: space-between; padding: 3px 0; }
.stButton > button {
    background: #1a2a4a !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    width: 100% !important;
    font-size: 14px !important;
}
.stButton > button:hover { background: #243a62 !important; }
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stNumberInput"] input {
    border-radius: 6px !important;
    border: 1px solid #ddd !important;
    font-size: 13px !important;
}
[data-testid="stCheckbox"] label { font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
col_logo, col_titulo = st.columns([1, 8])
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=70)
with col_titulo:
    st.markdown("""
    <div style="padding-top:8px">
        <div style="font-family:'DM Serif Display',serif;font-size:24px;color:#1a2a4a">
            Generador de Presupuestos
        </div>
        <div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#888;margin-top:2px">
            Puertas Acorazadas · Seguridad Reina S.A.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
col_form, col_preview = st.columns([3, 2], gap="large")

with col_form:

    # ── CLIENTE ──────────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Datos del cliente</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    nombre    = c1.text_input("Nombre / Empresa", placeholder="Nombre completo")
    telefono  = c2.text_input("Teléfono", placeholder="600 000 000")
    email     = c1.text_input("Email", placeholder="correo@ejemplo.com")
    direccion = c2.text_input("Dirección", placeholder="Calle, número, piso")
    cp_col, ciudad_col = st.columns(2)
    cp     = cp_col.text_input("C.P.", placeholder="28000")
    ciudad = ciudad_col.text_input("Ciudad", placeholder="Madrid")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── PUERTA ───────────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Puerta</div>', unsafe_allow_html=True)
    modelo_sel    = st.selectbox("Modelo", list(MODELOS.keys()))
    escalas       = list(MODELOS[modelo_sel].keys())
    escala_sel    = st.selectbox("Escala / Medida", escalas)
    precio_puerta = MODELOS[modelo_sel][escala_sel]
    es_trastero   = modelo_sel in TRASTERO_MODELOS
    if es_trastero:
        st.info("Sin jambas ni embocadura · Cilindro Iseo R7 incluido · Ventilación e inversión incluidas.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── TABLEROS ─────────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Tableros</div>', unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)

    with tc1:
        st.markdown("**Interior**")
        ti_labels = [t[0] for t in TABLEROS_INTERIOR]
        ti_sel    = st.selectbox("Tablero interior", ti_labels, label_visibility="collapsed")
        ti_data   = next(t for t in TABLEROS_INTERIOR if t[0] == ti_sel)
        ti_precio_manual = 0
        if ti_data[2] == "manual":
            ti_precio_manual = st.number_input("Precio tablero interior (€)", min_value=0, value=0, step=1, key="ti_manual")

    with tc2:
        st.markdown("**Exterior**")
        te_labels = [t[0] for t in TABLEROS_EXTERIOR]
        te_sel    = st.selectbox("Tablero exterior", te_labels, label_visibility="collapsed")
        te_data   = next(t for t in TABLEROS_EXTERIOR if t[0] == te_sel)
        te_precio_manual = 0
        if te_data[2] == "manual":
            te_precio_manual = st.number_input("Precio tablero exterior (€)", min_value=0, value=0, step=1, key="te_manual")

    es_aluminio = te_data[2] == "aluminio"
    if es_aluminio:
        st.info("Tablero aluminio: 1 juego de jambas · Sin embocadura · F1+29+68 automático.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── CILINDRO ─────────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Cilindro</div>', unsafe_allow_html=True)
    doble_cerradura = st.checkbox("Doble cerradura  (+219 €)")
    if not es_trastero:
        if doble_cerradura:
            st.markdown("**Cilindros amaestrados**")
            cil_d_labels = [c[0] for c in CILINDROS_DOBLE]
            cil_d_sel    = st.selectbox("Cilindros amaestrados", cil_d_labels)
            cil_precio   = next(c[1] for c in CILINDROS_DOBLE if c[0] == cil_d_sel)
            st.caption("Kaba Expert no incluido — sustituido por amaestrados.")
        else:
            cil_labels = [c[0] for c in CILINDROS]
            cil_sel    = st.selectbox("Cilindro", cil_labels)
            cil_precio = next(c[1] for c in CILINDROS if c[0] == cil_sel)
    else:
        st.info("Cilindro Iseo R7 incluido en el precio.")
        cil_precio = 0
        doble_cerradura = False
    st.markdown('</div>', unsafe_allow_html=True)

    # ── JAMBAS Y EMBOCADURA ──────────────────────────────────────────────────
    if not es_trastero:
        st.markdown('<div class="seccion"><div class="sec-titulo">Jambas y embocadura</div>', unsafe_allow_html=True)
        j1, j2 = st.columns(2)
        n_jambas = j1.number_input("Juegos de jambas",
                                    min_value=0, max_value=4,
                                    value=1 if es_aluminio else 2, step=1)
        emb_opts = ["Sin embocadura", "≤150 mm  (98 €)", ">150 mm  (112 €)"]
        emb_sel  = j2.selectbox("Embocadura", emb_opts,
                                 index=0 if es_aluminio else 1)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        n_jambas = 0
        emb_sel  = "Sin embocadura"

    # ── EXTRAS ───────────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Extras y accesorios</div>', unsafe_allow_html=True)
    extras_sel = []
    col_e1, col_e2 = st.columns(2)
    for i, (nom_extra, pre_extra) in enumerate(EXTRAS):
        col = col_e1 if i % 2 == 0 else col_e2
        if col.checkbox(f"{nom_extra}  ({pre_extra} €)", key=f"extra_{i}"):
            ud = 1
            extras_sel.append((nom_extra, pre_extra, ud))
    # Unidades para extras que lo necesiten
    for idx, (nom, pre, ud) in enumerate(extras_sel):
        if any(x in nom for x in ["THS", "Tirador", "Mirilla"]):
            nuevo_ud = st.number_input(f"Unidades — {nom}", min_value=1, max_value=10, value=1, key=f"ud_{idx}")
            extras_sel[idx] = (nom, pre, nuevo_ud)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── DESCUENTOS / COMISIONES ──────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Descuentos / Comisiones</div>', unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    dto_extra_pct = d1.number_input("Descuento adicional (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    dto_extra_lbl = d1.text_input("Etiqueta descuento", placeholder="Dto. especial")
    com_pct       = d2.number_input("Comisión (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    com_lbl       = d2.text_input("Etiqueta comisión", placeholder="Comisión comercial")
    com_suma      = d2.radio("La comisión...", ["Se resta", "Se suma"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Construir líneas ──────────────────────────────────────────────────────────
lineas = []

lineas.append({"desc": f"{modelo_sel} · {escala_sel}",
               "ud": 1, "precio_u": precio_puerta, "total": precio_puerta})

# Tablero interior
if ti_data[2] == "incluido":
    lineas.append({"desc": "Tablero interior sapelly liso", "ud": 1, "precio_u": 0, "total": 0})
elif ti_data[2] == "moldurado_sapelly":
    lineas.append({"desc": "Tablero exterior sapelly liso", "ud": 1, "precio_u": 0, "total": 0})
    lineas.append({"desc": f"Moldurado interior {ti_sel.split('(')[0].strip()}",
                   "ud": 1, "precio_u": ti_data[1], "total": ti_data[1]})
elif ti_data[2] == "manual":
    if ti_precio_manual > 0:
        lineas.append({"desc": "Tablero interior (precio especial)",
                       "ud": 1, "precio_u": ti_precio_manual, "total": ti_precio_manual})
else:
    lineas.append({"desc": ti_sel, "ud": 1, "precio_u": ti_data[1], "total": ti_data[1]})

# Tablero exterior
if te_data[2] == "incluido_ext":
    lineas.append({"desc": "Tablero exterior sapelly liso", "ud": 1, "precio_u": 0, "total": 0})
elif te_data[2] == "manual":
    if te_precio_manual > 0:
        lineas.append({"desc": "Tablero exterior (precio especial)",
                       "ud": 1, "precio_u": te_precio_manual, "total": te_precio_manual})
else:
    lineas.append({"desc": te_sel, "ud": 1, "precio_u": te_data[1], "total": te_data[1]})

# F1+29+68 aluminio
if es_aluminio:
    lineas.append({"desc": "F1+29+68 (aluminio)", "ud": 1, "precio_u": F1_29_68, "total": F1_29_68})

# Cilindro / doble cerradura
if doble_cerradura:
    lineas.append({"desc": "Extra cerradura doble", "ud": 1,
                   "precio_u": DOBLE_CERRADURA, "total": DOBLE_CERRADURA})
    lineas.append({"desc": cil_d_sel, "ud": 1, "precio_u": cil_precio, "total": cil_precio})
else:
    if cil_precio > 0:
        lineas.append({"desc": cil_sel if not es_trastero else "Cilindro Iseo R7",
                       "ud": 1, "precio_u": cil_precio, "total": cil_precio})

# Jambas
if n_jambas > 0:
    lineas.append({"desc": f"Jambas — {n_jambas} juego{'s' if n_jambas>1 else ''}",
                   "ud": n_jambas, "precio_u": JAMBAS_PRECIO, "total": n_jambas * JAMBAS_PRECIO})

# Embocadura
if emb_sel == "≤150 mm  (98 €)":
    lineas.append({"desc": "Embocadura ≤150 mm", "ud": 1, "precio_u": EMBOCADURA_150, "total": EMBOCADURA_150})
elif emb_sel == ">150 mm  (112 €)":
    lineas.append({"desc": "Embocadura >150 mm", "ud": 1, "precio_u": EMBOCADURA_150P, "total": EMBOCADURA_150P})

# Extras
for nom, pre, ud in extras_sel:
    lineas.append({"desc": nom, "ud": ud, "precio_u": pre, "total": pre * ud})

# ── Calcular ──────────────────────────────────────────────────────────────────
subtotal      = sum(ln['total'] for ln in lineas)
dto_ppp       = round(subtotal * 0.05, 2)
base          = round(subtotal - dto_ppp, 2)
total         = base
dto_extra_imp = 0
com_imp       = 0

if dto_extra_pct > 0:
    dto_extra_imp = round(base * dto_extra_pct / 100, 2)
    total = round(total - dto_extra_imp, 2)

if com_pct > 0:
    com_imp = round(total * com_pct / 100, 2)
    total   = round(total + com_imp if com_suma == "Se suma" else total - com_imp, 2)

# ── Panel preview ─────────────────────────────────────────────────────────────
with col_preview:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="resumen-card"><h3>Resumen del presupuesto</h3>', unsafe_allow_html=True)

    for ln in lineas:
        clase = "linea-cero" if ln['total'] == 0 else ""
        st.markdown(f"""
        <div class="linea-item">
            <span class="{clase}">{ln['desc']}</span>
            <span class="{clase}">{fmt(ln['total'])}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:12px;border-top:1px solid rgba(255,255,255,0.2);padding-top:10px">
        <div class="dto-linea"><span>Subtotal</span><span>{fmt(subtotal)}</span></div>
        <div class="dto-linea"><span>Dto. 5% PPP</span><span>- {fmt(dto_ppp)}</span></div>
    """, unsafe_allow_html=True)

    if dto_extra_pct > 0:
        lbl = dto_extra_lbl or f"Dto. adicional {dto_extra_pct}%"
        st.markdown(f'<div class="dto-linea"><span>{lbl}</span><span>- {fmt(dto_extra_imp)}</span></div>',
                    unsafe_allow_html=True)
    if com_pct > 0:
        lbl  = com_lbl or f"Comisión {com_pct}%"
        sign = "+" if com_suma == "Se suma" else "-"
        st.markdown(f'<div class="dto-linea"><span>{lbl}</span><span>{sign} {fmt(com_imp)}</span></div>',
                    unsafe_allow_html=True)

    st.markdown(f"""
    </div>
    <div class="total-box">
        <span class="label">Total IVA incl.</span>
        <span class="importe">{fmt(total)}</span>
    </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Generar PDF ───────────────────────────────────────────────────────────
    if st.button("⬇  Generar PDF"):
        cliente_dict = {
            "nombre": nombre, "telefono": telefono, "email": email,
            "direccion": direccion, "cp": cp, "ciudad": ciudad
        }
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        generar_pdf(
            path=tmp_path,
            lineas=lineas,
            cliente=cliente_dict,
            descuento_extra=dto_extra_pct,
            descuento_extra_label=dto_extra_lbl,
            comision=com_pct,
            comision_label=com_lbl,
            comision_suma=(com_suma == "Se suma")
        )

        with open(tmp_path, "rb") as f:
            pdf_bytes = f.read()
        os.unlink(tmp_path)

        nombre_archivo = f"presupuesto_{(nombre or 'kiuso').lower().replace(' ','_')}.pdf"
        st.download_button(
            label="📄  Descargar PDF",
            data=pdf_bytes,
            file_name=nombre_archivo,
            mime="application/pdf",
        )
