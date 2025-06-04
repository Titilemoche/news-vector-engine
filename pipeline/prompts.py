PROMPT_SUMMARY = """
Tu es un assistant spécialisé en veille IA.
Résume l'article suivant en 5 phrases maximum.

Article :
{article}
"""

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
Return only a comma-separated list of concise tags, without comments or explanations.

Article Text:
{article_text}

Tags:
"""
