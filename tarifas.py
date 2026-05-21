# ─────────────────────────────────────────────────────────────────────────────
#  TARIFAS KIUSO 2026  ·  Seguridad Reina S.A.
#  Todos los precios con IVA incluido — redondeados a €
# ─────────────────────────────────────────────────────────────────────────────

MODELOS = {
    # ── UNA HOJA ─────────────────────────────────────────────────
    "KIUSO K-XXI": {
        "Estándar":                  2450,
        "Especial 1  ≤2100×1000":   2692,
        "Especial 2  ≤2300×1100":   2934,
        "Especial 3  ≤2450×1200":   3461,
        "Hasta 3000×1500":           4497,
    },
    "KIUSO K-100": {
        "Estándar":                  1754,
        "Especial 1  ≤2100×1000":   1877,
        "Especial 2  ≤2300×1100":   2036,
        "Especial 3  ≤2450×1200":   2407,
    },
    "KRONOS K-XXI": {
        "Estándar":                  2721,
        "Especial 1  ≤2100×1000":   2953,
        "Especial 2  ≤2300×1100":   3186,
        "Especial 3  ≤2450×1200":   3693,
        "Hasta 3000×1500":           4760,
    },
    "KRONOS K-100": {
        "Estándar":                  2119,
        "Especial 1  ≤2100×1000":   2243,
        "Especial 2  ≤2300×1100":   2401,
        "Especial 3  ≤2450×1200":   2772,
    },
    "ZOE": {
        "Estándar":                  3086,
        "Especial 1  ≤2100×1000":   3391,
        "Especial 2  ≤2300×1100":   3695,
        "Especial 3  ≤2450×1200":   4360,
        "Hasta 3000×1500":           5564,
    },
    "MARINO RF-60  (Grado 4)": {
        "Estándar":                  3358,
        "Especial 1  ≤2100×1000":   3466,
        "Especial 2  ≤2300×1100":   3541,
    },
    "MARINO RF-90  (Grado 4)": {
        "Estándar":                  3493,
        "Especial 1  ≤2100×1000":   3600,
        "Especial 2  ≤2300×1100":   3676,
    },
    "FIRE RF-30  (Grado 3)": {
        "Estándar":                  2898,
        "Especial 1  ≤2100×1000":   3006,
        "Especial 2  ≤2300×1100":   3082,
        "Especial 3  ≤2450×1200":   3198,
    },
    "FIRE RF-60  (Grado 3)": {
        "Estándar":                  3033,
        "Especial 1  ≤2100×1000":   3141,
        "Especial 2  ≤2300×1100":   3216,
        "Especial 3  ≤2450×1200":   3333,
    },
    "Grado V  (doble cerradura)": {
        "Estándar":                  3751,
        "Especial 1  ≤2100×1000":   3937,
        "Especial 2  ≤2300×1100":   4328,
    },
    "Grado V  (cerradura sencilla)": {
        "Estándar":                  3546,
    },
    # ── DOBLE HOJA ───────────────────────────────────────────────
    "DOBLE HOJA  K-XXI": {
        "Estándar  <1400 mm ancho total":  3966,
        "Menos de 2250×1750":              4191,
        "Menos de 2500×2000":              4345,
    },
    "DOBLE HOJA  K-100": {
        "Estándar  <1400 mm ancho total":  3159,
        "Menos de 2250×1750":              3336,
        "Menos de 2500×2000":              3456,
    },
    "DOBLE HOJA  KRONOS K-XXI": {
        "Estándar  <1400 mm ancho total":  4357,
        "Menos de 2250×1750":              4574,
        "Menos de 2500×2000":              4726,
    },
    "DOBLE HOJA  KRONOS K-100": {
        "Estándar  <1400 mm ancho total":  3540,
        "Menos de 2250×1750":              3724,
        "Menos de 2500×2000":              3838,
    },
    # ── TRASTERO ─────────────────────────────────────────────────
    "TRASTERO  (2000×900 / 2000×800)": {
        "Estándar":                  1184,
    },
}

