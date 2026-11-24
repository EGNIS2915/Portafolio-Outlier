# 05 — NEXA / SIE_MOV

## Qué es

Una app Android para organizar el semestre. Materias, horario, tareas, notas, archivos, evaluaciones, temas, promedios, plan de estudio y sueño. Paquete `com.tesh.sie`. No es un mockup de Figma: hay APK instalable de 23,882,565 bytes con SHA-256 documentado.

## Qué le metí

- Persistencia local para perfil, materias y horario. La app funciona sin internet para lo básico.
- CRUD de materias con **borrado en cascada**. Si borras una materia, se van sus tareas, notas, evaluaciones, temas, archivos y clases del horario. No dejo basura colgando.
- Horario editable lunes a sábado, con alta, edición y borrado de clases.
- Sincronización por **código de grupo** con Firestore.
- Notificaciones de tareas y exámenes. El permiso se pide durante la instalación, no escondido.
- Datos de ejemplo de 5.º ISC removibles con un toque. La app sirve para cualquier carrera.
- Tema visual galaxia y navegación reorganizada.

El APK beta es debug, versión `1.0`. Después salieron builds `v1.0.1-rc1`, `v1.0.2-ui`, `v1.0.3-fix` y `v1.0.4-full`. Cada nombre viene de una corrección real, no de marketing.

## Lo que le quité a propósito

El chatbot NEXA IA quedó deshabilitado en esta build. La demo dependía de un servidor y no quería que la exposición se cayera por una llamada fallida. La app lo dice en el manual: “El chatbot no está en esta build para no depender del servidor durante la demo.”

También está claro que la sincronización necesita internet y que, si falla, la app lo reporta en vez de quedarse callada. Es una beta debug, no una versión firmada para tienda. Eso va escrito en la documentación que entregué.

## Cómo se prueba

El manual trae un recorrido de 3–5 minutos:

1. Inicio con resumen del día.
2. Chip de perfil: carrera, grupo y semestre.
3. Campana: notificación de prueba.
4. Materias: crear, editar, borrar y recorrer Tareas/Notas/Archivos/Eval/Temas.
5. Horario: cambiar de día y abrir una clase.
6. Tareas, notas, datos, sincronización, plan de estudio, sueño y promedios.

También hay `.bat` para instalar el APK en el emulador de Android Studio y comando directo: `adb install -r NEXA_Beta_5NOV.apk`.

## Lo que hay aquí

- `03_Evidencia/NEXA/NEXA_Beta_5NOV.apk`
- `03_Evidencia/NEXA/NEXA_Manual_Tecnico.pdf`
- `03_Evidencia/NEXA/NEXA_Manual_Tecnico.docx`
- `03_Evidencia/NEXA/NEXA_Entrega_Scrum_20261119.rar`
- `03_Evidencia/NEXA/COMO_INSTALAR_Y_PROBAR_NEXA.txt`
- `03_Evidencia/NEXA/NEXA_v1.0.4-full-debug.apk`

Hash del beta: `39D11242F9AE671B7B8ED93A71AD61D79B54D07ABEFF4F8616E68AFBB6371009`.

Beta sí, invento no. Se instala, se navega y se explica. Se me hizo divertido arreglar lo que salía mal.
