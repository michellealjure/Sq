# sq

Ilustración panorámica para el interior de una caja: **Parte 1 + Lomo + Parte 2**.
Lienzo de 56,7 × 35,1 cm (incluye 0,5 cm de sangrado por lado; guías del montaje en `TRIM_*` de `generar.py`), 300 dpi.

| Sección | Ancho | Contenido |
|---|---|---|
| Parte 1 | 27,8 cm | 29 (2 arriba, 9 abajo) construido con retícula de cuadrados que muestran fragmentos del paisaje y se dispersan progresivamente; el paisaje entra por la derecha con borde escalonado |
| Lomo | 3 cm | continuación de la imagen |
| Parte 2 | 27,7 cm | imagen (copas de árboles) con recortes cuadrados blancos (mismo blanco del fondo) concentrados en el centro |

## Versiones

Las dos comparten exactamente la misma distribución del 29, la dispersión, los huecos y los recortes.

| Carpeta | Imagen | Estilo |
|---|---|---|
| `output/arboles/` | `assets/arboles.jpg` (copa de árboles) | foto en alta resolución |
| `output/paisaje/` | `assets/paisaje.jpg` (valle) | ilustración puntillista con grano de papel; en el PNG también los puntos blancos del puntillismo son transparentes |

En cada carpeta:
- `sq_caja_56.7x35.1cm_300dpi.png`: PNG RGBA a 300 dpi, los espacios blancos son transparentes.
- `sq_caja_56.7x35.1cm_300dpi_fondo_blanco.pdf`: la misma composición sobre blanco.
- Solo en `output/paisaje/`: `carta_1_izquierda_300dpi.png/.pdf` (13,52–35,11 cm) y `carta_2_derecha_300dpi.png/.pdf` (35,11–56,70 cm), desde arriba, tamaño carta (21,59 × 27,94 cm, 2550 × 3300 px) con la ilustración completa: sin 29, sin recortes, sin blancos.
- `preview.jpg`, `preview_guias.jpg` (guías rosadas del montaje; no se imprime).

## Archivos

- `generar.py`: `pip install numpy pillow scipy`, luego `python3 generar.py` (ambas), `python3 generar.py arboles` o `python3 generar.py paisaje`.
- `assets/rng_layout.json`: fija la distribución aprobada.
- `assets/recortes_parte2.json`: posiciones aprobadas de los recortes de la Parte 2.
- `assets/boceto_29.jpg`: boceto del 29.
- `PROMPT_generador.md`: prompt para pasar la composición por un generador de imágenes.

## Primera hoja (piezas para pegar sobre la hoja lila)

`python3 primera_hoja.py` (después de `python3 generar.py paisaje`). Salida en `output/primera_hoja/`:

- `piezas/`: PNG sueltos con fondo transparente, tamaño real a 300 dpi: fondo de postal (8,6 × 13,2 cm, para la foto de 6,7 × 10 cm), nube, mosaico tejido, 12 cuadros sueltos y franja de montañas en serigrafía.
- `imprimir_hoja_1` / `imprimir_hoja_2` (.png y .pdf): todas las piezas acomodadas en carta horizontal para imprimir y recortar.
- `maqueta_hoja_lila.jpg`, `maqueta_libro_abierto.jpg`: propuesta de composición (solo referencia).
