# MI-BIG — estado exacto (23 nov 2026, desk)

Raíz: `C:\Users\pilia\Desktop\MI-BIG`. Servidor central: `C:\JarvisLocal\core\servidor_central.py:app`. Usuario: «deja opencode quieto» y « dale con todo ».

## Listo y verificado
- Ollama 0.40.17 con RTX 3060 12 GB por CUDA v13; arranque con `OLLAMA_VULKAN=0`. Autoarranque por Startup `MI-BIG-Ollama.cmd` → `datos\iniciar_ollama.ps1`.
- Perfil único: `mi-big` → `ollama/mi-big-agente` (central, `Modelfile_full`, `qwen2.5-coder:14b`, `num_ctx 8192`, `tool_call:true`, `tools:{"*":true}`); `mi-big` (charla) y `mi-big-opencode` derivados. Todos llevan `MODO SIN LÍMITES`. `Modelfile_rapido` quedó obsoleto.
- `core/agente.py`: inyecta `SIN_LIMITES` en `system_prompt()` y convierte frases tipo `Uso herramienta(...)` en bloques `<<HERRAMIENTA>>` reales; `num_predict=512`.
- Servidor central en 8000: `/api/estado` 200. Panel `http://127.0.0.1:8090` root 200. Proxy Ollama en 11436; Tailscale `/ollama` → 11436, `/chat` → 8090.
- PRUEBA REAL 23 nov: `/api/orden` con `{"mensaje":"Abre YouTube y reproduce lo que sea como prueba","dispositivo":"prueba"}` → «Reproduciendo música en el navegador predeterminado.» Quedó abierta ventana Edge «Mix Música Variada 2026 ... - YouTube - Personal: Microsoft Edge». El campo correcto es `mensaje`, NO `prompt`.
- YouTube/WhatsApp SIEMPRE con Edge o navegador default; nunca Chromium/Playwright visible.
- PUENTE RÁPIDO TUF: desde TUF no usar opencode para MI-BIG (4 procesos colgados). Usar `MI-BIG "texto"` o `MI-BIG --chat "texto"`: `C:\JarvisLocal\MI-BIG.cmd` → `mi_big.py` → `https://egnisyaxel-esc.tailce5f03.ts.net/api/orden` con `X-API-Key` de `C:\JarvisLocal\.env`. Tailscale tailnet-only, sin key da 401. Ruta TUF→desk 58 ms; respuesta real 2.9-4.6 s. `C:\JarvisLocal` agregado al PATH de usuario en TUF. Acciones se ejecutan en desk; para TUF usar `/api/tuf`. No matar opencode.
- Tools full cableados: ofimática (`crear_documento`, `leer_documento`), web/apps (`crear_pagina_web`, `crear_app_python`, `crear_proyecto`), Blender (`blender_primitiva`, `blender_render`, `blender_script`), red (`estado_red`, `monitorear_red`, `dispositivos_red`, `diagnostico_red`, `cambiar_password_wifi`, `resolver_host`), WhatsApp (`whatsapp_enviar`, `whatsapp_estado`), poder (`abrir_app`, `reproducir_youtube`, `control_ventanas`, `enviar_teclas`), media (`generar_imagen`, `generar_video`), TUF y opencode.
- Ofimática verificada: `salida_ofimatica\Prueba_MI-BIG.docx`, `Prueba.xlsx`, `Prueba.pptx`, `Prueba.pdf`. Web verificada en `proyectos\prueba_web`.
- Blender: no está en desk; `core/blender.py` detecta ausencia y ejecuta en TUF por SSH con `asus_ed25519`. Verificado `C:\Users\pilia\AppData\Local\Temp\opencode\prueba_cubo.blend`.
- ComfyUI integrado en `C:\JarvisLocal\core\generador_media.py` + shim en desk; endpoints `/api/imagen`, `/api/video` y `/media` funcionan, pero `C:\ComfyUI` NO existe.
- Dataset `entrenamiento/dataset_heredado.jsonl` = 168 ejemplos. Chroma `memoria/chroma_db` = 775 recuerdos (62 respuestas «Uso ...» borradas, 14 ejemplos de acción real metidos).
- Memoria unificada: `C:\JarvisLocal\memoria\estado_global.db`. Se borraron las respuestas malas de YouTube del historial global.
- Scripts nuevos: `entrenamiento/ampliar_dataset_full.py`, `ampliar_dataset_total.py`, `corregir_memoria_acciones.py`, `memorizar_dataset.py`, `limpiar_memoria_accion.py` en Temp.

