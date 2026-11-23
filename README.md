# sq

Ilustración panorámica para el interior de una caja: **Parte 1 + Lomo + Parte 2**.
Lienzo de 58,5 × 35,1 cm (incluye 0,5 cm de sangrado por lado), 300 dpi.

| Sección | Ancho | Contenido |
|---|---|---|
| Parte 1 | 27,8 cm | 29 (2 arriba, 9 abajo) construido con retícula de cuadrados que muestran fragmentos del paisaje y se dispersan progresivamente; el paisaje entra por la derecha con borde escalonado |
| Lomo | 3 cm | continuación del paisaje |
| Parte 2 | 27,7 cm | paisaje con recortes cuadrados blancos (mismo blanco del fondo) concentrados en el centro |

## Archivos

- `generar.py`: genera la composición (`pip install numpy pillow scipy && python3 generar.py`).
- `assets/paisaje.jpg`: fotografía base. `assets/boceto_29.jpg`: boceto del 29.
- `output/sq_caja_58.5x35.1cm_300dpi.png` / `.pdf`: archivo para imprimir (RGB).
- `output/preview.jpg`: vista previa. `output/preview_guias.jpg`: con sangrado (rojo) y pliegues (azul); no se imprime.
- `PROMPT_generador.md`: prompt para pasar la composición por un generador de imágenes.
