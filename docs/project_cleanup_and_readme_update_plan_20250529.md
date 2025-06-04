# Plan: Project Cleanup and README Update (2025-05-29)

This document outlines the plan for cleaning up parts of the `news-vector-engine` project and updating the `README.md` to reflect the current state and future roadmap.

## 1. Nettoyage & Cohérence du Projet

### a. `pipeline/enrich_articles.py`

*   **Action:** Add `from dotenv import load_dotenv` and `load_dotenv()` at the top of the file for explicit environment variable loading.
*   **Details:**
    *   The line `from dotenv import load_dotenv` will be inserted.
    *   The line `load_dotenv()` will be inserted immediately after it.
    *   These will be placed after the existing `import glob` (around line 13) and before the `from pipeline.nlp_modules import ...` (around line 14).
*   **Proposed Snippet to Insert:**
    ```python
    from dotenv import load_dotenv
    load_dotenv()
    ```

## 2. Clarification des modules NLP

For each of the following files, a module-level docstring will be added at the very beginning of the file (line 1).

### a. `pipeline/nlp_modules/tagger.py`

*   **Proposed Docstring:**
    ```python
    """
    Module: pipeline.nlp_modules.tagger
    Status: Stub / Placeholder
    Description: This module is intended to tag articles with relevant keywords.
                 Currently, it returns a static list of placeholder tags: ["tag1", "tag2", "placeholder_tag"].
    LLM Usage: No (currently returns static data).
    TODO: Implement actual tagging logic. This could involve rule-based methods,
          machine learning models, or leveraging an LLM with a dedicated prompt
          in `pipeline/prompts.py`.
    """
    ```

### b. `pipeline/nlp_modules/classifier.py`

*   **Proposed Docstring:**
    ```python
    """
    Module: pipeline.nlp_modules.classifier
    Status: Stub / Placeholder
    Description: This module is intended to classify articles into predefined categories.
                 Currently, it returns a static example category: "technology_news".
    LLM Usage: No (currently returns static data).
    TODO: Implement actual classification logic. This could involve rule-based methods,
          machine learning models, or leveraging an LLM with a dedicated prompt
          in `pipeline/prompts.py`.
    """
    ```

### c. `pipeline/nlp_modules/entities.py`

*   **Proposed Docstring:**
    ```python
    """
    Module: pipeline.nlp_modules.entities
    Status: Stub / Placeholder
    Description: This module is intended to extract named entities (persons, organizations,
                 locations, etc.) from articles. Currently, it returns a static
                 dictionary of placeholder entities.
    LLM Usage: No (currently returns static data).
    TODO: Implement actual entity extraction logic. This could involve using NLP
          libraries like spaCy or NLTK, or leveraging an LLM with a dedicated
          prompt in `pipeline/prompts.py`.
    """
    ```

### d. `pipeline/nlp_modules/cleaner.py`

*   **Proposed Docstring:**
    ```python
    """
    Module: pipeline.nlp_modules.cleaner
    Status: Stub / Placeholder (currently returns original text)
    Description: This module is intended to clean article text by removing unwanted
                 elements like HTML tags, special characters, or excessive whitespace.
                 Currently, it acts as a pass-through, returning the original text.
    LLM Usage: No.
    TODO: Implement actual text cleaning logic. Common libraries for this include
          BeautifulSoup4 (for HTML) and regex.
    """
    ```

## 3. Mise à jour du `README.md`

