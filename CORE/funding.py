"""
Moteur de financement quadratique pondéré par le Trust pour NeoC.
"""
import math

def calculate_quadratic_funding(contributions: list[dict], base_pool_allocation: float) -> dict:
    """
    Calcule la distribution des fonds publics aux projets.
    
    contributions: liste de dicts [{'project_id': str, 'contributor_id': str, 'amount': float, 'trust_score': float}]
    base_pool_allocation: montant total d'énergie/matière disponible dans le pool du socle.
    """
    projects = {}
    
    # 1. Agrégation des contributions par projet avec pondération du Trust
    for c in contributions:
        proj_id = c["project_id"]
        amount = c["amount"]
        trust = c["trust_score"]
        
        if proj_id not in projects:
            projects[proj_id] = {"sqrt_sum": 0.0, "total_direct": 0.0}
            
        # Formula: sum(sqrt(contribution * trust))
        weighted_value = math.sqrt(amount * trust)
        projects[proj_id]["sqrt_sum"] += weighted_value
        projects[proj_id]["total_direct"] += amount

    # 2. Calcul des scores quadratiques bruts et du besoin de fonds complémentaires
    total_match_score = 0.0
    for proj_id, data in projects.items():
        quadratic_score = data["sqrt_sum"] ** 2
        # Le match correspond au bonus généré par la pluralité des soutiens
        match_score = max(0.0, quadratic_score - data["total_direct"])
        projects[proj_id]["match_score"] = match_score
        total_match_score += match_score

    # 3. Distribution proportionnelle des ressources du pool public
    results = {}
    for proj_id, data in projects.items():
        if total_match_score > 0:
            matching_grant = (data["match_score"] / total_match_score) * base_pool_allocation
        else:
            matching_grant = 0.0
            
        results[proj_id] = {
            "total_direct": round(data["total_direct"], 2),
            "matching_grant": round(matching_grant, 2),
            "total_allocated": round(data["total_direct"] + matching_grant, 2)
        }
        
    return results


if __name__ == "__main__":
    # Exemple : Projet A soutenu par beaucoup de petits contributeurs à fort Trust
    # Projet B soutenu par une seule grosse contribution d'un agent suspect
    test_contributions = [
        # Projet A (soutien large)
        {"project_id": "projet_A", "contributor_id": "u1", "amount": 10.0, "trust_score": 0.95},
        {"project_id": "projet_A", "contributor_id": "u2", "amount": 10.0, "trust_score": 0.90},
        {"project_id": "projet_A", "contributor_id": "u3", "amount": 10.0, "trust_score": 0.85},
        # Projet B (soutien concentré / faible trust)
        {"project_id": "projet_B", "contributor_id": "sybil_whale", "amount": 100.0, "trust_score": 0.12}
    ]
    
    pool_socle = 1000.0
    allocations = calculate_quadratic_funding(test_contributions, pool_socle)
    
    print("=== RÉSULTATS DU FINANCEMENT QUADRATIQUE ===")
    for proj, res in allocations.items():
        print(f"• {proj} : Direct={res['total_direct']} | Subvention Socle={res['matching_grant']} | Total={res['total_allocated']}")
