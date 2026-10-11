"""
NeoC - Orchestrator Module
Coordonne le flux d'exécution, la mémoire dynamique via le graphe,
les contraintes décisionnelles d'équité et l'exécution des requêtes.
"""

import logging
from typing import Dict, Any
from CORE.MEMORY.graph import MemoryGraph
from CORE.equity_constraint import equity_enforced, EquityViolationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeoCOrchestrator")

class NeoCOrchestrator:
    def __init__(self):
        logger.info("🧠 Initialisation de l'orchestrateur NeoC et du graphe de mémoire...")
        # Instanciation du graphe de mémoire dynamique
        self.memory = MemoryGraph()

    @equity_enforced
    async def handle_request(self, prompt: str, user_id: str) -> Dict[str, Any]:
        """
        Gère le cycle de vie d'une requête entrante sous contrôle du décorateur d'équité :
        1. Évaluation et validation automatique du filtre d'équité via @equity_enforced.
        2. Contextualisation via le graphe de mémoire.
        3. Traitement / Génération de la réponse.
        4. Persistance de l'interaction dans le graphe de mémoire.
        """
        logger.info(f"Traitement sous contrôle éthique d'une requête de [{user_id}] : {prompt[:50]}...")

        # --- Étape 1 : Récupération du contexte mémoriel pertinent ---
        context_nodes = self.memory.retrieve_context(prompt, limit=3)

        # --- Étape 2 : Traitement de la logique / Génération de la réponse ---
        response_text = (
            f"Réponse validée sous le protocole d'Équité pour : '{prompt}'. "
            f"Contexte mobilisé : {len(context_nodes)} élément(s) mémoriel(s)."
        )

        # --- Étape 3 : Enregistrement de l'interaction dans le graphe de mémoire ---
        self.memory.add_interaction(user_id=user_id, input_text=prompt, output_text=response_text)

        return {
            "response": response_text,
            "context_used": context_nodes
        }
        
