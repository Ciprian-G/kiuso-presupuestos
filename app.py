import os, tempfile
import streamlit as st
from tarifas import *
from pdf_gen import generar_pdf, fmt

st.set_page_config(page_title="KIUSO · Presupuestos", page_icon="🔒",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Outfit', sans-serif !important; }
.stApp { background: #f5f3ef; }

label[data-testid="stWidgetLabel"] p { font-size: 16px !important; font-weight: 500 !important; color: #2a2520 !important; }
[data-testid="stTextInput"] input    { font-size: 16px !important; padding: 11px 14px !important; border-radius: 8px !important; border: 1.5px solid #d5d0c8 !important; background: #fffefb !important; }
[data-testid="stSelectbox"] > div > div { font-size: 16px !important; border-radius: 8px !important; border: 1.5px solid #d5d0c8 !important; background: #fffefb !important; }
[data-testid="stNumberInput"] input  { font-size: 16px !important; border-radius: 8px !important; border: 1.5px solid #d5d0c8 !important; background: #fffefb !important; }
[data-testid="stCheckbox"] label p   { font-size: 15px !important; }
[data-testid="stRadio"] label p      { font-size: 15px !important; }

/* Sección */
.seccion { background: #fffefb; border-radius: 14px; padding: 26px 30px; margin-bottom: 16px; border: 1.5px solid #e5e0d8; box-shadow: 0 2px 8px rgba(26,20,10,0.04); }

/* Título de sección — grande y centrado */
.sec-titulo {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    color: #1a2a4a;
    text-align: center;
    border-bottom: 2px solid #1a2a4a;
    padding-bottom: 12px;
    margin-bottom: 20px;
}

/* Cabecera de categoría en extras */
.cat-header {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #8a7f70;
    margin: 18px 0 8px 0;
    padding-bottom: 5px;
    border-bottom: 1px solid #e5e0d8;
    text-align: center;
}

/* Panel resumen */
.resumen-card { background: #1a2a4a; color: #f0ece4; border-radius: 14px; padding: 28px; }
.resumen-titulo { font-family: 'Cormorant Garamond', serif; font-size: 26px; font-weight: 600; color: white; margin: 0 0 20px 0; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 14px; text-align: center; }
.li { display:flex; justify-content:space-between; font-size:14px; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.06); gap:10px; line-height:1.4; }
.li span:first-child { opacity:.82; flex:1; }
.li span:last-child  { font-weight:500; white-space:nowrap; color:#d4cfc6; }
.li0 { opacity:.35 !important; font-style:italic; }
.subtotales { margin-top:14px; border-top:1px solid rgba(255,255,255,0.15); padding-top:12px; }
.dto  { color:#f08878; font-size:14px; display:flex; justify-content:space-between; padding:3px 0; }
.srow { color:rgba(255,255,255,0.65); font-size:14px; display:flex; justify-content:space-between; padding:3px 0; }
.total-box { background:white; color:#1a2a4a; border-radius:10px; padding:18px 22px; margin-top:18px; display:flex; justify-content:space-between; align-items:center; }
.total-lbl { font-size:11px !important; font-weight:700 !important; letter-spacing:2px; text-transform:uppercase; color:#888; }
.total-imp { font-family:'Cormorant Garamond',serif; font-size:34px; font-weight:600; color:#1a2a4a; }

/* Botón */
.stButton > button { background:#1a2a4a !important; color:white !important; border:none !important; border-radius:10px !important; font-family:'Outfit',sans-serif !important; font-weight:600 !important; font-size:16px !important; width:100% !important; padding:15px !important; }
.stButton > button:hover { background:#253d6e !important; }

/* Barra búsqueda */
.search-box { background:#f0ece4; border-radius:8px; padding:2px 0 10px 0; margin-bottom:6px; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────
logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
cl, ct = st.columns([1, 9])
with cl:
    if os.path.exists(logo_path): st.image(logo_path, width=72)
with ct:
    st.markdown("""<div style="padding-top:8px">
        <div style="font-family:'Cormorant Garamond',serif;font-size:34px;color:#1a2a4a;font-weight:600;letter-spacing:-0.5px">Generador de Presupuestos</div>
        <div style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#9a9285;margin-top:4px">Puertas Acorazadas · Seguridad Reina S.A.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
col_form, col_prev = st.columns([3, 2], gap="large")

with col_form:

    # ── CLIENTE ────────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Datos del cliente</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    nombre    = r1.text_input("Nombre / Empresa", placeholder="Nombre completo")
    telefono  = r2.text_input("Teléfono",         placeholder="600 000 000")
    email     = r1.text_input("Email",             placeholder="correo@ejemplo.com")
    direccion = r2.text_input("Dirección",         placeholder="Calle, número, piso")
    rcp, rciu = st.columns(2)
    cp     = rcp.text_input("Código postal", placeholder="28000")
    ciudad = rciu.text_input("Ciudad",       placeholder="Madrid")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── PUERTA ─────────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Puerta</div>', unsafe_allow_html=True)
    modelo_sel    = st.selectbox("Modelo", list(MODELOS.keys()))
    escala_sel    = st.selectbox("Escala / Medida", list(MODELOS[modelo_sel].keys()))
    precio_puerta = MODELOS[modelo_sel][escala_sel]
    es_trastero   = modelo_sel in TRASTERO_MODELOS
    if es_trastero:
        st.info("Sin jambas ni embocadura · Cilindro Iseo R7 incluido · Ventilación e inversión sin coste.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── TABLEROS ───────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Tableros</div>', unsafe_allow_html=True)
    t_labels = [t[0] for t in TABLEROS]
    tic, tec = st.columns(2)

    with tic:
        st.markdown("**Interior**")
        ti_sel  = st.selectbox("Tablero interior", t_labels, label_visibility="collapsed", key="ti")
        ti_data = next(t for t in TABLEROS if t[0] == ti_sel)
        ti_inc_col, ti_ud_col = st.columns([2, 1])
        ti_incluido = ti_inc_col.checkbox("Incluido en la puerta", key="ti_inc",
                                   value=(es_trastero and ti_data[2] in ("madera","sapelly") and
                                          any(x in ti_sel for x in ["MAD blanco","Chapa galvanizada","Sapelly liso"])))
        ti_ud = ti_ud_col.number_input("Unidades", min_value=1, max_value=4, value=1, step=1, key="ti_ud",
                                        help="2 para doble hoja")
        ti_manual = 0
        ti_desc_custom = ""
        if ti_data[2] == "manual":
            ti_desc_custom = st.text_input("Descripción tablero interior", placeholder="Ej: Diseño especial roble natural", key="ti_desc")
            ti_manual = st.number_input("Precio interior (€)", min_value=0, value=0, step=1, key="ti_m")
        ti_mol = st.selectbox("Moldurado interior", [m[0] for m in MOLDURADOS], key="ti_mol")
        ti_mol_precio = next(m[1] for m in MOLDURADOS if m[0] == ti_mol)

    with tec:
        st.markdown("**Exterior**")
        te_sel  = st.selectbox("Tablero exterior", t_labels, label_visibility="collapsed", key="te")
        te_data = next(t for t in TABLEROS if t[0] == te_sel)
        te_inc_col, te_ud_col = st.columns([2, 1])
        te_incluido = te_inc_col.checkbox("Incluido en la puerta", key="te_inc",
                                   value=(es_trastero and te_data[2] in ("madera","sapelly") and
                                          any(x in te_sel for x in ["MAD blanco","Chapa galvanizada","Sapelly liso"])))
        te_ud = te_ud_col.number_input("Unidades", min_value=1, max_value=4, value=1, step=1, key="te_ud",
                                        help="2 para doble hoja")
        te_manual = 0
        te_desc_custom = ""
        if te_data[2] == "manual":
            te_desc_custom = st.text_input("Descripción tablero exterior", placeholder="Ej: Sapelly decoración especial", key="te_desc")
            te_manual = st.number_input("Precio exterior (€)", min_value=0, value=0, step=1, key="te_m")
        te_mol = st.selectbox("Moldurado exterior", [m[0] for m in MOLDURADOS], key="te_mol")
        te_mol_precio = next(m[1] for m in MOLDURADOS if m[0] == te_mol)

    es_aluminio = te_data[2] in ("aluminio", "rustico")
    if es_aluminio:
        st.info("Tablero aluminio/rústico: 1 juego de jambas · Sin embocadura estándar · F1+29+68 automático.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── CERRADURA ──────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Cerradura</div>', unsafe_allow_html=True)
    cerr_sel   = st.selectbox("Cerradura principal", [c[0] for c in CERRADURAS_PRINCIPALES])
    cerr_precio = next(c[1] for c in CERRADURAS_PRINCIPALES if c[0] == cerr_sel)
    st.markdown("**Extras de cerradura**")
    cerr_extras_sel = []
    ce_cols = st.columns(2)
    for i, (nom, pre) in enumerate(EXTRAS_CERRADURA):
        if ce_cols[i % 2].checkbox(f"{nom}  ({pre} €)", key=f"ce_{i}"):
            cerr_extras_sel.append((nom, pre))
    st.markdown('</div>', unsafe_allow_html=True)

    # ── CILINDRO ───────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Cilindro</div>', unsafe_allow_html=True)
    doble = st.checkbox("Doble cerradura  (+219 €)", key="doble")
    if not es_trastero:
        if doble:
            cil_d_sel  = st.selectbox("Cilindros amaestrados", [c[0] for c in CILINDROS_DOBLE])
            cil_precio = next(c[1] for c in CILINDROS_DOBLE if c[0] == cil_d_sel)
            cil_incluido = False
            st.caption("Kaba Expert por defecto no se incluye — sustituido por los amaestrados.")
        else:
            cil_sel    = st.selectbox("Cilindro", [c[0] for c in CILINDROS])
            cil_precio = next(c[1] for c in CILINDROS if c[0] == cil_sel)
            cil_incluido = st.checkbox("Incluido en la puerta", key="cil_inc", value=False)
    else:
        cil_precio = 0; doble = False; cil_incluido = True
        st.info("Cilindro Iseo R7 incluido en el precio de la puerta.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── JAMBAS Y EMBOCADURA ────────────────────────────────────────────────
    if not es_trastero:
        st.markdown('<div class="seccion"><div class="sec-titulo">Jambas y embocadura</div>', unsafe_allow_html=True)
        jc1, jc2 = st.columns(2)
        n_jambas = jc1.number_input("Juegos de jambas", min_value=0, max_value=4,
                                     value=1 if es_aluminio else 2, step=1)
        emb_opts = ["Sin embocadura","≤150 mm  (98 €)",">150 mm  (112 €)",
                    "MDA ≤150 mm  (158 €)","MDA >150 mm  (197 €)",
                    "Aluminio ≤150 mm  (181 €)","Aluminio >150 mm  (217 €)"]
        emb_sel  = jc2.selectbox("Embocadura", emb_opts, index=0 if es_aluminio else 1)
        if es_aluminio:
            st.caption("Tablero aluminio/rústico: revisa si necesitas F1+29+68 abajo — no se añade automáticamente.")
        f1_col1, f1_col2 = st.columns([2, 1])
        f1_check = f1_col1.checkbox("F1+29+68  (134 €/ud — remate tablero aluminio)", key="f1_check",
                                     value=es_aluminio)
        f1_ud = f1_col2.number_input("Unidades", min_value=1, max_value=4, value=1, step=1, key="f1_ud")
        st.markdown('</div>', unsafe_allow_html=True)
    else:

        n_jambas = 0; emb_sel = "Sin embocadura"; f1_check = False; f1_ud = 1

    # ── FIJOS Y MONTANTES — agrupados ──────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Fijos y montantes</div>', unsafe_allow_html=True)
    fm_sel = []
    for fi, (grupo, sub_items) in enumerate(FIJOS_GRUPOS):
        tiene_sub = not (len(sub_items) == 1 and sub_items[0][0] is None)
        checked = st.checkbox(f"{grupo}", key=f"fm_{fi}")
        if checked:
            if tiene_sub:
                sub_labels = [s[0] for s in sub_items]
                sub_prices = {s[0]: s[1] for s in sub_items}
                cols_fm = st.columns([2, 1])
                sub_sel = cols_fm[0].selectbox("Medida / tipo", sub_labels, key=f"fm_sub_{fi}", label_visibility="collapsed")
                ud = cols_fm[1].number_input("Ud.", min_value=1, max_value=10, value=1, key=f"fm_ud_{fi}")
                pre = sub_prices[sub_sel]
                desc = f"{grupo} — {sub_sel}"
            else:
                pre = sub_items[0][1]
                desc = grupo
                cols_fm = st.columns([3, 1])
                ud = cols_fm[1].number_input("Ud.", min_value=1, max_value=10, value=1, key=f"fm_ud_{fi}")
            fm_sel.append((desc, pre, ud))
    st.markdown('</div>', unsafe_allow_html=True)

    # ── CAMBIO DE CERRADURA ────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Cambio de cerradura</div>', unsafe_allow_html=True)
    cambio_checked = st.checkbox("Incluir cambio de cerradura", key="cambio_check")
    cambio_sel_list = []
    if cambio_checked:
        cam_cols = st.columns([2, 1, 1])
        cam_tipo = cam_cols[0].selectbox("Tipo de cerradura", [c[0] for c in CAMBIOS_CERRADURA],
                                          label_visibility="collapsed")
        cam_ud   = cam_cols[1].number_input("Ud.", min_value=1, max_value=5, value=1, key="cam_ud")
        cam_pre  = next(c[1] for c in CAMBIOS_CERRADURA if c[0] == cam_tipo)
        cambio_sel_list.append((f"Cambio cerradura — {cam_tipo}", cam_pre, cam_ud))
    st.markdown('</div>', unsafe_allow_html=True)

    # ── EXTRAS — con buscador ──────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Extras y accesorios</div>', unsafe_allow_html=True)
    busqueda = st.text_input("🔍  Buscar extra...", placeholder="Ej: escalón, tedee, tirador...", key="busqueda")
    busqueda_lower = busqueda.strip().lower()

    extras_sel = []
    # Inicializar session_state para extras seleccionados
    if "extras_on" not in st.session_state:
        st.session_state.extras_on = {}

    global_ex_idx = 0
    for cat_name, items in EXTRAS_CATS:
        # Filtrar por búsqueda
        items_vis = [(n, p) for n, p in items
                     if not busqueda_lower or busqueda_lower in n.lower() or busqueda_lower in cat_name.lower()]
        if not items_vis:
            global_ex_idx += len(items)
            continue

        st.markdown(f'<div class="cat-header">{cat_name}</div>', unsafe_allow_html=True)
        exc = st.columns(2)
        for n, p in items_vis:
            idx = global_ex_idx + next(i for i, (nn,_) in enumerate(items) if nn == n)
            col = exc[idx % 2]
            prev_val = st.session_state.extras_on.get(f"ex_{idx}", False)
            checked = col.checkbox(f"{n}  ({p} €)", key=f"ex_{idx}", value=prev_val)
            st.session_state.extras_on[f"ex_{idx}"] = checked
            if checked:
                ud = 1
                if any(x in n for x in ["THS","Tirador","Mirilla","Tedee","hora","metro","unidad","reja","Llave","burlete","capuchones",
                                        "Grado 4","aislante","apertura invertida"]):
                    ud = col.number_input("Ud.", min_value=1, max_value=100, value=1, key=f"exud_{idx}")
                extras_sel.append((n, p, ud))
        global_ex_idx += len(items)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── LÍNEAS LIBRES ─────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Líneas personalizadas</div>', unsafe_allow_html=True)
    st.caption("Escribe cualquier concepto que no esté en la tarifa — aparecerá exactamente así en el PDF.")
    n_libres = st.number_input("Número de líneas", min_value=0, max_value=10, value=0, step=1, key="n_libres")
    lineas_libres = []
    for li in range(int(n_libres)):
        lc1, lc2 = st.columns([3, 1])
        l_desc  = lc1.text_input(f"Descripción línea {li+1}", placeholder="Ej: Tablero diseño especial Art Decó", key=f"ll_desc_{li}")
        l_price = lc2.number_input(f"Precio (€)", min_value=0, value=0, step=1, key=f"ll_price_{li}")
        if l_desc:
            lineas_libres.append((l_desc, l_price))
    st.markdown('</div>', unsafe_allow_html=True)

    # ── DESCUENTOS ─────────────────────────────────────────────────────────
    st.markdown('<div class="seccion"><div class="sec-titulo">Descuentos / Comisiones</div>', unsafe_allow_html=True)
    mostrar_dto = st.checkbox("Mostrar descuento 5% PPP en el PDF", value=False, key="mostrar_dto")
    dc1, dc2 = st.columns(2)
    dto_pct = dc1.number_input("Descuento adicional (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    dto_lbl = dc1.text_input("Etiqueta descuento", placeholder="Dto. especial cliente")
    com_pct = dc2.number_input("Comisión (%)",        min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    com_lbl = dc2.text_input("Etiqueta comisión",    placeholder="Comisión comercial")
    com_op  = dc2.radio("La comisión...", ["Se resta","Se suma"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── CALCULAR LÍNEAS ───────────────────────────────────────────────────────────
def precio_tab(data, manual, mol):
    if data[2] == "ninguno": return None   # Sin tablero — no añadir línea
    if data[2] == "manual":  return manual + mol
    base = data[1] or 0
    return base + mol

def desc_tab(sel, data, custom_desc):
    if data[2] == "manual" and custom_desc:
        return custom_desc
    return sel

lineas = []

# 1. Puerta
lineas.append({"desc": f"{modelo_sel} · {escala_sel}", "ud":1,
               "precio_u": precio_puerta, "total": precio_puerta})

# 2. Tablero interior
ti_base = precio_tab(ti_data, ti_manual, 0)
if ti_base is not None:
    ti_mol_nom = ti_mol.split("  ")[0] if ti_mol_precio > 0 else ""
    ti_desc_final = desc_tab(ti_sel, ti_data, ti_desc_custom)
    if ti_mol_nom:
        ti_desc_final = f"{ti_desc_final} + {ti_mol_nom}"
    ti_unit  = (0 if ti_incluido else ti_base) + ti_mol_precio
    ti_total = ti_unit * ti_ud
    lineas.append({"desc": f"Tablero interior — {ti_desc_final}",
                   "ud": ti_ud, "precio_u": 0 if ti_incluido else ti_unit,
                   "total": 0 if ti_incluido else ti_total, "incluido": ti_incluido})

# 3. Tablero exterior
te_base = precio_tab(te_data, te_manual, 0)
if te_base is not None:
    te_mol_nom = te_mol.split("  ")[0] if te_mol_precio > 0 else ""
    te_desc_final = desc_tab(te_sel, te_data, te_desc_custom)
    if te_mol_nom:
        te_desc_final = f"{te_desc_final} + {te_mol_nom}"
    te_unit  = (0 if te_incluido else te_base) + te_mol_precio
    te_total = te_unit * te_ud
    lineas.append({"desc": f"Tablero exterior — {te_desc_final}",
                   "ud": te_ud, "precio_u": 0 if te_incluido else te_unit,
                   "total": 0 if te_incluido else te_total, "incluido": te_incluido})

# 4. Cerradura principal + extras
if cerr_precio > 0:
    lineas.append({"desc": cerr_sel, "ud":1, "precio_u":cerr_precio, "total":cerr_precio})
for nom, pre in cerr_extras_sel:
    lineas.append({"desc": nom, "ud":1, "precio_u":pre, "total":pre})

# 5. Cilindro (simple o doble)
if doble:
    lineas.append({"desc":"Extra cerradura doble", "ud":1, "precio_u":DOBLE_CERRADURA, "total":DOBLE_CERRADURA})
    lineas.append({"desc":cil_d_sel, "ud":1, "precio_u":cil_precio, "total":cil_precio})
elif cil_precio > 0 or cil_incluido:
    lineas.append({"desc": cil_sel if not es_trastero else "Cilindro Iseo R7",
                   "ud":1, "precio_u":0 if cil_incluido else cil_precio,
                   "total":0 if cil_incluido else cil_precio, "incluido": cil_incluido})

# 6. Jambas
if n_jambas > 0:
    lineas.append({"desc":f"Jambas — {n_jambas} juego{'s' if n_jambas>1 else ''}",
                   "ud":n_jambas, "precio_u":JAMBAS_PRECIO, "total":n_jambas*JAMBAS_PRECIO})

# 7. Embocadura
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
    lineas.append({"desc":ed, "ud":1, "precio_u":ep, "total":ep})

# 8. F1+29+68
if f1_check:
    f1_total = F1_29_68 * f1_ud
    lineas.append({"desc":"F1+29+68 (remate aluminio)", "ud":f1_ud, "precio_u":F1_29_68, "total":f1_total})

# 9. Fijos y montantes
for nom, pre, ud in fm_sel:
    lineas.append({"desc":nom, "ud":ud, "precio_u":pre, "total":pre*ud})

# 10. Cambio de cerradura
for nom, pre, ud in cambio_sel_list:
    lineas.append({"desc":nom, "ud":ud, "precio_u":pre, "total":pre*ud})

# 11. Extras
for nom, pre, ud in extras_sel:
    lineas.append({"desc":nom, "ud":ud, "precio_u":pre, "total":pre*ud})

# 12. Líneas libres
for l_desc, l_price in lineas_libres:
    lineas.append({"desc":l_desc, "ud":1, "precio_u":l_price, "total":l_price})

subtotal = sum(ln['total'] for ln in lineas)
dto_ppp  = round(subtotal * 0.05, 2) if mostrar_dto else 0
base     = round(subtotal - dto_ppp, 2)
total    = base
dto_imp = com_imp = 0
if dto_pct > 0:
    dto_imp = round(base * dto_pct / 100, 2); total = round(total - dto_imp, 2)
if com_pct > 0:
    com_imp = round(total * com_pct / 100, 2)
    total   = round(total + com_imp if com_op == "Se suma" else total - com_imp, 2)


# ── PANEL DERECHO ─────────────────────────────────────────────────────────────
with col_prev:
    st.markdown('<div class="resumen-card">', unsafe_allow_html=True)
    st.markdown('<div class="resumen-titulo">Resumen</div>', unsafe_allow_html=True)

    for ln in lineas:
        if ln.get("incluido", False):
            st.markdown(
                f'<div class="li"><span class="li0">{ln["desc"]}</span>'
                f'<span style="color:#5aad7a;font-style:italic;font-size:12px">Incl. en puerta</span></div>',
                unsafe_allow_html=True)
        else:
            c0 = "li0" if ln["total"] == 0 else ""
            st.markdown(
                f'<div class="li"><span class="{c0}">{ln["desc"]}</span>'
                f'<span class="{c0}">{fmt(ln["total"])}</span></div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="subtotales">
        <div class="srow"><span>Subtotal</span><span>{fmt(subtotal)}</span></div>
        {"" if not mostrar_dto else f'<div class="dto"><span>Dto. 5% PPP</span><span>− {fmt(dto_ppp)}</span></div>'}""",
        unsafe_allow_html=True)

    if dto_pct > 0:
        lbl = dto_lbl or f"Dto. adicional {dto_pct}%"
        st.markdown(f'<div class="dto"><span>{lbl}</span><span>− {fmt(dto_imp)}</span></div>',
                    unsafe_allow_html=True)
    if com_pct > 0:
        lbl  = com_lbl or f"Comisión {com_pct}%"
        sign = "+" if com_op == "Se suma" else "−"
        col_c = "#7ec8a0" if com_op == "Se suma" else "#f08878"
        st.markdown(f'<div class="dto" style="color:{col_c}"><span>{lbl}</span><span>{sign} {fmt(com_imp)}</span></div>',
                    unsafe_allow_html=True)

    st.markdown(f"""</div>
    <div class="total-box">
        <div class="total-lbl">Total IVA incluido</div>
        <div class="total-imp">{fmt(total)}</div>
    </div></div>""", unsafe_allow_html=True)

    # ── CATÁLOGO ──────────────────────────────────────────────────────────
    incluir_catalogo = st.checkbox("Incluir catálogo K100/KXXI al final del PDF", value=False, key="catalogo")

    # ── OPCIONES ADICIONALES ─────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="background:#e8ecf2;border-radius:10px;padding:14px 18px;margin-bottom:10px">
        <div style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#1a2a4a;margin-bottom:10px">
            Opciones adicionales
        </div>
        <div style="font-size:13px;color:#555;margin-bottom:8px">
            Se muestran al pie del PDF como extras no incluidos en el presupuesto.
        </div>
    </div>""", unsafe_allow_html=True)
    opciones_sel = []
    for i, (nom, pre) in enumerate(OPCIONES_ADICIONALES):
        if st.checkbox(f"{nom}  —  {pre} €", key=f"opc_{i}"):
            opciones_sel.append((nom, pre))

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if st.button("⬇  Generar PDF", key="btn_pdf"):
        cliente_dict = {"nombre":nombre,"telefono":telefono,"email":email,
                        "direccion":direccion,"cp":cp,"ciudad":ciudad}
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name
        generar_pdf(path=tmp_path, lineas=lineas, cliente=cliente_dict,
                    descuento_extra=dto_pct, descuento_extra_label=dto_lbl,
                    comision=com_pct, comision_label=com_lbl,
                    comision_suma=(com_op=="Se suma"),
                    opciones=opciones_sel, mostrar_dto=mostrar_dto,
                    incluir_catalogo=incluir_catalogo)
        with open(tmp_path,"rb") as f: pdf_bytes = f.read()
        os.unlink(tmp_path)
        fname = f"presupuesto_{(nombre or 'kiuso').lower().replace(' ','_')}.pdf"
        st.download_button("📄  Descargar PDF", pdf_bytes, fname, "application/pdf", key="btn_dl")
