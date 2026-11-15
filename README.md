# 🎙️ IA Sin Filtro — Podcast Feed & Landing Page

Repositorio público del podcast **"IA Sin Filtro"**, alojado mediante **GitHub Pages** para la sindicación y distribución automática del feed RSS hacia **Spotify**, **Apple Podcasts**, **iVoox**, **Amazon Music** y **YouTube Podcasts**.

---

## 📡 Enlaces de Sindicación

* **Feed RSS Oficial:** `https://mgjosea.github.io/ia-sin-filtro-podcast/feed.xml`
* **Landing Page & Web Player:** `https://mgjosea.github.io/ia-sin-filtro-podcast/`
* **Carátula Oficial (3000 x 3000 px):** [`cover.jpg`](cover.jpg)

---

## 📺 Episodios Publicados & YouTube Shorts

| Episodio | Título | Vídeo 1080p | YouTube Short (45s) |
| :---: | :--- | :---: | :---: |
| **01** | ¿Qué es realmente la Inteligencia Artificial? | [Ver en YouTube](https://youtu.be/pML8hddbp48) | [Ver Short](https://youtube.com/shorts/_Vaze1GxP78) |
| **02** | Breve historia de la IA: Del sueño de Turing a nuestro bolsillo | [Ver en YouTube](https://youtu.be/teKFPxBZ0MY) | [Ver Short](https://youtube.com/shorts/5QFpT_E-INc) |
| **03** | Mitos vs. Realidades de la Inteligencia Artificial | [Ver en YouTube](https://youtu.be/5XNrgmXdGKE) | [Ver Short](https://youtube.com/shorts/Mguy_63KV3s) |

---

## 🛠️ Cómo Funciona la Automatización (0€ de Coste)

1. **Generación & Masterización:** Todos los jueves a las 09:00 AM, **n8n** orquesta la locución mediante **ElevenLabs** y la masterización profesional con **Auphonic** (-16 LUFS, intro y outro con música de sintetizador).
2. **Publicación Serverless:** El audio final se publica en los *Releases* de este repositorio (con soporte para streaming por rangos de bytes `Accept-Ranges: bytes`).
3. **Actualización del RSS:** n8n inyecta el nuevo episodio en [`feed.xml`](feed.xml) y hace commit automático.
4. **Distribución Mundial:** Los bots de Spotify, Apple Podcasts e iVoox detectan el cambio en GitHub Pages y difunden el episodio a todos los suscriptores.

---

© 2026 IA Sin Filtro. Conducido por José IA. Todos los derechos reservados.
