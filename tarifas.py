# ─────────────────────────────────────────────
#  TARIFAS KIUSO 2026  ·  Seguridad Reina S.A.
#  Precios con IVA incluido — redondeados a €
# ─────────────────────────────────────────────

MODELOS = {
    "KIUSO K-XXI": {
        "Estándar":          2450,
        "Especial 1 (≤2100×1000)": 2692,
        "Especial 2 (≤2300×1100)": 2934,
        "Especial 3 (≤2450×1200)": 3461,
        "Hasta 3000×1500":   4497,
    },
    "KIUSO K-100": {
        "Estándar":          1754,
        "Especial 1 (≤2100×1000)": 1877,
        "Especial 2 (≤2300×1100)": 2036,
        "Especial 3 (≤2450×1200)": 2407,
    },
    "KRONOS K-XXI": {
        "Estándar":          2721,
        "Especial 1 (≤2100×1000)": 2953,
        "Especial 2 (≤2300×1100)": 3186,
        "Especial 3 (≤2450×1200)": 3693,
        "Hasta 3000×1500":   4760,
    },
    "KRONOS K-100": {
        "Estándar":          2119,
        "Especial 1 (≤2100×1000)": 2243,
        "Especial 2 (≤2300×1100)": 2401,
        "Especial 3 (≤2450×1200)": 2772,
    },
    "ZOE": {
        "Estándar":          3086,
        "Especial 1 (≤2100×1000)": 3391,
        "Especial 2 (≤2300×1100)": 3695,
        "Especial 3 (≤2450×1200)": 4360,
        "Hasta 3000×1500":   5564,
    },
    "MARINO RF-60 (Grado 4)": {
        "Estándar":          3358,
        "Especial 1 (≤2100×1000)": 3466,
        "Especial 2 (≤2300×1100)": 3541,
    },
    "MARINO RF-90 (Grado 4)": {
        "Estándar":          3493,
        "Especial 1 (≤2100×1000)": 3600,
        "Especial 2 (≤2300×1100)": 3676,
    },
    "FIRE RF-30 (Grado 3)": {
        "Estándar":          2898,
        "Especial 1 (≤2100×1000)": 3006,
        "Especial 2 (≤2300×1100)": 3082,
        "Especial 3 (≤2450×1200)": 3198,
    },
    "FIRE RF-60 (Grado 3)": {
        "Estándar":          3033,
        "Especial 1 (≤2100×1000)": 3141,
        "Especial 2 (≤2300×1100)": 3216,
        "Especial 3 (≤2450×1200)": 3333,
    },
    "TRASTERO (2000×900 / 2000×800)": {
        "Estándar":          1184,
    },
}

# True = es puerta trastero (sin jambas, sin embocadura, cilindro Iseo R7 incluido)
TRASTERO_MODELOS = {"TRASTERO (2000×900 / 2000×800)"}

# Tableros interiores: (etiqueta, precio, tipo)
# tipo: 'incluido', 'fijo', 'moldurado_sapelly', 'moldurado_blanco', '20f'
TABLEROS_INTERIOR = [
    ("Sapelly liso (incluido en puerta)",        0,    "incluido"),
    ("Blanco liso",                              80,   "fijo"),
    ("Roble liso",                               80,   "fijo"),
    ("Haya vaporizada",                          80,   "fijo"),
    ("Sapelly 20S (moldurado)",                  78,   "moldurado_sapelly"),
    ("Blanco 4 fresas",                          193,  "fijo"),
    ("Blanco 20S (moldurado)",                   158,  "fijo"),
    ("MAD sapelly/roble",                        87,   "fijo"),
    ("MAD blanco",                               93,   "fijo"),
    ("Tablero liso lacado RAL",                  151,  "fijo"),
    ("20F Standard roble",                       301,  "fijo"),
    ("20F Standard blanco",                      301,  "fijo"),
    ("Precio especial (introducir manualmente)", None, "manual"),
]

# Tableros exteriores
TABLEROS_EXTERIOR = [
    ("Sapelly liso (incluido en puerta)",        0,    "incluido_ext"),
    ("Roble liso",                               80,   "fijo"),
    ("Blanco liso",                              80,   "fijo"),
    ("Haya vaporizada",                          80,   "fijo"),
    ("MAD sapelly/roble",                        87,   "fijo"),
    ("MAD blanco",                               93,   "fijo"),
    ("Sapelly 10 cuadros moldura pegada",        390,  "fijo"),
    ("Sapelly fajeado 3 cuadros + plafón",       785,  "fijo"),
    ("Aluminio liso blanco",                     245,  "aluminio"),
    ("Aluminio liso s/RAL",                      341,  "aluminio"),
    ("Aluminio blanco con dibujo",               313,  "aluminio"),
    ("Aluminio dibujo RAL",                      381,  "aluminio"),
    ("Aluminio imitación madera (estándar)",     640,  "aluminio"),
    ("Aluminio imitación madera (3000×1250)",    1321, "aluminio"),
    ("5 cuadros pantografiado + zócalo",         630,  "fijo"),
    ("Plumeado dos aguas",                       395,  "fijo"),
    ("Precio especial (introducir manualmente)", None, "manual"),
]

CILINDROS = [
    ("Kaba Expert (por defecto)",    192),
    ("Kaba Matrix",                  137),
    ("Kaba Expert Extrem",           301),
    ("Keso 8000 Omega2",             362),
    ("Iseo R7",                       63),
    ("Iseo R7 amaestrado",           250),
    ("Abus Magnet",                  210),
    ("Cerradura electrónica a red y pilas", 2147),
    ("Cerradura electrónica solo pilas",    1903),
]

CILINDROS_DOBLE = [
    ("Kaba Matrix amaestrados (por defecto)", 350),
    ("Kaba Expert amaestrados",               452),
    ("Keso 8000 Omega2 amaestrados",          797),
    ("Iseo R7 amaestrados",                   175),
]

EXTRAS = [
    ("Extra Grado 4",               267),
    ("Extra aislante lana de roca",  26),
    ("Extra apertura invertida",    162),
    ("Extra pintado/barnizado RAL",  71),
    ("Protector THS",               129),
    ("Escalón drenante",             38),
    ("Escalón nuevo de agua",       145),
    ("Muelle cierrapuertas",        269),
    ("Mirilla digital",             142),
    ("Mirilla digital grabadora",   329),
    ("Tirador 600 mm cromo",         72),
    ("Tirador 1000 mm cromo",        91),
    ("Tirador 600 mm negro",         90),
    ("Tirador 1000 mm negro",       109),
    ("Forro de cerco",               88),
    ("Zócalo hasta 30 cm",           70),
    ("Tedee",                       467),
    ("Adaptador Tedee",              66),
]

JAMBAS_PRECIO   = 88
EMBOCADURA_150  = 98
EMBOCADURA_150P = 112
F1_29_68        = 134
DOBLE_CERRADURA = 219
