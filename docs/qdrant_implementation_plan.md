# Plan d'Implémentation : Intégration Qdrant

**Date:** 2025-05-30

**Objectif :** Mettre en place une intégration robuste avec Qdrant pour stocker et interroger les articles vectorisés du projet, avec la flexibilité d'ajouter d'autres types de contenu à l'avenir. L'approche retenue est une mono-collection avec un champ `content_type` pour la différenciation des contenus.

## Plan d'Implémentation Détaillé

### Phase 1 : Configuration et Initialisation de Qdrant

1.  **Installation du Client Qdrant :**
    *   **Action :** S'assurer que `qdrant-client` est présent dans le fichier `requirements.txt` et installé dans l'environnement.
        ```txt
        # In requirements.txt
        qdrant-client>=1.7.0 # Ou la version la plus récente/stable
        ```
    *   **Vérification :** Exécuter `pip install -r requirements.txt`.

2.  **Configuration du Client :**
    *   **Action :** Mettre en place une manière centralisée d'initialiser le client Qdrant.
    *   **Détails :**
        *   Le client se connectera à l'instance Qdrant (ex: `host='localhost'`, `port=6333` pour une instance locale par défaut).
        *   Ces configurations devraient idéalement provenir de variables d'environnement (via le fichier `.env`).
    *   **Fichier suggéré :** `pipeline/qdrant_utils.py` (à créer).
        *   Ce fichier contiendra les fonctions utilitaires pour interagir avec Qdrant, y compris l'initialisation du client.

### Phase 2 : Gestion de la Collection Qdrant

1.  **Définition des Paramètres de la Collection :**
    *   **Nom de la collection :** `news_vectors`
    *   **Taille du Vecteur :** **1536** (correspondant au modèle `text-embedding-3-small`).
    *   **Distance :** `Cosine` (recommandé pour les embeddings textuels).

2.  **Script/Fonction de Création de Collection :**
    *   **Action :** Développer une fonction dans `pipeline/qdrant_utils.py` qui :
        *   Initialise le client Qdrant.
        *   Vérifie si la collection `news_vectors` existe.
        *   Si elle n'existe pas, la crée avec les paramètres de vecteur définis ci-dessus.
        *   **Indexation du Payload :** Configure l'indexation du payload pour les filtres efficaces. Champs à indexer (à créer lors de la création de la collection ou via des appels `create_payload_index`) :
            *   `source_persona`: type `keyword`
            *   `content_type`: type `keyword`
            *   `tags`: type `keyword` (pour les listes de chaînes)
            *   `category`: type `keyword`
            *   `published`: type `datetime`
            *   Optionnel : `link` (type `keyword`, si utilisé comme ID et pour récupération directe).

### Phase 3 : Adaptation du Pipeline d'Ingestion des Données

1.  **Nouveau Script d'Ingestion :**
    *   **Fichier suggéré :** `pipeline/ingest_to_qdrant.py` (à créer).
    *   **Rôle :** Lire les fichiers JSON du répertoire `data/embeddings/`, les transformer et les envoyer à Qdrant.

2.  **Stratégie de Génération d'ID Uniques et Stables :**
    *   **Importance :** Essentiel pour les mises à jour (upserts) et pour éviter les doublons.
    *   **Suggestion :** Utiliser le champ `link` de l'article comme base. Pour garantir l'unicité et un format compatible avec Qdrant (UUID ou entier), on peut :
        *   Hasher le lien (ex: SHA256) et tronquer/convertir pour obtenir un ID.
        *   Utiliser `uuid.uuid5(NAMESPACE_URL, link)` pour générer un UUID déterministe à partir du lien.

