# Plan: LLM-Based Tagging Implementation (2025-05-29)

This document outlines the plan for implementing an LLM-based tagging system using Gemini for the `news-vector-engine` project.

## 1. Advanced Prompt Engineering for Tagging

The quality of tags heavily depends on the prompt.

*   **Key Prompt Elements:**
    *   **Role Definition:** e.g., "You are an expert news analyst..."
    *   **Task Specificity:** Request "tags" or "keywords," specify quantity (e.g., 5-7), and types (technologies, companies, topics).
    *   **Output Format:** Request a clear, parsable format (e.g., comma-separated string).
    *   **Language:** Specify English or French.
    *   **Conciseness & Relevance:** Emphasize these qualities.

*   **Example Enhanced Prompt (to be added to `pipeline/prompts.py`):**
    *(Using the English version as the primary example here, the French version is also available in the discussion history if preferred)*
    ```python
    # In pipeline/prompts.py

    PROMPT_TAGGING_ADVANCED_EN = """
    You are an expert AI and technology news analyst. Your task is to extract the most relevant and concise tags from the provided article text.

    Please provide:
    1.  Up to 5-7 primary tags covering the main topics, technologies, and key concepts.
    2.  Up to 3 tags for any specific companies or organizations central to the article.
    3.  Up to 2 tags for any notable individuals mentioned, if they are key to the article's focus.

    Guidelines:
    - Tags should be in English.
    - Tags should be concise (1-3 words ideally).
    - Prioritize relevance and specificity. Avoid overly broad tags.
    - If a company or person is only mentioned in passing, do not tag them.

    Return all tags as a single comma-separated string.

    Article Text:
    {article_text}

    Tags:
    """
    ```

## 2. Code Implementation in `pipeline/nlp_modules/tagger.py`

Update the existing stub file to use the LLM client and the new prompt.

*   **Proposed Code for `pipeline/nlp_modules/tagger.py`:**
    ```python
    # pipeline/nlp_modules/tagger.py
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
    # Assuming PROMPT_TAGGING_ADVANCED_EN will be added to prompts.py
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
        logging.basicConfig(level=logging.INFO)
        sample_text_en = """
        Google's DeepMind division today announced a breakthrough in AI-driven weather forecasting with their new model, GraphCast. 
        This model, detailed in a Science paper, can predict weather conditions up to 10 days in advance with greater accuracy 
        and speed than traditional numerical weather prediction systems. GraphCast leverages graph neural networks and was trained 
        on decades of historical weather data. Key figures like Remi Lam from DeepMind highlighted its potential to revolutionize 
        how we prepare for extreme weather events.
        """
        tags_en = tag_article(sample_text_en)
        print(f"Sample Tags (EN): {tags_en}")
    ```

## 3. Output Parsing & Post-Processing

*   **Parsing:** Split comma-separated string from LLM.
*   **Cleaning:** Strip whitespace, filter empty strings.
*   **Normalization:** Convert to lowercase, remove duplicates, sort.
*   **Optional Further Post-Processing:** Synonym consolidation, max tag limits, denylist filtering.

## 4. Important Considerations

*   **API Costs and Latency:** Be mindful of these for each article.
*   **Error Handling:** Implement robust error handling for API calls.
*   **Persona-Specific Prompts:** If needed, define multiple prompts and modify `tag_article` to select based on persona.
*   **Token Limits:** Ensure input text fits within Gemini's context window. Use summaries or truncated text if necessary.
*   **Evaluation:** Continuously evaluate and refine tag quality and prompt effectiveness.

This plan provides a comprehensive approach to implementing LLM-based tagging.