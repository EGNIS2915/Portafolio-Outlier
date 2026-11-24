# MI-BIG — arquitectura y operación

Asistente agéntico 100 % local en desk (i9-10900K, RTX 3060 12 GB). Sin API de pago. Modelo principal `mi-big` (base `qwen2.5-coder:14b`), visión `qwen2.5vl:7b`, embeddings `nomic-embed-text`.

## Estructura

- `core/config.py`: rutas, modelo, VRAM, redacción de secretos, flag `CONFIRMAR_COMANDOS = False`.
- `core/agente.py`: bucle agéntico, protocolo `<<HERRAMIENTA>>` / `<<FINAL>>`, compactación de contexto.
- `core/herramientas.py`: archivos, terminal, memoria, sentidos y web; respaldo automático antes de editar.
- `core/sentidos.py`: imagen, pantalla (mss) y video (fotogramas cada 3 s + Whisper int8).
- `core/navegador.py`: lectura DOM, ejecución de JS con captura y búsqueda DuckDuckGo.
- `memoria/rag_engine.py`: Chroma persistente + embeddings Ollama; `guardar_recuerdo` / `buscar_recuerdo`.
- `entrenamiento/extraer_historial.py`: herencia de sesiones OpenCode + ADN operativo → `dataset_heredado.jsonl`.
- `entrenamiento/entrenar.py`: QLoRA 4-bit con Unsloth → GGUF Q4_K_M → `ollama create mi-big`.
- `modelos/Modelfile`: `num_ctx 16384`, `temperature 0.2`, SYSTEM con la metodología de ingeniería.
- `datos/`: logs, capturas, respaldos y dataset de memoria.

## Arranque

Doble clic en `iniciar_jarvis.bat`: arranca Ollama si hace falta, crea `mi-big` y abre la consola.
Comandos dentro de la consola: `/salir`, `/limpiar`, `/aprender [nota]`, `/memoria [texto]`, `/estado`, `/modelo [nombre]`.

Ejecución puntual:

```bat
.venv\Scripts\python.exe core\agente.py "revisa el estado del proyecto y resume los pendientes"
```

## Memoria y herencia

```bat
.venv\Scripts\python.exe entrenamiento\extraer_historial.py
.venv\Scripts\python.exe memoria\rag_engine.py indexar
.venv\Scripts\python.exe memoria\rag_engine.py adn
.venv\Scripts\python.exe memoria\rag_engine.py stats
```

El extractor lee `~/.local/share/opencode`, `%APPDATA%\opencode`, `%LOCALAPPDATA%\opencode` y `~/.config/opencode` (JSON/JSONL y SQLite), redacta PAT/llaves y guarda pares usuario-asistente en formato ShareGPT. El ADN son reglas de metodología, herramientas, seguridad y estilo.

## Entrenamiento continuo

Cada tarea exitosa se guarda con `/aprender` (o llamando a la herramienta `aprender`). Para reentrenar:

1. En WSL2 con CUDA (Unsloth no corre en Windows nativo): `pip install unsloth trl transformers datasets accelerate bitsandbytes`
2. `python entrenamiento/entrenar.py --solo-preparar` revisa el dataset y escribe `datos/plan_entrenamiento.json`.
3. `python entrenamiento/entrenar.py` entrena QLoRA (batch 1, accum 4, 4-bit), exporta GGUF Q4_K_M y actualiza `mi-big`.

## VRAM y contexto

- `num_ctx` fijo en 16384; el agente compacta mensajes antiguos y trunca salidas largas de terminal.
- Visión usa `keep_alive: "15s"` y se descarga tras cada consulta; el modelo 14B se mantiene en `30m`.
- `OLLAMA_VULKAN=0` es obligatorio en esta máquina: con Vulkan activo Ollama ignora la RTX 3060 y corre en CPU.

## Verificación rápida

```bat
ollama list
curl http://localhost:11434/api/tags
.venv\Scripts\python.exe -m compileall -q core memoria entrenamiento
```
