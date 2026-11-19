# 🛡️ Blindaje de Arquitectura: Desacoplamiento de Fases (IA Sin Filtro)

Este documento detalla la reestructuración y blindaje del pipeline de automatización para **IA Sin Filtro**, resolviendo de forma permanente el problema de retroalimentación donde la Fase 4 intentaba volver a ejecutar la generación de guion y la locución de ElevenLabs.

---

## 🛑 El Problema Resuelto

En implementaciones monolíticas en n8n:
1. Si la **Fase 4 (Publicación & Redes)** comparte lienzo y linaje de datos con las **Fases 1, 2 y 3 (Guion, Locución y Aprobación)**, cualquier reintento o reanudación tras la validación humana puede reevaluar nodos hacia atrás.
2. Esto causaba llamadas no deseadas a Gemini y síntesis duplicadas en ElevenLabs, consumiendo cuota innecesariamente y retrasando la publicación.

---

## 🏗️ La Solución: Desacoplamiento Estricto en 2 Workflows

Se dividió el proceso en dos flujos 100% aislados:

```
[WORKFLOW 1: Fases 1 a 3 — Generación, Síntesis y Aprobación]
  Cron Lunes 08:00 CET
    ↳ Generación de Guion (Gemini)
    ↳ Locución (ElevenLabs) + Masterizado EBU R128 (-16 LUFS)
    ↳ Render Dinámico de Short (9:16)
    ↳ Envío de Notificación con Botón/Webhook de Aprobación
        ↳ [STOP - No continúa automáticamente a publicación]

═══════════════════════════════════════════════════════════════
                      BARRERA DE AISLAMIENTO
═══════════════════════════════════════════════════════════════

[WORKFLOW 2: Fase 4 — Publicación y Difusión Multicanal]
  Webhook de Aprobación / Cron Jueves 09:00 CET
    ↳ Normalización de Datos Aprobados (Sin dependencias de nodos previos)
    ↳ Ejecución de automation/publish_episode.py (Idempotente)
    ↳ Git Commit & Push a GitHub Pages (feed.xml + index.html)
    ↳ Publicación del Anuncio en 𝕏 (@IAsinfiltr0)
    ↳ Notificación de Éxito Final (Telegram / Email / Dashboard)
```

---

## 📁 Archivos de la Solución

* [`automation/publish_episode.py`](publish_episode.py): Script en Python puro (sin dependencias externas) que actualiza `feed.xml` respetando namespaces de Apple Podcasts (`itunes:`) y actualiza el reproductor web en `index.html`.
* [`workflows/01_fases1_a_3_generacion_y_aprobacion.json`](../workflows/01_fases1_a_3_generacion_y_aprobacion.json): Workflow de n8n para guion y audio que finaliza tras emitir la solicitud de aprobación.
* [`workflows/02_fase4_publicacion_blindada.json`](../workflows/02_fase4_publicacion_blindada.json): Workflow de n8n para la Fase 4 blindada, sin nodos de ElevenLabs ni Gemini.

---

## 🚀 Ejecución Manual o por CLI de la Fase 4

Si se requiere forzar la publicación de un episodio de forma manual o mediante un script de mantenimiento:

```bash
python3 automation/publish_episode.py \
  --season 1 \
  --episode 4 \
  --title "IA Estrecha (ANI) vs. IA General (AGI)" \
  --concept "Diferencia entre algoritmos especializados de hoy y la hipotética inteligencia humana artificial" \
  --audio "Temporada_1_Episodio_4_IA_Estrecha_ANI_vs_IA_General_AGI.mp3" \
  --bytes 11254849 \
  --duration "05:51" \
  --yt-video "https://www.youtube.com/@jose.iasinfiltro" \
  --yt-short "https://ia-sin-filtro.duckdns.org/episodes/shorts_ep4_youtube.mp4"
```
