from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Panel Monitoreo MI-BIG")

PYTHON = r"C:\Users\pilia\Desktop\MI-BIG\.venv\Scripts\python.exe"
SALUD = r"C:\JarvisLocal\herramientas\test_salud_opencode.py"
PROXY = r"C:\JarvisLocal\core\proxy_ollama.py"
LOG = r"C:\JarvisLocal\datos\proxy_llamadas.log"
DATASET = r"C:\JarvisLocal\entrenamiento\dataset_continuo.jsonl"
ESTADO = r"C:\JarvisLocal\entrenamiento\estado_entrenamiento.json"
GGUF = r"G:\JarvisLocal\modelos\mi-big-entrenado.Q4_K_M.gguf"
MODELFILE = r"G:\JarvisLocal\modelos\Modelfile_entrenado"
AGENTS = r"C:\Users\pilia\.config\opencode\AGENTS.md"


def ejecutar(comando: list[str], timeout: int = 8) -> str:
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return (resultado.stdout or "") + (resultado.stderr or "")
    except Exception as error:
        return f"ERROR: {type(error).__name__}: {error}"


def pid_puerto(puerto: int) -> str:
    salida = ejecutar(["netstat", "-ano", "-p", "TCP"])
    for linea in salida.splitlines():
        partes = linea.split()
        if len(partes) >= 5 and partes[1].endswith(f":{puerto}") and partes[3].upper() == "LISTENING":
            return partes[-1]
    return "-"


def gpu() -> dict:
    salida = ejecutar(
        ["nvidia-smi", "--query-gpu=memory.used,memory.free,utilization.gpu", "--format=csv,noheader,nounits"]
    ).strip().splitlines()
    if not salida or "ERROR" in salida[0]:
        return {"usado": "-", "libre": "-", "carga": "-"}
    partes = [p.strip() for p in salida[0].split(",")]
    return {
        "usado": partes[0] if len(partes) > 0 else "-",
        "libre": partes[1] if len(partes) > 1 else "-",
        "carga": partes[2] if len(partes) > 2 else "-",
    }


def contar_lineas(ruta: str) -> int:
    archivo = Path(ruta)
    if not archivo.exists():
        return 0
    with archivo.open("r", encoding="utf-8", errors="replace") as manejador:
        return sum(1 for linea in manejador if linea.strip())


def hashes_estado() -> int:
    ruta = Path(ESTADO)
    if not ruta.exists():
        return 0
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        return len(datos.get("hashes", []))
    except Exception:
        return 0


def entrenamiento() -> dict:
    salida = ejecutar(
        [
            "wsl", "-d", "MI-BIG-Train", "--", "bash", "-lc",
            "ps -ef | grep -E 'entrenar_qlora_wsl|unsloth_convert|llama-quantize' | grep -v grep | head -6",
        ]
    )
    if "entrenar_qlora_wsl" in salida:
        fase = "QLoRA"
    elif "unsloth_convert" in salida:
        fase = "Convirtiendo a GGUF"
    elif "llama-quantize" in salida:
        fase = "Cuantizando Q4_K_M"
    elif salida.strip():
        fase = "Otra fase"
    else:
        fase = "Detenido"
    return {"fase": fase, "detalle": salida.strip()[:1200]}


def cola_log() -> str:
    archivo = Path(LOG)
    if not archivo.exists():
        return "Sin log todavía."
    with archivo.open("r", encoding="utf-8", errors="replace") as manejador:
        lineas = manejador.read().splitlines()
    return "\n".join(lineas[-14:])


def banderas() -> dict:
    proxy = Path(PROXY).read_text(encoding="utf-8", errors="replace") if Path(PROXY).exists() else ""
    agents = Path(AGENTS).read_text(encoding="utf-8", errors="replace") if Path(AGENTS).exists() else ""
    return {
        "guard_error_tool": "TOOL_ERROR_CORREGIDO" in proxy,
        "guard_saludos": "prefijos_saludo" in proxy,
        "respuesta_capacidad": "respuesta_capacidad" in proxy,
        "modo_maestro": "Modo maestro" in proxy and "Modo maestro" in agents,
        "prompt_markdown_rechazado": "PROMPT_INVALIDO" in Path(r"C:\JarvisLocal\herramientas\generar_imagen.py").read_text(encoding="utf-8", errors="replace"),
    }


