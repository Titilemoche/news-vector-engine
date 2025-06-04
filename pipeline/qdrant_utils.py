import os
import logging
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct, PayloadSchemaType

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        handlers=[
            logging.StreamHandler(os.sys.stdout)
        ]
    )

# Load environment variables from .env file (assuming .env is in the project root)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(project_root, ".env"))

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") # For Qdrant Cloud or secured instances

COLLECTION_NAME = "news_vectors"
VECTOR_SIZE = 1536  # Corresponds to text-embedding-3-small
DISTANCE_METRIC = Distance.COSINE

def get_qdrant_client():
    """Initializes and returns a Qdrant client."""
    try:
        if QDRANT_API_KEY:
            client = QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT, # Or https_port if using https
                api_key=QDRANT_API_KEY,
                # prefer_grpc=True, # Uncomment if you prefer gRPC and have it configured
            )
            logger.info(f"Successfully connected to Qdrant Cloud at {QDRANT_HOST} (secured).")
        else:
            client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            logger.info(f"Successfully connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT} (unsecured).")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}", exc_info=True)
        raise

def create_collection_if_not_exists(client: QdrantClient):
    """
    Creates the specified collection in Qdrant if it doesn't already exist,
    and sets up payload indexing.
    """
    try:
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        if COLLECTION_NAME not in collection_names:
            logger.info(f"Collection '{COLLECTION_NAME}' not found. Creating it...")
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=DISTANCE_METRIC)
            )
            logger.info(f"Collection '{COLLECTION_NAME}' created successfully.")

            # Create payload indexes
            # Note: For Qdrant versions before 1.2.0, use client.update_collection for creating indexes.
            # For newer versions, client.create_payload_index is preferred.
            # The client handles this internally, but good to be aware.

            logger.info(f"Creating payload indexes for collection '{COLLECTION_NAME}'...")
            client.create_payload_index(collection_name=COLLECTION_NAME, field_name="source_persona", field_schema=PayloadSchemaType.KEYWORD)
            client.create_payload_index(collection_name=COLLECTION_NAME, field_name="content_type", field_schema=PayloadSchemaType.KEYWORD)
            client.create_payload_index(collection_name=COLLECTION_NAME, field_name="category", field_schema=PayloadSchemaType.KEYWORD)
            client.create_payload_index(collection_name=COLLECTION_NAME, field_name="tags", field_schema=PayloadSchemaType.KEYWORD) # For lists of keywords
            client.create_payload_index(collection_name=COLLECTION_NAME, field_name="published", field_schema=PayloadSchemaType.DATETIME)
            # Optional: Index 'link' if it's used as a filterable ID
            # client.create_payload_index(collection_name=COLLECTION_NAME, field_name="link", field_schema=PayloadSchemaType.KEYWORD)
            logger.info(f"Payload indexes created for collection '{COLLECTION_NAME}'.")
        else:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists. Skipping creation.")
            # Potentially, you might want to verify existing indexes here if needed.

    except Exception as e:
        logger.error(f"Error during collection creation or index setup for '{COLLECTION_NAME}': {e}", exc_info=True)
        raise

if __name__ == '__main__':
    # Example usage (for testing this module directly)
    try:
        qdrant_client = get_qdrant_client()
        if qdrant_client:
            create_collection_if_not_exists(qdrant_client)
            logger.info("Qdrant utils setup check completed.")
    except Exception as e:
        logger.error(f"Failed to run Qdrant utils setup check: {e}")