"""Verificación integral de OpenCode -> proxy MI-BIG -> Ollama."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time

import requests

URL = "http://127.0.0.1:11436/v1/chat/completions"
OLLAMA = r"C:\Users\pilia\AppData\Local\Programs\Ollama\ollama.exe"
MODELO = "mi-big-agente"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Executes a command",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
            },
        },
    }
]

RESULTADOS: list[tuple[str, bool, str]] = []


def registrar(nombre: str, ok: bool, detalle: str) -> None:
    RESULTADOS.append((nombre, ok, detalle))
    print(f"{'PASS' if ok else 'FAIL'} | {nombre} | {detalle}")


def eventos_sse(respuesta: requests.Response) -> tuple[list[dict], list[str]]:
    lineas = [linea for linea in respuesta.iter_lines(decode_unicode=True) if linea]
    chunks = []
    for linea in lineas:
        if linea.startswith("data:") and "{" in linea:
            try:
                chunks.append(json.loads(linea[5:].strip()))
            except ValueError:
                pass
    return chunks, lineas


def delta_de(chunk: dict) -> dict:
    return ((chunk.get("choices") or [{}])[0].get("delta") or {})


def pedir(mensaje: str, tools: list[dict] | None = None) -> tuple[requests.Response, list[dict], list[str]]:
    cuerpo = {
        "model": MODELO,
        "messages": [{"role": "user", "content": mensaje}],
        "stream": True,
    }
    if tools:
        cuerpo["tools"] = tools
    respuesta = requests.post(URL, json=cuerpo, timeout=120, stream=True)
    chunks, lineas = eventos_sse(respuesta)
    return respuesta, chunks, lineas


def test_1_saludo() -> None:
    respuesta, chunks, lineas = pedir("hola we")
    primero = delta_de(chunks[0]) if chunks else {}
    contenido = primero.get("content") or ""
    finishes = [((c.get("choices") or [{}])[0].get("finish_reason")) for c in chunks]
    done = any(linea.strip() == "data: [DONE]" for linea in lineas)
    ok = (
        respuesta.status_code == 200
        and primero.get("role") == "assistant"
        and bool(contenido.strip())
        and finishes[-1:] == ["stop"]
        and done
    )
    registrar("TEST 1 Charla/saludo", ok, f"HTTP {respuesta.status_code}, content={contenido[:70]!r}, finish={finishes[-1:]}")


def test_2_tecnica() -> None:
    respuesta, chunks, lineas = pedir("En una frase, ¿qué hace un índice en MySQL?")
    texto = "".join((delta_de(c).get("content") or "") for c in chunks)
    limpio = bool(texto.strip()) and not any(
        marca in texto[:250] for marca in ("Eres MI-BIG", "REGLA FINAL", "# Tools", "Traceback")
    )
    ok = respuesta.status_code == 200 and limpio and any(
        linea.strip() == "data: [DONE]" for linea in lineas
    )
    registrar("TEST 2 Respuesta técnica", ok, f"HTTP {respuesta.status_code}, content={texto[:80]!r}")


def test_3_herramienta() -> None:
    mensaje = (
        "Usa la herramienta bash con command para ejecutar echo HOLA_SALUD_OK "
        "y responde solo con el JSON de la herramienta."
    )
    respuesta, chunks, lineas = pedir(mensaje, TOOLS)
    llamadas = []
    for chunk in chunks:
        for herramienta in delta_de(chunk).get("tool_calls") or []:
            funcion = herramienta.get("function") or {}
            llamadas.append((funcion.get("name"), funcion.get("arguments")))
    finishes = [((c.get("choices") or [{}])[0].get("finish_reason")) for c in chunks]
    ok = (
        respuesta.status_code == 200
        and bool(llamadas)
        and llamadas[0][0] == "bash"
        and "echo HOLA_SALUD_OK" in str(llamadas[0][1])
        and "tool_calls" in finishes
        and any(linea.strip() == "data: [DONE]" for linea in lineas)
    )
    registrar("TEST 3 Herramienta bash", ok, f"HTTP {respuesta.status_code}, tool_calls={len(llamadas)}, finish={finishes[-1:]}")


def test_4_rendimiento() -> None:
    cuerpo = {
        "model": MODELO,
        "messages": [{"role": "user", "content": "Di OK y nada más."}],
        "stream": False,
        "keep_alive": "15m",
        "options": {"num_ctx": 6144},
    }
    inicio = time.time()
    respuesta = requests.post("http://127.0.0.1:11434/api/chat", json=cuerpo, timeout=180)
    datos = respuesta.json()
    duracion = max(float(datos.get("eval_duration") or 1) / 1e9, 0.001)
    tokens = int(datos.get("eval_count") or 0)
    velocidad = tokens / duracion
    estado = subprocess.run([OLLAMA, "ps"], capture_output=True, text=True, timeout=30)
    linea_modelo = next((linea for linea in estado.stdout.splitlines() if MODELO in linea), "")
    gpu = "100% GPU" in linea_modelo
    ok = respuesta.status_code == 200 and gpu and velocidad > 25
    registrar(
        "TEST 4 Rendimiento",
        ok,
        f"HTTP {respuesta.status_code}, GPU={'100%' if gpu else 'NO'}, {velocidad:.1f} tok/s, {time.time()-inicio:.1f}s",
    )


def main() -> int:
    try:
        test_1_saludo()
        test_2_tecnica()
        test_3_herramienta()
        test_4_rendimiento()
    except Exception as error:
        registrar("EXCEPCION", False, str(error)[:300])
    total = len(RESULTADOS)
    buenos = sum(1 for _, ok, _ in RESULTADOS if ok)
    print(f"RESUMEN {buenos}/{total}")
    return 0 if buenos == total == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