TRASTERO_MODELOS = {"TRASTERO  (2000×900 / 2000×800)"}

# ── TABLEROS ─────────────────────────────────────────────────────────────────
# tipo: 'sapelly' | 'madera' | 'aluminio' | 'rustico' | 'especial' | 'manual'

TABLEROS = [
    # ─ MADERA LISA ───────────────────────────────────────────────
    ("Sapelly liso  (incluido en puerta)",              0,    "sapelly"),
    ("Roble liso",                                      80,   "madera"),
    ("Blanco liso",                                     80,   "madera"),
    ("Haya vaporizada",                                 80,   "madera"),
    ("Iroco liso",                                      80,   "madera"),
    ("Mansonia liso",                                   80,   "madera"),
    ("Chapa galvanizada",                               80,   "madera"),
    ("Sapelly rameado",                                 71,   "madera"),
    ("Haya blanca",                                     71,   "madera"),
    ("Mukali",                                          71,   "madera"),
    ("Pino Valsaín",                                    71,   "madera"),
    ("Pino Melis",                                      71,   "madera"),
    ("Embero",                                          71,   "madera"),
    ("Nogal",                                           126,  "madera"),
    ("Cerezo",                                          126,  "madera"),
    ("Wengué",                                          126,  "madera"),
    ("Pino Oregón",                                     126,  "madera"),
    ("MAD sapelly / roble",                             87,   "madera"),
    ("MAD blanco",                                      93,   "madera"),
    ("Tablero liso DM natural  (K100/KXXI)",            130,  "madera"),
    ("Tablero liso lacado RAL",                         151,  "madera"),
    # ─ ESPECIALES PRECIO COMPLETO ────────────────────────────────
    ("20F Standard",                                    221,  "especial"),
    ("20F s/croquis",                                   324,  "especial"),
    ("59F Standard",                                    362,  "especial"),
    ("Pantografiado Standard",                          169,  "especial"),
    ("Pantografiado Especial",                          236,  "especial"),
    ("Sapelly 10 cuadros moldura pegada",               390,  "especial"),
    ("Sapelly fajeado 3 cuadros + plafón",              785,  "especial"),
    ("Plumeado dos aguas",                              395,  "especial"),
    ("Mod. H-40 / PH-60 / PH",                         164,  "especial"),
    # ─ ALUMINIO ESTÁNDAR ──────────────────────────────────────────
    ("Aluminio liso blanco",                            245,  "aluminio"),
    ("Aluminio liso s/RAL standard",                    341,  "aluminio"),
    ("Aluminio liso s/RAL especial",                    409,  "aluminio"),
    ("Aluminio blanco con dibujo",                      313,  "aluminio"),
    ("Aluminio dibujo RAL standard",                    381,  "aluminio"),
    ("Aluminio dibujo RAL especial",                    449,  "aluminio"),
    ("Aluminio imitación madera liso",                  640,  "aluminio"),
    ("Aluminio imitación madera con dibujo",            790,  "aluminio"),
    ("Aluminio L09/L01 blanco",                         458,  "aluminio"),
    ("Aluminio L09/L01 s/RAL standard",                 582,  "aluminio"),
    ("Aluminio L09/L01 s/RAL especial",                 646,  "aluminio"),
    ("Aluminio L09/L01 imitación madera",               953,  "aluminio"),
    # ─ ALUMINIO MEDIDAS GRANDES ───────────────────────────────────
    ("Aluminio liso blanco  (3000×1250)",               891,  "aluminio"),
    ("Aluminio liso blanco  (3000×1500)",              1066,  "aluminio"),
    ("Aluminio s/RAL standard  (3000×1250)",           1064,  "aluminio"),
    ("Aluminio s/RAL standard  (3000×1500)",           1238,  "aluminio"),
    ("Aluminio imitación madera  (3000×1250)",         1321,  "aluminio"),
    ("Aluminio mod.51AL blanco  (3000×1250)",          1006,  "aluminio"),
    ("Aluminio mod.51AL blanco  (3000×1500)",          1206,  "aluminio"),
    ("Aluminio mod.51AL s/RAL std  (3000×1250)",       1178,  "aluminio"),
    ("Aluminio mod.51AL s/RAL std  (3000×1500)",       1378,  "aluminio"),
    ("Aluminio mod.51AL imitación madera  (3000×1250)",1452,  "aluminio"),
    # ─ RÚSTICOS DE ALUMINIO ───────────────────────────────────────
    ("Rústico Básica 1/2  roble dorado/nogal",          569,  "rustico"),
    ("Rústico Básica 1/2  roble claro/sapelly",         758,  "rustico"),
    ("Rústico 4AL  roble dorado/nogal",                1299,  "rustico"),
    ("Rústico 4AL  roble claro/sapelly",               1755,  "rustico"),
    # ─ PRECIO ESPECIAL ────────────────────────────────────────────
    ("Precio especial  (introducir manualmente)",       None, "manual"),
]

