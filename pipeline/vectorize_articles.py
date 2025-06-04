import sys
import os
import json
import logging
from pathlib import Path
import glob
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, AuthenticationError

# Add project root to sys.path to allow imports if run directly or from other modules
# Assumes this script is in 'news-vector-engine/pipeline/'
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment variables from .env file
load_dotenv(dotenv_path=project_root / ".env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
        # Optional: Add a FileHandler here if you want to log to a file
        # logging.FileHandler("vectorization.log")
    ]
)
logger = logging.getLogger(__name__)

# --- Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # As per plan
ENRICHED_DATA_DIR = project_root / "data" / "enriched"
EMBEDDINGS_DIR = project_root / "data" / "embeddings"
TEXT_FOR_EMBEDDING_FIELD = "text_for_embedding"
EMBEDDING_FIELD_NAME = "embedding"

def get_embedding(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> list[float] | None:
    """
    Generates an embedding for the given text using the specified OpenAI model.
    """
    if not text or not text.strip():
        logger.warning("Received empty text for embedding. Skipping.")
        return None
    try:
        logger.debug(f"Requesting embedding for text (first 100 chars): '{text[:100]}...'")
        response = client.embeddings.create(input=[text], model=model)
        embedding = response.data[0].embedding
        logger.debug(f"Successfully received embedding of dimension {len(embedding)}.")
        return embedding
    except RateLimitError as e:
        logger.error(f"OpenAI API rate limit exceeded: {e}. Try again later or check your plan.")
    except AuthenticationError as e:
        logger.error(f"OpenAI API authentication error: {e}. Check your API key.")
    except APIError as e:
        logger.error(f"OpenAI API error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while getting embedding: {e}", exc_info=True)
    return None

def process_persona_articles(persona_name: str):
    """
    Processes all enriched articles for a given persona, generates embeddings,
    and saves them.
    """
    persona_enriched_dir = ENRICHED_DATA_DIR / persona_name
    persona_embeddings_dir = EMBEDDINGS_DIR / persona_name

    if not persona_enriched_dir.is_dir():
        logger.warning(f"Enriched data directory not found for persona {persona_name}: {persona_enriched_dir}. Skipping.")
        return

    try:
        persona_embeddings_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured output directory exists: {persona_embeddings_dir}")
    except Exception as e:
        logger.error(f"Could not create output directory {persona_embeddings_dir}: {e}", exc_info=True)
        return

    enriched_article_files = glob.glob(str(persona_enriched_dir / "*.json"))
    if not enriched_article_files:
        logger.info(f"No enriched articles found for persona {persona_name} in {persona_enriched_dir}.")
        return

    logger.info(f"Found {len(enriched_article_files)} enriched articles to process for persona: {persona_name}")

    for article_path_str in enriched_article_files:
        article_path = Path(article_path_str)
        output_article_path = persona_embeddings_dir / article_path.name
        article_title_for_log = article_path.stem # Use stem for a cleaner log

        # Skip if already processed to avoid re-processing and costs (optional, can be made more robust)
        if output_article_path.exists():
            logger.info(f"Article '{article_title_for_log}' already has an embedding: {output_article_path}. Skipping.")
            continue

        logger.info(f"--- Processing article: '{article_title_for_log}' (Persona: {persona_name}) ---")
        try:
            with open(article_path, "r", encoding="utf-8") as f:
                article_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {article_path}: {e}. Skipping article.")
            continue
        except Exception as e:
            logger.error(f"Error reading article file {article_path}: {e}. Skipping article.", exc_info=True)
            continue

        text_to_embed = article_data.get(TEXT_FOR_EMBEDDING_FIELD)
        if not text_to_embed:
            logger.warning(f"Field '{TEXT_FOR_EMBEDDING_FIELD}' not found or empty in article {article_path.name}. Skipping embedding.")
            # Optionally, save the article without embedding or handle differently
            continue

        embedding_vector = get_embedding(text_to_embed)

        if embedding_vector:
            article_data[EMBEDDING_FIELD_NAME] = embedding_vector
            try:
                with open(output_article_path, "w", encoding="utf-8") as f:
                    json.dump(article_data, f, indent=2, ensure_ascii=False)
                logger.info(f"✅ Article with embedding saved: {output_article_path}")
            except Exception as e:
                logger.error(f"Error saving article with embedding to {output_article_path}: {e}", exc_info=True)
        else:
            logger.warning(f"Could not generate embedding for article {article_path.name}. Article not saved with embedding.")

def main():
    logger.info("===== Starting Article Vectorization Process =====")

    if not ENRICHED_DATA_DIR.is_dir():
        logger.error(f"Enriched data directory not found: {ENRICHED_DATA_DIR}. Exiting.")
        return

    # Create base embeddings directory if it doesn't exist
    try:
        EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Could not create base embeddings directory {EMBEDDINGS_DIR}: {e}. Exiting.", exc_info=True)
        return

    persona_folders = [d for d in ENRICHED_DATA_DIR.iterdir() if d.is_dir()]

    if not persona_folders:
        logger.warning(f"No persona subdirectories found in {ENRICHED_DATA_DIR}.")
    else:
        logger.info(f"Found {len(persona_folders)} persona(s) to process: {[p.name for p in persona_folders]}")
        for persona_dir in persona_folders:
            persona_name = persona_dir.name
            logger.info(f"\n===== Processing Persona: {persona_name} =====")
            process_persona_articles(persona_name)
            logger.info(f"--- Finished processing persona {persona_name}. ---")

    logger.info("===== Article Vectorization Process Finished. =====")

if __name__ == "__main__":
    main()