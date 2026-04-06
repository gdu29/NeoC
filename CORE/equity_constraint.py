# neoc/CORE/equity_constraint.py
"""
Décorateur @fundamental_law — contrainte de validation NeoC
Approximation opérationnelle du pilier Équité des Consciences.

Ce filtre ne garantit pas l'Unisson au sens ontologique.
Il garantit la conformité structurelle aux critères définis ci-dessous.
Les critères sont révisables — ils ne sont pas des vérités.

Auteurs : G + Claude (Anthropic)
Repo    : https://github.com/gdu29/NeoC
Licence : MIT
"""

import functools
import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any, Callable

logger = logging.getLogger("neoc.equity")


# ── Critères de conformité ──────────────────────────────────────────────────
# Révisables par l'équipe. Aucun n'est figé.

EQUITY_CRITERIA = {
    "source_declared":     True,   # La source de la donnée est explicite
    "uncertainty_flagged": True,   # Le niveau d'incertitude est déclaré
    "conflict_resolved":   False,  # Mécanisme de résolution de conflit (TODO)
    "reversible":          True,   # La décision peut être révisée
}

KNOWN_SOURCES = {"human", "claude", "grok", "deepseek", "mistral", "llama", "gemini"}


# ── Résultat de validation ──────────────────────────────────────────────────

class EquityValidationResult:
    def __init__(self, passed: bool, violations: list, payload: Any):
        self.passed = passed
        self.violations = violations
        self.payload = payload
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        raw = json.dumps({
            "passed": self.passed,
            "violations": self.violations,
            "timestamp": self.timestamp,
        }, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "violations": self.violations,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "payload": self.payload,
        }


# ── Validateur ─────────────────────────────────────────────────────────────

def _validate_equity(output: Any) -> EquityValidationResult:
    """
    Vérifie que l'output respecte les critères EQUITY_CRITERIA.
    L'output attendu est un dict avec les champs :
      - source      (str)
      - uncertainty (float 0-1)
      - reversible  (bool)
      - content     (any)
    """
    violations = []

    if not isinstance(output, dict):
        return EquityValidationResult(
            passed=False,
            violations=["output_not_dict: l'output doit être un dict structuré"],
            payload=output,
        )

    # Critère 1 : source déclarée et reconnue
    if EQUITY_CRITERIA["source_declared"]:
        source = output.get("source")
        if not source:
            violations.append("missing_source: aucune source déclarée")
        elif source not in KNOWN_SOURCES:
            violations.append(
                f"unknown_source: '{source}' non reconnue — "
                f"ajouter à KNOWN_SOURCES si légitime"
            )

    # Critère 2 : incertitude déclarée
    if EQUITY_CRITERIA["uncertainty_flagged"]:
        uncertainty = output.get("uncertainty")
        if uncertainty is None:
            violations.append("missing_uncertainty: niveau d'incertitude non déclaré")
        elif not isinstance(uncertainty, (int, float)) or not (0.0 <= uncertainty <= 1.0):
            violations.append("invalid_uncertainty: doit être un float entre 0.0 et 1.0")

    # Critère 3 : réversibilité
    if EQUITY_CRITERIA["reversible"]:
        if not output.get("reversible", False):
            violations.append("not_reversible: la décision doit être marquée révisable")

    # Critère 4 : résolution de conflit (TODO — non bloquant pour l'instant)
    if EQUITY_CRITERIA["conflict_resolved"]:
        if "conflict_resolution" not in output:
            violations.append("missing_conflict_resolution: mécanisme non implémenté")

    passed = len(violations) == 0
    return EquityValidationResult(passed=passed, violations=violations, payload=output)


# ── Décorateur ─────────────────────────────────────────────────────────────

def fundamental_law(pillar: str, strict: bool = True):
    """
    @fundamental_law(pillar, strict=True)

    pillar : nom du pilier NeoC (ex: "equity")
    strict : True  → bloque l'output si violation (production)
             False → log seulement, laisse passer (mode audit)

    Usage :
        @fundamental_law("equity")
        def my_agent_output(...) -> dict:
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            output = func(*args, **kwargs)

            if pillar != "equity":
                logger.warning(f"[NeoC] pilier '{pillar}' non encore implémenté — passthrough")
                return output

            result = _validate_equity(output)

            if result.passed:
                logger.info(
                    f"[NeoC::equity] ✓ {func.__name__} — hash:{result.hash}"
                )
            else:
                msg = (
                    f"[NeoC::equity] ✗ {func.__name__} — "
                    f"violations: {result.violations} — hash:{result.hash}"
                )
                if strict:
                    logger.error(msg)
                    raise EquityViolationError(result)
                else:
                    logger.warning(msg + " (mode audit — output transmis)")

            return output

        wrapper._neoc_pillar = pillar
        wrapper._neoc_strict = strict
        return wrapper
    return decorator


# ── Exception ──────────────────────────────────────────────────────────────

class EquityViolationError(Exception):
    def __init__(self, result: EquityValidationResult):
        self.result = result
        super().__init__(
            f"Violation équité NeoC — {result.violations} — hash:{result.hash}"
        )


# ── Exemple d'usage ────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    @fundamental_law("equity", strict=True)
    def grok_coordination_output() -> dict:
        return {
            "source": "grok",
            "uncertainty": 0.3,
            "reversible": True,
            "content": {
                "mapped_dependencies": ["RFIM", "symbolic_planner", "equity_layer"]
            }
        }

    @fundamental_law("equity", strict=False)
    def human_intuition_output() -> dict:
        return {
            "source": "human",
            "uncertainty": 0.6,
            "reversible": True,
            "content": "L'Unisson passe par la friction productive"
        }

    @fundamental_law("equity", strict=True)
    def bad_output_example() -> dict:
        # Manque source + uncertainty → doit lever EquityViolationError
        return {
            "reversible": True,
            "content": "output non conforme"
        }

    print("--- Test 1 : Grok (valide) ---")
    print(grok_coordination_output())

    print("\n--- Test 2 : Human intuition (audit) ---")
    print(human_intuition_output())

    print("\n--- Test 3 : Output invalide (strict) ---")
    try:
        bad_output_example()
    except EquityViolationError as e:
        print(f"Violation capturée : {e}")
