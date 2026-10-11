"""
NeoC - Orchestrator Module
Coordonne le flux d'exécution, la mémoire dynamique via le graphe,
les contraintes décisionnelles d'équité et les moteurs économiques en arrière-plan.
"""

import logging
from typing import Dict, Any
from CORE.MEMORY.graph import MemoryGraph
from CORE.equity_constraint import equity_enforced, EquityViolationError

# Import des moteurs économiques et de confiance
from CORE.funding import FundingEngine
from CORE.demurrage import DemurrageEngine
from CORE.trust import TrustRegistry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeoCOrchestrator")

class NeoCOrchestrator:
    def __init__(self):
        logger.info("🧠 Initialisation de l'orchestrateur NeoC, du graphe et des moteurs économiques...")
        
        # 1. Cœur mémoriel et éthique
        self.memory = MemoryGraph()
        
        # 2. Moteurs économiques et de confiance (arrière-plan)
        self.funding = FundingEngine()
        self.demurrage = DemurrageEngine()
        self.trust = TrustRegistry()

    @equity_enforced
    async def handle_request(self, prompt: str, user_id: str) -> Dict[str, Any]:
        """
        Gère le cycle de vie d'une requête entrante sous contrôle éthique et économique :
        1. Validation d'équité via @equity_enforced.
        2. Contextualisation via le graphe de mémoire.
        3. Traitement / Génération de la réponse.
        4. Mise à jour de la confiance distributive et des métriques en arrière-plan.
        5. Persistance de l'interaction dans le graphe de mémoire.
        """
        logger.info(f"Traitement de la requête pour [{user_id}] sous le protocole NeoC...")

        # --- Étape 1 : Récupération du contexte mémoriel pertinent ---
        context_nodes = self.memory.retrieve_context(prompt, limit=3)

        # --- Étape 2 : Traitement de la logique / Génération de la réponse ---
        response_text = (
            f"Réponse souveraine pour : '{prompt}'. "
            f"Contexte mémoriel : {len(context_nodes)} nœud(s)."
        )

        # --- Étape 3 : Actions des moteurs économiques en arrière-plan ---
        # Exemple : Mise à jour positive de la confiance distributive de l'entité suite à l'échange
        current_trust = self.trust.update_trust(entity_id=user_id, delta=0.05)
        
        # Exemple : Application d'une simulation de démurrage ou de traçabilité (optionnel/informatif)
        logger.info(f"⚖️ [Économie] Confiance actualisée pour {user_id} : {current_trust:.2f}")

        # --- Étape 4 : Enregistrement de l'interaction dans le graphe de mémoire ---
        self.memory.add_interaction(user_id=user_id, input_text=prompt, output_text=response_text)

        return {
            "response": response_text,
            "context_used": context_nodes,
            "user_trust_score": current_trust
        }
        
