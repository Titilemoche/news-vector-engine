import os
import sys
import json
import logging
import glob
import uuid
from pathlib import Path
from datetime import datetime, timezone

# Add project root to sys.path to allow imports
project_root_path = Path(__file__).resolve().parent.parent
if str(project_root_path) not in sys.path:
    sys.path.insert(0, str(project_root_path))

from pipeline.qdrant_utils import get_qdrant_client, create_collection_if_not_exists, COLLECTION_NAME
from qdrant_client.http.models import PointStruct

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

EMBEDDINGS_DATA_DIR = project_root_path / "data" / "embeddings"
BATCH_SIZE = 100 # Number of points to upsert in a single batch

# Namespace for generating UUIDs from URLs (can be any valid UUID)
UUID_NAMESPACE = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8') # Example, use a consistent one

def generate_point_id(link: str) -> str:
    """Generates a stable UUID for a given link."""
    if not link:
        # Fallback for articles without a link, though this should be rare and handled
        logger.warning("Generating random UUID for an article without a link.")
        return str(uuid.uuid4())
    return str(uuid.uuid5(UUID_NAMESPACE, link))

def parse_published_date(date_str: str | None) -> str | None:
    """
    Parses a date string (e.g., 'Tue, 13 May 2025 00:00:00 GMT')
    and converts it to ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
    Returns None if parsing fails or input is None.
    """
    if not date_str:
        return None
    try:
        # Example format: 'Tue, 13 May 2025 00:00:00 GMT'
        # Adjust format string if your date format differs
        dt_object = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        # Ensure it's timezone-aware (assuming GMT if specified, otherwise UTC)
        if dt_object.tzinfo is None or dt_object.tzinfo.utcoffset(dt_object) is None:
             dt_object = dt_object.replace(tzinfo=timezone.utc)
        else:
            dt_object = dt_object.astimezone(timezone.utc)
        return dt_object.strftime('%Y-%m-%dT%H:%M:%SZ')
    except ValueError as e:
        logger.warning(f"Could not parse date string '{date_str}': {e}. Skipping date.")
        return None

def process_and_ingest_articles(qdrant_client):
    """
    Processes JSON files from the embeddings directory and ingests them into Qdrant.
    """
    logger.info(f"Starting ingestion process from: {EMBEDDINGS_DATA_DIR}")
    persona_folders = [d for d in EMBEDDINGS_DATA_DIR.iterdir() if d.is_dir()]

    if not persona_folders:
        logger.warning(f"No persona subdirectories found in {EMBEDDINGS_DATA_DIR}. Nothing to ingest.")
        return

    total_articles_processed = 0
    total_articles_ingested = 0

    for persona_dir in persona_folders:
        persona_name = persona_dir.name
        logger.info(f"\n===== Processing Persona: {persona_name} =====")
        
        article_files = glob.glob(str(persona_dir / "*.json"))
        if not article_files:
            logger.info(f"No embedding files found for persona {persona_name}. Skipping.")
            continue

        logger.info(f"Found {len(article_files)} articles to process for persona: {persona_name}")
        
        points_batch = []
        for article_path_str in article_files:
            article_path = Path(article_path_str)
            article_title_for_log = article_path.stem
            total_articles_processed += 1

            try:
                with open(article_path, "r", encoding="utf-8") as f:
                    article_data = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from {article_path}: {e}. Skipping article.")
                continue
            except Exception as e:
                logger.error(f"Error reading article file {article_path}: {e}. Skipping article.", exc_info=True)
                continue

            vector = article_data.get("embedding")
            if not vector:
                logger.warning(f"No 'embedding' field found in {article_path.name}. Skipping.")
                continue

            # Prepare payload
            payload = {key: value for key, value in article_data.items() if key != "embedding"}
            payload["content_type"] = "article" # Add content_type
            
            # Parse and format 'published' date
            parsed_date = parse_published_date(payload.get("published"))
            if parsed_date:
                payload["published"] = parsed_date
            elif "published" in payload: # If parsing failed but field exists, remove it or set to null
                del payload["published"] # Or payload["published"] = None, depending on Qdrant handling

            # Ensure tags is a list of strings
            if "tags" in payload and payload["tags"] is not None:
                if not isinstance(payload["tags"], list):
                    logger.warning(f"Tags in {article_path.name} is not a list. Converting to list.")
                    payload["tags"] = [str(payload["tags"])]
                else:
                    payload["tags"] = [str(tag) for tag in payload["tags"]]
            else:
                payload["tags"] = []


            point_id = generate_point_id(article_data.get("link", article_title_for_log)) # Use title as fallback for link

            points_batch.append(PointStruct(id=point_id, vector=vector, payload=payload))

            if len(points_batch) >= BATCH_SIZE:
                try:
                    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points_batch)
                    logger.info(f"Upserted batch of {len(points_batch)} points for persona {persona_name}.")
                    total_articles_ingested += len(points_batch)
                except Exception as e:
                    logger.error(f"Error upserting batch to Qdrant for persona {persona_name}: {e}", exc_info=True)
                points_batch = [] # Reset batch

            logger.debug(f"Processed article: '{article_title_for_log}' (ID: {point_id})")

        # Upsert any remaining points in the last batch
        if points_batch:
            try:
                qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points_batch)
                logger.info(f"Upserted final batch of {len(points_batch)} points for persona {persona_name}.")
                total_articles_ingested += len(points_batch)
            except Exception as e:
                logger.error(f"Error upserting final batch to Qdrant for persona {persona_name}: {e}", exc_info=True)
        
        logger.info(f"--- Finished processing persona {persona_name}. ---")

    logger.info(f"\n===== Ingestion Process Finished =====")
    logger.info(f"Total articles scanned: {total_articles_processed}")
    logger.info(f"Total articles successfully ingested/updated in Qdrant: {total_articles_ingested}")


def main():
    logger.info("===== Starting Qdrant Ingestion Script =====")
    try:
        qdrant_client = get_qdrant_client()
        if qdrant_client:
            # Ensure collection exists and is set up correctly
            create_collection_if_not_exists(qdrant_client)
            
            # Process and ingest articles
            process_and_ingest_articles(qdrant_client)
            
            logger.info("Qdrant ingestion script completed successfully.")
        else:
            logger.error("Could not establish connection with Qdrant. Aborting ingestion.")
    except Exception as e:
        logger.error(f"An error occurred during the Qdrant ingestion process: {e}", exc_info=True)

if __name__ == "__main__":
    main()