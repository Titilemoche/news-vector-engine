import sys
from pathlib import Path

# Add project root to sys.path to allow imports like 'from pipeline.nlp_modules import ...'
# This assumes the script is in 'news-vector-engine/pipeline/'
# and the project root is 'news-vector-engine/'
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
import json
import logging
from pathlib import Path
import glob # Added for finding feed files
from dotenv import load_dotenv
load_dotenv()
from pipeline.nlp_modules import summarize, cleaner, tagger, classifier, entities # Expanded NLP modules

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting article enrichment process...")

# Find all raw feed JSON files
feed_file_paths = glob.glob("data/feeds_raw/*.json")

if not feed_file_paths:
    logger.warning("No raw feed files found in data/feeds_raw/. Exiting enrichment process.")
else:
    logger.info(f"Found {len(feed_file_paths)} raw feed file(s) to process: {feed_file_paths}")

    for feed_file_path_str in feed_file_paths:
        feed_file_path = Path(feed_file_path_str)
        # Extract persona name from filename (e.g., "persona_ai_builder" from "persona_ai_builder.json")
        persona = feed_file_path.stem
        
        logger.info(f"\n===== Processing persona: {persona} from file: {feed_file_path} =====")

        current_input_file = feed_file_path
        current_output_dir = Path(f"data/enriched/{persona}")
        
        logger.info(f"Input file for {persona}: {current_input_file}")
        logger.info(f"Output directory for {persona}: {current_output_dir}")

        try:
            current_output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured output directory exists: {current_output_dir}")
        except Exception as e:
            logger.error(f"Could not create output directory {current_output_dir}: {e}", exc_info=True)
            logger.warning(f"Skipping persona {persona} due to directory creation error.")
            continue # Skip to the next persona/feed file

        # Load articles for the current persona
        articles = []
        try:
            logger.info(f"Loading articles from {current_input_file} for persona {persona}...")
            with open(current_input_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
            logger.info(f"Successfully loaded {len(articles)} articles for persona {persona}.")
        except FileNotFoundError:
            logger.error(f"Input file not found: {current_input_file} for persona {persona}. Skipping this persona.")
            continue # Skip to next persona
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {current_input_file} for persona {persona}: {e}", exc_info=True)
            logger.warning(f"Skipping persona {persona} due to JSON decoding error.")
            continue # Skip to next persona
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading articles from {current_input_file} for persona {persona}: {e}", exc_info=True)
            logger.warning(f"Skipping persona {persona} due to an unexpected error during loading.")
            continue # Skip to next persona

        if not articles:
            logger.warning(f"No articles loaded for persona {persona}. Continuing to next persona if any.")
            continue # Skip to the next feed file

        logger.info(f"Starting NLP enrichment for {len(articles)} articles for persona {persona}...")
        for i, article_data in enumerate(articles):
            article_title_for_log = article_data.get('title', 'N/A')
            logger.info(f"--- Processing article {i+1}/{len(articles)}: '{article_title_for_log}' (Persona: {persona}) ---")

            # a. Extract Text Fields
            title = article_data.get('title', '')
            summary_raw = article_data.get('summary', '') # Original summary from feed

            # b. Construct Input Text (as per user instruction)
            input_text = f"{title}\n\n{summary_raw}" if summary_raw else title
            logger.debug(f"Input text for NLP (first 100 chars): '{input_text[:100]}...'")

            # c. Clean Text
            # logger.info(f"Calling cleaner.clean_text for: {title}")
            cleaned_text = cleaner.clean_text(input_text)
            # logger.info(f"Text cleaning complete for: {title}")

            # d. Tag Article
            # logger.info(f"Calling tagger.tag_article for: {title}")
            tags = tagger.tag_article(cleaned_text)
            # logger.info(f"Tagging complete for: {title}")
            # Post-filter tags
            if isinstance(tags, list): # Ensure tags is a list before list comprehension
                tags = [tag for tag in tags if isinstance(tag, str) and len(tag) < 50 and "no " not in tag.lower()]
            elif isinstance(tags, str): # Handle case where tags might be a single string
                if len(tags) < 50 and "no " not in tags.lower():
                    tags = [tags] # Convert to list if valid
                else:
                    tags = [] # Discard if invalid
            else:
                logger.warning(f"Tags for article '{title}' are not a list or string, but {type(tags)}. Setting to empty list.")
                tags = [] # Default to empty list if type is unexpected

            # e. Classify Article
            # logger.info(f"Calling classifier.classify_article for: {title}")
            category = classifier.classify_article(cleaned_text)
            # logger.info(f"Classification complete for: {title}")

            # f. Extract Entities
            # logger.info(f"Calling entities.extract_entities for: {title}")
            extracted_entities = entities.extract_entities(cleaned_text)
            # logger.info(f"Entity extraction complete for: {title}")

            # g. Summarize Text (using cleaned text)
            # logger.info(f"Calling summarize.run for (enriched summary): {title}")
            enriched_summary = summarize.run(cleaned_text) # summarize.run has its own logging
            # logger.info(f"Enriched summarization complete for: {title}")

            # Structure the output JSON
            result = {
                "title": title,
                "link": article_data.get("link", ""),
                "published": article_data.get("published", None), # Added published date
                "source_persona": persona,
                "original_summary": summary_raw,
                # "input_text_for_nlp": input_text, # Removed as per user request (often redundant)
                "cleaned_text": cleaned_text,
                "enriched_summary": enriched_summary,
                "tags": tags,
                "category": category,
                "entities": extracted_entities,
                "text_for_embedding": f"{title}\n\n{enriched_summary}\n\nTags: {', '.join(tags) if isinstance(tags, list) else ''}" # Added text_for_embedding
                # Optional: "processing_timestamp": datetime.utcnow().isoformat() (requires import datetime)
            }
            logger.debug(f"Result structure prepared for '{title}': {json.dumps(result, indent=2, ensure_ascii=False)[:200]}...")

            # Sanitize title for filename
            slug_title = title if title else "untitled_article"
            # Basic replacements
            slug = slug_title.replace(" ", "_").replace("/", "-").replace(":", "_").replace("?", "").replace("\\", "-")
            # Remove other potentially problematic characters
            slug = slug.replace("*", "").replace("<", "").replace(">", "").replace("|", "").replace("\"", "")
            
            # Keep only alphanumeric, underscore, hyphen
            valid_chars = []
            for char_val in slug:
                if char_val.isalnum() or char_val in ['_', '-']:
                    valid_chars.append(char_val)
            slug = "".join(valid_chars)

            if not slug: # Handle cases where title is all special characters or empty after sanitization
                slug = f"article_{i+1}" # Use article index as fallback
            
            # Truncate slug to avoid overly long filenames (e.g., max 100 chars for the name part)
            output_filename = f"{slug[:100]}.json"
            output_path = current_output_dir / output_filename
            
            logger.info(f"Attempting to save enriched article to: {output_path}")
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                logger.info(f"✅ Article enriched and saved: {output_path}")
            except Exception as e:
                logger.error(f"Error saving enriched article to {output_path}: {e}", exc_info=True)
        
        logger.info(f"--- Finished processing all {len(articles)} articles for persona {persona}. ---\n")

logger.info("===== Article enrichment process finished. =====")
