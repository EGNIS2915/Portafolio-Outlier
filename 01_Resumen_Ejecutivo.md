# Resumen, sin tanto cuento

**Egnis Yaxel Piliado**  
Computer Systems Engineer & AI Automation Developer  
Huixquilucan, Estado de México · piliadoegnis@gmail.com · +52 720 258 9604

**No se espanten: sabe y le gusta.**

Estudiante de ingeniería en sistemas, TESH. Trabajo con Python, SQL, Rust y herramientas de bajo nivel. Lo que sigue no es una lista de “tecnologías que conozco”: son cosas que hice y que puedo abrir en una máquina.

## Los cinco

1. **MI-BIG / JarvisLocal.** Agente local con Qwen2.5-Coder 14B, FastAPI y un proxy en `:11436` que intercepta SSE y convierte respuestas en `tool_calls`. Le metí QLoRA en WSL2, RAG con Chroma, watchdog y automatización de Windows/Blender. Es el proyecto más completo y el que más peleé.

2. **UNIVERSIDAD / TECNO_BYTE.** Dos esquemas en MySQL. Normalicé hasta 3FN, puse JOIN, vistas, procedures, triggers, GRANT/REVOKE y transacciones con COMMIT/ROLLBACK. No tengo el dump a la mano; eso lo digo en la ficha.

3. **Solana Engineering Track EDOMEX.** Rust y contratos inteligentes. Hice pruebas unitarias y manejo de instrucciones con Solana CLI. El código no quedó en esta laptop; la certificación sí está en el CV.

4. **Gráficas y lógica digital.** Octave para transformaciones 2D/3D y WinCUPL/Proteus para llevar una ecuación a un P22V10. Aquí sí hay archivos: `.m`, `.pld`, `.jed` y `.pdsprj` reales.

5. **NEXA / SIE_MOV.** App Android con Firestore, notificaciones y borrado en cascada. Hay APK beta de 23 MB y manual técnico con hash. El chatbot lo desactivé para la demo; no quería que la exposición dependiera de un servidor.

## Números que medí en MI-BIG

- `4/4` en el test de salud.
- `61.6 tok/s` en la última corrida. La primera vez, frío, fueron `27.0 tok/s` con TTFT de `0.776 s`. No es lo mismo y no lo disfrazo.
- `100% GPU` con `OLLAMA_VULKAN=0`. Con Vulkan activo se iba a CPU y corría como carreta.
- `8.37 GB` el GGUF `Q4_K_M`.
- `217` ejemplos en el dataset, `158` ya metidos en el ciclo de entrenamiento. Los otros `59` quedaron pendientes porque detuve la corrida a petición del usuario antes de que terminara.

## Stack que realmente toqué

Python · FastAPI · Ollama · Qwen2.5-Coder · QLoRA/Unsloth · WSL2/CUDA · MySQL · Rust/Solana · GNU Octave · WinCUPL/Proteus · Android/Firestore · Blender `bpy` · Windows automation
