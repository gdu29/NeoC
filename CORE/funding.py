"""
NeoC - Funding Module (CORE/funding.py)
Gère l'allocation des ressources selon des principes de financement équitable.
"""

import logging

logger = logging.getLogger("NeoCFunding")

class FundingEngine:
    def __init__(self):
        logger.info("💰 Moteur de financement initialisé.")

    def calculate_quadratic_funding(self, contributions: list) -> float:
        """Calcule un score ou une distribution basé sur le financement quadratique."""
        if not contributions:
            return 0.0
        # Somme des racines carrées des contributions, le tout au carré
        sum_sqrt = sum(c ** 0.5 for c in contributions)
        return sum_sqrt ** 2
        
