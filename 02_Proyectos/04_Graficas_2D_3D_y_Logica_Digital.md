# 04 — Octave y lógica digital

Este proyecto tiene dos partes que no parecen pero se parecen: en las dos estoy describiendo algo con números y reglas, y esperando que la máquina lo dibuje o lo ejecute.

## Parte A — Gráficas en GNU Octave

Aquí hice algoritmos de transformación 2D/3D: traslación, escalamiento, rotación y reflexión sobre figuras base. La idea era no depender de una librería que ya dibujara por mí.

Los scripts `.m` construyen las figuras con coordenadas. Por ejemplo, `casa.m` son 15 líneas: cuatro arreglos `x/y` y un `plot`. No es nada elegante, pero funciona y se entiende. En el examen completo hay decenas de `patch`, `view(-37.5, 30)` y `axis square` para cerrar la proyección 3D.

Lo que hay en la carpeta:

- `casa.m`, `Cuadrado.m`, `Octagono.m`, `Tronco_Piramide_Rectangular.m`
- `Buitre.m`, `Delfin.m`, `gallito.m`, `PatoR.m`
- `Examen_completo.m`, `Examen_corregido.m`

`Examen_corregido.m` existe porque la primera versión traía typos. Eso también es parte del trabajo.

## Parte B — WinCUPL y Proteus

Acá sí se siente el hardware. Escribí ecuaciones en WinCUPL y las sinteticé a un **P22V10**. El caso más claro es arranque y paro de motor:

```cupl
MOTOR = (A # MOTOR) & !B;
MOTOR_OFF = !MOTOR;
```

Eso es un latch: `A` arranca, `B` para y el estado se mantiene por realimentación. `MOTOR_OFF` es la salida complementaria. El archivo `Arran_paro.pld` dice `Designer Piliado`, `Company TESH`, fecha `08/10/26` y `Device P22V10`. No es un ejemplo copiado de internet.

De ahí salen:

- `.pld` — fuente CUPL.
- `.jed` — mapa de fusibles ya sintetizado.
- `.pdsprj` — proyectos de simulación en Proteus: compuertas, contadores, verificación y prácticas.

## Por qué me gusta este proyecto

Porque pasa de la ecuación al archivo que un dispositivo físico puede consumir. No es “dibujar un cuadrado en Octave” ni “prender un LED en Proteus”. Es entender qué significa que una expresión booleana se convierta en fusibles.

Si me preguntan por el orden de una matriz de transformación o por qué el latch mantiene estado sin un flip-flop explícito, respondo sin buscar apuntes.

De la ecuación al fusible, sin intermediarios. Se siente raro verlo funcionar la primera vez.
