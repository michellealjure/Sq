"""
SQ — ilustración panorámica para el interior de una caja (Parte 1 + Lomo + Parte 2).

Lienzo: 56,7 x 35,1 cm a 300 dpi (incluye 0,5 cm de sangrado por lado).
  Áreas de corte según las guías del montaje (ver TRIM_*):
  Parte 1: 0,5   – 27,4 cm  -> número 29 construido con cuadrados (fondo blanco)
  Lomo   : 27,85 – 29,05 cm -> continuación del paisaje
  Parte 2: 29,6  – 56,2 cm  -> paisaje con recortes cuadrados blancos

Unidad gráfica: el cuadrado. No se dibuja ningún círculo.
Uso:
  python3 generar.py arboles   -> foto de los árboles en alta resolución (output/arboles/)
  python3 generar.py paisaje   -> ilustración puntillista del valle (output/paisaje/)
  python3 generar.py           -> ambas
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from scipy.ndimage import distance_transform_edt, gaussian_filter, zoom

RNG = np.random.default_rng(29)
DPI = 300
PX_CM = DPI / 2.54

def cm(v):
    return int(round(v * PX_CM))

# Medidas del documento (guías rosadas del montaje): 56,7 x 35,1 cm con 0,5 cm de sangrado.
W, H = cm(56.7), cm(35.1)
# Áreas de corte medidas sobre las guías: Parte 1, lomo y Parte 2 (cm desde la izquierda)
TRIM_P1, TRIM_LOMO, TRIM_P2 = (0.5, 27.4), (27.85, 29.05), (29.6, 56.2)
P1_END, LOMO_END = cm(TRIM_P1[1]), cm(TRIM_P2[0])
BLEED = cm(0.5)
PAPER = np.array([251, 250, 246], np.float32)       # blanco papel (Parte 1)
CUT_WHITE = np.array([250, 248, 242], np.float32)   # recorte blanco
CUT_CREAM = np.array([241, 235, 220], np.float32)   # recorte crema
MARK = 4  # tamaño de la marca puntillista (px a 300 dpi ≈ 0,34 mm), cuadrada

# Versiones. STYLE "foto": la fotografía en alta resolución, sin reinterpretar.
#            STYLE "puntillista": reinterpretación con marcas cuadradas y grano de impresión.
VERSIONS = {
    "arboles": dict(SRC="assets/arboles.jpg", STYLE="foto"),
    "paisaje": dict(SRC="assets/paisaje.jpg", STYLE="puntillista"),
}
if len(sys.argv) < 2:
    for v in VERSIONS:
        os.system(f"{sys.executable} {__file__} {v}")
    sys.exit()
VERSION = sys.argv[1]
SRC, STYLE = VERSIONS[VERSION]["SRC"], VERSIONS[VERSION]["STYLE"]
OUT = f"output/{VERSION}"
os.makedirs(OUT, exist_ok=True)
TRANSPARENT = True  # los espacios blancos se exportan sin fondo (PNG con transparencia)

# ---------------------------------------------------------------------------
# 1. Paisaje puntillista (marcas cuadradas, textura de impresión artesanal)
# ---------------------------------------------------------------------------
def stylize(img, out_w, out_h):
    """Reinterpreta una foto como ilustración de marcas pequeñas y planos de color."""
    ww, wh = out_w // MARK, out_h // MARK
    im = img.resize((ww, wh), Image.LANCZOS)
    # simplificar formas: suavizado que conserva bordes + filtro modal
    for _ in range(2):
        im = im.filter(ImageFilter.MedianFilter(5))
    im = ImageEnhance.Color(im).enhance(1.45)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    # paleta reducida tipo tintas de impresión
    q = im.quantize(colors=18, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = q.filter(ImageFilter.ModeFilter(5))
    base = np.asarray(q.convert("RGB"), np.float32)

    # desplazar la paleta hacia verdes / azules / amarillos con acentos cálidos
    r, g, b = base[..., 0], base[..., 1], base[..., 2]
    lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255.0
    green = (g > r) & (g > b)
    base[..., 1] = np.where(green, g * 1.04, g)
    base[..., 0] = np.where(green & (lum > 0.45), r * 1.08, r)  # verdes claros -> amarillentos
    sky = (b >= g) & (lum > 0.45)
    base[..., 2] = np.where(sky, b * 1.05, b)

    h, w = base.shape[:2]
    out = base.copy()
    # mezcla puntillista: algunas marcas toman el color de una vecina cercana
    for k in range(3):
        dy = RNG.integers(-3, 4, size=(h, w))
        dx = RNG.integers(-3, 4, size=(h, w))
        yy = np.clip(np.arange(h)[:, None] + dy, 0, h - 1)
        xx = np.clip(np.arange(w)[None, :] + dx, 0, w - 1)
        pick = RNG.random((h, w)) < 0.16
        out[pick] = base[yy, xx][pick]
    # variación de tinta por marca
    out += RNG.normal(0, 7, out.shape).astype(np.float32)
    out *= (1 + RNG.normal(0, 0.05, (h, w, 1))).astype(np.float32)
    # papel visible entre marcas (más en zonas claras)
    lum = (0.3 * out[..., 0] + 0.59 * out[..., 1] + 0.11 * out[..., 2]) / 255.0
    p_paper = 0.015 + 0.12 * np.clip(lum, 0, 1) ** 2
    gap = RNG.random((h, w)) < p_paper
    out[gap] = out[gap] * 0.25 + PAPER * 0.75
    # marcas oscuras dispersas (grano de impresión)
    dark = RNG.random((h, w)) < 0.035
    out[dark] *= 0.72
    out = np.clip(out, 0, 255)

    full = np.repeat(np.repeat(out, MARK, 0), MARK, 1)
    pad_h, pad_w = out_h - full.shape[0], out_w - full.shape[1]
    full = np.pad(full, ((0, pad_h), (0, pad_w), (0, 0)), mode="edge")
    # máscara de las marcas de papel (puntos blancos del puntillismo), a tamaño final
    g = np.repeat(np.repeat(gap, MARK, 0), MARK, 1)
    stylize.last_gap = np.pad(g, ((0, pad_h), (0, pad_w)), mode="edge")
    return full


photo = Image.open(SRC).convert("RGB")
pw, ph = photo.size

# Imagen a sangre en todo el lienzo (escala "cover" + recorte centrado)
scale = max(W / pw, H / ph)
rw, rh = int(np.ceil(pw * scale)), int(np.ceil(ph * scale))
x_off, y_off = (rw - W) // 2, (rh - H) // 2
photo_pan = photo.resize((rw, rh), Image.LANCZOS).crop((x_off, y_off, x_off + W, y_off + H))

if STYLE == "puntillista":
    landscape = stylize(photo_pan, W, H)
    land_gap = stylize.last_gap
else:
    landscape = np.asarray(photo_pan, np.float32)
# los cuadrados del 29 muestran la imagen que hay "debajo" del papel
fragments = landscape
if STYLE == "puntillista":
    # ilustración anterior: el 29 muestra la zona baja del valle (montañas y vegetación)
    fx0, fy0 = int(pw * 0.02), int(ph * 0.47)
    fw = int((ph - fy0) * P1_END / H)
    fragments = stylize(photo.crop((fx0, fy0, fx0 + fw, ph)), P1_END, H)
    frag_gap = stylize.last_gap

# Distribución aprobada (posiciones del 29, dispersión, huecos y recortes):
# se restaura el estado aleatorio con el que se generó, para que cambiar
# la imagen no mueva ningún cuadrado.
import json
RNG.bit_generator.state = json.load(open("assets/rng_layout.json"))

# ---------------------------------------------------------------------------
# 2. Lienzo base: papel blanco en Parte 1, paisaje desde la intrusión hacia la derecha
# ---------------------------------------------------------------------------
canvas = np.empty((H, W, 3), np.float32)
canvas[:] = PAPER
alpha = np.zeros((H, W), bool)  # True = imagen, False = blanco / transparente
src_map = np.zeros((H, W), np.uint8)  # 1 = paisaje, 2 = fragmentos del 29

# Retícula del 29
CELL = cm(1.15)  # un poco más pequeño que la versión anterior (1,26 cm)
glyph_2 = [
    "..XXXXXX..",
    ".XXXXXXXXX",
    "XXX....XXX",
    "XX......XX",
    "........XX",
    "......XXX.",
    "....XXXX..",
    "..XXXX....",
    ".XXX......",
    "XXXXXXXXXX",
    "XXXXXXXXXX",
]
glyph_9 = [
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    "XX......XX",
    "XX......XX",
    "XX......XX",
    "XXXXXXXXXX",
    ".XXXXXXXXX",
    "........XX",
    "........XX",
    "XXXXXXXXXX",
    "XXXXXXXXX.",
]
GH = len(glyph_2)
NUM_ROWS = GH + 1 + GH  # 2 arriba, 9 abajo (según boceto)
num_left = cm((TRIM_P1[0] + TRIM_P1[1]) / 2) - 5 * CELL  # centrado en la Parte 1
num_top = (H - NUM_ROWS * CELL) // 2
MAX_COL = int((P1_END - num_left) // CELL)  # última columna completa dentro de la Parte 1

C0 = -int(np.ceil(num_left / CELL)) - 1
R0 = -int(np.ceil(num_top / CELL)) - 1
ncols = MAX_COL - C0
nrows = NUM_ROWS - 2 * R0
shape = np.zeros((nrows, ncols), bool)
for r, line in enumerate(glyph_2):
    for c, ch in enumerate(line):
        shape[r - R0, c - C0] = ch == "X"
for r, line in enumerate(glyph_9):
    for c, ch in enumerate(line):
        shape[r + GH + 1 - R0, c - C0] = ch == "X"

dist = distance_transform_edt(~shape)  # distancia (en celdas) al número

# borde del paisaje escalonado e irregular (entra en la Parte 1)
edge = []
e = MAX_COL - 1
for ri in range(nrows):
    e = int(np.clip(e + RNG.integers(-1, 2), MAX_COL - 3, MAX_COL))
    edge.append(e)
for ri in range(nrows):
    y0 = max(num_top + (ri + R0) * CELL, 0)
    y1 = min(num_top + (ri + R0 + 1) * CELL, H)
    if y1 > y0:
        x0 = num_left + edge[ri] * CELL
        canvas[y0:y1, x0:] = landscape[y0:y1, x0:]
        alpha[y0:y1, x0:] = True
        src_map[y0:y1, x0:] = 1
canvas[:, P1_END:] = landscape[:, P1_END:]
alpha[:, P1_END:] = True
src_map[:, P1_END:] = 1

squares = []  # (x0, y0, size, source)
for ri in range(nrows):
    for ci in range(ncols):
        c, r = ci + C0, ri + R0
        if c >= edge[ri]:
            continue
        cx = num_left + c * CELL + CELL / 2
        cy = num_top + r * CELL + CELL / 2
        if shape[ri, ci]:
            n = shape[max(ri - 1, 0):ri + 2, max(ci - 1, 0):ci + 2].sum() - 1
            s = 0.80 + 0.16 * (n / 8) + RNG.normal(0, 0.03)
            s = float(np.clip(s, 0.76, 0.97))
            src = "frag"
        else:
            d = dist[ri, ci]
            s_num = 0.32 * np.exp(-(d - 1) * 0.5) * RNG.uniform(0.8, 1.15)
            if d > 2.5 and RNG.random() > max(0.4, np.exp(-(d - 2.5) * 0.3)):
                s_num = 0
            s_num = max(s_num, RNG.uniform(0.035, 0.06) if RNG.random() < 0.6 else 0)
            dl = edge[ri] - c  # 1 = celda pegada al paisaje
            s_land = 0.76 * np.exp(-(dl - 1) * 0.6) * RNG.uniform(0.8, 1.08)
            s = float(min(s_num, 0.92))
            src = "frag"
        if s <= 0:
            continue
        size = max(int(round(CELL * s)), 6)
        x0, y0 = int(round(cx - size / 2)), int(round(cy - size / 2))
        squares.append((x0, y0, size, src))

for x0, y0, size, src in squares:
    xa, ya = max(x0, 0), max(y0, 0)
    xb, yb = min(x0 + size, W), min(y0 + size, H)
    if xb <= xa or yb <= ya:
        continue
    tex = fragments if (src == "frag" and xb <= P1_END) else landscape
    canvas[ya:yb, xa:xb] = tex[ya:yb, xa:xb]
    alpha[ya:yb, xa:xb] = True
    src_map[ya:yb, xa:xb] = 2 if tex is fragments and fragments is not landscape else 1

# ---------------------------------------------------------------------------
# 2b. Cuadrados blancos "desprendidos" del paisaje junto a su borde
for ri in range(nrows):
    for c in range(edge[ri], MAX_COL + 1):
        k = c - edge[ri]
        if RNG.random() > (0.30 if k == 0 else 0.16 if k == 1 else 0.07):
            continue
        cx = num_left + c * CELL + CELL / 2
        cy = num_top + (ri + R0) * CELL + CELL / 2
        RNG.uniform(0.45, 0.88)  # (mantiene la secuencia aleatoria del resto)
        # hueco a celda completa: sin franja de paisaje alrededor
        size = CELL
        x0, y0 = num_left + c * CELL, num_top + (ri + R0) * CELL
        if x0 + size > P1_END - cm(0.2):
            continue
        canvas[max(y0, 0):max(y0 + size, 0), x0:x0 + size] = PAPER
        alpha[max(y0, 0):max(y0 + size, 0), x0:x0 + size] = False

# ---------------------------------------------------------------------------
# 3. Parte 2: recortes cuadrados blancos / crema concentrados en el centro
# ---------------------------------------------------------------------------
# Recortes aprobados (assets/recortes_parte2.json, en el lienzo anterior de 58,5 cm).
# Se reubican proporcionalmente en la nueva Parte 2 y se descartan los que tocan el margen.
import json
OLD_P2 = (cm(30.8), cm(58.0))
NEW_P2 = (cm(TRIM_P2[0]), cm(TRIM_P2[1]))
REMOVED = {(6690, 1813, 77)}  # recorte pegado al margen derecho (pedido de borrar)
placed = []
for ox, oy, size in json.load(open("assets/recortes_parte2.json")):
    if (ox, oy, size) in REMOVED:
        continue
    ocx = ox + size / 2
    ncx = NEW_P2[0] + (ocx - OLD_P2[0]) * (NEW_P2[1] - NEW_P2[0]) / (OLD_P2[1] - OLD_P2[0])
    x0 = int(round(ncx - size / 2))
    if x0 < NEW_P2[0] + cm(0.4) or x0 + size > NEW_P2[1] - cm(0.4):
        continue
    placed.append((x0, oy, size))

for x0, y0, size in placed:
    RNG.random()  # (mantiene la secuencia aleatoria)
    # mismo blanco del fondo de la Parte 1: todo lo que no es imagen es blanco
    canvas[y0:y0 + size, x0:x0 + size] = PAPER
    alpha[y0:y0 + size, x0:x0 + size] = False

# ---------------------------------------------------------------------------
# 4. Textura de papel impreso en toda la superficie
# ---------------------------------------------------------------------------
if STYLE == "puntillista":
    grain = RNG.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    grain = zoom(gaussian_filter(grain, 0.6), 2, order=1)
    grain = np.pad(grain, ((0, max(0, H - grain.shape[0])), (0, max(0, W - grain.shape[1]))), mode="edge")[:H, :W]
    blot = zoom(gaussian_filter(RNG.normal(0, 1, (H // 40, W // 40)).astype(np.float32), 3), 40, order=1)
    blot = np.pad(blot, ((0, max(0, H - blot.shape[0])), (0, max(0, W - blot.shape[1]))), mode="edge")[:H, :W]
    tex = 1 + 0.022 * grain + 0.05 * blot
    canvas *= tex[..., None]
canvas = np.clip(canvas, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------------------
# 4b. Hojas tamaño carta con la ilustración completa (sin 29, sin recortes, sin blancos)
# ---------------------------------------------------------------------------
# Zonas elegidas sobre el montaje (cm desde la esquina superior izquierda del documento).
CARTA_W, CARTA_H = cm(21.59), cm(27.94)  # 8,5 x 11 in
CARTAS = {
    "carta_1_izquierda": (13.52, 0.0),  # 13,52 – 35,11 cm (cruza el lomo)
    "carta_2_derecha": (56.7 - 21.59, 0.0),                     # 35,11 – 56,70 cm
}
if STYLE == "puntillista":
    full_illu = np.clip(landscape * tex[..., None], 0, 255).astype(np.uint8)
    for name, (xc, yc) in CARTAS.items():
        x0, y0 = cm(xc), cm(yc)
        sheet = Image.fromarray(full_illu[y0:y0 + CARTA_H, x0:x0 + CARTA_W], "RGB")
        assert sheet.size == (CARTA_W, CARTA_H), sheet.size
        sheet.save(f"{OUT}/{name}_300dpi.png", dpi=(DPI, DPI), optimize=True)
        sheet.save(f"{OUT}/{name}_300dpi.pdf", resolution=DPI)

# ---------------------------------------------------------------------------
# 5. Exportación
# ---------------------------------------------------------------------------
img = Image.fromarray(canvas, "RGB")  # versión sobre blanco
if TRANSPARENT:
    rgba = img.copy()
    if STYLE == "puntillista":
        # los puntos blancos del puntillismo también quedan transparentes
        specks = np.zeros((H, W), bool)
        specks[src_map == 1] = land_gap[src_map == 1]
        if fragments is not landscape:
            fr = np.zeros((H, W), bool)
            fr[:, :P1_END] = frag_gap[:, :P1_END]
            specks |= (src_map == 2) & fr
        alpha &= ~specks
    rgba.putalpha(Image.fromarray(alpha.astype(np.uint8) * 255, "L"))
    rgba.save(f"{OUT}/sq_caja_56.7x35.1cm_300dpi.png", dpi=(DPI, DPI), optimize=True)
else:
    img.save(f"{OUT}/sq_caja_56.7x35.1cm_300dpi.png", dpi=(DPI, DPI), optimize=True)
img.save(f"{OUT}/sq_caja_56.7x35.1cm_300dpi_fondo_blanco.pdf", resolution=DPI)

prev = img.resize((2400, int(2400 * H / W)), Image.LANCZOS)
prev.save(f"{OUT}/preview.jpg", quality=90)

# guías (solo referencia, no imprimir): sangrado, pliegues, área segura
g = prev.copy()
d = ImageDraw.Draw(g)
k = 2400 / W
def vline(x, color, dash=False):
    X = x * k
    if dash:
        for y in range(0, g.height, 14):
            d.line([(X, y), (X, y + 7)], fill=color, width=2)
    else:
        d.line([(X, 0), (X, g.height)], fill=color, width=2)
b = BLEED * k
d.rectangle([0, 0, g.width - 1, g.height - 1], outline=(230, 40, 200), width=2)
for x0c, x1c in (TRIM_P1, TRIM_LOMO, TRIM_P2):
    d.rectangle([cm(x0c) * k, b, cm(x1c) * k, g.height - b], outline=(230, 40, 200), width=2)
g.save(f"{OUT}/preview_guias.jpg", quality=90)
print("ok", W, H, "cuadrados 29:", len(squares), "recortes:", len(placed))