3.  **Enrichissement et Transformation du Payload :**
    *   **Action :** Dans `pipeline/ingest_to_qdrant.py`, pour chaque fichier JSON d'article :
        *   **Ajouter `content_type` :** Au dictionnaire du payload, ajouter `{"content_type": "article"}`.
        *   **Convertir `published` :** Le format actuel (ex: `"Tue, 13 May 2025 00:00:00 GMT"`) doit être parsé (par exemple avec `datetime.strptime`) et converti en une chaîne ISO 8601 (ex: `YYYY-MM-DDTHH:MM:SSZ` ou `YYYY-MM-DDTHH:MM:SS`) pour l'indexation `datetime` dans Qdrant.
        *   **Préparer les `tags` :** S'assurer que c'est une liste de chaînes. Si `null` ou absent, utiliser une liste vide.

4.  **Formatage en `PointStruct` Qdrant :**
    *   **Action :** Pour chaque article, construire un objet `PointStruct` de `qdrant_client.http.models` avec :
        *   `id`: L'ID stable généré.
        *   `vector`: Le champ `embedding` du fichier JSON.
        *   `payload`: Le dictionnaire de métadonnées enrichi et transformé.

5.  **Ingestion par Lots (Batch Upsert) :**
    *   **Action :** Utiliser la méthode `client.upsert(collection_name="news_vectors", points=[...])` avec une liste de `PointStructs`.
    *   **Efficacité :** Traiter les points par lots (par exemple, 100 à 500 points par appel `upsert`) pour de meilleures performances.

6.  **Journalisation et Gestion des Erreurs :**
    *   Intégrer une journalisation (logging) détaillée pour suivre le processus d'ingestion (nombre de points traités, succès, erreurs).
    *   Mettre en place une gestion des erreurs robuste pour les appels à l'API Qdrant (ex: `try-except` autour des appels `upsert`).

### Phase 4 : Planification pour les Futurs Types de Contenu

*   Lorsque de nouveaux types de contenu (ex: "résumé utilisateur", "réponse persona") sont introduits :
    *   Leur pipeline d'ingestion devra générer un vecteur et un payload approprié.
    *   Le payload devra inclure le champ `content_type` pertinent (ex: `{"content_type": "user_summary"}`).
    *   L'ingestion se fera dans la même collection `news_vectors` en utilisant la même logique d'upsert.

## Diagramme du Flux d'Implémentation Proposé

```mermaid
graph TD
    subgraph Source_Data ["Fichiers JSON Enrichis et Vectorisés"]
        A["data/embeddings/*.json"]
    end

    subgraph Pipeline_Ingestion_Qdrant ["pipeline/ingest_to_qdrant.py"]
        A --> B{Lecture & Parsing JSON};
        B --> C[Génération ID Stable (ex: à partir de 'link')];
        B --> D[Extraction Vecteur ('embedding')];
        B --> E{Construction Payload};
        E -- Ajout 'content_type: article' --> F[Payload Final];
        E -- Conversion 'published' (date) --> F;
        C & D & F --> G[Création Objet PointStruct Qdrant];
        G --> H[Accumulation des Points en Lots];
    end

    subgraph Qdrant_Utils ["pipeline/qdrant_utils.py"]
        I[Initialisation Client Qdrant];
        J[Fonction create_collection_if_not_exists];
        J -- Configure Index Payload --> K[Index: source_persona, content_type, tags, etc.];
    end

    subgraph Interaction_Qdrant ["Instance Qdrant"]
        L[Collection: 'news_vectors'];
        I --> H;
        J --> L;
        H -- Upsert par Lots de Points --> L;
    end

    subgraph Application_Utilisatrice ["Application / Personas"]
        M[Module de Requête API];
        M -- Construit Requête (avec filtres: content_type, etc.) --> L;
        L -- Retourne Résultats --> M;
    end
```

## Prochaines Étapes Suggérées

1.  Créer le fichier `pipeline/qdrant_utils.py` et implémenter l'initialisation du client et la création/vérification de la collection avec indexation du payload.
2.  Créer le fichier `pipeline/ingest_to_qdrant.py` et implémenter la logique de lecture, transformation et ingestion des points.
3.  Tester l'ingestion avec un sous-ensemble de données.
4.  Développer des exemples de requêtes pour valider le fonctionnement des filtres et de la recherche sémantique.