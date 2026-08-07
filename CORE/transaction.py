import math
import json

def process_neoc_transaction(tx_dict: dict, current_base_pool: float) -> tuple[dict, float]:
    """
    Valide une transaction NeoC, applique la fonte exponentielle (démurrage)
    et réinjecte la valeur perdue dans le pool commun du socle.
    """
    # 1. Vérification de la présence des champs obligatoires
    required_fields = ["version", "tx_hash", "timestamp", "tick", "type", "sender", "recipient", "payload"]
    for field in required_fields:
        if field not in tx_dict:
            raise ValueError(f"Transaction invalide : le champ « {field} » est manquant.")

    payload = tx_dict["payload"]
    demurrage_info = payload.get("demurrage_applied", {})
    
    gross_amount = payload.get("gross_amount", 0.0)
    holding_time = demurrage_info.get("holding_time_ticks", 0)
    rate_lambda = demurrage_info.get("rate_lambda", 0.0)

    # 2. Calcul de la fonte : S(t) = S0 * e^(-lambda * t)
    net_amount = gross_amount * math.exp(-rate_lambda * holding_time)
    decay_loss = gross_amount - net_amount

    # 3. Mise à jour des valeurs au sein de la transaction
    demurrage_info["decay_loss"] = round(decay_loss, 4)
    demurrage_info["net_amount"] = round(net_amount, 4)
    demurrage_info["recycled_to_base_pool"] = round(decay_loss, 4)

    # 4. Réinjection automatique dans le stock du socle
    updated_base_pool = current_base_pool + decay_loss

    return tx_dict, updated_base_pool


# --- Exemple d'utilisation ---
if __name__ == "__main__":
    raw_tx = {
      "version": "0.3.0",
      "tx_hash": "0x7f9a2b4c8e1d3f5a6b7c8d9e0f1a2b3c4d5e6f7a",
      "timestamp": 1788734670,
      "tick": 104,
      "type": "QUADRATIC_FUNDING_CONTRIBUTION",
      "sender": {"node_id": "node_socle_892", "trust_score": 0.95},
      "recipient": {"type": "MILESTONE_VAULT", "vault_id": "vault_project_creative_42"},
      "payload": {
        "asset": "MATTER_B",
        "gross_amount": 100.0,
        "demurrage_applied": {
          "rate_lambda": 0.005,
          "holding_time_ticks": 12
        }
      },
      "signature": "3045022100a8f9..."
    }

    pool_initial = 88468.7
    tx_traitee, pool_mis_a_jour = process_neoc_transaction(raw_tx, pool_initial)

    print("=== TRANSACTION TRAITÉE ===")
    print(f"Montant brut : {tx_traitee['payload']['gross_amount']} MATTER_B")
    print(f"Montant net transféré : {tx_traitee['payload']['demurrage_applied']['net_amount']} MATTER_B")
    print(f"Valeur fondue (recyclée) : {tx_traitee['payload']['demurrage_applied']['decay_loss']} MATTER_B")
    print(f"Nouveau solde du pool socle : {pool_mis_a_jour:.4f}")
  
