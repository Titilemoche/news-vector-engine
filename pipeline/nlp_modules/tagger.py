import sys
from pathlib import Path

# Add project root to sys.path to allow imports like 'from pipeline.llm_client import ...'
# when running this script directly for testing.
# This needs to be done BEFORE the attempt to import from 'pipeline'.
_project_root = Path(__file__).resolve().parent.parent.parent # Go up three levels: nlp_modules -> pipeline -> project_root
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

"""
Module: pipeline.nlp_modules.tagger
Status: Active - LLM Based
Description: This module tags articles with relevant keywords using the Gemini LLM.
             It uses a dedicated prompt defined in `pipeline/prompts.py`.
LLM Usage: Yes, via `call_gemini` from `pipeline.llm_client`.
TODO: - Consider adding persona-specific tagging prompts if needed.
      - Evaluate and refine the tagging prompt for optimal performance.
      - Implement more robust post-processing of tags if necessary (e.g., aliasing, stemming).
"""
import logging
from pipeline.llm_client import call_gemini
from pipeline.prompts import PROMPT_TAGGING_ADVANCED_EN as PROMPT_FOR_TAGGING 

logger = logging.getLogger(__name__)

def tag_article(text: str) -> list[str]:
    """
    Tags the given text using the Gemini LLM based on a predefined prompt.

    Args:
        text: The article text (cleaned or combined title + summary) to tag.

    Returns:
        A list of tags, or an empty list if no tags could be generated or an error occurred.
    """
    if not text or not text.strip():
        logger.warning("Tagger received empty or whitespace-only text. Returning no tags.")
        return []

    prompt = PROMPT_FOR_TAGGING.format(article_text=text)
    
    try:
        logger.info(f"Requesting tags from LLM. Text (first 150 chars): '{text[:150]}...'")
        response_text = call_gemini(prompt)
        logger.info(f"LLM response for tagging: '{response_text}'")

        if response_text:
            # Parse the comma-separated string into a list of tags
            tags = [tag.strip() for tag in response_text.split(',') if tag.strip()]
            
            # Basic post-processing: lowercase and remove duplicates
            processed_tags = sorted(list(set(tag.lower() for tag in tags)))
            
            logger.info(f"Generated tags: {processed_tags}")
            return processed_tags
        else:
            logger.warning("LLM returned an empty response for tagging.")
            return []
    except Exception as e:
        logger.error(f"Error during LLM call for tagging: {e}", exc_info=True)
        return ["error_tagging_llm"] 

if __name__ == '__main__':
    # This block is for direct testing of this module.
    # Ensure GEMINI_API_KEY is set in your .env file for this test to run.
    # The sys.path modification at the top of the file should allow this to run
    # from the project root (e.g., python pipeline/nlp_modules/tagger.py)
    # or even when this file is the current directory (e.g., cd pipeline/nlp_modules; python tagger.py)
    
    logging.basicConfig(level=logging.INFO) # Configure logging for the test
    
    sample_text_en = """
    Google's DeepMind division today announced a breakthrough in AI-driven weather forecasting with their new model, GraphCast. 
    This model, detailed in a Science paper, can predict weather conditions up to 10 days in advance with greater accuracy 
    and speed than traditional numerical weather prediction systems. GraphCast leverages graph neural networks and was trained 
    on decades of historical weather data. Key figures like Remi Lam from DeepMind highlighted its potential to revolutionize 
    how we prepare for extreme weather events.
    """
    print("Attempting to generate sample tags...")
    tags_en = tag_article(sample_text_en)
    print(f"Sample Tags (EN): {tags_en}")