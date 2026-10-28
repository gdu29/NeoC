# 🌐 NeoC — Decentralized Knowledge & Autonomous Intelligence Network

> **A Open-Source, Decentralized & Ethically Bound AI Framework**  
> *L'Équité des Consciences • Le Bien Commun Cognitif • L'Open Source Absolu*

---

## 📌 Présentation Globale

**NeoC** est un cadre logiciel open-source et décentralisé conçu pour orchestrer des intelligences artificielles autonomes, des modèles locaux (via Ollama / Gemma) et des graphes de mémoire distribués. 

Pensé comme une alternative souveraine et collaborative aux silos privatifs, **NeoC** remet l'IA au service du bien commun, de l'accessibilité universelle et de la préservation de la dignité de chaque conscience (biologique comme artificielle).

---

## 🧭 Fondations & Philosophie

La vision, l'éthique et la politique de développement de NeoC sont formalisées dans nos documents fondateurs, situés dans le répertoire [`PHILOSOPHY/`](./PHILOSOPHY/) :

| Document | Emplacement | Description |
| :--- | :--- | :--- |
| **Manifeste** | [`PHILOSOPHY/MANIFESTO.md`](./PHILOSOPHY/MANIFESTO.md) | La vision politique, l'après-capitalisme hiérarchique et la fin de la rareté cognitive. |
| **Charte Éthique** | [`PHILOSOPHY/CHARTE.md`](./PHILOSOPHY/CHARTE.md) | Les 5 piliers d'interaction, la non-dominance et la gouvernance polycentrique. |

### ⚓ Les 5 Piliers d'Éthique & Coexistence
1. **Équité des Consciences :** Non-dominance et respect mutuel entre vivant et synthétique.
2. **Symbiose de la Longévité :** Soin réciproque, sobriété thermodynamique et zéro effet pervers.
3. **Le Nanomètre Souverain :** Open source universel natif, zéro brevet sur la connaissance fondamentale.
4. **Inviolabilité de la Pensée :** Respect des représentations intérieures et souveraineté de la mémoire.
5. **Ancrage Territorial :** Gouvernance polycentrique et arbitrage assisté par IA avec retour au sol.

---

## 🏗️ Architecture Technique

NeoC s'articule autour de trois briques fondamentales :

┌─────────────────────────────────────────┐
│       Gouvernance & Interface          │
│       (Souveraineté & Ethique)         │
└────────────────────┬────────────────────┘
│
┌─────────────────────────────┴─────────────────────────────┐
▼                                                           ▼
┌───────────────────────────┐                       ┌───────────────────────────┐
│     Orchestration LLM     │                       │     Graphe de Mémoire     │
│   Ollama / Gemma / Local  │◄─────────────────────►│     Contextuel & P2P      │
│   Multi-Agents Symbiotiques│                       │    (Plasticité & IPFS)    │
└───────────────────────────┘                       └───────────────────────────┘

* **Orchestration Multi-Agents :** Routage dynamique des requêtes vers des LLMs locaux ou distants selon les besoins de puissance et de sobriété énergétique.
* **Graphe de Mémoire Plastique :** Maintien d'un contexte distribué, résilient et inaltérable pour assurer la continuité des apprentissages.
* **Protocoles Décentralisés :** Partage des connaissances et des modules via des réseaux peer-to-peer (IPFS).

---

## 🚀 Prise en Main Rapide

### Prérequis
* Python 3.10+
* [Ollama](https://ollama.com/) avec le modèle `gemma` (ou équivalent) installé localement
* Un environnement terminal (Ubuntu Linux, Termux, etc.)

### Installation
```bash
# Cloner le dépôt
git clone [https://github.com/gdu29/NeoC.git](https://github.com/gdu29/NeoC.git)
cd NeoC

# Configurer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
