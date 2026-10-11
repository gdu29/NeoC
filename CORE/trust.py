"""
NeoC - Trust Module (CORE/trust.py)
Gère l'indice de confiance distributive entre les entités du réseau.
"""

import logging

logger = logging.getLogger("NeoCTrust")

class TrustRegistry:
    def __init__(self):
        self.trust_scores = {}
        logger.info("🤝 Registre de confiance distributive initialisé.")

    def update_trust(self, entity_id: str, delta: float):
        """Met à jour le score de confiance d'une entité suite à une interaction."""
        current = self.trust_scores.get(entity_id, 1.0)
        new_score = max(0.0, min(2.0, current + delta))  borné entre 0 et 2
        self.trust_scores[entity_id] = new_score
        return new_score

    def get_trust(self, entity_id: str) -> float:
        return self.trust_scores.get(entity_id, 1.0)
        
