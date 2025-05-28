# 🧠 Persona News Engine

Un système de recommandation de news personnalisées basé sur des **bases de données vectorielles hiérarchisées**, des **personas évolutifs** et des modèles d’intelligence artificielle.

## 📌 Objectif du projet

Créer une plateforme qui simule une **agence de presse intelligente et personnalisée**, capable de :

- Scraper et vectoriser de grandes quantités de contenus (news/articles)
- Les organiser dans une **base vectorielle mère** structurée en clusters thématiques
- Permettre à des **personas intelligents** de récupérer des articles pertinents
- Générer des résumés, reformulations ou bulletins personnalisés à partir de ces contenus
- Évoluer au fil du temps en fonction de leurs lectures

## 🧩 Concept

- Une **base vectorielle mère** contient tous les contenus vectorisés.
- Des **nœuds bleus** représentent des sous-bases ou clusters thématiques.
- Des **points rouges (personas)** interrogent la base, explorent les clusters proches, et forment leur propre base évolutive.
- Chaque persona peut ensuite :
  - Consulter, lire ou ignorer les contenus proposés
  - Évoluer (grâce à une mémoire vectorielle)
  - Recevoir des résumés personnalisés grâce à un LLM

## 🛠️ Stack envisagée (en cours de validation)

| Composant | Outil pressenti |
|-----------|-----------------|
| Vector DB | Qdrant (Cloud ou local) |
| Embeddings | OpenAI `text-embedding-3-small` |
| Scraping | `newspaper3k`, RSS, APIs |
| Matching sémantique | LangChain / Python |
| Résumé / reformulation | GPT-4 / Claude 3 / Mistral |
| Interface | Streamlit ou React (via ShadCN / Next.js) |

## 🚧 Roadmap

### ✅ Étape 0 – Définition
- [x] Rédiger la mini-spec
- [X] Finaliser les personas de départ
- [X] Choisir les premières sources à scraper

### ⏳ Étape 1 – Prototype de base
- [ ] Scraping basique (flux RSS ou APIs)
- [ ] Stockage local + vectorisation
- [ ] Mise en place d’une base Qdrant + quelques clusters

### ⏳ Étape 2 – Matching & personnalisation
- [ ] Simulation de matching persona ↔ cluster
- [ ] Recherche vectorielle dans les articles pertinents
- [ ] Génération d’un résumé personnalisé

### ⏳ Étape 3 – Mémoire évolutive
- [ ] Création d’une base par persona
- [ ] Ajout d’historique de lecture
- [ ] Adaptation du profil vectoriel

---

## 🧠 Inspirations & Concepts techniques

- Hierarchical Vector Indexing
- Meta-Embeddings
- Retrieval-Augmented Generation (RAG)
- Cognitive Agents with Evolving Memory

---

## 📄 Licence

Ce projet est sous licence [Apache 2.0](LICENSE).

---

## ✨ À venir

- Visualisations du système
- Démo Streamlit
- Interface simple de test pour personas

