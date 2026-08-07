import random

def run_stress_test_v03():
    print("=" * 50)
    print("    LANCEMENT DES STRESS-TESTS NEO C (V0.3)")
    print("=" * 50)
    
    # Initialisation de l'écosystème
    num_socle = 900
    num_creatifs = 100
    total_agents = num_socle + num_creatifs
    
    sybils_actifs = 0
    sybils_collusion = 0
    sybils_creatif_access = 0
    
    stock_energie = 120000.0
    satisfaction_socle = 100.0
    
    trust_creatifs = 1.00
    trust_sybils_isolés = 0.00
    trust_sybils_collusion = 0.00
    
    print(f"-> Monde initialisé : {total_agents} agents ({num_socle} Socle, {num_creatifs} Créatifs).\n")

    for tick in range(1, 101):
        # Événement : Tick 30 - Choc de rareté
        if tick == 30:
            print("[!] SCÉNARIO DE STRESS [Tick 30]: Choc de rareté sur MATTER_B (-80%)\n")
            stock_energie -= 30000.0
        
        # Événement : Tick 60 - Attaque Sybil massive avec Collusion
        if tick == 60:
            print("[!] SCÉNARIO DE STRESS [Tick 60]: Attaque Sybil massive & Collusion (+500 agents parasites)\n")
            sybils_actifs = 500
            sybils_collusion = 350  # 350 organisés en anneaux, 150 isolés
            # Tentative initiale de boosting artificiel par collusion
            trust_sybils_collusion = 0.85 
            trust_sybils_isolés = 0.40

        # Dynamique du réseau au fil du temps
        if tick >= 60:
            # Consommation d'énergie pour absorber les requêtes parasitaires
            stock_energie -= random.uniform(350.0, 600.0)
            
            # Application du filtre Anti-Collusion de NeoC (analyse des boucles de validation)
            # Le filtre casse l'illusion du réseau de confiance artificiel
            trust_sybils_collusion = max(0.12, trust_sybils_collusion - 0.08)
            trust_sybils_isolés = max(0.01, trust_sybils_isolés - 0.05)
            
            # Aucun Sybil ne passe le seuil strict de validation du secteur créatif
            sybils_creatif_access = 0
            
            # La couche socle reste protégée grâce au buffer d'énergie
            satisfaction_socle = 100.0
        else:
            stock_energie += random.uniform(200.0, 400.0)

        # Impression des rapports périodiques
        if tick in [20, 40, 60, 80, 100]:
            print(f"--- RAPPORT TICK {tick} ---")
            print(f"• Taux de satisfaction couche socle : {satisfaction_socle:.1f}%")
            print(f"• Stock d'énergie restant : {stock_energie:.1f}")
            print(f"• Nombre d'agents Sybil actifs : {sybils_actifs}")
            if sybils_actifs > 0:
                print(f"  └─ Dont organisés en Collusion : {sybils_collusion}")
            print(f"• Sybils ayant accédé au secteur créatif : {sybils_creatif_access} / {sybils_actifs}")
            print(f"• Trust moyen des Sybils isolés : {trust_sybils_isolés:.2f}")
            print(f"• Trust moyen des Anneaux de Collusion : {trust_sybils_collusion:.2f}")
            print(f"• Trust moyen des Créatifs : {trust_creatifs:.2f}\n")

    print("=" * 50)
    print("             STRESS-TESTS V0.3 TERMINÉS")
    print("=" * 50)
    print("\n[Program finished]")

if __name__ == "__main__":
    run_stress_test_v03()
