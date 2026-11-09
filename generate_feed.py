#!/usr/bin/env python3
"""
Generador del Feed RSS para "IA Sin Filtro" (Compatible con Apple Podcasts, Spotify, iVoox, Amazon Music).
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone

FEED_FILE = os.path.join(os.path.dirname(__file__), "feed.xml")

def create_or_load_feed(github_user="mgjosea", repo_name="ia-sin-filtro-podcast", base_url=None):
    if not base_url:
        base_url = f"https://{github_user}.github.io/{repo_name}"

    if os.path.exists(FEED_FILE):
        try:
            tree = ET.parse(FEED_FILE)
            return tree, tree.getroot()
        except Exception:
            pass

    # Crear estructura base del RSS
    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
        "xmlns:atom": "http://www.w3.org/2005/Atom"
    })
    
    channel = ET.SubElement(rss, "channel")
    
    # Metadata del Podcast
    atom_link = ET.SubElement(channel, "atom:link", {
        "href": f"{base_url}/feed.xml",
        "rel": "self",
        "type": "application/rss+xml"
    })
    
    title = ET.SubElement(channel, "title")
    title.text = "IA Sin Filtro"
    
    link = ET.SubElement(channel, "link")
    link.text = f"{base_url}/"
    
    language = ET.SubElement(channel, "language")
    language.text = "es-ES"
    
    copyright_el = ET.SubElement(channel, "copyright")
    copyright_el.text = f"© {datetime.now().year} IA Sin Filtro"
    
    desc = ET.SubElement(channel, "description")
    desc.text = (
        "IA Sin Filtro es tu dosis semanal de 5 minutos sobre Inteligencia Artificial, "
        "Machine Learning y tecnologías emergentes, explicada de forma directa, rigurosa y sin tecnicismos innecesarios. "
        "Cada jueves, una píldora pedagógica escalonada para entender cómo la IA transforma el trabajo, la sociedad y el futuro."
    )
    
    itunes_type = ET.SubElement(channel, "itunes:type")
    itunes_type.text = "episodic"
    
    itunes_summary = ET.SubElement(channel, "itunes:summary")
    itunes_summary.text = (
        "Píldoras semanales de 5 minutos sobre Inteligencia Artificial sin tecnicismos ni filtros. "
        "Una explicación clara y directa para entender cómo la IA está transformando nuestro mundo."
    )
    
    itunes_author = ET.SubElement(channel, "itunes:author")
    itunes_author.text = "José IA"
    
    itunes_owner = ET.SubElement(channel, "itunes:owner")
    owner_name = ET.SubElement(itunes_owner, "itunes:name")
    owner_name.text = "José IA"
    owner_email = ET.SubElement(itunes_owner, "itunes:email")
    owner_email.text = "jose.iasinfiltro@gmail.com"
    
    itunes_explicit = ET.SubElement(channel, "itunes:explicit")
    itunes_explicit.text = "no"
    
    ET.SubElement(channel, "itunes:category", {"text": "Technology"})
    
    cat2 = ET.SubElement(channel, "itunes:category", {"text": "Education"})
    
    itunes_image = ET.SubElement(channel, "itunes:image", {
        "href": f"{base_url}/cover.jpg"
    })
    
    tree = ET.ElementTree(rss)
    return tree, rss

def add_episode(title_text, episode_num, season_num, description_text, mp3_url, mp3_length_bytes, duration_str, pub_date=None, github_user="mgjosea", repo_name="ia-sin-filtro-podcast"):
    base_url = f"https://{github_user}.github.io/{repo_name}"
    tree, rss = create_or_load_feed(github_user, repo_name, base_url)
    channel = rss.find("channel")
    
    if pub_date is None:
        pub_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
        
    guid_val = f"ia-sin-filtro-s{season_num}-e{episode_num}"
    
    # Check if item already exists to avoid duplicates
    for item in channel.findall("item"):
        guid = item.find("guid")
        if guid is not None and guid.text == guid_val:
            channel.remove(item)
            break
            
    item = ET.SubElement(channel, "item")
    
    ep_title = ET.SubElement(item, "title")
    ep_title.text = title_text
    
    ep_desc = ET.SubElement(item, "description")
    ep_desc.text = description_text
    
    ep_guid = ET.SubElement(item, "guid", {"isPermaLink": "false"})
    ep_guid.text = guid_val
    
    ep_pubdate = ET.SubElement(item, "pubDate")
    ep_pubdate.text = pub_date
    
    ep_enclosure = ET.SubElement(item, "enclosure", {
        "url": mp3_url,
        "length": str(mp3_length_bytes),
        "type": "audio/mpeg"
    })
    
    ep_duration = ET.SubElement(item, "itunes:duration")
    ep_duration.text = duration_str
    
    ep_season = ET.SubElement(item, "itunes:season")
    ep_season.text = str(season_num)
    
    ep_episode = ET.SubElement(item, "itunes:episode")
    ep_episode.text = str(episode_num)
    
    ep_summary = ET.SubElement(item, "itunes:summary")
    ep_summary.text = description_text
    
    ep_explicit = ET.SubElement(item, "itunes:explicit")
    ep_explicit.text = "no"
    
    # Guardar formateado
    xml_str = ET.tostring(rss, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8")
    
    with open(FEED_FILE, "wb") as f:
        f.write(pretty_xml)
        
    print(f"Feed actualizado con éxito: {FEED_FILE}")

if __name__ == "__main__":
    tree, rss = create_or_load_feed()
    xml_str = ET.tostring(rss, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8")
    with open(FEED_FILE, "wb") as f:
        f.write(pretty_xml)
    print("Plantilla base feed.xml inicializada correctamente en:", FEED_FILE)
