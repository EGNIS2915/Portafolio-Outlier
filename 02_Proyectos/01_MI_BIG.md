# 01 — MI-BIG / JarvisLocal

## Qué es

Un agente que corre en esta máquina (i9-10900K, RTX 3060 12 GB) sin pagar APIs. Qwen2.5-Coder 14B por Ollama, FastAPI en el centro, un proxy en `:11436` y herramientas que sí se ejecutan en Windows. No es un chatbot con prompts elegantes: abre apps, mueve ventanas, escribe documentos y corre Blender en la TUF por SSH.

## Cómo quedó armado

```text
OpenCode / cliente
        │
        ▼
Proxy Ollama (:11436) ── SSE + guard de tool_calls ──► Ollama (:11434)
        │                                              │
        ▼                                              ▼
FastAPI (:8000)                              mi-big-agente (Q4_K_M)
        │
        ├── Windows: ventanas, teclas, apps
        ├── ofimática: docx / xlsx / pptx / pdf
        ├── web: DOM, búsqueda, navegador default
        ├── red: estado, dispositivos, diagnóstico
        ├── Blender: SSH a TUF con bpy
        ├── memoria: Chroma + RAG
        └── watchdog 24/7 + panel en FastAPI
```

## Lo que hice yo

- Puse el proxy delante de Ollama porque el modelo solo no sabe cuándo una frase es acción y cuándo es saludo. El proxy decide eso.
- Arreglé un bug que me volvió loco: si en el historial había un tool_call con error, el modelo le contestaba “Error corregido: el comando anterior traía Markdown...” a un simple `hola como estas chavo`. Metí la condición `es_saludo or es_capacidad` para que esos casos ignoraran el error viejo. Quedó: `Estoy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?`, cero tool_calls.
- Organicé el entrenamiento continuo: QLoRA 4-bit con Unsloth en WSL2, exportación a GGUF y recreación del modelo con `ollama create`.
- Corregí `ollama create` a la fuerza. El primer script lo mandaba por `cmd.exe /c` con comillas dobles y reventaba. Lo cambié por un helper `a_ruta_wsl()` que pasa la ruta directa `/mnt/.../ollama.exe`. Resultado: `success`.
- Metí smoke tests después de entrenar: throughput `>50 tok/s` y revisión de GPU. Si el modelo se cae a CPU, se nota al toque.
- Implementé generación de imágenes con SDXL-Turbo y un guard que rechaza prompts con Markdown antes de cargar el modelo. Antes se colgaba; ahora sale `PROMPT_INVALIDO=usa una sola frase de objeto/estilo, sin Markdown ni comandos`, RC `2`.
- Dejé Blender fuera de esta máquina y lo llamo por SSH. Aquí no está instalado y no iba a meterlo solo por presumir.

## Lo que se me complicó

- **OOM:** un entrenamiento 14B se comió la RAM hasta dejar 1.4 GB libres. Hice `wsl --shutdown`, recuperé 9.5 GB y bajé el modelo de Ollama antes de volver a intentar.
- **Vulkan:** con `OLLAMA_VULKAN=1`, Ollama ignoraba la RTX 3060 y corría en CPU. Variable a `0` y se acabó el problema.
- **Segunda corrida de entrenamiento:** llegó hasta conversión a GGUF, pero la detuve antes de que terminara porque el usuario necesitaba la máquina para otro trabajo. No actualicé el estado ni el modelo. Los 59 ejemplos nuevos siguen pendientes. No digo que estén entrenados.
- **Panel de monitoreo:** lo escribí y compilé, pero no lo dejé corriendo. El puerto `:8090` ya estaba ocupado por el servidor de entregables de OpenCode; el panel está pensado para `:8091`.

## Números que sí medí

| Prueba | Resultado |
|---|---|
| `test_salud_opencode.py` | `4/4 PASS` |
| Última corrida | `61.6 tok/s`, `100% GPU` |
| Corrida fría anterior | TTFT `0.776 s`, `27.0 tok/s` |
| Corrida caliente anterior | TTFT `0.09 s`, `51.7 tok/s` |
| Modelo | `mi-big-agente`, GGUF `Q4_K_M`, `8.37 GB` |
| Dataset | `217` ejemplos vivos, `158` ya destilados |
| Acción real | `/api/orden` abrió Edge y reprodujo YouTube; `control_ventanas` confirmó la ventana |

## Cómo lo probé

- `test_salud_opencode.py` → 4/4.
- `test_multiturno_proxy.py` → 3/3.
- `test_capacidad.py 'sabes crear  imagenes'` → `TOOL_CALLS=0`, respuesta en `0.02 s`.
- `test_tool_error_guard.py` → simula un error de tool viejo y confirma que no contamina el saludo.
- Prueba real: `/api/orden` con `{"mensaje":"Abre YouTube y reproduce lo que sea como prueba","dispositivo":"prueba"}`. Ojo: el campo es `mensaje`, no `prompt`.

## Lo que tengo aquí

- `03_Evidencia/MI-BIG/README_ARQUITECTURA.md`
- `03_Evidencia/MI-BIG/ESTADO_23NOV.md`
- `03_Evidencia/MI-BIG/proxy_ollama.py`
- `03_Evidencia/MI-BIG/test_salud_opencode.py`
- `03_Evidencia/MI-BIG/panel_monitoreo_mibig.py`
- `03_Evidencia/MI-BIG/Modelfile_entrenado`

No es un demo de escritorio: se le mide el throughput y se le revisa la GPU. Aquí mejor corro el número y lo vemos.
