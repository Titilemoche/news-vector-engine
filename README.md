# 🚀 news-vector-engine

**`news-vector-engine` est une pipeline d'ingestion et de traitement de données conçue pour agréger des articles d'actualité, les enrichir grâce à des techniques de Traitement Naturel du Langage (NLP) avancées, les vectoriser et permettre leur interrogation via une base de données vectorielle.**

L'objectif principal est de fournir un flux de travail automatisé pour transformer des articles bruts en informations structurées et sémantiquement riches, prêtes à être explorées et analysées, notamment par des "personas" ou agents vectoriels spécialisés.

Ce projet s'adresse aux développeurs, chercheurs et analystes de données intéressés par :
- La veille technologique et informationnelle automatisée.
- La création de bases de connaissances sémantiques.
- L'expérimentation avec les modèles de langage (LLM) pour l'enrichissement de texte.
- L'utilisation de bases de données vectorielles pour la recherche sémantique.

## 📜 Table des Matières

1.  [✨ Présentation du Projet](#-news-vector-engine)
2.  [📂 Structure du Projet](#-structure-du-projet)
3.  [🛠️ Technologies Utilisées](#️-technologies-utilisées)
4.  [⚙️ Architecture Globale](#️-architecture-globale)
5.  [🚀 Démarrage Rapide (Installation et Lancement)](#-démarrage-rapide-installation-et-lancement)
    *   [Prérequis](#prérequis)
    *   [Installation](#installation)
    *   [Configuration](#configuration)
    *   [Exécution du Pipeline](#exécution-du-pipeline)
6.  [🔁 Détail du Pipeline de Données](#-détail-du-pipeline-de-données)
    *   [1. Scraping des Flux RSS](#1-scraping-des-flux-rss)
    *   [2. Enrichissement des Articles](#2-enrichissement-des-articles)
    *   [3. Vectorisation des Articles](#3-vectorisation-des-articles)
    *   [4. Indexation dans Qdrant](#4-indexation-dans-qdrant)
    *   [5. Export pour TensorFlow Projector](#5-export-pour-tensorflow-projector)
7.  [🧠 Fonctionnement des Personas](#-fonctionnement-des-personas)
8.  [🔍 Interrogation de la Base Vectorielle (Qdrant)](#-interrogation-de-la-base-vectorielle-qdrant)
9.  [🧪 Exemples et Résultats (À venir)](#-exemples-et-résultats-à-venir)
10. [🤝 Contribuer au Projet](#-contribuer-au-projet)
11. [📄 Licence](#-licence)
12. [🙏 Remerciements](#-remerciements)

## 📂 Structure du Projet

Voici l'arborescence principale du projet et la description de chaque répertoire/fichier clé :

```
news-vector-engine/
├── .env                   # Variables d'environnement (API clés, etc.) - NON VERSIONNÉ
├── .gitignore             # Fichiers et dossiers ignorés par Git
├── LICENSE                # Licence du projet (MIT)
├── README.md              # Ce fichier
├── requirements.txt       # Dépendances Python du projet
│
├── config/                # Fichiers de configuration
│   └── sources.json       # Configuration des sources de données (flux RSS par persona)
│
├── data/                  # Données générées et traitées par le pipeline
│   ├── feeds_raw/         # Articles bruts scrapés des flux RSS (JSON par persona)
│   ├── enriched/          # Articles enrichis par les modules NLP (JSON par persona et par article)
│   ├── embeddings/        # Articles avec leurs embeddings vectoriels (JSON par persona et par article)
│   └── tensorflow_projector/ # Données exportées pour TensorFlow Projector (vectors.tsv, metadata.tsv)
│
> **Note :** Les sous-répertoires de `data/` (`feeds_raw/`, `enriched/`, `embeddings/`, `tensorflow_projector/`) sont inclus dans le dépôt avec une structure vide (maintenue par des fichiers `.gitkeep` que nous allons créer). Ils seront remplis avec les données générées uniquement lorsque vous exécuterez les scripts du pipeline. Aucune donnée d'article réelle n'est versionnée dans ces répertoires.
│
├── docs/                  # Documentation additionnelle, plans d'architecture, spécifications
│
├── personas/              # Configuration spécifique aux personas (prévu pour évolutions futures)
│   └── personas_config.json # Fichier de configuration détaillé par persona (actuellement vide)
│
└── pipeline/              # Scripts principaux du pipeline de traitement
    ├── __init__.py
    ├── scrape_feed.py     # Script de scraping des flux RSS
    ├── enrich_articles.py # Script d'orchestration de l'enrichissement NLP
    ├── vectorize_articles.py # Script de génération des embeddings vectoriels
    ├── ingest_to_qdrant.py # Script d'ingestion des données dans Qdrant
    ├── export_for_tensorflow_projector.py # Script d'export pour TensorFlow Projector
    ├── llm_client.py      # Client pour interagir avec les API LLM (Gemini)
    ├── prompts.py         # Définitions des prompts pour les LLM
    ├── qdrant_utils.py    # Fonctions utilitaires pour Qdrant (client, création de collection)
    │
    └── nlp_modules/       # Modules spécifiques pour les tâches NLP
        ├── __init__.py
        ├── cleaner.py     # Module de nettoyage de texte (actuellement placeholder)
        ├── summarize.py   # Module de résumé de texte via LLM
        ├── tagger.py      # Module de tagging (actuellement stub, prévu pour LLM)
        ├── classifier.py  # Module de classification (actuellement stub)
        └── entities.py    # Module d'extraction d'entités (actuellement stub)
```

## 🛠️ Technologies Utilisées

Ce projet s'appuie sur les technologies et librairies suivantes :

-   **Langage :** Python 3.x
-   **Gestion des dépendances :** `pip` et `requirements.txt`
-   **Manipulation de données :**
    -   `feedparser` : Pour parser les flux RSS.
    -   `json` : Pour la manipulation des fichiers de données intermédiaires.
-   **Variables d'environnement :**
    -   `python-dotenv` : Pour charger les configurations depuis le fichier `.env`.
-   **Modèles de Langage (LLM) :**
    -   `google-generativeai` : Pour interagir avec l'API Gemini (summarization).
    -   `openai` : Pour générer les embeddings vectoriels (modèle `text-embedding-3-small`).
-   **Base de Données Vectorielle :**
    -   `qdrant-client` : Pour interagir avec la base de données vectorielle Qdrant (stockage et recherche sémantique).
-   **Visualisation (Prévu) :**
    -   TensorFlow Projector : Pour la visualisation 3D des embeddings (via export TSV).
-   **Qualité de code et outillage (Recommandé pour contribution) :**
    -   Linters (e.g., Flake8, Pylint)
    -   Formatters (e.g., Black, isort)

## ⚙️ Architecture Globale

Le schéma ci-dessous illustre le flux de données global du projet `news-vector-engine` :

```mermaid
graph TD
    A[Flux RSS Sources (.json)] --> B(pipeline/scrape_feed.py);
    B --> C[data/feeds_raw/*.json];
    C --> D(pipeline/enrich_articles.py);
    D -- Utilise --> E(pipeline/nlp_modules/*);
    E -- Notamment --> F(pipeline/nlp_modules/summarize.py);
    F -- Appelle --> G(pipeline/llm_client.py);
    G -- Interagit avec --> H[API Google Gemini];
    D --> I[data/enriched/{persona}/*.json];
    I --> J(pipeline/vectorize_articles.py);
    J -- Interagit avec --> K[API OpenAI Embeddings];
    J --> L[data/embeddings/{persona}/*.json];
    L --> M(pipeline/ingest_to_qdrant.py);
    M -- Utilise --> N(pipeline/qdrant_utils.py);
    N -- Interagit avec --> O[Base de Données Qdrant];
    L --> P(pipeline/export_for_tensorflow_projector.py);
    P --> Q[data/tensorflow_projector/*.tsv];
    Q --> R[Visualisation TensorFlow Projector];

    subgraph "Configuration"
        A
        H
        K
        O
    end

    subgraph "Pipeline de Traitement"
        B
        D
        E
        F
        G
        J
        M
        N
        P
    end

    subgraph "Stockage Intermédiaire des Données"
        C
        I
        L
        Q
    end
```

## 🚀 Démarrage Rapide (Installation et Lancement)

Suivez ces étapes pour configurer et lancer le projet en local.

### Prérequis

-   Python 3.8 ou supérieur.
-   Un compte Google Cloud avec une clé API pour Gemini (pour les résumés).
-   Un compte OpenAI avec une clé API (pour la génération des embeddings).
-   Une instance Qdrant en cours d'exécution (locale via Docker ou sur Qdrant Cloud).
    -   Pour Docker : `docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant`

### Installation

1.  **Clonez le dépôt :**
    ```bash
    git clone <URL_DU_DEPOT_GIT>
    cd news-vector-engine
    ```

2.  **Créez et activez un environnement virtuel (recommandé) :**
    ```bash
    python -m venv venv
    # Sur macOS/Linux
    source venv/bin/activate
    # Sur Windows
    .\venv\Scripts\activate
    ```

3.  **Installez les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Un fichier `.env.example` est fourni à la racine du projet.** Copiez-le et renommez la copie en `.env`.
2.  **Ajoutez vos clés API et configurations Qdrant dans le fichier `.env` :**

    ```env
    # Clé API pour Google Gemini (utilisée par pipeline/llm_client.py)
    GEMINI_API_KEY="VOTRE_CLE_API_GOOGLE_GEMINI"
    # ou GOOGLE_API_KEY="VOTRE_CLE_API_GOOGLE_GEMINI"

    # Clé API pour OpenAI (utilisée par pipeline/vectorize_articles.py)
    OPENAI_API_KEY="VOTRE_CLE_API_OPENAI"

    # Configuration Qdrant (utilisée par pipeline/qdrant_utils.py)
    # Pour une instance Qdrant locale (par défaut si non spécifié pour le cloud)
    QDRANT_HOST="localhost"
    QDRANT_PORT=6333

    # Pour Qdrant Cloud (décommentez et adaptez si besoin)
    # QDRANT_HOST="VOTRE_URL_CLUSTER_QDRANT"
    # QDRANT_PORT=6333 # ou 6334 pour gRPC/HTTPS
    # QDRANT_API_KEY="VOTRE_CLE_API_QDRANT" # Si authentification activée
    ```

    Assurez-vous que votre instance Qdrant est accessible avec ces paramètres.

### Exécution du Pipeline

Les scripts du pipeline peuvent être exécutés séquentiellement. Chaque script effectue une étape spécifique du traitement des données.

1.  **Scraping des flux RSS :**
    Récupère les articles bruts depuis les sources définies dans [`config/sources.json`](config/sources.json:1) et les sauvegarde dans [`data/feeds_raw/`](data/feeds_raw/.gitkeep:1).
    ```bash
    python pipeline/scrape_feed.py
    ```

2.  **Enrichissement des articles :**
    Traite les articles bruts, applique les modules NLP (nettoyage, résumé LLM, tagging stub, etc.) et sauvegarde les résultats dans [`data/enriched/`](data/enriched/persona_ai_builder/_Liger_GRPO_meets_TRL.json:1).
    ```bash
    python pipeline/enrich_articles.py
    ```

3.  **Vectorisation des articles (Création des Embeddings) :**
    Génère les embeddings vectoriels pour les articles enrichis en utilisant l'API OpenAI et les sauvegarde dans [`data/embeddings/`](data/embeddings/.gitkeep:1).
    ```bash
    python pipeline/vectorize_articles.py
    ```

4.  **Indexation dans Qdrant :**
    Ingère les articles (avec leurs embeddings et métadonnées) dans la collection Qdrant spécifiée.
    ```bash
    python pipeline/ingest_to_qdrant.py
    ```

5.  **Export pour TensorFlow Projector (Optionnel) :**
    Exporte les vecteurs et métadonnées au format TSV pour visualisation avec TensorFlow Projector. Les fichiers sont sauvegardés dans [`data/tensorflow_projector/`](data/tensorflow_projector/metadata.tsv:1).
    ```bash
    python pipeline/export_for_tensorflow_projector.py
    ```

Chaque script utilise le module `logging` pour afficher sa progression et les éventuels problèmes dans la console.

## 🔁 Détail du Pipeline de Données

### 1. Scraping des Flux RSS

-   **Script :** [`pipeline/scrape_feed.py`](pipeline/scrape_feed.py:1)
-   **Entrée :** Configuration des sources dans [`config/sources.json`](config/sources.json:1).
    ```json
    [
      {
        "persona_id": "persona_ai_builder",
        "source_name": "Hugging Face Blog",
        "type": "rss",
        "url": "https://huggingface.co/blog/feed.xml"
      }
      // ... autres sources
    ]
    ```
-   **Processus :** Utilise `feedparser` pour lire chaque URL de flux RSS. Extrait le titre, le lien, la date de publication, le résumé brut, et associe le `persona_id` et `source_name`.
-   **Sortie :** Fichiers JSON (un par `persona_id`) dans [`data/feeds_raw/`](data/feeds_raw/.gitkeep:1), contenant une liste d'articles bruts.

### 2. Enrichissement des Articles

-   **Script :** [`pipeline/enrich_articles.py`](pipeline/enrich_articles.py:1)
-   **Entrée :** Fichiers JSON de [`data/feeds_raw/`](data/feeds_raw/.gitkeep:1).
-   **Processus :**
    1.  Pour chaque article, combine le titre et le résumé brut.
    2.  **Nettoyage (`pipeline/nlp_modules/cleaner.py`) :** Actuellement un placeholder, retourne le texte original. Prévu pour des opérations comme la suppression de HTML, la normalisation, etc.
    3.  **Tagging (`pipeline/nlp_modules/tagger.py`) :** Actuellement un stub retournant des tags statiques. Un prompt avancé (`PROMPT_TAGGING_ADVANCED_EN` dans [`pipeline/prompts.py`](pipeline/prompts.py:1)) est défini pour une future implémentation LLM.
    4.  **Classification (`pipeline/nlp_modules/classifier.py`) :** Actuellement un stub retournant une catégorie statique.
    5.  **Extraction d'Entités (`pipeline/nlp_modules/entities.py`) :** Actuellement un stub retournant des entités statiques.
    6.  **Résumé LLM (`pipeline/nlp_modules/summarize.py`) :** Utilise `call_gemini` (via [`pipeline/llm_client.py`](pipeline/llm_client.py:1)) et `PROMPT_SUMMARY` pour générer un résumé concis.
    7.  Crée un champ `text_for_embedding` combinant le titre, le résumé enrichi et les tags.
-   **Sortie :** Fichiers JSON individuels pour chaque article enrichi dans [`data/enriched/{persona_name}/`](data/enriched/persona_ai_builder/_Liger_GRPO_meets_TRL.json:1). Chaque fichier contient l'article original enrichi avec les nouvelles métadonnées (résumé LLM, tags, catégorie, entités, texte pour embedding).

### 3. Vectorisation des Articles

-   **Script :** [`pipeline/vectorize_articles.py`](pipeline/vectorize_articles.py:1)
-   **Entrée :** Fichiers JSON d'articles enrichis de [`data/enriched/`](data/enriched/persona_ai_builder/_Liger_GRPO_meets_TRL.json:1).
-   **Processus :**
    1.  Pour chaque article, récupère le champ `text_for_embedding`.
    2.  Appelle l'API OpenAI Embeddings (modèle `text-embedding-3-small`, configurable) pour générer un vecteur d'embedding.
    3.  Ajoute le vecteur d'embedding à l'objet JSON de l'article.
-   **Sortie :** Fichiers JSON (un par article) dans [`data/embeddings/{persona_name}/`](data/embeddings/.gitkeep:1), contenant les articles enrichis plus leur vecteur d'embedding.

### 4. Indexation dans Qdrant

-   **Script :** [`pipeline/ingest_to_qdrant.py`](pipeline/ingest_to_qdrant.py:1)
-   **Utilitaires :** [`pipeline/qdrant_utils.py`](pipeline/qdrant_utils.py:1)
-   **Entrée :** Fichiers JSON avec embeddings de [`data/embeddings/`](data/embeddings/.gitkeep:1).
-   **Processus :**
    1.  Se connecte au client Qdrant (configuré via `.env`).
    2.  S'assure que la collection (`news_vectors`, taille de vecteur 1536, distance Cosine) existe et crée les index de payload nécessaires (pour `source_persona`, `content_type`, `category`, `tags`, `published`) si ce n'est pas déjà fait.
    3.  Pour chaque article :
        -   Génère un ID de point stable (UUIDv5 basé sur le lien de l'article).
        -   Prépare le payload (toutes les métadonnées de l'article sauf l'embedding). La date de publication est normalisée au format ISO 8601. Les tags sont assurés d'être une liste de chaînes.
        -   Ingère les points (ID, vecteur, payload) dans Qdrant par lots.
-   **Sortie :** Données indexées dans la collection Qdrant.

### 5. Export pour TensorFlow Projector

-   **Script :** [`pipeline/export_for_tensorflow_projector.py`](pipeline/export_for_tensorflow_projector.py:1)
-   **Entrée :** Fichiers JSON avec embeddings de [`data/embeddings/`](data/embeddings/.gitkeep:1).
-   **Processus :**
    1.  Crée deux fichiers TSV : `vectors.tsv` et `metadata.tsv`.
    2.  `metadata.tsv` inclut un en-tête défini (`title`, `tags`, `published`, `persona`, `link`, `category`, `enriched_summary`).
    3.  Pour chaque article, écrit son vecteur dans `vectors.tsv` et ses métadonnées correspondantes dans `metadata.tsv`. Les valeurs sont nettoyées pour le format TSV.
-   **Sortie :** Fichiers `vectors.tsv` et `metadata.tsv` dans [`data/tensorflow_projector/`](data/tensorflow_projector/metadata.tsv:1).

## 🧠 Fonctionnement des Personas

Dans ce projet, un "persona" représente un profil d'intérêt ou un agent vectoriel spécialisé. Actuellement, les personas sont principalement utilisés pour :

1.  **Organiser les sources de données :** Dans [`config/sources.json`](config/sources.json:1), chaque flux RSS est associé à un `persona_id`. Cela permet de collecter des articles pertinents pour des thèmes ou des perspectives spécifiques (par exemple, "AI Builder", "AI Creator", "AI Investor").
2.  **Segmenter les données traitées :** Les données brutes, enrichies et vectorisées sont stockées dans des sous-répertoires nommés d'après le `persona_id` (e.g., `data/feeds_raw/persona_ai_builder.json`).
3.  **Filtrage potentiel dans Qdrant :** Le champ `source_persona` est indexé dans Qdrant, ce qui permettra à l'avenir de filtrer les recherches vectorielles par persona.

**Évolutions futures pour les personas :**

-   Le fichier [`personas/personas_config.json`](personas/personas_config.json:1) (actuellement vide) est prévu pour définir des configurations plus fines par persona, telles que :
    -   Des mots-clés spécifiques pour affiner le filtrage ou le scoring des articles.
    -   Des prompts LLM personnalisés pour le résumé ou le tagging, adaptés au style ou aux besoins du persona.
    -   Des stratégies de requêtage spécifiques pour la base vectorielle.

L'idée est que chaque persona puisse interagir avec la base de connaissances vectorielle d'une manière qui lui est propre, en se concentrant sur les informations les plus pertinentes pour son domaine d'expertise ou d'intérêt.

## 🔍 Interrogation de la Base Vectorielle (Qdrant)

Une fois les articles vectorisés et indexés dans Qdrant, vous pouvez effectuer des recherches sémantiques pour trouver des articles similaires à une requête donnée ou explorer les données.

Actuellement, le projet ne fournit pas de script dédié pour l'interrogation, mais cela peut être fait en utilisant le client Qdrant en Python. Voici un exemple conceptuel de la manière dont vous pourriez interroger la base :

```python
# Exemple conceptuel de requête Qdrant (à adapter dans un script dédié)
from qdrant_client import QdrantClient, models # Ajout de models pour Filter
from openai import OpenAI # Pour générer l'embedding de la requête

# Charger les configurations (API Keys, Qdrant host)
# ... (similaire à qdrant_utils.py ou vectorize_articles.py)

# Initialiser les clients
qdrant_client = QdrantClient(host="localhost", port=6333) # ou config cloud
openai_client = OpenAI(api_key="VOTRE_CLE_API_OPENAI")

COLLECTION_NAME = "news_vectors"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

def get_query_embedding(text: str):
    response = openai_client.embeddings.create(input=[text], model=OPENAI_EMBEDDING_MODEL)
    return response.data[0].embedding

# Votre requête de recherche
query_text = "Quelles sont les dernières avancées en matière de modèles de langage multimodaux ?"
query_vector = get_query_embedding(query_text)

# Effectuer la recherche dans Qdrant
search_results = qdrant_client.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_vector,
    limit=5,  # Nombre de résultats à retourner
    # Optional: query_filter pour filtrer par persona, date, etc.
    # query_filter=models.Filter(
    #     must=[
    #         models.FieldCondition(key="source_persona", match=models.MatchValue(value="persona_ai_builder"))
    #     ]
    # )
    with_payload=True # Pour récupérer les métadonnées des articles
)

for hit in search_results:
    print(f"Article ID: {hit.id}, Score: {hit.score}")
    print(f"Titre: {hit.payload.get('title')}")
    print(f"Lien: {hit.payload.get('link')}")
    print(f"Résumé Enrichi: {hit.payload.get('enriched_summary')}")
    print("-" * 20)
```

**Points clés pour l'interrogation :**

1.  **Vectorisation de la requête :** Votre texte de requête doit être transformé en un vecteur d'embedding en utilisant le même modèle que celui utilisé pour les articles (ici, `text-embedding-3-small` d'OpenAI).
2.  **Utilisation de `qdrant_client.search()` :** Cette fonction prend le vecteur de requête et retourne les points les plus similaires de la collection.
3.  **Filtrage (Optionnel) :** Vous pouvez utiliser des filtres pour affiner les résultats en fonction des métadonnées (e.g., `source_persona`, `category`, `published` date).
4.  **`with_payload=True` :** Pour récupérer les informations stockées dans le payload de chaque point (titre, résumé, etc.).

Un script dédié ou une petite API (par exemple avec FastAPI ou Flask) pourrait être développé pour faciliter ces interrogations.

## 🧪 Exemples et Résultats (À venir)

Cette section sera complétée avec :

-   Des exemples concrets de requêtes et les résultats obtenus.
-   Des captures d'écran ou des liens vers des visualisations TensorFlow Projector.
-   Des analyses ou des insights tirés des données traitées.

## 🤝 Contribuer au Projet

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, voici quelques pistes :

-   **Implémenter les modules NLP manquants :** Remplacer les stubs de `cleaner`, `tagger`, `classifier`, `entities` par des logiques fonctionnelles (basées sur des règles, du ML classique, ou des appels LLM avec les prompts avancés).
-   **Développer une interface de requête :** Créer un script ou une API simple pour interroger la base Qdrant.
-   **Améliorer la configuration des personas :** Exploiter [`personas/personas_config.json`](personas/personas_config.json:1) pour une personnalisation plus poussée.
-   **Ajouter des tests unitaires et d'intégration.**
-   **Améliorer la gestion des erreurs et le monitoring du pipeline.**
-   **Étendre à d'autres sources de données.**
-   **Optimiser les performances.**

**Processus de contribution :**

1.  Forkez le dépôt.
2.  Créez une nouvelle branche pour votre fonctionnalité ou correction (`git checkout -b feature/ma-nouvelle-feature`).
3.  Effectuez vos modifications et commitez-les (`git commit -m 'Ajout de ma nouvelle feature'`).
4.  Poussez votre branche (`git push origin feature/ma-nouvelle-feature`).
5.  Ouvrez une Pull Request en expliquant clairement vos changements.

Veuillez vous assurer que votre code respecte les standards de qualité et inclut la documentation nécessaire.

## 📄 Licence

Ce projet est distribué sous la licence MIT. Voir le fichier [`LICENSE`](LICENSE:1) pour plus de détails.

## 🙏 Remerciements

-   Aux créateurs et mainteneurs des librairies open source utilisées dans ce projet.
-   À la communauté pour ses inspirations et ses outils.

---

N'hésitez pas à ouvrir une issue si vous rencontrez des problèmes ou si vous avez des suggestions d'amélioration !