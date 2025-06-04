import json
import feedparser
from pathlib import Path

# Charger les sources RSS depuis le fichier de configuration
with open("config/sources.json", "r", encoding="utf-8") as f:
    sources = json.load(f)

# Dossier de sortie pour les articles bruts
output_dir = Path("data/feeds_raw")
output_dir.mkdir(parents=True, exist_ok=True)

# Parcourir chaque flux RSS défini dans sources.json
for source in sources:
    feed = feedparser.parse(source["url"])
    articles = []

    for entry in feed.entries:
        articles.append({
            "title": entry.get("title"),
            "link": entry.get("link"),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "persona_id": source["persona_id"],
            "source": source["source_name"]
        })

    # Sauvegarder les articles de ce flux dans un fichier par persona
    out_file = output_dir / f"{source['persona_id']}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

print("✅ Scraping terminé. Articles enregistrés dans /data/feeds_raw/")