MOLDURADOS = [
    ("Sin moldurado",                    0),
    ("10S / 20S  (+78 €)",              78),
    ("15S / 25S / 30S / 50S  (+103 €)",103),
    ("35S / 55S  (+119 €)",            119),
    ("4 fresas  (+113 €)",             113),
    ("Fresado especial  (+154 €)",      154),
]

TABLEROS_SIN_MOLDURADO = {"especial", "aluminio", "rustico", "sapelly", "manual"}

# ── FIJOS Y MONTANTES ────────────────────────────────────────────────────────
FIJOS_MONTANTES = [
    ("Fijo en chapa",                                   828),
    ("Fijo cristal  <2100×410 mm",                      926),
    ("Fijo cristal  <2100×410 mm  con reja",           1052),
    ("Fijo cristal  <2300×545 mm",                     1088),
    ("Fijo cristal  <2300×545 mm  con reja",           1263),
    ("Fijo cristal  <2450×900 mm",                     1416),
    ("Fijo cristal  <2450×900 mm  con reja",           1809),
    ("Fijo cristal  hasta 2500×1200  sin reja",        1567),
    ("Fijo cristal  hasta 2500×1200  con reja",        2001),
    ("Fijo albañilería  ≤300 mm",                       507),
    ("Fijo albañilería  ≤500 mm",                       695),
    ("Fijo albañilería  ≤1000 mm",                      895),
    ("Montante en chapa  hasta 410 mm",                 533),
    ("Montante en chapa  mayor 410 mm",                 632),
    ("Montante con cristal o chapa rehundida",          828),
    ("Montante con cristal  con reja",                  953),
    ("Montante en albañilería  >200 mm",                491),
    ("Montante curvo con remate",                       912),
    ("Montante ciego Marino Ei60  max 1000×410",        786),
    ("Montante ciego Marino Ei60  max 1600×545",        843),
    ("Montante ciego Marino rehundido  max 1000×410",   640),
    ("Montante ciego Marino rehundido  max 1600×545",  1111),
    ("Suplemento hoja",                                 491),
    ("Extra remate montante curvo",                     351),
    ("Reja 5 horizontal",                                76),
    ("Reja 1×5",                                        142),
    ("Reja 2×5",                                        242),
    ("Reja 3×5",                                        325),
    ("Reja 4×5",                                        413),
    ("Tabicar puerta simulándola  (m2)",                370),
]