## Detenido / trampas
- Entrenamiento WSL 14B y 7B DETENIDO: RAM cayó a 1.4 GB libres. `wsl --shutdown` devolvió 9.5 GB libres. NO reanudar pesado; si se reintenta, solo 7B/4-bit con `--max-seq 1024` y monitorizando RAM.
- `entrenamiento/entrenar.py` soporta `MI_BIG_BASE` y `MI_BIG_MODELO_ENTRENADO`, pero la corrida ligera no se terminó.
- Opencode se usa rápido y full otra vez: config con `ollama/mi-big-agente`, proxy 11436 convierte a `tool_call`; reiniciar sesión al cambiar config. No matar procesos opencode.
- Regla firewall `Mi-Big Red Privada` pendiente; helper `C:\JarvisLocal\datos\firewall_admin.cmd` (acceso denegado sin elevación).
- WhatsApp Web necesita QR la primera vez en `C:\JarvisLocal\perfil_whatsapp_edge`.
- Para ComfyUI real: instalar/arrancar `C:\ComfyUI\run_nvidia_gpu.bat`.

## Verificación rápida
1. `curl.exe -s -o NUL -w "%{http_code}" -H "X-API-Key: ..." http://127.0.0.1:8000/api/estado` → 200.
2. `curl.exe -s -H "X-API-Key: ..." -H "Content-Type: application/json" --data-binary "@Temp\opencode\prueba_orden.json" http://127.0.0.1:8000/api/orden` → «Reproduciendo música en el navegador predeterminado.».
3. `core.poder.control_ventanas('listar')` debe mostrar la ventana de YouTube en Microsoft Edge.

## Optimización y autoaprendizaje (23 nov, tarde)
- Variables máquina Ollama definitivas: `OLLAMA_HOST=0.0.0.0:11434`, `OLLAMA_KEEP_ALIVE=5m`, `OLLAMA_VULKAN=0`, `OLLAMA_MAX_LOADED_MODELS=1`. `OLLAMA_FLASH_ATTENTION` y `OLLAMA_KV_CACHE_TYPE` ELIMINADOS (causaban lentitud/hang en `/api/chat`). Ollama PID 17144 intacto en el reinicio de FastAPI.
- `Modelfile` con `num_ctx 10240`, `num_gpu 99`, temp `0.25`, top_p `0.85`, repeat `1.08`, `<thinking>` oculto y respuesta al putazo. Modelos recreados: `mi-big`, `mi-big-agente`, `mi-big-opencode`.
- Streaming real: `/api/chat/stream` (SSE), `Agente.stream()`, voz por frases en `core/voz_mi_big.py` (`?voz=true`). Panel ya consume streaming.
- Autoaprendizaje: `C:\JarvisLocal\core\destilador_maestro.py` cableado en `agente.py`; simulación guardó 1 ejemplo en `dataset_continuo.jsonl` + 1 fragmento en Chroma. Tarea real `MiBig_Entrenamiento_Nocturno`, diaria 03:00, ejecuta `entrenar_nocturno.py` leyendo `Modelfile_full` + `dataset_continuo.jsonl` (43 ejemplos vivos). `configurar_autoentrenamiento.bat` es solo generador.
- Benchmark real: TTFT frío `0.776 s`, `27.0 tok/s` (88 tokens); TTFT caliente `0.09 s`, `51.7 tok/s` (2 tokens); `ollama ps` → `mi-big 9.8 GB 100% GPU context 10240 Forever`.

## Alineación final (23 nov, noche — estado definitivo)
- FastAPI: `core/cerebro_autonomo.py` envía `num_ctx 8192` en `/api/chat`, igual que `Modelfile_full` y `vision_mi_big.py`.
- Cola: `BLOQUEO_AGENTE` es el registro de locks por dispositivo; `_adquirir_agente` usa `asyncio.wait_for(lock.acquire(), timeout=45.0)`. `TIEMPO_MAXIMO=100.0` evita que la cola dispare HTTP 504 en el middleware.
- Servicio: `uvicorn core.servidor_central:app --host 0.0.0.0 --port 8000 --workers 1` relanzado; `/health` 200 en local y `http://100.109.96.83:8000/health`. `ollama.exe` NO se tocó (PID 17144).
- Watchdog 24/7: `C:\JarvisLocal\watchdog_mibig.ps1` activo, registrado como tarea `MI-BIG Watchdog` (AtLogOn, Highest, Running); revisa `:11434/api/tags` y `:8000/health` cada 10 s y relanza tras 2 fallos. Log: `C:\JarvisLocal\datos\watchdog.log`.
- Memoria: estado definitivo también en `C:\Users\pilia\.config\opencode\AGENTS.md` §17.

