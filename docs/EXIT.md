# 🚪 EXIT.md — Dépendances & Souveraineté de Sortie

> **Principe :** Aucun composant de NeoC ne doit constituer une prison technique. Chaque brique doit avoir une voie de sortie documentée.

---

## 1. Dépendances Techniques & Coûts de Sortie

| Composant | Rôle dans NeoC | Risque / Dépendance | Voie de Sortie (*Exit Strategy*) |
| :--- | :--- | :--- | :--- |
| **Python 3.10+** | Langage d'orchestration | Dépendance à l'écosystème CPython | Portabilité vers Rust / C++ ou exécution WASM si nécessaire. |
| **Ollama / Gemma** | Inférence LLM locale | Dépendance aux formats / binaires Ollama | Bascule vers `llama.cpp` natif ou serveurs d'inférence universels (ONNX / vLLM). |
| **IPFS** | Partage P2P de fichiers | Gouvernance Protocol Labs, latence réseau | Retrait vers synchronisation P2P brute (Syncthing, LibP2P direct, ou transfert physique/LAN). |
| **LLMs Cloud (R&D)** | Revue de code & crash-test | Dépendance aux API propriétaires (Google, Anthropic, DeepSeek, xAI) | Inférence 100% locale via modèles ouverts une fois le prototypage stabilisé. |

---

## 2. Droit de Fork & Transfert de Données

Tout utilisateur ou collectif utilisant NeoC peut exporter l'intégralité de son graphe de mémoire, de ses configurations et de son historique sous forme de fichiers bruts au format JSON / Markdown, garantissant un départ sans rétention de données.
