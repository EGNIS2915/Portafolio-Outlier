# 03 — Solana / Rust

## Lo que hice

Entré al Solana Engineering Track EDOMEX y trabajé en contratos inteligentes en Rust. No fue cosa de conectar una wallet y ya: estuve en el modelo de cuentas de Solana, en la definición de instrucciones y en la validación de firmantes.

Lo que hice en el track:

- Programs en Rust con instrucciones deterministas.
- Manejo de cuentas: propietario del programa, datos persistentes, rent y límites de espacio.
- Validación de estado antes de ejecutar cada instrucción.
- Pruebas unitarias para revisar la lógica antes de desplegar.
- Solana CLI para correr y comprobar el programa.

## Cómo lo entiendo

Un contrato no es un backend al que le haces fetch. Expone instrucciones y cualquiera puede llamarlas si cumple las reglas. Por eso la validación de cuentas no es un detalle: es la seguridad del programa. Si no revisas quién firma y qué cuenta se pasó, abriste la puerta.

Rust ayuda bastante aquí. El compilador te obliga a declarar tipos y a manejar errores en vez de dejarlos pasar. Se siente más lento al escribir, pero así se evitan bugs que en otro lenguaje aparecen en producción.

## Lo que puedo defender en entrevista

- Diferencia entre cuenta, programa y usuario firmante.
- Por qué una instrucción debe ser predecible o, mejor aún, idempotente.
- Cómo se prueba un programa antes de devnet.
- Por qué importa el compute budget.

## Lo que no meto aquí

El código `.rs` no quedó en esta laptop ni en la TUF cuando armé el portafolio. La certificación sí está en el CV: *Solana Engineering Track EDOMEX — Blockchain & Rust Bootcamp*. Prefiero decir eso a subir un repo prestado para rellenar.

Si alguien quiere ver código, lo reconstruyo y lo muestro. La charla técnica se sostiene igual.

No es solo prender una wallet: aquí se habla de cuentas, firmantes y estado determinista. Se nota cuando algo está mal planteado.
