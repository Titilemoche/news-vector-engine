# NLP Enrichment Pipeline Plan

**Objective:**

Modify the `pipeline/enrich_articles.py` script to:
1.  Process all `*.json` files found in the `data/feeds_raw/` directory.
2.  For each article within these files, apply a sequence of NLP processing steps using the modules: `cleaner.py`, `tagger.py`, `classifier.py`, `entities.py`, and the existing `summarize.py`.
3.  Produce an enriched JSON output file for each article, stored in a persona-specific directory under `data/enriched/persona_X/`, containing the results from all NLP modules.

**Detailed Plan:**

1.  **Update Imports in `pipeline/enrich_articles.py`:**
    *   Add `import glob` to find input files.
    *   Modify the `pipeline.nlp_modules` import to include all necessary modules:
        ```python
        from pipeline.nlp_modules import summarize, cleaner, tagger, classifier, entities
        ```

2.  **Dynamic Input File and Persona Handling:**
    *   Remove the hardcoded `persona = "persona_ai_builder"` line.
    *   Use `glob.glob("data/feeds_raw/*.json")` to get a list of all raw feed JSON file paths.
    *   Implement a main loop that iterates over each `feed_file_path` obtained from `glob`.
    *   Inside this loop:
        *   Extract the `persona` name from `feed_file_path`. For example, from `"data/feeds_raw/persona_ai_creator.json"`, the persona would be `"persona_ai_creator"`. The `Path(feed_file_path).stem` can be useful here.
        *   Set `input_file = Path(feed_file_path)`.
        *   Set `output_dir = Path(f"data/enriched/{persona}")`.
        *   Ensure `output_dir.mkdir(parents=True, exist_ok=True)` is called for each persona.
        *   Load articles from the current `input_file`.

3.  **Iterate Through All Articles:**
    *   Within the loop for each persona file, after loading `articles = json.load(f)`, ensure you loop through *every* `article` in the `articles` list. The current logic `article = articles[0]` must be changed to a `for article in articles:` loop.

4.  **NLP Processing Pipeline for Each Article:**
    *   Inside the `for article in articles:` loop:
        *   a.  **Extract Text Fields:**
            *   `title = article.get('title', '')`
            *   `summary_raw = article.get('summary', '')`
        *   b.  **Construct Input Text:**
            *   `input_text = f"{title}\n\n{summary_raw}" if summary_raw else title`
        *   c.  **Clean Text:**
            *   `cleaned_text = cleaner.clean_text(input_text)`
        *   d.  **Tag Article:**
            *   `tags = tagger.tag_article(cleaned_text)`
        *   e.  **Classify Article:**
            *   `category = classifier.classify_article(cleaned_text)`
        *   f.  **Extract Entities:**
            *   `extracted_entities = entities.extract_entities(cleaned_text)`
        *   g.  **Summarize Text (using cleaned text):**
            *   `enriched_summary = summarize.run(cleaned_text)`

5.  **Structure the Output JSON:**
    *   For each article, the `result` dictionary to be saved as JSON should include:
        ```python
        result = {
            "title": title,
            "link": article.get("link", ""),
            "source_persona": persona, # The persona derived from the input file
            "original_summary": summary_raw, # The original summary from the feed
            "input_text_for_nlp": input_text, # The text block fed to NLP modules
            "cleaned_text": cleaned_text, # Output of the cleaner module
            "enriched_summary": enriched_summary, # Output of the summarize module
            "tags": tags, # Output of the tagger module
            "category": category, # Output of the classifier module
            "entities": extracted_entities, # Output of the entities module
            # Optional: "processing_timestamp": datetime.utcnow().isoformat() (requires datetime import)
        }
        ```

6.  **Output File Naming and Saving:**
    *   The slug generation for the output filename should be robust. The current one is a good start:
        `slug = title.replace(" ", "_").replace("/", "-").replace(":", "_").replace("?", "")`
        Consider adding more sanitization if titles can contain other problematic characters for filenames.
    *   The `output_path` will be `output_dir / f"{slug}.json"`.
    *   Save the `result` dictionary to this `output_path`.

7.  **Enhanced Logging:**
    *   Update logging messages to be more informative in the context of processing multiple files and articles:
        *   Log the start and end of processing for each `feed_file_path`.
        *   Log the persona being processed.
        *   Log the number of articles found in each file.
        *   Optionally, log the title of each article being processed or a progress counter (e.g., "Processing article X of Y for persona Z").

**Flow Diagram:**

```mermaid
graph TD
    A[Start Enrichment Process] --> B{Find all `data/feeds_raw/*.json` files};
    B -- For each `feed_file.json` --> C{Extract Persona from filename};
    C --> D[Set Input File & Output Directory for Persona];
    D --> E[Create Persona Output Directory if not exists];
    E --> F[Load Articles from Persona JSON];
    F -- For each `article` in articles list --> G{Get `title` & `summary_raw`};
    G --> H[Construct `input_text` (title + summary_raw)];
    H --> H_clean[Call `cleaner.clean_text(input_text)` → `cleaned_text`];
    H_clean --> I[Call `tagger.tag_article(cleaned_text)` → `tags`];
    I --> J[Call `classifier.classify_article(cleaned_text)` → `category`];
    J --> K[Call `entities.extract_entities(cleaned_text)` → `extracted_entities`];
    K --> L[Call `summarize.run(cleaned_text)` → `enriched_summary`];
    L --> M[Assemble Enriched Article JSON Data (title, link, persona, original_summary, input_text_for_nlp, cleaned_text, enriched_summary, tags, category, entities)];
    M --> N[Generate Output Filename (`slug.json`) based on title];
    N --> O[Save Enriched Article to `data/enriched/PERSONA/slug.json`];
    O -- Next Article --> G;
    O -- All Articles in File Processed --> P{Any more `feed_file.json`?};
    P -- Yes --> C;
    P -- No --> Q[End Enrichment Process];