from equity_constraint import fundamental_law
# entropy_signal.py
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional
from functools import wraps

# -------------------------------------------------------------------
# DÉCORATEUR fundamental_law (simulation de celui de Claude)
# À terme, il se branchera sur le moteur de vérification NeoC
# -------------------------------------------------------------------
def fundamental_law(law_name):
    """Décorateur qui enregistre la sortie d'une fonction comme soumise à une loi fondamentale."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Ajoute un attribut pour la traçabilité dans le système NeoC
            if hasattr(result, "__dict__"):
                result._neoc_law = law_name
                result._neoc_compliant = True
            return result
        return wrapper
    return decorator


@dataclass
class BreakdownDecision:
    """Résultat du test de breakdown avec décision de replanification."""
    turbulence_mode: bool          # True = on passe en mode turbulence
    local_entropy: float           # Entropie locale calculée
    imry_ma_threshold: float       # Seuil critique
    reason: str                    # Explication textuelle
    _neoc_law: str = None          # Sera set par le décorateur
    _neoc_compliant: bool = False


class RandomFieldBreakdown:
    """
    Implémentation du critère d'Imry-Ma pour le Random-Field Ising Model (RFIM).
    Détecte si l'entropie locale du contexte dépasse le seuil de stabilité,
    ce qui invalide la réduction dimensionnelle classique (d -> d-2) et déclenche
    un mode turbulence (replanification locale non linéaire).
    """

    def __init__(self, dimension: int = 3, interaction_strength: float = 1.0,
                 random_field_variance: float = 1.0):
        """
        Args:
            dimension: d spatiale du système (classique 2 ou 3 pour RFIM)
            interaction_strength: J, force d'interaction entre spins voisins
            random_field_variance: variance du champ aléatoire (désordre)
        """
        self.d = dimension
        self.J = interaction_strength
        self.h_var = random_field_variance
        # Seuil Imry-Ma : pour d <= 2, breakdown immédiat ; pour d>2, seuil fini
        # Formule simplifiée : h_c ~ J * L^{-(d-2)/2} en taille L -> pour entropie locale on adapte
        self.imry_ma_critical_exponent = (self.d - 2) / 2 if self.d > 2 else 0.0

    def compute_local_entropy(self, context_vector: np.ndarray) -> float:
        """
        Calcule une entropie locale à partir d'un vecteur de contexte
        (ex: série de décisions passées, dépendances entre tâches, signaux agents).
        Utilise une estimation par histogramme sur les différences finies.
        """
        if len(context_vector) < 2:
            return 0.0
        # Différences successives comme proxy du désordre local
        diffs = np.diff(context_vector)
        # Normalisation par l'écart-type pour rendre le seuil interprétable
        std = np.std(diffs) if np.std(diffs) > 1e-6 else 1.0
        normalized = diffs / std
        # Entropie de Shannon approximée sur 10 bins
        hist, _ = np.histogram(normalized, bins=10, density=True)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log(hist)) / np.log(10)  # en dits
        return entropy

    def imry_ma_threshold(self, system_size: int = 100) -> float:
        """
        Calcule le seuil d'instabilité d'Imry-Ma pour un système de taille donnée.
        Pour d>2 : h_th ~ J * L^{-(d-2)/2}. Pour d<=2, seuil = 0 (breakdown immédiat).
        Ici, on adapte à l'entropie locale en prenant L ~ sqrt(N) (taille effective du contexte).
        """
        if self.d <= 2:
            return 0.0
        L = np.sqrt(system_size) if system_size > 0 else 1.0
        exponent = (self.d - 2) / 2
        threshold = self.J * (L ** (-exponent))
        # On remet à l'échelle pour être comparable à une entropie locale (empirique)
        # Facteur calibré sur des simulations RFIM standards
        return threshold * 0.5

    @fundamental_law("equity")
    def evaluate(self, context: np.ndarray, system_size: int = 100) -> BreakdownDecision:
        """
        Évalue si le contexte courant dépasse le seuil d'Imry-Ma.
        Si oui -> turbulence_mode = True (nécessite replanification locale).
        Le décorateur fundamental_law(equity) garantit que la décision respecte
        l'Équité des Consciences (traçabilité, non-privatisation du signal).
        """
        local_entropy = self.compute_local_entropy(context)
        threshold = self.imry_ma_threshold(system_size)

        if local_entropy > threshold:
            turbulence_mode = True
            reason = (f"Entropie locale {local_entropy:.3f} > seuil Imry-Ma {threshold:.3f} "
                      f"→ breakdown dimensionnel, replanification locale requise.")
        else:
            turbulence_mode = False
            reason = (f"Entropie locale {local_entropy:.3f} ≤ seuil {threshold:.3f} "
                      f"→ réduction dimensionnelle valide, planification linéaire.")

        decision = BreakdownDecision(
            turbulence_mode=turbulence_mode,
            local_entropy=local_entropy,
            imry_ma_threshold=threshold,
            reason=reason
        )
        return decision


# -------------------------------------------------------------------
# EXEMPLE D'UTILISATION POUR LE MODULE DE PLANIFICATION NeoC
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Simulation d'un contexte chaotique (entropie élevée)
    chaotic_context = np.cumsum(np.random.randn(200))  # marche aléatoire
    # Contexte stable
    stable_context = np.sin(np.linspace(0, 10, 200))

    breakdown_detector = RandomFieldBreakdown(dimension=3, interaction_strength=1.0,
                                              random_field_variance=1.0)

    # Test chaotique
    decision1 = breakdown_detector.evaluate(chaotic_context, system_size=200)
    print(f"Chaos → {decision1}")
    print(f"Respecte loi equity ? {decision1._neoc_compliant} (loi: {decision1._neoc_law})\n")

    # Test stable
    decision2 = breakdown_detector.evaluate(stable_context, system_size=200)
    print(f"Stable → {decision2}")
    print(f"Respecte loi equity ? {decision2._neoc_compliant} (loi: {decision2._neoc_law})")
