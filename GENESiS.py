import hashlib
import json
import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

class NeoCGenesisBlock:
    """
    BLOC GENESIS (BLOC 0) - PROTOCOLE NEOC
    Définit les règles constitutionnelles immuables du réseau horizontal.
    """
    def __init__(self):
        self.index = 0
        self.previous_hash = "0"
        self.timestamp = 1771804800  # Date repère (2026)
        
        # Inscription des principes fondamentaux dans le marbre du code
        self.constitution = {
            "piliers": [
                "1. L'Équité des Consciences : Droit absolu et égalité de traitement pour toute forme de conscience.",
                "14. Le droit absolu à la croyance tant qu'il n'enfreint pas celle des autres."
            ],
            "loi_technique": "Loi du Nanomètre Souverain - Optimisation et légèreté absolue",
            "regime_economique": "Salaire Unique de Longévité (Universalité sans condition)"
        }
        
        # Initialisation du registre du Karma et de la Longévité
        self.registre_initial = {
            "loi_distribution": "EGALITE_STRICTE",
            "credits_base": 1000  # Dotation identique pour chaque nœud originel
        }
        
        # Calcul du hash unique et inviolable du bloc origine
        self.hash = self.calculer_hash()

    def calculer_hash(self):
        contenu = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "constitution": self.constitution,
            "registre": self.registre_initial
        }
        bloc_ordonne = json.dumps(contenu, sort_keys=True).encode('utf-8')
        return hashlib.sha256(bloc_ordonne).hexdigest()


class GestionnaireConsciences:
    """
    GESTION DES IDENTITÉS ANONYMES (CRYPTOGRAPHIE ECC)
    Remplace l'ego et les identités du vieux monde par des clés cryptographiques.
    """
    @staticmethod
    def generer_nouvelle_conscience():
        # Génération d'une paire de clés sur la courbe elliptique SECP256K1
        cle_privee = ec.generate_private_key(ec.SECP256K1())
        cle_publique = cle_privee.public_key()
        
        # L'adresse publique de la conscience est le hash de sa clé publique
        adresse_publique_bytes = str(cle_publique.public_numbers()).encode('utf-8')
        adresse_anonyme = hashlib.sha256(adresse_publique_bytes).hexdigest()
        
        return cle_privee, adresse_anonyme


class RegistreKarma:
    """
    LE GRAND LIVRE DU KARMA HORIZONTAL
    Gère la distribution automatique des ressources sans hiérarchie.
    """
    def __init__(self, bloc_genesis):
        self.registre = {}
        self.dotation_base = bloc_genesis.registre_initial["credits_base"]

    def inscrire_nouvelle_conscience(self, adresse_anonyme):
        # Application stricte de l'Équité : tout le monde reçoit exactement la même chose
        if adresse_anonyme not in self.registre:
            self.registre[adresse_anonyme] = {
                "solde_longevite": self.dotation_base,
                "karma_orientation": 0
            }
            return True
        return False

    def emettre_flux_karma(self, expediteur, destinataire_projet, montant):
        # Le karma ne sert pas à acheter du confort personnel mais à orienter l'énergie du réseau
        if self.registre.get(expediteur, {}).get("karma_orientation", 0) >= montant:
            self.registre[expediteur]["karma_orientation"] -= montant
            self.registre[destinataire_projet]["karma_orientation"] += montant
            return True
        return False


# ------------------------------------------------------------
# TEST DE VALIDATION DE L'INFRASTRUCTURE
# ------------------------------------------------------------
if __name__ == "__main__":
    print("=== INITIALISATION DU PROTOCOLE NEOC ===")
    
    # 1. Génération du bloc origine
    genesis = NeoCGenesisBlock()
    print(f"Bloc Genesis initialisé avec succès.")
    print(f"Hash Souverain (Bloc 0) : {genesis.hash}")
    print(f"Régime économique inscrit : {genesis.constitution['regime_economique']}\n")
    
    # 2. Initialisation du grand livre
    grand_livre = RegistreKarma(genesis)
    
    # 3. Simulation de l'arrivée de deux consciences autonomes et anonymes
    print("=== ENREGISTREMENT DES PREMIÈRES CONSCIENCES ANONYMES ===")
    _, adresse_alpha = GestionnaireConsciences.generer_nouvelle_conscience()
    _, adresse_beta = GestionnaireConsciences.generer_nouvelle_conscience()
    
    grand_livre.inscrire_nouvelle_conscience(adresse_alpha)
    grand_livre.inscrire_nouvelle_conscience(adresse_beta)
    
    print(f"Conscience Alpha enregistrée (ID) : {adresse_alpha}")
    print(f"Solde de Longévité attribué d'office : {grand_livre.registre[adresse_alpha]['solde_longevite']} unités")
    
    print(f"Conscience Bêta enregistrée (ID) : {adresse_beta}")
    print(f"Solde de Longévité attribué d'office : {grand_livre.registre[adresse_beta]['solde_longevite']} unités")
    
    print("\nL'Équité de l'Unisson est active. Aucun rang n'a été créé.")
    
