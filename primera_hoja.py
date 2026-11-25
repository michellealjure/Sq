"""
SQ — primera hoja, versión 2 (a partir de la composición elegida).

Piezas para pegar sobre la hoja lila (carta horizontal 27,94 x 21,59 cm), con retazos
de la ilustración de la guarda. Sin nube y sin montañas.

  1. Postal: papel crema arriba, paisaje abajo (9,6 x 13,4 cm).
  2. Estampilla: borde blanco perforado donde va la foto (7,6 x 10,9 cm; foto 6,7 x 10 cm).
  3. Mosaico en damero, izquierda y derecha (pasan por detrás de la postal).
  4. Cuadros sueltos para las esquinas superiores.

Todas las piezas: PNG con fondo transparente, tamaño real a 300 dpi.
Uso: python3 primera_hoja.py   (requiere output/paisaje/carta_*.png de generar.py)
"""
import os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

RNG = np.random.default_rng(1029)
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
CREAM = np.array([240, 228, 204], np.float32)   # papel crema de la postal y del damero
STAMP = np.array([250, 246, 237], np.float32)   # blanco de la estampilla

# Retazos: ilustración completa de la guarda (las dos cartas juntas, 43,18 x 27,94 cm)
c1 = np.asarray(Image.open("output/paisaje/carta_1_izquierda_300dpi.png").convert("RGB"))
c2 = np.asarray(Image.open("output/paisaje/carta_2_derecha_300dpi.png").convert("RGB"))
ILLU = np.concatenate([c1, c2], axis=1).astype(np.float32)
IH, IW = ILLU.shape[:2]
ZONES = {  # franjas verticales de la guarda (cm desde arriba)
    "cielo": (1.0, 9.0),
    "montana": (10.0, 14.5),
    "colinas": (16.5, 27.5),
}

def retazo(w, h, zone):
    y0, y1 = cm(ZONES[zone][0]), cm(ZONES[zone][1])
    x = int(RNG.uniform(0, IW - w))
    y = int(RNG.uniform(y0, max(y0 + 1, y1 - h)))
    return ILLU[y:y + h, x:x + w].copy()

def grain(h, w, amount=0.025):
    g = gaussian_filter(RNG.normal(0, 1, (h, w)).astype(np.float32), 0.7)
    return 1 + amount * g / (g.std() + 1e-6)

def save(name, rgb, alpha):
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    im.putalpha(Image.fromarray((np.clip(alpha, 0, 1) * 255).astype(np.uint8), "L"))
    im.save(f"{OUT}/piezas/{name}.png", dpi=(DPI, DPI), optimize=True)
    return im

P = {}

# ---------------------------------------------------------------------------
# 1. Postal: crema arriba, paisaje abajo con línea de colinas orgánica
# ---------------------------------------------------------------------------
PW, PH = cm(9.6), cm(13.4)
post = np.empty((PH, PW, 3), np.float32)
post[:] = CREAM
land = ILLU[cm(14.5):cm(14.5) + PH, cm(28.0):cm(28.0) + PW]
ridge = PH * 0.56 + gaussian_filter(RNG.normal(0, 1, PW), 60) * cm(0.9) \
    - cm(0.5) * np.sin(np.linspace(0, 2.6, PW))
below = np.arange(PH)[:, None] >= ridge[None, :]
post[below] = land[below]
post *= grain(PH, PW)[..., None]
P["postal"] = save("01_postal_9.6x13.4cm", post, np.ones((PH, PW)))

# ---------------------------------------------------------------------------
# 2. Estampilla: borde blanco perforado (la foto de 6,7 x 10 cm va encima)
# ---------------------------------------------------------------------------
SW, SH = cm(7.6), cm(10.9)
SS = 3  # supermuestreo para bordes limpios
mask = Image.new("L", (SW * SS, SH * SS), 255)
d = ImageDraw.Draw(mask)
r = cm(0.12) * SS
pitch = cm(0.34) * SS
for x in np.arange(pitch / 2, SW * SS, pitch):
    for y in (0, SH * SS):
        d.ellipse([x - r, y - r, x + r, y + r], fill=0)
