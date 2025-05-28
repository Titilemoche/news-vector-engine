# Plan: Vectorize Articles

This plan outlines the steps to set up the environment, create a Python script for vectorization, and execute the script.

## 1. Environment Preparation

*   **Update Dependencies:**
    *   The libraries `openai` and `tqdm` will be added to the `requirements.txt` file.
*   **Install Dependencies:**
    *   You will need to run the following command in your terminal to install the necessary libraries:
        ```bash
        pip install -r requirements.txt
        ```
*   **Configure OpenAI API Key:**
    *   **Crucial Step:** You must set your OpenAI API key as an environment variable named `OPENAI_API_KEY`. The method for setting environment variables depends on your operating system:
        *   **Linux/macOS (bash/zsh):**
            ```bash
            export OPENAI_API_KEY='your_api_key_here'
            ```
            (You might want to add this line to your `~/.bashrc` or `~/.zshrc` file for persistence across sessions).
        *   **Windows (Command Prompt):**
            ```bash
            set OPENAI_API_KEY=your_api_key_here
            ```
        *   **Windows (PowerShell):**
            ```bash
            $env:OPENAI_API_KEY='your_api_key_here'
            ```
            (For persistence in PowerShell, you can add this to your PowerShell profile script).
        *   **IDE/Environment Specific:** Many IDEs (like VS Code) allow setting environment variables through `.env` files or launch configurations. Please consult your IDE's documentation if you prefer this method.

## 2. Create Vectorization Script

*   A new Python script will be created at `pipeline/vectorize_articles.py`.
*   **Script Content:**
    ```python
    import os
    import json
    from pathlib import Path
    from tqdm import tqdm
    import openai

    # Configuration de l'API OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Répertoire contenant les articles scrappés
    input_dir = Path("data/feeds_raw")
    output_dir = Path("data/embeddings")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fonction pour obtenir l'embedding d'un texte
    def get_embedding(text, model="text-embedding-ada-002"):
        # Ensure text is not empty or just whitespace, and not excessively long
        if not text or not text.strip():
            print("Warning: Empty content found, skipping embedding.")
            return None # Or handle as appropriate, e.g., return a zero vector
        
        # OpenAI's API has token limits. text-embedding-ada-002 has a limit of 8191 tokens.
        # This is a simplistic check; a proper tokenizer would be better for precise control.
        # Assuming an average of ~4 chars per token for English.
        # Adjust if your content is very different or you need more precision.
        max_chars = 8000 * 4 # A bit conservative
        if len(text) > max_chars:
            print(f"Warning: Content too long ({len(text)} chars), truncating to {max_chars} chars.")
            text = text[:max_chars]

        try:
            response = openai.Embedding.create(
                input=text,
                model=model
            )
            return response['data'][0]['embedding']
        except openai.APIError as e:
            print(f"OpenAI API Error: {e}")
            return None # Or handle as appropriate

    # Traitement de chaque fichier JSON
    for file_path in input_dir.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            articles = json.load(f)

        enriched_articles = []
        for article in tqdm(articles, desc=f"Vectorisation de {file_path.name}"):
            content = article.get("summary", "") or article.get("title", "")
            if content and content.strip(): # Ensure there's actual content
                embedding = get_embedding(content)
                if embedding: # Only add embedding if successfully generated
                    article["embedding"] = embedding
            else:
                print(f"Skipping article due to empty content: {article.get('title', 'N/A')}")
            enriched_articles.append(article) # Append article even if embedding failed, or decide to skip

        # Sauvegarde des articles enrichis
        output_file = output_dir / file_path.name
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(enriched_articles, f, indent=2, ensure_ascii=False)

    print("✅ Vectorisation terminée. Les fichiers sont disponibles dans 'data/embeddings'.")
    ```

## 3. Execute the Script

*   Once the environment is set up and the script is created, you will run it from your terminal using the following command:
    ```bash
    python pipeline/vectorize_articles.py
    ```
*   The script will process JSON files from `data/feeds_raw/` and save the vectorized articles into `data/embeddings/`.

## Workflow Diagram

```mermaid
graph TD
    A[Start] --> B{Set OPENAI_API_KEY?};
    B -- Yes --> C[Update requirements.txt];
    B -- No --> D[Instruct User to Set API Key];
    D --> C;
    C --> E[Install Dependencies: pip install -r requirements.txt];
    E --> F[Create pipeline/vectorize_articles.py];
    F --> G[Run Script: python pipeline/vectorize_articles.py];
    G --> H[Process JSON files from data/feeds_raw];
    H --> I[Generate Embeddings via OpenAI API];
    I --> J[Save enriched articles to data/embeddings];
    J --> K[End: Vectorization Complete];