@app.get("/", response_class=HTMLResponse)
def indice() -> str:
    return PAGINA


@app.get("/api/estado")
def estado() -> dict:
    total = contar_lineas(DATASET)
    hechos = hashes_estado()
    proxies = pid_puerto(11436)
    ollama = pid_puerto(11434)
    central = pid_puerto(8000)
    tren = entrenamiento()
    salud_ok = proxies != "-" and ollama != "-" and central != "-" and tren["fase"] != "Detenido"
    return {
        "maquina": os.environ.get("COMPUTERNAME", "-"),
        "modelo": "mi-big-agente",
        "proxy_pid": proxies,
        "ollama_pid": ollama,
        "central_pid": central,
        "gpu": gpu(),
        "dataset": total,
        "entrenado": hechos,
        "pendientes": max(0, total - hechos),
        "gguf_gb": round(Path(GGUF).stat().st_size / (1024 ** 3), 2) if Path(GGUF).exists() else 0,
        "modelfile": Path(MODELFILE).exists(),
        "entrenamiento": tren,
        "banderas": banderas(),
        "general": "TODO BIEN" if salud_ok else "REVISAR",
        "log": cola_log(),
    }


@app.post("/api/salud")
def correr_salud() -> dict:
    salida = ejecutar([PYTHON, SALUD], timeout=120)
    return {"salida": salida[-4000:]}


@app.post("/api/recargar")
def recargar() -> dict:
    salida = ejecutar(
        ["cmd.exe", "/c", 'schtasks /end /tn "MI-BIG Watchdog" && schtasks /run /tn "MI-BIG Watchdog"'],
        timeout=30,
    )
    return {"salida": salida[-2000:]}


@app.post("/api/matar_reintentos")
def matar_reintentos() -> dict:
    comando = (
        "$p=@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
        "Where-Object { $_.CommandLine -like '*generar_imagen.py*' } | "
        "Select-Object -ExpandProperty ProcessId); "
        "if($p.Count -gt 0){ Stop-Process -Id $p -Force -ErrorAction SilentlyContinue }; "
        "'MATADOS=' + ($p -join ',')"
    )
    salida = ejecutar(["powershell", "-NoProfile", "-Command", comando], timeout=30)
    return {"salida": salida[-1000:]}


