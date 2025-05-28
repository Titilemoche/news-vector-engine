import os
import json
from pathlib import Path
from tqdm import tqdm
import openai
from openai import OpenAI # Added import

# Configuration de l'API OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("La variable d'environnement OPENAI_API_KEY n'est pas définie.")
    api_key = input("Veuillez entrer votre clé API OpenAI : ").strip()

if not api_key:
    print("Aucune clé API fournie. Arrêt du script.")
    exit()

client = OpenAI(api_key=api_key) # Explicitly pass API key

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
        response = client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding
    except openai.APIError as e: # Keeping general APIError for now
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