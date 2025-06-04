import logging
from pipeline.prompts import PROMPT_SUMMARY
from pipeline.llm_client import call_gemini

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

def run(article: str) -> str:
    logger.info(f"Summarize function called for article of length: {len(article)}")
    if not article or article.isspace():
        logger.warning("Empty or whitespace-only article received. Returning empty summary.")
        return ""
    
    prompt = PROMPT_SUMMARY.format(article=article)
    logger.debug(f"Prompt created: {prompt[:200]}...") # Log first 200 chars of prompt
    
    try:
        summary = call_gemini(prompt)
        logger.info(f"Summary generated: {summary[:200]}...") # Log first 200 chars of summary
        return summary
    except Exception as e:
        logger.error(f"Error during call_gemini: {e}", exc_info=True)
        return "Error generating summary."

if __name__ == "__main__":
    logger.info("Executing summarize.py directly for testing.")
    sample_article_text = """
    This is a sample news article for testing the summarization module.
    It contains several sentences and aims to demonstrate how the logging
    and summarization functions work together. The Gemini LLM is expected
    to provide a concise summary of this text. We are checking if the logs
    appear as expected.
    """
    logger.info(f"Test article: {sample_article_text}")
    summary_result = run(sample_article_text)
    logger.info(f"Test summary result: {summary_result}")