PAGINA = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>MI-BIG / Monitoreo</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#0b0f18;--card:#141b2a;--txt:#e9f2ff;--ok:#2ee6a8;--bad:#ff6b6b;--dim:#8fa7c5;--accent:#5cc8ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:15px system-ui,Segoe UI,Arial;padding:22px}
h1{margin:0 0 4px;font-size:24px}h2{font-size:15px;color:var(--dim);margin:0 0 12px;text-transform:uppercase;letter-spacing:.08em}
.top{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:18px;flex-wrap:wrap}
.badge{padding:9px 14px;border-radius:10px;font-weight:800;background:#123b2f;color:var(--ok)}
.badge.bad{background:#3b1620;color:var(--bad)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.card{background:var(--card);border:1px solid #24304a;border-radius:14px;padding:16px}
.big{font-size:30px;font-weight:800;margin:4px 0}
.ok{color:var(--ok)}.bad{color:var(--bad)}.dim{color:var(--dim)}
button{background:#1d5f8a;color:white;border:0;border-radius:9px;padding:10px 12px;font-weight:700;cursor:pointer;margin:4px 4px 0 0}
button:hover{background:#267bb2}pre{white-space:pre-wrap;word-break:break-word;font-size:12px;color:#bcd4ee;margin:0}
.tag{display:inline-block;background:#1b2740;border:1px solid #304261;border-radius:7px;padding:4px 8px;margin:3px;font-size:12px}
.acc{color:var(--accent)}
</style>
</head>
<body>
<div class="top">
  <div><h1>MI-BIG / Monitoreo real</h1><div class="dim" id="maquina">Cargando...</div></div>
  <div class="badge" id="general">...</div>
</div>
<div class="grid">
  <div class="card"><h2>Modelo</h2><div class="big">mi-big-agente</div><div class="dim">GGUF <span id="gguf">-</span> GB</div><div id="modelfile"></div></div>
  <div class="card"><h2>Servicios</h2><div>Proxy :11436 <b id="proxy"></b></div><div>Ollama :11434 <b id="ollama"></b></div><div>Central :8000 <b id="central"></b></div></div>
  <div class="card"><h2>GPU</h2><div class="big" id="gpufree">-</div><div class="dim">MB libres</div><div>Usados <b id="gpuused">-</b> MB / carga <b id="gpucarga">-</b>%</div></div>
  <div class="card"><h2>Entrenamiento</h2><div class="big" id="fase">-</div><div class="dim" id="pendientes"></div><div id="tren_detalle"></div></div>
  <div class="card"><h2>Dataset</h2><div class="big" id="dataset">-</div><div class="dim">ejemplos totales</div><div>Entrenados <b id="entrenado">-</b></div></div>
  <div class="card"><h2>Guardas activas</h2><div id="banderas"></div></div>
</div>
<div class="card" style="margin-top:14px">
  <h2>Acciones</h2>
  <button onclick="accion('/api/salud','salida')">Correr prueba 4/4</button>
  <button onclick="accion('/api/recargar','salida')">Recargar proxy</button>
  <button onclick="accion('/api/matar_reintentos','salida')">Matar reintentos</button>
  <button onclick="cargar()">Actualizar ahora</button>
  <pre id="accion_salida"></pre>
</div>
<div class="card" style="margin-top:14px"><h2>Últimos mensajes del proxy</h2><pre id="log"></pre></div>
<script>
function estadoColor(v){return v && v!=='-' && v!=='Detenido'}
async function cargar(){
  const r=await fetch('/api/estado'); const d=await r.json();
  document.getElementById('maquina').textContent=d.maquina+' · actualizado '+new Date().toLocaleTimeString();
  const g=document.getElementById('general'); g.textContent=d.general; g.className='badge'+(d.general==='TODO BIEN'?'':' bad');
  document.getElementById('gguf').textContent=d.gguf_gb;
  document.getElementById('modelfile').innerHTML=d.modelfile?'<span class="tag ok">Modelfile listo</span>':'<span class="tag bad">Falta Modelfile</span>';
  for(const k of ['proxy','ollama','central']){const e=document.getElementById(k); e.textContent=d[k+'_pid']; e.className=estadoColor(d[k+'_pid'])?'ok':'bad';}
  document.getElementById('gpufree').textContent=d.gpu.libre;
  document.getElementById('gpuused').textContent=d.gpu.usado;
  document.getElementById('gpucarga').textContent=d.gpu.carga;
  const f=document.getElementById('fase'); f.textContent=d.entrenamiento.fase;
  f.className=d.entrenamiento.fase==='Detenido'?'':'ok';
  document.getElementById('pendientes').textContent=d.pendientes+' ejemplos por entrenar';
  document.getElementById('tren_detalle').textContent=d.entrenamiento.detalle.slice(0,180);
  document.getElementById('dataset').textContent=d.dataset;
  document.getElementById('entrenado').textContent=d.entrenado;
  const b=document.getElementById('banderas'); b.innerHTML='';
  for(const [k,v] of Object.entries(d.banderas)){
    const s=document.createElement('span'); s.className='tag '+(v?'ok':'bad'); s.textContent=(v?'OK · ':'FALTA · ')+k.replaceAll('_',' '); b.appendChild(s);
  }
  document.getElementById('log').textContent=d.log;
}
async function accion(url,clave){
  const out=document.getElementById('accion_'+clave); out.textContent='Ejecutando...';
  const r=await fetch(url,{method:'POST'}); const d=await r.json(); out.textContent=d[clave]||JSON.stringify(d);
}
cargar(); setInterval(cargar,7000);
</script>
</body>
</html>
"""
