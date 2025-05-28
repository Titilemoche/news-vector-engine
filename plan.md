# Plan for RSS Feed Scraper Setup

This document outlines the steps to set up a Python-based RSS feed scraper.

**Phase 1: File Creation (Architect Mode - Planning)**

1.  **Define `sources.json`**:
    *   Location: Root directory (`c:/Users/Teler/Documents/DAFUNK STUDIO/news-vector-engine/sources.json`).
    *   Content:
        ```json
        [
          {
            "persona_id": "persona_ai_builder",
            "source_name": "Hugging Face Blog",
            "type": "rss",
            "url": "https://huggingface.co/blog/feed.xml"
          },
          {
            "persona_id": "persona_ai_creator",
            "source_name": "Playform.io Editorial",
            "type": "rss",
            "url": "https://playform.io/editorial?format=rss"
          },
          {
            "persona_id": "persona_ai_investor",
            "source_name": "TechCrunch Fundings & Exits",
            "type": "rss",
            "url": "https://techcrunch.com/fundings-exits/feed/"
          }
        ]
        ```
2.  **Define `pipeline/scrape_feeds.py`**:
    *   Location: `pipeline` directory (`c:/Users/Teler/Documents/DAFUNK STUDIO/news-vector-engine/pipeline/scrape_feeds.py`).
    *   Content:
        ```python
        import json
        import feedparser
        from pathlib import Path

        # Charger les sources
        with open("../sources.json", "r") as f: # Adjusted path for script location
            sources = json.load(f)

        # Dossier de sortie
        output_dir = Path("../data/feeds_raw") # Adjusted path for script location
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
        ```
3.  **Define `requirements.txt`**:
    *   Location: Root directory (`c:/Users/Teler/Documents/DAFUNK STUDIO/news-vector-engine/requirements.txt`).
    *   Content:
        ```
        feedparser
        ```

**Phase 2: Implementation (to be handled by Code Mode)**

1.  **Create `sources.json`** using the content defined above.
2.  **Create `pipeline/scrape_feeds.py`** using the content defined above.
3.  **Create `requirements.txt`** using the content defined above.
4.  **Install `feedparser`**: Execute `pip install feedparser` in the terminal.
5.  **Run the Scraper Script**: Execute `python pipeline/scrape_feeds.py` from the root directory to fetch the feeds and generate the output files in `data/feeds_raw/`.
6.  **Verify**: Check for output files in `data/feeds_raw/`.

**Mermaid Diagram:**
```mermaid
graph TD
    A[Start Planning] --> B{Define sources.json};
    B --> C{Define pipeline/scrape_feeds.py};
    C --> D{Define requirements.txt};
    D --> E[Plan Complete];
    E --> F[Switch to Code Mode for Implementation];
    F --> G[Code Mode: Create sources.json];
    G --> H[Code Mode: Create pipeline/scrape_feeds.py];
    H --> I[Code Mode: Create requirements.txt];
    I --> J[Code Mode: pip install feedparser];
    J --> K[Code Mode: python pipeline/scrape_feeds.py];
    K --> L[Code Mode: Verify output in data/feeds_raw];
    L --> M[End Task];