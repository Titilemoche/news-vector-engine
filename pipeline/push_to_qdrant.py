from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import json
from pathlib import Path
import uuid
import os

# Connexion locale à Qdrant (déjà lancé)
# Consider making host and port configurable via environment variables for flexibility
qdrant_host = os.getenv("QDRANT_HOST", "localhost")
qdrant_port = int(os.getenv("QDRANT_PORT", 6333)) # Ensure port is an integer
client = QdrantClient(host=qdrant_host, port=qdrant_port)

collection_name = "articles_ia" # Consider making this configurable

# (Re)création de la collection Qdrant
# Note: recreate_collection will delete the collection if it already exists.
# For production, you might want to use ensure_collection or check existence first.
try:
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=1536,                # Taille de l'embedding (OpenAI text-embedding-ada-002)
            distance=Distance.COSINE
        )
    )
    print(f"Collection '{collection_name}' (re)created successfully.")
except Exception as e:
    print(f"Error (re)creating collection '{collection_name}': {e}")
    # Depending on the error, you might want to exit or try to proceed if it's non-critical
    # For now, we'll let it proceed to see if upsert works (e.g., if collection already exists and is compatible)

# Chargement des articles enrichis
input_dir = Path("data/embeddings")
points = []

if not input_dir.exists() or not any(input_dir.glob("*.json")):
    print(f"Warning: Input directory '{input_dir}' does not exist or contains no JSON files. No data to process.")
else:
    for file_path in input_dir.glob("*.json"):
        print(f"Processing file: {file_path.name}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                articles = json.load(f)

            for article_idx, article in enumerate(articles):
                # Ensure embedding exists and is of the correct type (list of floats)
                embedding = article.get("embedding")
                if not embedding or not isinstance(embedding, list) or not all(isinstance(x, float) for x in embedding):
                    print(f"Warning: Skipping article (index {article_idx} in {file_path.name}) due to missing or invalid embedding: {article.get('title', 'N/A')}")
                    continue
                
                # Ensure embedding size matches collection config (optional but good practice)
                if len(embedding) != 1536:
                    print(f"Warning: Skipping article (index {article_idx} in {file_path.name}) due to unexpected embedding size ({len(embedding)} instead of 1536): {article.get('title', 'N/A')}")
                    continue

                points.append(PointStruct(
                    id=str(uuid.uuid4()), # Generate a unique ID for each point
                    vector=embedding,
                    payload={
                        "title": article.get("title"),
                        "link": article.get("link"),
                        # Extract persona from filename if not in article data
                        "persona": article.get("persona_id", file_path.stem.replace("persona_", "")), 
                        "source": article.get("source"),
                        "published": article.get("published"),
                        "summary": article.get("summary")
                    }
                ))
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from file {file_path.name}. Skipping this file.")
        except Exception as e:
            print(f"An unexpected error occurred while processing {file_path.name}: {e}. Skipping this file.")

# Injection dans Qdrant
if points:
    try:
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"✅ {len(points)} vecteurs ont été injectés dans la collection '{collection_name}'.")
    except Exception as e:
        print(f"Error upserting points to Qdrant collection '{collection_name}': {e}")
elif input_dir.exists() and any(input_dir.glob("*.json")):
    print("No valid points were generated from the embedding files to inject into Qdrant.")
# If input_dir didn't exist or was empty, the warning was already printed.