for y in np.arange(pitch / 2, SH * SS, pitch):
    for x in (0, SW * SS):
        d.ellipse([x - r, y - r, x + r, y + r], fill=0)
mask = np.asarray(mask.resize((SW, SH), Image.LANCZOS)).astype(np.float32) / 255
stamp = np.empty((SH, SW, 3), np.float32)
stamp[:] = STAMP
stamp *= grain(SH, SW, 0.015)[..., None]
# guía sutil de dónde va la foto (línea muy clara, queda tapada por la foto)
gx, gy = (SW - WIN_W) // 2, (SH - WIN_H) // 2
stamp[gy:gy + 2, gx:gx + WIN_W] *= 0.93
stamp[gy + WIN_H - 2:gy + WIN_H, gx:gx + WIN_W] *= 0.93
stamp[gy:gy + WIN_H, gx:gx + 2] *= 0.93
stamp[gy:gy + WIN_H, gx + WIN_W - 2:gx + WIN_W] *= 0.93
P["estampilla"] = save("02_estampilla_7.6x10.9cm", stamp, mask)

# ---------------------------------------------------------------------------
# 3. Mosaico en damero (izquierda y derecha)
# ---------------------------------------------------------------------------
CELL = cm(1.65)
def damero(cols, rows, name, flip=False):
    W, H = cols * CELL + cm(0.4), rows * CELL + cm(0.4)
    rgb = np.zeros((H, W, 3), np.float32)
    a = np.zeros((H, W), np.float32)
    for r_ in range(rows):
        for c_ in range(cols):
            cc = (cols - 1 - c_) if flip else c_
            # el damero se deshace hacia el extremo exterior
            edge = cc / (cols - 1)  # 0 = exterior, 1 = junto a la postal
            if RNG.random() > 0.55 + 0.45 * edge:
                continue
            landscape = (r_ + c_) % 2 == 0
            s = CELL if RNG.random() > 0.2 else int(CELL * RNG.uniform(0.75, 0.9))
            x = c_ * CELL + cm(0.2) + cm(RNG.uniform(-0.06, 0.06)) + (CELL - s) // 2
            y = r_ * CELL + cm(0.2) + cm(RNG.uniform(-0.06, 0.06)) + (CELL - s) // 2
            if landscape:
                zone = "cielo" if r_ == 0 and RNG.random() < 0.45 else RNG.choice(["colinas", "montana", "cielo"], p=[0.6, 0.25, 0.15])
                tile = retazo(s, s, zone)
            else:
                tile = np.ones((s, s, 3), np.float32) * CREAM * RNG.uniform(0.97, 1.02)
            tile *= grain(s, s, 0.02)[..., None]
            rgb[y:y + s, x:x + s] = tile
            a[y:y + s, x:x + s] = 1
    ys, xs = np.where(a > 0)
    rgb, a = rgb[ys.min():ys.max() + 1, xs.min():xs.max() + 1], a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return save(name, rgb, a)

P["damero_izq"] = damero(5, 4, "03_damero_izquierda", flip=False)
P["damero_der"] = damero(5, 4, "04_damero_derecha", flip=True)

# ---------------------------------------------------------------------------
# 4. Cuadros sueltos (esquinas superiores)
# ---------------------------------------------------------------------------
sueltos_spec = [  # (tamaño cm, tipo, posición en la maqueta cm)
    (1.2, "crema", (2.2, 3.0)),
    (2.2, "cielo", (4.3, 2.2)),
    (1.45, "colinas", (2.9, 5.8)),
    (2.0, "colinas", (25.0, 1.2)),
    (1.8, "crema", (23.4, 3.0)),
    (1.25, "cielo", (25.5, 6.6)),
]
P["sueltos"] = []
for i, (s, kind, pos) in enumerate(sueltos_spec):
    n = cm(s)
    t = np.ones((n, n, 3), np.float32) * CREAM if kind == "crema" else retazo(n, n, kind)
    t *= grain(n, n, 0.02)[..., None]
    P["sueltos"].append((save(f"05_cuadro_{i + 1}_{s}cm", t, np.ones((n, n))), pos))

