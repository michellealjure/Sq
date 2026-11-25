"""
SQ — piezas sueltas para pegar sobre la primera hoja (lila), alrededor de la ventana.

Hoja: carta horizontal 27,94 x 21,59 cm. Ventana del libro: 6,7 x 10 cm (vertical), centrada.
Todas las piezas: PNG con fondo transparente, tamaño real a 300 dpi, para recortar a mano.
La textura del paisaje sale de la ilustración de la guarda (output/paisaje/carta_*).

Uso: python3 primera_hoja.py   (requiere haber corrido antes generar.py paisaje)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter, zoom

RNG = np.random.default_rng(2929)
DPI = 300
PX_CM = DPI / 2.54
def cm(v):
    return int(round(v * PX_CM))

OUT = "output/primera_hoja"
os.makedirs(f"{OUT}/piezas", exist_ok=True)

PAGE_W, PAGE_H = cm(27.94), cm(21.59)
WIN_W, WIN_H = cm(6.7), cm(10.0)
WIN_X, WIN_Y = (PAGE_W - WIN_W) // 2, (PAGE_H - WIN_H) // 2
LILA = (207, 186, 255)
CREAM = np.array([241, 235, 220], np.float32)
MARK = 4

# ---------------------------------------------------------------------------
# Fuente: ilustración completa de la guarda (las dos cartas, una al lado de la otra)
# ---------------------------------------------------------------------------
c1 = np.asarray(Image.open("output/paisaje/carta_1_izquierda_300dpi.png").convert("RGB"))
c2 = np.asarray(Image.open("output/paisaje/carta_2_derecha_300dpi.png").convert("RGB"))
ILLU = np.concatenate([c1, c2], axis=1).astype(np.float32)  # 43,18 x 27,94 cm
IH, IW = ILLU.shape[:2]


def paper_grain(h, w, amount=0.03):
    g = gaussian_filter(RNG.normal(0, 1, (h, w)).astype(np.float32), 0.7)
    return 1 + amount * g / (g.std() + 1e-6)


def save(name, rgb, alpha):
    a = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    im.putalpha(Image.fromarray(a, "L"))
    im.save(f"{OUT}/piezas/{name}.png", dpi=(DPI, DPI), optimize=True)
    return im


def rough_edge(mask, strength=3.0, scale=1.2):
    """Borde de papel recortado: perturba el contorno con ruido fino."""
    m = gaussian_filter(mask.astype(np.float32), scale)
    n = gaussian_filter(RNG.normal(0, 1, mask.shape).astype(np.float32), strength)
    n /= n.std() + 1e-6
    return (m + 0.08 * n) > 0.5


pieces = {}

# ---------------------------------------------------------------------------
# 1. Fondo de postal (referente 3): rectángulo vertical, arriba papel, abajo paisaje
# ---------------------------------------------------------------------------
FW, FH = cm(8.6), cm(13.2)
fondo = np.empty((FH, FW, 3), np.float32)
split = int(FH * 0.52)
fondo[:split] = CREAM * np.array([0.965, 0.965, 0.975], np.float32)  # papel gris cálido
# paisaje: zona de montañas y colinas de la guarda
sx, sy = cm(17.0), cm(15.2)
fondo[split:] = ILLU[sy:sy + FH - split, sx:sx + FW]
fondo *= paper_grain(FH, FW, 0.025)[..., None]
pieces["fondo_postal"] = save("01_fondo_postal_8.6x13.2cm", fondo, np.ones((FH, FW)))

# ---------------------------------------------------------------------------
# 2. Nube recortada (referente 3), con el puntillismo de la guarda
# ---------------------------------------------------------------------------
NW, NH = cm(17.0), cm(9.5)
lo = 8  # se construye a baja resolución y luego se amplía
h, w = NH // lo, NW // lo
yy, xx = np.mgrid[:h, :w].astype(np.float32)
field = np.zeros((h, w), np.float32)
# cúmulo: muchas protuberancias sobre una base plana
for _ in range(70):
    cx = RNG.uniform(0.1, 0.9) * w
    top = max(0.05, 1 - abs(cx / w - 0.5) * 1.7)  # más alta en el centro
    cy = h * (0.86 - RNG.uniform(0.05, 0.66) * top)
    r = RNG.uniform(0.045, 0.1) * w * (0.7 + 0.5 * top)
    field += np.exp(-(((xx - cx) ** 2) + ((yy - cy) ** 2)) / (2 * (r * 0.62) ** 2))
field *= (yy < h * 0.9)  # base más o menos plana
cloud = field > 0.62
cloud = zoom(cloud.astype(np.float32), lo, order=1)
cloud = np.pad(cloud, ((0, max(0, NH - cloud.shape[0])), (0, max(0, NW - cloud.shape[1]))))[:NH, :NW] > 0.5
cloud = rough_edge(cloud, strength=4, scale=2.0)
# sombreado: más oscuro abajo y hacia los bordes internos
dist = gaussian_filter(cloud.astype(np.float32), cm(0.9))
lit = gaussian_filter(np.roll(cloud.astype(np.float32), cm(0.5), axis=0) < cloud, cm(0.25))
shade = np.clip(0.15 + 0.8 * dist - 0.55 * (np.arange(NH)[:, None] / NH) + 1.4 * lit, 0, 1)
shade += gaussian_filter(RNG.normal(0, 1, (NH, NW)).astype(np.float32), cm(0.35)) * 0.6
shade = np.clip(shade, 0, 1)
pal = np.array([[122, 146, 192], [162, 184, 219], [204, 215, 235], [245, 243, 238]], np.float32)
# puntillismo: marcas cuadradas de 4 px con mezcla aleatoria entre tonos vecinos
sm = shade[::MARK, ::MARK]
idx = np.clip(sm * 3 + RNG.normal(0, 0.55, sm.shape), 0, 3).round().astype(int)
marks = pal[idx] + RNG.normal(0, 5, (*sm.shape, 3))
nube = np.repeat(np.repeat(marks, MARK, 0), MARK, 1)
nube = np.pad(nube, ((0, max(0, NH - nube.shape[0])), (0, max(0, NW - nube.shape[1])), (0, 0)), mode='edge')[:NH, :NW]
nube *= paper_grain(NH, NW, 0.02)[..., None]
pieces["nube"] = save("02_nube_17x9.5cm", nube, cloud)

# ---------------------------------------------------------------------------
# 3. Mosaico tejido (referente 1): tiras y cuadros con fragmentos de la guarda
# ---------------------------------------------------------------------------
MW, MH = cm(23.0), cm(6.4)
pad = cm(0.8)
mos = np.zeros((MH + 2 * pad, MW + 2 * pad, 3), np.float32)
ma = np.zeros(mos.shape[:2], np.float32)
src_x0, src_y0 = cm(9.0), cm(20.8)  # zona de la guarda que se "teje"
x = 0
cols = []
while x < MW:
    cw = int(cm(RNG.choice([0.9, 1.2, 1.6, 2.0, 2.4])))
    cols.append((x, min(cw, MW - x)))
    x += cw
rows = [0]
while rows[-1] < MH:
    rows.append(rows[-1] + cm(RNG.uniform(1.4, 2.1)))
rows[-1] = MH
tiles_loose = []
for cx, cw in cols:
    strip = RNG.random() < 0.18  # tira vertical continua desplazada
    sdy = cm(RNG.uniform(-0.6, 0.6)) if strip else 0
    for r0, r1 in zip(rows[:-1], rows[1:]):
        th = r1 - r0
        dx = cm(RNG.uniform(-0.08, 0.08))
        dy = sdy + (0 if strip else cm(RNG.uniform(-0.12, 0.12)))
        X, Y = pad + cx + dx, pad + r0 + dy
        roll = RNG.random()
        if roll < 0.2:
            tile = np.ones((th, cw, 3), np.float32) * CREAM * RNG.uniform(0.95, 1.02)
        elif roll < 0.32:
            # fragmento "fuera de lugar": otra zona de la guarda (más verde)
            ox, oy = int(RNG.uniform(0, IW - cw)), int(RNG.uniform(cm(19), IH - th))
            tile = ILLU[oy:oy + th, ox:ox + cw].copy()
        else:
            ox = src_x0 + cx + cm(RNG.uniform(-0.3, 0.3))
            oy = src_y0 + r0 + cm(RNG.uniform(-0.3, 0.3))
            tile = ILLU[oy:oy + th, ox:ox + cw].copy()
        tile *= RNG.uniform(0.93, 1.05)
        mos[Y:Y + th, X:X + cw] = tile
        ma[Y:Y + th, X:X + cw] = 1
        # sombra mínima en el borde inferior = papel superpuesto
        mos[Y + th - 3:Y + th, X:X + cw] *= 0.82
        if RNG.random() < 0.09:
            tiles_loose.append(tile.copy())
# bordes irregulares: quitar algunas celdas de las esquinas/bordes
for cx, cw in cols:
    for r0, r1 in [(rows[0], rows[1]), (rows[-2], rows[-1])]:
        if RNG.random() < 0.35:
            ma[pad + r0 - cm(0.2):pad + r1 + cm(0.2), pad + cx:pad + cx + cw] = 0
mos *= paper_grain(*ma.shape, 0.02)[..., None]
ys, xs = np.where(ma > 0)
mos, ma = mos[ys.min():ys.max() + 1, xs.min():xs.max() + 1], ma[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
pieces["mosaico"] = save("03_mosaico_tejido_23x6.4cm", mos, ma)

# ---------------------------------------------------------------------------
# 4. Cuadros sueltos (para dispersar)
# ---------------------------------------------------------------------------
sizes = [0.8, 1.0, 1.0, 1.3, 1.3, 1.6, 1.6, 2.0, 2.0, 2.4, 2.8, 3.2]
loose = []
for i, s in enumerate(sizes):
    n = cm(s)
    if i % 4 == 3:
        t = np.ones((n, n, 3), np.float32) * CREAM
    else:
        ox, oy = int(RNG.uniform(0, IW - n)), int(RNG.uniform(cm(8), IH - n))
        t = ILLU[oy:oy + n, ox:ox + n].copy()
    t *= paper_grain(n, n, 0.02)[..., None]
    loose.append(save(f"04_cuadro_{i + 1:02d}_{s}cm", t, np.ones((n, n))))
pieces["cuadros"] = loose

# ---------------------------------------------------------------------------
# 5. Franja de montañas en serigrafía (referente 2): tintas planas, borde de tinta
# ---------------------------------------------------------------------------
BW, BH = cm(26.5), cm(7.0)
def ridge(base, amp, freq, phase):
    t = np.linspace(0, 1, BW)
    y = base
    for k, (a, f) in enumerate(zip(amp, freq)):
        y = y - a * np.sin(2 * np.pi * f * t + phase[k])
    noise = gaussian_filter(RNG.normal(0, 1, BW), 25) * 18
    return (y + noise).astype(int)

inks = [  # de atrás hacia adelante
    ((232, 170, 168), ridge(cm(2.3), [cm(1.4), cm(0.5)], [0.6, 1.7], RNG.uniform(0, 6, 2))),  # rosa
    ((111, 143, 192), ridge(cm(3.2), [cm(0.9), cm(0.4)], [0.9, 2.3], RNG.uniform(0, 6, 2))),  # azul guarda
    ((52, 92, 34), ridge(cm(3.9), [cm(1.0), cm(0.3)], [1.1, 3.1], RNG.uniform(0, 6, 2))),     # verde
    ((181, 166, 72), ridge(cm(4.8), [cm(0.7), cm(0.3)], [0.8, 2.6], RNG.uniform(0, 6, 2))),   # oliva
    ((216, 100, 52), ridge(cm(5.5), [cm(0.6), cm(0.25)], [1.4, 3.4], RNG.uniform(0, 6, 2))),  # naranja
    ((38, 68, 28), ridge(cm(6.1), [cm(0.5), cm(0.2)], [1.0, 2.9], RNG.uniform(0, 6, 2))),     # verde oscuro
]
band = np.zeros((BH, BW, 3), np.float32)
ba = np.zeros((BH, BW), np.float32)
rows_idx = np.arange(BH)[:, None]
for color, top in inks:
    m = rows_idx >= np.clip(top, 0, BH)[None, :]
    m = rough_edge(m, strength=2.5, scale=1.5)
    ink = np.array(color, np.float32) * (1 + RNG.normal(0, 0.035, (BH, BW, 1)))
    # textura de tinta: grano y pequeñas faltas de tinta (papel que asoma)
    voids = gaussian_filter(RNG.random((BH, BW)).astype(np.float32), 1.2) > 0.535
    ink[voids] = ink[voids] * 0.35 + CREAM * 0.65
    band[m] = ink[m]
    ba[m] = 1
# cuadrados de la caja: algunos módulos recortados en la franja (huecos)
for _ in range(7):
    s = cm(RNG.uniform(0.5, 1.3))
    x0, y0 = int(RNG.uniform(0, BW - s)), int(RNG.uniform(cm(3.2), BH - s - cm(0.3)))
    ba[y0:y0 + s, x0:x0 + s] = 0
band *= paper_grain(BH, BW, 0.025)[..., None]
pieces["montanas"] = save("05_montanas_serigrafia_26.5x7cm", band, ba)

# ---------------------------------------------------------------------------
# 6. Maqueta de composición sobre la hoja lila (solo referencia)
# ---------------------------------------------------------------------------
page = Image.new("RGBA", (PAGE_W, PAGE_H), LILA + (255,))
def place(im, x, y):
    page.alpha_composite(im, (int(x), int(y)))
place(pieces["nube"], (PAGE_W - NW) // 2 + cm(0.8), WIN_Y - cm(2.4))
place(pieces["mosaico"], (PAGE_W - pieces["mosaico"].width) // 2, PAGE_H - BH - cm(3.2))
place(pieces["montanas"], (PAGE_W - BW) // 2, PAGE_H - BH + cm(0.3))
fx, fy = WIN_X - (FW - WIN_W) // 2, WIN_Y - (FH - WIN_H) // 2
place(pieces["fondo_postal"], fx, fy)
for im, (x, y) in zip(pieces["cuadros"], [(3.0, 2.4), (4.8, 4.2), (22.4, 2.6), (24.2, 4.4), (20.8, 1.4),
                                         (2.0, 6.2), (23.9, 7.2), (5.2, 1.2), (21.7, 5.6), (1.2, 1.1),
                                         (25.0, 0.9), (1.5, 8.6)]):
    place(im, cm(x), cm(y))
# ventana / foto (marcador)
d = ImageDraw.Draw(page)
d.rectangle([WIN_X, WIN_Y, WIN_X + WIN_W, WIN_Y + WIN_H], fill=(120, 110, 105, 255))
d.rectangle([WIN_X, WIN_Y, WIN_X + WIN_W, WIN_Y + WIN_H], outline=(255, 255, 255, 255), width=cm(0.25))
mock = page.convert("RGB")
mock.save(f"{OUT}/maqueta_hoja_lila.jpg", quality=90)

# libro abierto: guarda (como quedó impresa, girada) + hoja lila
guarda = Image.open("output/paisaje/carta_1_izquierda_300dpi.png").convert("RGB").rotate(90, expand=True)
spread = Image.new("RGB", (PAGE_W * 2 + cm(0.3), PAGE_H), (60, 60, 60))
spread.paste(guarda.resize((PAGE_W, PAGE_H)), (0, 0))
spread.paste(mock, (PAGE_W + cm(0.3), 0))
spread.resize((spread.width // 3, spread.height // 3), Image.LANCZOS).save(f"{OUT}/maqueta_libro_abierto.jpg", quality=88)

# ---------------------------------------------------------------------------
# 7. Hojas para imprimir y recortar (carta horizontal, fondo blanco)
# ---------------------------------------------------------------------------
def sheet(items, name):
    s = Image.new("RGBA", (PAGE_W, PAGE_H), (255, 255, 255, 255))
    for im, (x, y) in items:
        s.alpha_composite(im, (cm(x), cm(y)))
    s = s.convert("RGB")
    s.save(f"{OUT}/{name}.png", dpi=(DPI, DPI))
    s.save(f"{OUT}/{name}.pdf", resolution=DPI)

sheet([(pieces["montanas"], (0.72, 0.8)), (pieces["mosaico"], (0.8, 9.0))], "imprimir_hoja_1")
items = [(pieces["nube"], (0.8, 0.8)), (pieces["fondo_postal"], (18.6, 0.8))]
x, y = 0.8, 11.2
for im in pieces["cuadros"]:
    wcm = im.width / PX_CM
    if x + wcm > 17.8:
        x, y = 0.8, y + 3.6
    items.append((im, (x, y)))
    x += wcm + 0.6
sheet(items, "imprimir_hoja_2")
print("ok")
