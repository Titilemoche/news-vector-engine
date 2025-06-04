import os
import sys
import json
import logging
import glob
from pathlib import Path

# Add project root to sys.path to allow imports if run directly
project_root_path = Path(__file__).resolve().parent.parent
if str(project_root_path) not in sys.path:
    sys.path.insert(0, str(project_root_path))

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers: # Check if handlers are already configured
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

EMBEDDINGS_DATA_DIR = project_root_path / "data" / "embeddings"
OUTPUT_DIR = project_root_path / "data" / "tensorflow_projector"
VECTORS_TSV_FILENAME = "vectors.tsv"
METADATA_TSV_FILENAME = "metadata.tsv"

# Define the headers for the metadata file
# Order matters for TensorFlow Projector if you want specific columns to appear first.
METADATA_HEADERS = ["title", "tags", "published", "persona", "link", "category", "enriched_summary"]

def sanitize_for_tsv(text: str | None) -> str:
    """Removes tabs and newlines from text to prevent breaking TSV format."""
    if text is None:
        return ""
    return str(text).replace("\t", " ").replace("\n", " ").replace("\r", " ")

def main():
    logger.info("===== Starting Export for TensorFlow Projector =====")

    if not EMBEDDINGS_DATA_DIR.is_dir():
        logger.error(f"Embeddings data directory not found: {EMBEDDINGS_DATA_DIR}. Exiting.")
        return

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured output directory exists: {OUTPUT_DIR}")
    except Exception as e:
        logger.error(f"Could not create output directory {OUTPUT_DIR}: {e}", exc_info=True)
        return

    vectors_file_path = OUTPUT_DIR / VECTORS_TSV_FILENAME
    metadata_file_path = OUTPUT_DIR / METADATA_TSV_FILENAME

    processed_count = 0

    try:
        with open(vectors_file_path, "w", encoding="utf-8") as vf, \
             open(metadata_file_path, "w", encoding="utf-8") as mf:
            
            # Write metadata header
            mf.write("\t".join(METADATA_HEADERS) + "\n")

            persona_folders = [d for d in EMBEDDINGS_DATA_DIR.iterdir() if d.is_dir()]
            if not persona_folders:
                logger.warning(f"No persona subdirectories found in {EMBEDDINGS_DATA_DIR}.")
                return

            for persona_dir in persona_folders:
                persona_name = persona_dir.name
                logger.info(f"Processing persona: {persona_name}")
                
                article_files = glob.glob(str(persona_dir / "*.json"))
                if not article_files:
                    logger.info(f"No embedding files found for persona {persona_name}. Skipping.")
                    continue
                
                for article_path_str in article_files:
                    article_path = Path(article_path_str)
                    try:
                        with open(article_path, "r", encoding="utf-8") as f:
                            article_data = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding JSON from {article_path}: {e}. Skipping.")
                        continue
                    except Exception as e:
                        logger.error(f"Error reading article file {article_path}: {e}. Skipping.", exc_info=True)
                        continue

                    vector = article_data.get("embedding")
                    if not vector or not isinstance(vector, list):
                        logger.warning(f"No valid 'embedding' field found in {article_path.name}. Skipping.")
                        continue
                    
                    # Write vector
                    vf.write("\t".join(map(str, vector)) + "\n")

                    # Prepare and write metadata
                    metadata_values = []
                    for header in METADATA_HEADERS:
                        value = article_data.get(header)
                        if header == "tags" and isinstance(value, list):
                            value = "; ".join(map(str, value)) # Join tags with "; "
                        elif header == "persona": # Special case to use the folder name
                            value = persona_name
                        
                        metadata_values.append(sanitize_for_tsv(value))
                    
                    mf.write("\t".join(metadata_values) + "\n")
                    processed_count += 1
                    if processed_count % 100 == 0:
                        logger.info(f"Processed {processed_count} articles...")

            logger.info(f"Successfully processed {processed_count} articles.")
            logger.info(f"Vectors saved to: {vectors_file_path}")
            logger.info(f"Metadata saved to: {metadata_file_path}")

    except IOError as e:
        logger.error(f"IOError during file writing: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

    logger.info("===== Export for TensorFlow Projector Finished =====")

if __name__ == "__main__":
    main()