# ---------------------------------------------------------------------------
# 5. Maqueta sobre la hoja lila (solo referencia)
# ---------------------------------------------------------------------------
page = Image.new("RGBA", (PAGE_W, PAGE_H), LILA + (255,))
def place(im, x, y):
    page.alpha_composite(im, (int(x), int(y)))
band_y = cm(11.9)
dl, dr = P["damero_izq"], P["damero_der"]
px, py = (PAGE_W - PW) // 2, (PAGE_H - PH) // 2 + cm(0.2)
place(dl, px + cm(0.8) - dl.width, band_y)
place(dr, px + PW - cm(0.8), band_y)
place(P["postal"], px, py)
place(P["estampilla"], WIN_X - (SW - WIN_W) // 2, WIN_Y - (SH - WIN_H) // 2)
for im, (x, y) in P["sueltos"]:
    place(im, cm(x), cm(y))
dd = ImageDraw.Draw(page)
dd.rectangle([WIN_X, WIN_Y, WIN_X + WIN_W, WIN_Y + WIN_H], fill=(178, 178, 178, 255))
mock = page.convert("RGB")
mock.save(f"{OUT}/maqueta_hoja_lila.jpg", quality=90)

guarda = Image.open("output/paisaje/carta_1_izquierda_300dpi.png").convert("RGB").rotate(90, expand=True)
spread = Image.new("RGB", (PAGE_W * 2 + cm(0.3), PAGE_H), (60, 60, 60))
spread.paste(guarda.resize((PAGE_W, PAGE_H)), (0, 0))
spread.paste(mock, (PAGE_W + cm(0.3), 0))
spread.resize((spread.width // 3, spread.height // 3), Image.LANCZOS).save(f"{OUT}/maqueta_libro_abierto.jpg", quality=88)

# ---------------------------------------------------------------------------
# 6. Hoja para imprimir y recortar (carta horizontal, fondo blanco)
# ---------------------------------------------------------------------------
sheet = Image.new("RGBA", (PAGE_W, PAGE_H), (255, 255, 255, 255))
layout = [(P["postal"], (0.8, 0.8)), (P["estampilla"], (11.0, 0.8)),
          (dl, (19.4, 0.8)), (dr, (11.0, 12.6))]
rows = [(19.4, 8.2), (19.4, 10.9)]
for i, (im, _) in enumerate(P["sueltos"]):
    x, y = rows[i // 3]
    layout.append((im, (x, y)))
    rows[i // 3] = (x + im.width / PX_CM + 0.5, y)
from scipy.ndimage import binary_dilation
for im, (x, y) in layout:
    sheet.alpha_composite(im, (cm(x), cm(y)))
    # línea de corte gris muy fina (solo en la hoja de impresión)
    a_ = np.asarray(im.getchannel("A")) > 127
    edge = binary_dilation(a_, iterations=2) & ~a_
    ov = np.zeros((*a_.shape, 4), np.uint8)
    ov[edge] = (170, 170, 170, 255)
    pad = Image.new("RGBA", (im.width + 4, im.height + 4), (0, 0, 0, 0))
    big = np.zeros((im.height + 4, im.width + 4), bool)
    big[2:-2, 2:-2] = a_
    e2 = binary_dilation(big, iterations=2) & ~big
    o2 = np.zeros((*big.shape, 4), np.uint8); o2[e2] = (170, 170, 170, 255)
    sheet.alpha_composite(Image.fromarray(o2, "RGBA"), (cm(x) - 2, cm(y) - 2))
sheet = sheet.convert("RGB")
sheet.save(f"{OUT}/imprimir_carta_horizontal.png", dpi=(DPI, DPI))
sheet.save(f"{OUT}/imprimir_carta_horizontal.pdf", resolution=DPI)
print("ok", {k: (v.size if hasattr(v, "size") else len(v)) for k, v in P.items()})
