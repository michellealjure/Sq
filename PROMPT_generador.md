# Prompt para generador de imágenes — SQ

Usar **`output/preview.jpg`** (o el PNG a 300 dpi) como **imagen de referencia / estructura** (image-to-image, "structure reference" o "composition reference"), con una fuerza de referencia alta (≈ 0,6–0,8) para que se conserven el 29, la retícula y los recortes.

Formato: horizontal, proporción **58,5 : 35,1 (≈ 5:3)**. Si el generador no acepta esa proporción, usar 16:9 o 3:2 y recortar después, o reescalar el resultado sobre el lienzo de `generar.py`.

---

## Prompt (inglés — suele funcionar mejor en los generadores)

> Editorial panoramic illustration, horizontal 5:3, printed on textured off-white paper. Keep the exact composition of the reference image.
>
> LEFT THIRD: pure white paper background. A large number "29" stacked vertically (the "2" on top, the "9" below), built ONLY from a strict grid of square modules — no typeface. The squares that form the 2 and the 9 are big and almost touching; each square is a small window showing a fragment of a tree canopy (leaves, branches, sky). Around the number, the grid of squares dissolves progressively: medium squares next to the digits, then smaller ones, then tiny square specks scattered on the white paper. On the right edge of this area the landscape enters the white page through a stepped, pixel-like edge of squares.
>
> CENTER STRIP AND RIGHT HALF: one continuous photograph-like view looking up into a tree canopy — dark branches crossing the frame, dense green leaves, patches of blue sky and white clouds between the leaves, bright yellow-green bamboo foliage in the lower right corner. High resolution, crisp detail.
>
> Over the landscape, concentrated in the middle of the right half, pure white SQUARE cut-outs (same white as the paper background) of varied sizes (small and medium), randomly but evenly balanced, crisp straight edges, flat, no shadow, no outline, like holes punched out of the paper. The landscape stays visible around them.
>
> Geometric square system + organic nature. Contemporary, editorial, artisanal. No text, no letters other than the 29, no circles, no dots as shapes, no round forms in the modules.

**Negative prompt:**
> circles, round dots, ovals, rounded shapes, typography, letters, words, text, watermark, signature, photorealistic, 3D render, smooth gradients, glossy, vector flat clean, black squares, frame, border

---

## Prompt (español)

> Ilustración panorámica editorial, horizontal 5:3, impresa sobre papel blanco con textura. Mantener exactamente la composición de la imagen de referencia.
>
> TERCIO IZQUIERDO: fondo de papel blanco. Un número "29" grande, apilado en vertical (el "2" arriba, el "9" abajo), construido SOLO con una retícula estricta de módulos cuadrados, sin tipografía. Los cuadrados que forman el 2 y el 9 son grandes y casi se tocan; cada cuadrado es una ventana que muestra un fragmento de un la copa de los árboles (hojas, ramas, cielo). Alrededor del número la retícula se disuelve progresivamente: cuadrados medianos junto a los dígitos, luego más pequeños y finalmente diminutos cuadrados dispersos sobre el papel blanco. En el borde derecho de esta zona el paisaje entra en la página blanca con un borde escalonado de cuadrados.
>
> FRANJA CENTRAL Y MITAD DERECHA: una sola imagen continua mirando hacia arriba, a la copa de los árboles — ramas oscuras que cruzan el encuadre, hojas verdes densas, claros de cielo azul y nubes blancas entre las hojas, follaje de bambú verde-amarillo en la esquina inferior derecha. Alta resolución, detalle nítido.
>
> Sobre el paisaje, concentrados en el centro de la mitad derecha, recortes CUADRADOS blancos (el mismo blanco del fondo) de tamaños variados (pequeños y medianos), distribución aleatoria pero equilibrada, bordes rectos y nítidos, planos, sin sombra ni contorno, como perforaciones en el papel.
>
> Sin texto, sin letras aparte del 29, sin círculos.

---

## Recomendaciones

- [No Verificado] El comportamiento depende de cada generador. En general, los generadores tienden a "redondear" módulos o inventar texto; por eso el negative prompt insiste en *circles* y *text*.
- Pedir resolución máxima y, si es necesario, ampliar (upscale) a 6909 × 4146 px (58,5 × 35,1 cm a 300 dpi).
- Revisar que los pliegues queden en **27,8 cm** y **30,8 cm** desde la izquierda (ver `output/preview_guias.jpg`) y que nada importante quede en los 0,5 cm exteriores.
