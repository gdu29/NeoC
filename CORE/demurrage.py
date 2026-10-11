"""
NeoC - Demurrage Module (CORE/demurrage.py)
Applique la règle de dépréciation (démurrage) pour empêcher l'accumulation de capital.
"""

import logging

logger = logging.getLogger("NeoCDemurrage")

class DemurrageEngine:
    def __init__(self, decay_rate: float = 0.01):
        self.decay_rate = decay_rate  # Taux de fonte par cycle/jour
        logger.info(f"⏳ Moteur de démurrage initialisé (Taux : {decay_rate * 100}%).")

    def apply_decay(self, current_balance: float) -> float:
        """Applique la perte de valeur liée au temps pour encourager la circulation."""
        decayed_balance = current_balance * (1 - self.decay_rate)
        return max(0.0, decayed_balance)
      
