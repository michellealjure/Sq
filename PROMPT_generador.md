# Prompt para generador de imágenes — SQ

Usar **`output/preview.jpg`** (o el PNG a 300 dpi) como **imagen de referencia / estructura** (image-to-image, "structure reference" o "composition reference"), con una fuerza de referencia alta (≈ 0,6–0,8) para que se conserven el 29, la retícula y los recortes.

Formato: horizontal, proporción **58,5 : 35,1 (≈ 5:3)**. Si el generador no acepta esa proporción, usar 16:9 o 3:2 y recortar después, o reescalar el resultado sobre el lienzo de `generar.py`.

---

## Prompt (inglés — suele funcionar mejor en los generadores)

> Editorial panoramic illustration, horizontal 5:3, printed on textured off-white paper. Keep the exact composition of the reference image.
>
> LEFT THIRD: pure white paper background. A large number "29" stacked vertically (the "2" on top, the "9" below), built ONLY from a strict grid of square modules — no typeface. The squares that form the 2 and the 9 are big and almost touching; each square is a small window showing a fragment of a green mountain landscape. Around the number, the grid of squares dissolves progressively: medium squares next to the digits, then smaller ones, then tiny square specks scattered on the white paper. On the right edge of this area the landscape enters the white page through a stepped, pixel-like edge of squares.
>
> CENTER STRIP AND RIGHT HALF: one continuous mountain valley landscape — layered blue-green mountain ranges, rolling green hills, a valley with small red-roofed houses and red dirt paths, a lone pine tree, a wide cloudy sky. Rendered as a hand-printed stippled illustration: fine visible grain, colour built from tiny dots and marks, simplified organic shapes, risograph / screen-print texture, palette of greens, blues, soft yellows with small warm red-ochre accents. Not photographic, no smooth digital gradients, no clean vector look.
>
> Over the landscape, concentrated in the middle of the right half, white and cream SQUARE cut-outs of varied sizes (small and medium), randomly but evenly balanced, crisp straight edges with a very subtle inner shadow, like holes punched out of the paper. The landscape stays visible around them.
>
> Geometric square system + organic nature. Contemporary, editorial, artisanal. No text, no letters other than the 29, no circles, no dots as shapes, no round forms in the modules.

**Negative prompt:**
> circles, round dots, ovals, rounded shapes, typography, letters, words, text, watermark, signature, photorealistic, 3D render, smooth gradients, glossy, vector flat clean, black squares, frame, border

---

## Prompt (español)

> Ilustración panorámica editorial, horizontal 5:3, impresa sobre papel blanco con textura. Mantener exactamente la composición de la imagen de referencia.
>
> TERCIO IZQUIERDO: fondo de papel blanco. Un número "29" grande, apilado en vertical (el "2" arriba, el "9" abajo), construido SOLO con una retícula estricta de módulos cuadrados, sin tipografía. Los cuadrados que forman el 2 y el 9 son grandes y casi se tocan; cada cuadrado es una ventana que muestra un fragmento de un paisaje de montañas verdes. Alrededor del número la retícula se disuelve progresivamente: cuadrados medianos junto a los dígitos, luego más pequeños y finalmente diminutos cuadrados dispersos sobre el papel blanco. En el borde derecho de esta zona el paisaje entra en la página blanca con un borde escalonado de cuadrados.
>
> FRANJA CENTRAL Y MITAD DERECHA: un solo paisaje continuo de valle montañoso — cordilleras superpuestas azul-verdosas, colinas verdes, valle con pequeñas casas de techo rojo y caminos de tierra rojiza, un pino solitario, cielo amplio con nubes. Estilo ilustración puntillista impresa a mano: grano fino visible, color construido con pequeños puntos y marcas, formas orgánicas simplificadas, textura tipo risografía / serigrafía, paleta de verdes, azules, amarillos suaves y pequeños acentos cálidos. Nada fotográfico, sin degradados digitales, sin acabado vectorial limpio.
>
> Sobre el paisaje, concentrados en el centro de la mitad derecha, recortes CUADRADOS blancos y crema de tamaños variados (pequeños y medianos), distribución aleatoria pero equilibrada, bordes rectos y nítidos con una sombra interior muy sutil, como perforaciones en el papel.
>
> Sin texto, sin letras aparte del 29, sin círculos.

---

## Recomendaciones

- [No Verificado] El comportamiento depende de cada generador. En general, los generadores tienden a "redondear" módulos o inventar texto; por eso el negative prompt insiste en *circles* y *text*.
- Pedir resolución máxima y, si es necesario, ampliar (upscale) a 6909 × 4146 px (58,5 × 35,1 cm a 300 dpi).
- Revisar que los pliegues queden en **27,8 cm** y **30,8 cm** desde la izquierda (ver `output/preview_guias.jpg`) y que nada importante quede en los 0,5 cm exteriores.
