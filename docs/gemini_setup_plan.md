# Plan: Foundation - Gemini LLM Client Setup

**Goal:** Establish a clean interface for interacting with the Gemini LLM and ensure API key management.

**Steps:**

1.  **Create `llm_client.py`:**
    *   Create a new file named `pipeline/llm_client.py`.
    *   Populate it with the following Python code:
        ```python
        # pipeline/llm_client.py
        import os
        import google.generativeai as genai

        # Configure Gemini API (tu dois avoir ta clé API dans une variable d'environnement)
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel("gemini-pro")

        def call_gemini(prompt: str) -> str:
            response = model.generate_content(prompt)
            return response.text.strip()
        ```

2.  **Manage Environment Variables:**
    *   **Check/Create `.env` file:**
        *   Verify if a `.env` file exists at the root of the project.
        *   If it doesn't exist, create it.
        *   Add or update the file to include the line: `GEMINI_API_KEY=your_secret_key_here` (The implementer will need to replace `your_secret_key_here` with the actual Gemini API key).
    *   **Update `.gitignore` (Recommended):**
        *   Check if `.gitignore` exists. If not, create it.
        *   Ensure `.env` is listed in the `.gitignore` file to prevent committing sensitive API keys.

3.  **Integrate Environment Variable Loading:**
    *   **Update `requirements.txt`:**
        *   Add `python-dotenv` to `requirements.txt`.
    *   **Modify `enrich_articles.py`:**
        *   Open the file `pipeline/enrich_articles.py`.
        *   Add the following import statement at the beginning of the file:
            ```python
            from dotenv import load_dotenv
            ```
        *   Add the following line at the beginning of the script (e.g., before other imports or at the start of the `main` function if one exists) to load the environment variables:
            ```python
            load_dotenv()
            ```

## Mermaid Diagram of the Plan:

```mermaid
graph TD
    A[Start: User Request for Gemini Wrapper] --> B{Phase 1: Gemini LLM Client Setup};

    subgraph B [Phase 1: Gemini LLM Client Setup]
        B1[Create pipeline/llm_client.py]
        B2[Manage Environment Variables]
        B3[Integrate .env Loading in enrich_articles.py]
    end

    B1 --> B1a[Write Python code for call_gemini()];
    B2 --> B2a[Check/Create .env file];
    B2a --> B2b[Add GEMINI_API_KEY to .env];
    B2 --> B2c[Update .gitignore with .env (Recommended)];
    B3 --> B3a[Add python-dotenv to requirements.txt];
    B3 --> B3b[Modify pipeline/enrich_articles.py];
    B3b --> B3c[Add 'from dotenv import load_dotenv'];
    B3b --> B3d[Add 'load_dotenv()' call];

    B1a --> C{Plan Complete for Phase 1};
    B2b --> C;
    B2c --> C;
    B3a --> C;
    B3c --> C;
    B3d --> C;