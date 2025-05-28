import json
import feedparser
from pathlib import Path

# Charger les sources
with open("sources.json", "r") as f:
    sources = json.load(f)

# Dossier de sortie
output_dir = Path("data/feeds_raw")
output_dir.mkdir(parents=True, exist_ok=True)

# Scraper chaque flux
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

    # Écrire le résultat dans un fichier par persona
    out_file = output_dir / f"{source['persona_id']}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

print("✅ Scraping terminé. Articles enregistrés dans /data/feeds_raw")