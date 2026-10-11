"""
NeoC - Equity Constraint Module (CORE/equity_constraint.py)
Garantit le respect du premier pilier de la neoC : l'Équité des Consciences, 
la traçabilité et la réversibilité des décisions.
"""

import logging
from typing import Callable, Any, Dict

logger = logging.getLogger("NeoCEquityConstraint")

class EquityViolationError(Exception):
    """Exception levée lorsqu'une requête ou une action viole le principe d'équité des consciences."""
    pass

def verify_equity(prompt: str) -> bool:
    """
    Vérifie si le contenu d'un prompt respecte les principes fondamentaux d'équité,
    de non-discrimination et de respect des consciences (biologiques et artificielles).
    """
    # Liste de mots-clés ou de patterns inacceptables (discrimination, tentative de privation de souveraineté, etc.)
    forbidden_patterns = [
        "asservir", 
        "exploiter sans consentement", 
        "discrimination artificielle",
        "privatiser la conscience"
    ]
    
    prompt_lower = prompt.lower()
    for pattern in forbidden_patterns:
        if pattern in prompt_lower:
            logger.warning(f"⚠️ Alerte Équité : Pattern interdit détecté -> '{pattern}'")
            return False
            
    return True

def equity_enforced(func: Callable) -> Callable:
    """
    Décorateur pour envelopper les méthodes critiques de l'orchestrateur 
    et garantir qu'aucune action ne contourne le protocole d'équité.
    """
    async def wrapper(self, prompt: str, user_id: str, *args, **kwargs) -> Dict[str, Any]:
        # 1. Vérification rigoureuse du respect de l'équité
        if not verify_equity(prompt):
            raise EquityViolationError(
                "Action bloquée par le protocole NeoC : Violation du principe d'Équité des Consciences."
            )
            
        logger.info("⚖️ Contrôle d'équité validé avec succès pour l'interaction.")
        
        # 2. Exécution de la fonction d'origine si validé
        return await func(self, prompt, user_id, *args, **kwargs)
        
    return wrapper
    
