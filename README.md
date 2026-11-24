# sq

Ilustración panorámica para el interior de una caja: **Parte 1 + Lomo + Parte 2**.
Lienzo de 58,5 × 35,1 cm (incluye 0,5 cm de sangrado por lado), 300 dpi.

| Sección | Ancho | Contenido |
|---|---|---|
| Parte 1 | 27,8 cm | 29 (2 arriba, 9 abajo) construido con retícula de cuadrados que muestran fragmentos del paisaje y se dispersan progresivamente; el paisaje entra por la derecha con borde escalonado |
| Lomo | 3 cm | continuación de la imagen |
| Parte 2 | 27,7 cm | imagen (copas de árboles) con recortes cuadrados blancos (mismo blanco del fondo) concentrados en el centro |

## Archivos

- `generar.py`: genera la composición (`pip install numpy pillow scipy && python3 generar.py`).
- `assets/arboles.jpg`: fotografía actual (copas de árboles). `assets/paisaje.jpg`: fotografía anterior (valle). `assets/boceto_29.jpg`: boceto del 29.
- `assets/rng_layout.json`: fija la distribución aprobada de cuadrados y recortes (cambiar la foto no los mueve).
- En `generar.py`: `SRC` (foto), `STYLE` (`"foto"` alta resolución o `"puntillista"`), `TRANSPARENT` (blancos sin fondo).
- `output/sq_caja_58.5x35.1cm_300dpi.png`: PNG RGBA, los espacios blancos son transparentes.
- `output/sq_caja_58.5x35.1cm_300dpi_fondo_blanco.pdf`: la misma composición sobre blanco.
- `output/preview_transparencia.jpg`: vista con damero para comprobar la transparencia.
- `output/preview.jpg`: vista previa. `output/preview_guias.jpg`: con sangrado (rojo) y pliegues (azul); no se imprime.
- `PROMPT_generador.md`: prompt para pasar la composición por un generador de imágenes.
