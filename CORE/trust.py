"""
Module de calcul du Trust et de détection de la collusion pour NeoC.
"""

def compute_node_trust(interactions: dict) -> dict:
    """
    Calcule le score de Trust de chaque nœud (entre 0.01 et 1.00).
    
    interactions: dictionnaire {node_id: [liste_des_noeuds_valides]}
    """
    trust_scores = {}
    
    for node, targets in interactions.items():
        if not targets:
            trust_scores[node] = 0.10
            continue
            
        # Détection de la réciprocité directe et des boucles de collusion
        reciprocal_count = 0
        for target in targets:
            if target in interactions and node in interactions[target]:
                reciprocal_count += 1
                
        # Calcul du taux de collusion (plus la boucle est fermée, plus le risque est élevé)
        collusion_ratio = reciprocal_count / len(targets) if targets else 0.0
        
        # Le score de base dépend de la diversité des validations
        unique_validations = len(set(targets))
        base_trust = min(1.0, unique_validations / 10.0)
        
        # Pénalisation drastique si la collusion est détectée
        if collusion_ratio > 0.5:
            penalty = collusion_ratio * 0.8
            final_trust = max(0.01, base_trust - penalty)
        else:
            final_trust = max(0.01, base_trust)
            
        trust_scores[node] = round(final_trust, 2)
        
    return trust_scores


if __name__ == "__main__":
    # Test d'un réseau sain vs un anneau de collusion
    sample_network = {
        "node_creatif_1": ["node_socle_A", "node_socle_B", "node_socle_C"],
        "sybil_1": ["sybil_2", "sybil_3"],
        "sybil_2": ["sybil_1", "sybil_3"],  # Collusion en boucle
        "sybil_3": ["sybil_1", "sybil_2"]
    }
    
    scores = compute_node_trust(sample_network)
    print("=== SCORES DE TRUST CALCULÉS ===")
    for node, score in scores.items():
        print(f"• Nœud : {node} | Trust : {score}")
      
