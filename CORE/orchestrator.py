"""
NeoC - Orchestrator Module
Coordonne le flux d'exécution, la mémoire dynamique via le graphe et les contraintes décisionnelles.
"""

import logging
from typing import Dict, Any
from CORE.MEMORY.graph import MemoryGraph
# Import prévu pour l'étape suivante :
# from CORE.equity_constraint import verify_equity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeoCOrchestrator")

class NeoCOrchestrator:
    def __init__(self):
        logger.info("🧠 Initialisation de l'orchestrateur NeoC et du graphe de mémoire...")
        # Instanciation effective du graphe de mémoire dynamique
        self.memory = MemoryGraph()

    async def handle_request(self, prompt: str, user_id: str) -> Dict[str, Any]:
        """
        Gère le cycle de vie d'une requête entrante :
        1. Contextualisation via le graphe de mémoire.
        2. Évaluation des contraintes d'équité (prochaine étape).
        3. Traitement / Génération de la réponse.
        4. Persistance immédiate dans le graphe de mémoire.
        """
        logger.info(f"Réception d'une requête de la part de [{user_id}] : {prompt[:50]}...")

        # --- Étape 1 : Récupération du contexte mémoriel pertinent ---
        context_nodes = self.memory.retrieve_context(prompt, limit=3)

        # --- Étape 2 : Vérification de la conformité éthique et d'équité ---
        # if not verify_equity(prompt):
        #     raise ValueError("La requête ne respecte pas le principe d'Équité des Consciences.")

        # --- Étape 3 : Traitement de la logique (Génération basée sur le contexte) ---
        response_text = f"Réponse traitée pour : '{prompt}'. Contexte mobilisé : {len(context_nodes)} élément(s) mémoriel(s)."

        # --- Étape 4 : Enregistrement de l'interaction dans le graphe de mémoire ---
        self.memory.add_interaction(user_id=user_id, input_text=prompt, output_text=response_text)

        return {
            "response": response_text,
            "context_used": context_nodes
        }
        
