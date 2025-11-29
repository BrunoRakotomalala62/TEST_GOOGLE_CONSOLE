# Demo Google APIs - Gemini AI & Maps

## Overview
Application de demonstration des APIs Google incluant:
- **Gemini AI**: Chatbot intelligent propulse par Google Gemini 2.5
- **Google Maps**: Carte interactive avec geocodage et analyse de lieux

## Project Structure
```
/
├── app.py              # Application Flask principale
├── templates/
│   └── index.html      # Interface utilisateur
├── test_google_api.py  # Script de test de la cle API
└── replit.md           # Documentation du projet
```

## Configuration requise

### Secrets (Variables d'environnement)
- `GOOGLE_API_KEY`: Cle API Google (utilisee pour Gemini et Maps)
- Optionnel: `GEMINI_API_KEY` et `GOOGLE_MAPS_API_KEY` si vous voulez des cles separees

### APIs Google a activer
Dans la [Console Google Cloud](https://console.cloud.google.com/apis/library):
1. **Generative Language API** (pour Gemini AI)
2. **Maps Embed API** (pour Google Maps)

## Running the Application
Le serveur Flask demarre automatiquement sur le port 5000.

## Fonctionnalites
1. **Chat IA**: Posez des questions a Gemini AI
2. **Recherche de lieux**: Entrez une adresse pour la localiser sur la carte
3. **Analyse de lieux**: Obtenez des informations touristiques sur n'importe quel endroit

## Recent Changes
- 2025-11-29: Creation initiale du projet
