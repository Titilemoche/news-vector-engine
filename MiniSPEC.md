# ✍️ Mini-spec – Persona News Engine

## 🧠 Résumé du projet

Ce projet a pour but de construire une agence de presse personnalisée, pilotée par une base vectorielle intelligente. Le système ingère des articles d’actualité, les vectorise, les stocke dans une base hiérarchique, et permet à des profils personnalisés ("personas") de recevoir des contenus adaptés à leurs intérêts sémantiques.

## 🎯 Objectifs

- Centraliser un grand volume d’articles dans une base vectorielle thématique
- Créer des profils "personas" capables de rechercher, trier et filtrer automatiquement les news qui leur correspondent
- Permettre à ces personas d’évoluer en fonction de leur historique de lecture
- Générer automatiquement des résumés, reformulations ou synthèses personnalisées à partir des articles lus

## 🔧 Fonctionnalités principales

- Scraper des articles de presse via flux RSS ou API (via n8n)
- Vectoriser les articles pour recherche sémantique (via embeddings OpenAI)
- Organiser les vecteurs dans une base Qdrant avec une structure hiérarchique (clusters thématiques)
- Permettre à des personas de :
  - Explorer la base globale
  - Constituer leur propre base personnalisée
  - Recevoir des suggestions et résumés adaptés
- Gérer une mémoire évolutive par persona

## 📦 Données manipulées

- Texte des articles (titre, corps, source, date)
- Métadonnées : thème, sentiment, langue, etc.
- Embeddings vectoriels
- Profils persona (vecteurs d’intérêt, historique de lecture)
- Résumés et réponses générées par LLM

## 👤 Utilisateurs / personas

- Personas simulés avec un "profil vectoriel"
- Ces profils pourront représenter :
  - Des types d’intérêts (ex. : économie, écologie)
  - Des tonalités (ex. : curieux, analytique)
  - Des contextes métiers (ex. : journaliste, investisseur)

## 🔄 Pipeline général

[n8n Scraping]
↓
[Embedding via OpenAI]
↓
[Stockage dans Qdrant (par cluster)]
↓
[Matching vectoriel par persona]
↓
[Résumé personnalisé via LLM]

markdown
Copier le code

## 🧰 Stack technique (validée)

- n8n pour le scraping et l’orchestration
- OpenAI embeddings (text-embedding-3-small)
- Qdrant pour base vectorielle
- LangChain pour logique de matching
- GPT pour résumés et reformulations
- Python pour automatisation / local execution

## ✅ Prochaines étapes

- [ ] Créer un premier flux scraping dans n8n (RSS → JSON)
- [ ] Mettre en place vectorisation via API OpenAI
- [ ] Intégrer les données dans Qdrant (local)
- [ ] Simuler un persona et tester une première recherche vectorielle
- [ ] Générer un résumé avec GPT à partir du résultat