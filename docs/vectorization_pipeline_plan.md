# Plan for Article Vectorization Pipeline

🎯 **Goal:** Convert enriched articles into numerical vector representations (embeddings) to enable semantic search and other similarity-based operations.

## Script: `pipeline/vectorize_articles.py`

This script will be responsible for processing enriched articles, generating embeddings using an OpenAI model, and saving the results.

### 1. Initialization and Configuration

*   **Imports:**
    *   `json` (for reading/writing JSON data)
    *   `pathlib.Path` (for robust path manipulation)
    *   `glob` (for finding enriched article files)
    *   `openai` (OpenAI Python client library)
    *   `logging` (for progress and error tracking)
    *   `os` and `dotenv` (for loading API keys from `.env`)
*   **Environment Variables:**
    *   Load `OPENAI_API_KEY` from a `.env` file.
*   **Logging:**
    *   Configure a logger to output information about the process, including successes, warnings, and errors.
*   **OpenAI Model:**
    *   Define the embedding model to be used (e.g., `"text-embedding-3-small"`). This could be a constant or configurable.
*   **Paths:**
    *   Input directory: `data/enriched/`
    *   Output directory: `data/embeddings/`

### 2. Core Logic

The script will iterate through each persona's enriched data and process articles one by one.

```mermaid
graph TD
    A[Start Vectorization Process] --> B{Find Persona Folders in data/enriched/};
    B -- For Each Persona --> C{Create Corresponding Persona Folder in data/embeddings/};
    C --> D{Find Enriched JSON Files for Persona};
    D -- For Each Article JSON --> E[Load Article Data];
    E --> F[Extract 'text_for_embedding' Field];
    F --> G{Call OpenAI Embedding API with Text};
    G -- Success --> H[Receive Embedding Vector];
    G -- API Error --> I[Log Error, Skip Article/Handle Gracefully];
    H --> J[Add 'embedding: [vector]' to Article Data];
    J --> K[Save Updated Article JSON to data/embeddings/persona/];
    K --> D;
    D -- No More Articles --> B;
    B -- No More Personas --> L[End Vectorization Process];
```

*   **Iterate Through Personas:**
    *   Scan the `data/enriched/` directory for subdirectories (each representing a persona).
*   **For Each Persona:**
    1.  **Ensure Output Directory:** Create a corresponding subdirectory within `data/embeddings/` if it doesn't already exist (e.g., `data/embeddings/persona_ai_builder/`).
    2.  **Iterate Through Enriched Articles:**
        *   Use `glob` to find all `.json` files within the current persona's enriched data folder (e.g., `data/enriched/persona_ai_builder/*.json`).
    3.  **For Each Article File:**
        *   **Load Data:** Read the JSON content of the enriched article.
        *   **Extract Text:** Get the value of the `text_for_embedding` field. If this field is missing or empty, log a warning and skip to the next article.
        *   **Generate Embedding:**
            *   Make an API call to the specified OpenAI embedding model with the extracted text.
            *   Implement error handling for the API call (e.g., network issues, API errors, rate limits) with retries or graceful skipping.
        *   **Add Embedding to Data:** If the API call is successful, add the returned embedding vector (a list of floats) to the article's JSON data under a new key, e.g., `"embedding"`.
        *   **Save Result:** Write the modified JSON data (including the new embedding) to a new file in the corresponding persona's output directory in `data/embeddings/`. The filename should be the same as the input file.
*   **Logging:**
    *   Log the start and end of the overall process.
    *   Log the processing of each persona.
    *   Log the successful vectorization of each article and the path to the saved output file.
    *   Log any errors encountered during file operations or API calls.

### 3. Input

*   Enriched article files in JSON format located in `data/enriched/{persona_name}/`.
*   Each JSON file is expected to have a `text_for_embedding` field containing the string to be vectorized.

### 4. Output

*   JSON files containing the original enriched article data плюс a new `embedding` field.
*   These files will be saved in `data/embeddings/{persona_name}/`, mirroring the input structure.
*   Example structure of an output article:
    ```json
    {
      "title": "...",
      "link": "...",
      "source_persona": "...",
      "published": "2024-09-22T10:34:00Z",
      "cleaned_text": "...",
      "enriched_summary": "...",
      "tags": ["ai", "code agents", "structure"],
      "category": "technology_news",
      "entities": { "...": [...] },
      "text_for_embedding": "Title...\n\nSummary...\n\nTags: ...",
      "embedding": [0.0023, -0.0001, ..., 0.0456] // Example 1536 values for text-embedding-3-small
    }
    ```

### 5. Error Handling and Resilience

*   **File Operations:** Handle potential `FileNotFoundError` or `IOError` when reading/writing files.
*   **JSON Parsing:** Handle `JSONDecodeError` if an input file is not valid JSON.
*   **API Errors:**
    *   Implement try-except blocks for OpenAI API calls.
    *   Handle specific OpenAI errors (e.g., `openai.APIError`, `openai.RateLimitError`, `openai.AuthenticationError`).
    *   Consider a simple retry mechanism for transient errors.
*   **Missing Data:** If `text_for_embedding` is missing, log and skip the article.

### 6. Dependencies

*   `openai` Python library.
*   `python-dotenv` for managing environment variables.

This plan provides a clear path to implementing the vectorization step.