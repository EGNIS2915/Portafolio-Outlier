# Índice de verificación

Si algo en las fichas suena muy bien escrito, ven aquí y abre el archivo. Esto no vende: solo dice dónde está cada cosa.

## MI-BIG

| Afirmación | Evidencia |
|---|---|
| Arquitectura Python/FastAPI/Ollama, herramientas y RAG | `03_Evidencia/MI-BIG/README_ARQUITECTURA.md` |
| Estado operativo real, endpoints y automatizaciones | `03_Evidencia/MI-BIG/ESTADO_23NOV.md` |
| Proxy SSE, tool_calls y guards de errores | `03_Evidencia/MI-BIG/proxy_ollama.py` |
| Pruebas de salud del stack | `03_Evidencia/MI-BIG/test_salud_opencode.py` |
| Panel de monitoreo | `03_Evidencia/MI-BIG/panel_monitoreo_mibig.py` |
| Modelo QLoRA y parámetros del runner | `03_Evidencia/MI-BIG/Modelfile_entrenado` |

Métricas reportadas en la validación del 23 nov: `4/4 PASS`, `61.6 tok/s`, `100% GPU`.

## Bases de datos

| Afirmación | Evidencia |
|---|---|
| Esquemas UNIVERSIDAD y TECNO_BYTE, normalización, JOIN, vistas, procedures, triggers, privilegios y ACID | Descripción técnica directa del candidato en `02_Proyectos/02_Bases_Datos_Relacionales.md` |

Nota: no se localizó dump `.sql` en DESK/TUF al armar esta entrega.

## Solana

| Afirmación | Evidencia |
|---|---|
| Contratos Rust y lógica descentralizada en Solana Engineering Track EDOMEX | Descripción técnica directa del candidato en `02_Proyectos/03_Solana_Rust_Blockchain.md` |

Nota: no se localizó código `.rs` en DESK/TUF al armar esta entrega.

## Gráficas y lógica digital

| Afirmación | Evidencia |
|---|---|
| Transformaciones y figuras 2D/3D en Octave | `03_Evidencia/Graficas_Octave/*.m` |
| Caso 3D con `patch`, `view` y `axis square` | `03_Evidencia/Graficas_Octave/Examen_completo.m` |
| Figura 2D básica | `03_Evidencia/Graficas_Octave/casa.m` |
| Latch de arranque/paro en P22V10 | `03_Evidencia/Logica_Digital/Arran_paro.pld` |
| Mapa de fusibles sintetizado | `03_Evidencia/Logica_Digital/Arran_paro.jed` |
| Compuertas y contadores | `03_Evidencia/Logica_Digital/gal.pld`, `gal.jed`, `Contador.pld`, `Contador.jed` |
| Simulaciones en Proteus | `03_Evidencia/Logica_Digital/*.pdsprj` |

## NEXA

| Afirmación | Evidencia |
|---|---|
| APK instalable y hash | `03_Evidencia/NEXA/NEXA_Beta_5NOV.apk` + `COMO_INSTALAR_Y_PROBAR_NEXA.txt` |
| Manual técnico y defensa | `03_Evidencia/NEXA/NEXA_Manual_Tecnico.pdf` y `.docx` |
| Entrega Scrum | `03_Evidencia/NEXA/NEXA_Entrega_Scrum_20261119.rar` |
| Builds adicionales | `03_Evidencia/NEXA/NEXA_v1.0.4-full-debug.apk` |

## Perfil

| Afirmación | Evidencia |
|---|---|
| Nombre, contacto, formación TESH, certificaciones Solana/SCRUM y resumen de los 5 proyectos | `04_Perfil/CV - Egnis Yaxel Piliado.pdf` |

CV validado: 1 página, 124,419 bytes, texto extraíble, sin cifrar, SHA-256 `16330d7d3e45fcc51d25c352da83600fe519ea17c9b928ead928b427f661870f`.

## Regla rápida

Si alguien pregunta “¿Cómo sé que es real?”: abrir este índice, escoger la fila y mostrar el archivo. Para Solana y SQL, la respuesta correcta es: “es proyecto real declarado; el código se entrega aparte si se solicita”.