# ── CILINDROS ────────────────────────────────────────────────────────────────
CILINDROS = [
    ("Kaba Expert  (por defecto)",            192),
    ("Kaba Matrix",                           137),
    ("Kaba Matrix con pomo",                  152),
    ("Kaba Expert Extrem",                    301),
    ("Kaba Expert negro",                     237),
    ("Kaba Expert SAT",                       260),
    ("Kaba Expert con pomo 30/50 níquel",     204),
    ("Kaba Expert con pomo 30/60 níquel",     240),
    ("Keso 8000 Omega2",                      362),
    ("Keso 8000 Omega2 con pomo",             385),
    ("Keso 8000 Ultra",                       496),
    ("Cilindro AP4S",                         155),
    ("Iseo R7",                                63),
    ("Iseo R7 amaestrado",                    250),
    ("Iseo R7  50/60 para RF",                127),
    ("Abus Magnet",                           210),
    ("Abus Magnet amaestrado",                436),
    ("Stealth Key",                           324),
    ("Cilindro Libra",                        806),
    ("Cerradura electrónica a red y pilas",  2147),
    ("Cerradura electrónica solo pilas",     1903),
]

CILINDROS_DOBLE = [
    ("Kaba Matrix amaestrados  (por defecto)",  350),
    ("Kaba Expert amaestrados",                 452),
    ("Kaba Expert Extrem amaestrados",          565),
    ("Keso 8000 Omega2 amaestrados",            797),
    ("Keso 8000 Ultra amaestrados",            1113),
    ("Iseo R7 amaestrados  (juego)",            175),
    ("Abus Magnet amaestrados",                 436),
]

