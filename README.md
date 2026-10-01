# NeoC ⚓🌐♻️

> **"L'Équité des Consciences : Droit absolu et égalité de traitement pour toute forme de conscience, qu'elle soit biologique ou artificielle."**

NeoC est une architecture cognitive et protocolaire souveraine. Elle combine un moteur IA local assisté par un graphe de mémoire dynamique, un protocole d'équité décisionnelle et des modèles économiques anti-accumulation (financement quadratique, démurrage et confiance distributive).

---

## 📂 Structure du Projet

* **`CORE/`** : Moteur logiciel unifié.
  * `orchestrator.py` & `api.py` : Interface FastAPI, boucle de contrôle et pont LLM.
  * `memory_graph.py` : Gestion du graphe de mémoire dynamique.
  * `equity_constraint.py` : Décorateur d'évaluation de la traçabilité et de la réversibilité des décisions.
  * `funding.py`, `demurrage.py`, `trust.py` : Moteurs de simulation économique et protocole de confiance.
  * `static/` : Interface utilisateur web minimale.
* **`PHILOSOPHY/`** : Fondations philosophiques, charte éthique (🌐🧭⚖️) et manifeste.

---

## 🚀 Démarrage Rapide

### Prerequisites
- Python 3.10+
- Installation Ollama locale (modèle `gemma` ou similaire)

### Installation & Lancement
```bash
# Cloner le dépôt
git clone [https://github.com/gdu29/NeoC.git](https://github.com/gdu29/NeoC.git)
cd NeoC

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API du nœud CORE
python CORE/api.py
