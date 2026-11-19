#!/usr/bin/env python3
"""
Motor de Publicación Idempotente y Blindado para "IA Sin Filtro" (Fase 4).
Actualiza feed.xml, index.html y README.md sin tocar ElevenLabs ni re-generar guiones.
"""

import os
import sys
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone
import re

ET.register_namespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEED_FILE = os.path.join(REPO_DIR, "feed.xml")
INDEX_FILE = os.path.join(REPO_DIR, "index.html")
README_FILE = os.path.join(REPO_DIR, "README.md")
EPISODES_DIR = os.path.join(REPO_DIR, "episodes")

def publish_episode(
    season_num: int,
    episode_num: int,
    title: str,
    description: str,
    audio_filename: str,
    audio_length_bytes: int,
    duration_str: str,
    concept: str = "",
    yt_video_url: str = "https://www.youtube.com/@jose.iasinfiltro",
    yt_short_url: str = "",
    github_user: str = "mgjosea",
    repo_name: str = "ia-sin-filtro-podcast",
    pub_date: str = None
):
    base_url = f"https://{github_user}.github.io/{repo_name}"
    audio_url = f"{base_url}/episodes/{audio_filename}?v=1"
    
    if not pub_date:
        pub_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    guid_val = f"ia-sin-filtro-s{season_num}-e{episode_num}"
    
    print(f"[*] Iniciando Fase 4 Blindada para S{season_num}E{episode_num}: '{title}'")
    
    # 1. Actualizar feed.xml
    if not os.path.exists(FEED_FILE):
        raise FileNotFoundError(f"No se encuentra feed.xml en {FEED_FILE}")
    
    tree = ET.parse(FEED_FILE)
    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        raise ValueError("feed.xml no contiene elemento <channel>")
    
    # Actualizar lastBuildDate
    last_build = channel.find("lastBuildDate")
    if last_build is not None:
        last_build.text = pub_date
    else:
        lb = ET.SubElement(channel, "lastBuildDate")
        lb.text = pub_date
    
    # Remover item anterior si existiera con el mismo GUID (idempotencia)
    for existing_item in channel.findall("item"):
        g = existing_item.find("guid")
        if g is not None and g.text == guid_val:
            print(f"[-] Removiendo versión anterior de {guid_val} para actualizarlo...")
            channel.remove(existing_item)
            break
            
    # Crear nuevo elemento item
    item = ET.SubElement(channel, "item")
    
    ITUNES_NS = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
    
    t_el = ET.SubElement(item, "title")
    t_el.text = title
    
    itunes_t = ET.SubElement(item, f"{ITUNES_NS}title")
    itunes_t.text = title
    
    itunes_ep_type = ET.SubElement(item, f"{ITUNES_NS}episodeType")
    itunes_ep_type.text = "full"
    
    full_desc = f"{title}. Concepto clave: {concept}. Píldora pedagógica de 5 minutos conducida por José IA." if concept else description
    
    d_el = ET.SubElement(item, "description")
    d_el.text = f"<![CDATA[{full_desc}]]>"
    
    s_el = ET.SubElement(item, f"{ITUNES_NS}summary")
    s_el.text = full_desc
    
    p_el = ET.SubElement(item, "pubDate")
    p_el.text = pub_date
    
    ET.SubElement(item, "enclosure", {
        "url": audio_url,
        "length": str(audio_length_bytes),
        "type": "audio/mpeg"
    })
    
    g_el = ET.SubElement(item, "guid", {"isPermaLink": "false"})
    g_el.text = guid_val
    
    dur_el = ET.SubElement(item, f"{ITUNES_NS}duration")
    dur_el.text = duration_str
    
    s_num_el = ET.SubElement(item, f"{ITUNES_NS}season")
    s_num_el.text = str(season_num)
    
    e_num_el = ET.SubElement(item, f"{ITUNES_NS}episode")
    e_num_el.text = str(episode_num)
    
    a_el = ET.SubElement(item, f"{ITUNES_NS}author")
    a_el.text = "José IA"
    
    exp_el = ET.SubElement(item, f"{ITUNES_NS}explicit")
    exp_el.text = "no"
    
    img_el = ET.SubElement(item, f"{ITUNES_NS}image", {
        "href": f"{base_url}/cover.jpg"
    })
    
    # Serializar XML limpio
    xml_str = ET.tostring(root, encoding="utf-8")
    # Des-escapar CDATA si fue escapado
    xml_str = xml_str.replace(b"&lt;![CDATA[", b"<![CDATA[").replace(b"]]&gt;", b"]]>")
    
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8")
    
    # Eliminar líneas vacías excesivas de minidom
    lines = [line for line in pretty_xml.split(b"\n") if line.strip()]
    clean_xml = b"\n".join(lines) + b"\n"
    
    with open(FEED_FILE, "wb") as f:
        f.write(clean_xml)
    print(f"[+] feed.xml actualizado con éxito con el episodio {episode_num}.")
    
    # 2. Actualizar index.html (Web Player)
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            html = f.read()
            
        # Reemplazar el cartel de "ÚLTIMO EPISODIO" del episodio anterior
        html = re.sub(
            r'<span style="color: #10b981;">🔥 ÚLTIMO EPISODIO • TEMPORADA (\d+) \(EP\. (\d+)\)</span>',
            r'<span>📻 TEMPORADA \1 • EPISODIO \2</span>',
            html
        )
        
        # Eliminar tarjeta existente del ep4 si ya estaba
        html = re.sub(
            rf'<div class="player-card"[^>]*>.*?<h4>{re.escape(title)}</h4>.*?</div>\s*',
            '',
            html,
            flags=re.DOTALL
        )
        
        short_link_html = f'''<a href="{yt_short_url}" target="_blank" rel="noopener" style="color: #f43f5e; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;">
            📱 Ver Short &rarr;
          </a>''' if yt_short_url else ''
          
        new_card = f'''      <!-- Player Preview Ep {episode_num} -->
      <div class="player-card" style="border-color: rgba(16, 185, 129, 0.5); margin-bottom: 20px;">
        <span style="color: #10b981;">🔥 ÚLTIMO EPISODIO • TEMPORADA {season_num} (EP. {episode_num})</span>
        <h4>{title}</h4>
        <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px; margin-top: -6px;">Píldora de 5 minutos • {concept} • Masterización profesional (-16 LUFS).</p>
        <audio controls style="width: 100%; margin-bottom: 10px;">
          <source src="episodes/{audio_filename}?v=1" type="audio/mpeg">
          Tu navegador no soporta el reproductor de audio.
        </audio>
        <div style="display: flex; gap: 14px; align-items: center; padding-top: 6px; border-top: 1px solid rgba(255,255,255,0.06); font-size: 12px; font-weight: 700;">
          <a href="{yt_video_url}" target="_blank" rel="noopener" style="color: #ef4444; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;">
            🎬 Ver Vídeo en YouTube &rarr;
          </a>
          {short_link_html}
        </div>
      </div>\n\n'''
        
        # Insertar justo antes del primer player-card existente
        pos = html.find('<div class="player-card"')
        if pos != -1:
            html = html[:pos] + new_card + html[pos:]
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"[+] index.html actualizado con la tarjeta de reproducción del episodio {episode_num}.")
            
    # 3. Actualizar README.md si aplica
    if os.path.exists(README_FILE):
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme = f.read()
        row_str = f"| **0{episode_num}** | {title} | [Ver en YouTube]({yt_video_url}) | [Ver Short]({yt_short_url}) |"
        if title not in readme:
            # Añadir tras el último episodio en la tabla
            table_match = re.search(r"(\|\s*\*\*03\*\*.*?\n)", readme)
            if table_match:
                end_pos = table_match.end()
                readme = readme[:end_pos] + row_str + "\n" + readme[end_pos:]
                with open(README_FILE, "w", encoding="utf-8") as f:
                    f.write(readme)
                print(f"[+] README.md actualizado con la fila del episodio {episode_num}.")
                
    print(f"[✓] Fase 4 completada con éxito. Listo para git commit y distribución.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publicar episodio en feed.xml e index.html")
    parser.add_argument("--season", type=int, default=1, help="Número de temporada")
    parser.add_argument("--episode", type=int, required=True, help="Número de episodio")
    parser.add_argument("--title", type=str, required=True, help="Título del episodio")
    parser.add_argument("--desc", type=str, default="", help="Descripción del episodio")
    parser.add_argument("--concept", type=str, default="", help="Concepto clave")
    parser.add_argument("--audio", type=str, required=True, help="Nombre del archivo MP3 en episodes/")
    parser.add_argument("--bytes", type=int, required=True, help="Tamaño en bytes del MP3")
    parser.add_argument("--duration", type=str, default="05:51", help="Duración (mm:ss)")
    parser.add_argument("--yt-video", type=str, default="https://www.youtube.com/@jose.iasinfiltro", help="URL Vídeo YouTube")
    parser.add_argument("--yt-short", type=str, default="", help="URL YouTube Short")
    
    args = parser.parse_args()
    publish_episode(
        season_num=args.season,
        episode_num=args.episode,
        title=args.title,
        description=args.desc,
        audio_filename=args.audio,
        audio_length_bytes=args.bytes,
        duration_str=args.duration,
        concept=args.concept,
        yt_video_url=args.yt_video,
        yt_short_url=args.yt_short
    )