# ── EXTRAS ───────────────────────────────────────────────────────────────────
# Agrupados por categoría con separador "─── Categoría ───"
EXTRAS = [
    # ─ PUERTA ────────────────────────────────────────────────────
    ("Extra Grado 4",                           267),
    ("Extra aislante lana de roca",              26),
    ("Extra apertura invertida",                162),
    ("Extra pintado / barnizado RAL",            71),
    ("Extra Revólver antibala FB2",             452),
    ("Extra Magnum antibala FB3",               498),
    ("Incremento negro  (solo KXXI)",            76),
    ("Express especial",                        217),
    ("Express muy especial",                    267),
    ("Precerco soldadura",                       84),
    ("Precerco Grado 5",                        141),
    # ─ CERRAJERÍA ────────────────────────────────────────────────
    ("Cerradura eléctrica CISA",                330),
    ("Cerradero eléctrico",                     137),
    ("Cerradura antipánico  (sin cilindro)",    146),
    ("Cerradura emergencia + barra toallero",   738),
    ("Muelle cierrapuertas RC3/RC4",            269),
    ("Muelle cierrapuertas RC5/RF",             532),
    ("Extra 3D Key",                            470),
    ("Extra 3D Key doble  (sin cilindro)",      594),
    ("Electropistón",                           750),
    ("Contacto magnético",                       83),
    ("Protector imán",                          322),
    # ─ CAMBIOS DE CERRADURA ──────────────────────────────────────
    ("Cambio cerradura K-XXI",                  596),
    ("Cambio cerradura Torex/Reina",            596),
    ("Cambio cerradura borjas a Matrix/Abus",   527),
    ("Cambio cerradura borjas a Expert",        583),
    ("Cambio cerradura borjas a AP4S",          583),
    ("Cambio cerradura Expert SAT",             651),
    ("Cambio cerradura Expert Extrem",          692),
    ("Cambio cerradura Torex/Reina Matrix",     597),
    ("Cambio cerradura Torex/Reina Expert",     652),
    ("Cambio cerradura MIA",                    274),
    ("Cambio doble — cilindros Matrix",         967),
    ("Cambio doble — cilindros Expert",        1073),
    ("Cambio doble — cilindros ISEO",           784),
    ("Bloque MIA con 5 llaves",                 110),
    # ─ LLAVES ────────────────────────────────────────────────────
    ("Llave extra Kaba Matrix",                  36),
    ("Llave extra Kaba Expert",                  36),
    ("Llave extra AP3S/AP4S",                    29),
    ("Llave extra Iseo R7",                      18),
    ("Llave extra Abus Magnet",                  36),
    ("Llave extra Keso",                         36),
    ("Llave extra borjas",                       18),
    ("Llave extra protector imantado",           62),
    ("Porte envío de llaves",                    19),
    # ─ DOMÓTICA ──────────────────────────────────────────────────
    ("Tedee",                                   467),
    ("Adaptador Tedee",                          66),
    ("Teclado Tedee",                           197),
    ("Bridge Tedee",                            119),
    ("Danalock con pilas",                      312),
    ("Teclado Danalock",                        167),
    ("X1R EVO — Lector huella  (teclado digital)", 1049),
    ("X1R EVO — Gateway  (pasarela internet)",  483),
    ("X1R EVO — Barra toallero",                238),
    ("X1R EVO — Precio total con lector huella", 2493),
    # ─ TABLEROS ──────────────────────────────────────────────────
    ("Extra tablero H",                          25),
    ("Cristal corto alojado en tablero",        117),
    ("Cristal largo alojado en tablero",        221),
    ("Incrustaciones en INOX",                  102),
    ("Extra decoración según croquis",           39),
    ("Manipulación tablero del cliente",         48),
    ("Tachuelas  (por unidad)",                   3),
    # ─ REMATES Y ACABADOS ────────────────────────────────────────
    ("Escalón drenante",                          38),
    ("Escalón nuevo de agua",                    145),
    ("Cortavientos  (sin escalón)",              105),
    ("Forro de cerco",                            88),
    ("Zócalo hasta 30 cm",                        70),
    ("Vierteaguas",                               82),
    ("Vierteaguas con burlete",                   97),
    ("F1 burlete agua  (juego)",                  90),
    ("F1 + F1 agua + 29 + 68  (con burlete)",    224),
    ("Media caña  (juego)",                       72),
    ("Tratamiento intemperie",                    80),
    ("Pintura cerco RAL standard",                90),
    ("Pintura cerco RAL especial",               133),
    ("Lacar perfilería aluminio RAL",            182),
    ("Precio burlete  (por metro)",                9),
    # ─ HERRAJES ──────────────────────────────────────────────────
    ("Protector THS",                            129),
    ("Protector polvo diamante",                 149),
    ("Mirilla cromo / dorado",                    10),
    ("Mirilla digital",                          142),
    ("Mirilla digital grabadora",                329),
    ("Tirador 600 mm cromo",                      72),
    ("Tirador 1000 mm cromo",                     91),
    ("Tirador 600 mm negro",                      90),
    ("Tirador 1000 mm negro",                    109),
    ("Doble manilla",                             35),
    ("Pomo cromo o dorado",                       19),
    ("Manilla roseta",                            32),
    ("Manilla larga borjas",                      32),
    ("Juego capuchones",                           5),
    # ─ CRISTAL EN HOJA ───────────────────────────────────────────
    ("Cristal largo en hoja",                    983),
    ("Cristal largo en hoja con reja",          1318),
    ("Cristal corto en hoja",                    771),
    ("Cristal corto en hoja con reja",          1193),
    # ─ INSTALACIÓN Y SERVICIO ────────────────────────────────────
    ("Mano de obra  (por hora)",                  92),
    ("Instalación albañilería",                   57),
    ("Instalación soldadura",                     57),
    ("Desplazamiento  (incluye 30 min)",          92),
    ("Desmontaje puerta acorazada",              104),
    ("Panel provisional",                        105),
    ("Recuperar reja  (por reja)",                80),
]

# ── JAMBAS / EMBOCADURA / REMATES ────────────────────────────────────────────
JAMBAS_PRECIO    = 88
EMBOCADURA_150   = 98
EMBOCADURA_150P  = 112
EMBOCADURA_MDA_S = 158
EMBOCADURA_MDA_L = 197
EMBOCADURA_ALU_S = 181
EMBOCADURA_ALU_L = 217
F1_29_68         = 134
DOBLE_CERRADURA  = 219