*   **Action:** The `README.md` file will be overwritten with the new content reflecting the actual project state and future plans.
*   **Proposed New Content for `README.md`:**

    ```markdown
    # news-vector-engine

    This project is designed to process news articles, enrich them with NLP techniques (including LLM-based summarization), and prepare them for vectorization and advanced analysis.

    ##  État du projet (Project Status)

    ### ✅ Fonctionnel (Functional)

    *   **Scraping des flux RSS par persona:**
        *   Le script `pipeline/scrape_feed.py` collecte les articles depuis les sources RSS définies dans `config/sources.json`.
        *   Les données brutes sont stockées dans `data/feeds_raw/` par persona.
    *   **Enrichissement des articles:**
        *   Le script `pipeline/enrich_articles.py` orchestre le processus.
        *   **Nettoyage de texte (`pipeline/nlp_modules/cleaner.py`):** Placeholder, retourne le texte original pour l'instant.
        *   **Résumé généré par LLM (Gemini) (`pipeline/nlp_modules/summarize.py`):** Fonctionnel, utilise le modèle Gemini via `pipeline/llm_client.py` et les prompts de `pipeline/prompts.py`.
        *   **Tagging (`pipeline/nlp_modules/tagger.py`):** Stub, retourne des tags statiques.
        *   **Classification (`pipeline/nlp_modules/classifier.py`):** Stub, retourne une catégorie statique.
        *   **Extraction d’entités (`pipeline/nlp_modules/entities.py`):** Stub, retourne des entités statiques.
        *   Les articles enrichis sont sauvegardés dans `data/enriched/`.

    ### 🟡 En Cours / Prévu (In Progress / Planned)

    *   **Création des embeddings vectoriels:**
        *   Prévu. Le répertoire `data/embeddings/` est prêt (`.gitkeep` existe).
        *   Nécessite le choix et l'implémentation d'un modèle d'embedding.
    *   **Indexation dans une base vectorielle:**
        *   À définir : Choix de la technologie (FAISS, Pinecone, Weaviate, Milvus, etc.) et implémentation.
    *   **Export en TSV pour visualisation 3D:**
        *   Prévu pour une utilisation avec des outils comme TensorFlow Projector. Le répertoire `data/tsv_exports/` sera créé.
    *   **Personnalisation fine des personas:**
        *   Via `personas/personas_config.json` (actuellement vide). Pourrait inclure des mots-clés spécifiques, des styles de résumé différents, etc.
    *   **Prompts LLM supplémentaires:**
        *   Définir des prompts dédiés dans `pipeline/prompts.py` pour améliorer le tagging, la classification et l'extraction d'entités en utilisant le LLM.
    *   **Implémentation de la logique métier pour `cleaner`, `tagger`, `classifier`, `entities`:**
        *   Remplacer les stubs actuels par une logique fonctionnelle (rule-based, ML classique, ou via LLM).


    ### 🛠️ À Venir (Upcoming Features)

    *   Interface utilisateur ou API pour interagir avec les données enrichies et/ou les capacités de recherche vectorielle.
    *   Monitoring et gestion des erreurs améliorés pour le pipeline.
    *   Extension à d'autres types de sources de données (au-delà du RSS).

    ## Project Structure

    - `personas/`: Configurations for different personas (e.g., `personas/personas_config.json`).
    - `data/`: Contains all data related to news articles.
      - `feeds_raw/`: Raw articles obtained from scraping (e.g., `data/feeds_raw/persona_ai_builder.json`).
      - `enriched/`: Processed articles with NLP enrichments (e.g., `data/enriched/persona_ai_builder/`).
      - `embeddings/`: Intended for storing vector embeddings of enriched articles (`data/embeddings/.gitkeep`).
      - `tsv_exports/`: (Prévu / Planned) Data exported in TSV format for 3D visualization.
    - `pipeline/`: All scripts for the data processing pipeline.
      - `nlp_modules/`: Specific modules for NLP tasks (e.g., `pipeline/nlp_modules/summarize.py`).
      - `scrape_feed.py`: Script for scraping RSS feeds.
      - `enrich_articles.py`: Script for enriching articles.
      - `llm_client.py`: Client for interacting with the Gemini LLM.
      - `prompts.py`: Stores prompts for the LLM.
    - `config/`: Configuration files for the project (e.g., `config/sources.json`).
    - `docs/`: Project documentation (e.g., `docs/enrichment_pipeline_plan.md`).
    - `README.md`: This file.
    - `LICENSE`: Project license information.
    - `requirements.txt`: Python dependencies for the project.
    - `.env`: Environment variables (e.g., API keys). Should be in `.gitignore`.