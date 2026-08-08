# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Core Router, Persistent Engine & Cryptographic Sovereignty)
Version : 4.2.0 - Secure Identity & Protocol Integrated Core
"""

import json
import os
import urllib.request
import urllib.error

# Importation des modules protocolaires et cryptographiques de NeoC
try:
    from core.trust import compute_node_trust
    from core.transaction import process_neoc_transaction
    from core.funding import calculate_quadratic_funding
    from core.identity import NeoCIdentity
except ImportError:
    from trust import compute_node_trust
    from transaction import process_neoc_transaction
    from funding import calculate_quadratic_funding
    from identity import NeoCIdentity


class NeoCOrchestrator:
    def __init__(self, storage_dir=None, local_url=None, model_name="gemma2:2b", initial_base_pool=100000.0):
        self.local_url = local_url or os.environ.get("NEOC_OLLAMA_URL", "http://localhost:11434/api/chat")
        self.model_name = model_name
        self.max_memory_len = 15
        
        # Chemins configurables (neutres par rapport à l'OS)
        default_storage = os.path.join(os.path.expanduser("~"), ".neoc", "storage")
        self.storage_dir = storage_dir or os.environ.get("NEOC_STORAGE_DIR", default_storage)
        self.memory_file = os.path.join(self.storage_dir, "history.json")
        
        # Souveraineté cryptographique du nœud
        self.identity = NeoCIdentity()
        self.node_id = self.identity.get_public_key_bytes()
        
        # État du protocole monétaire et réseau NeoC
        self.base_pool = initial_base_pool
        self.network_graph = {}
        self.pending_contributions = []
        self.trust_scores = {}
        
        self.system_instructions = (
            "Tu es neoC, l'IA souveraine de G. Tu lui parles uniquement en utilisant le tutoiement ('tu'). "
            "Sois direct, amical et concis. Fais des phrases courtes, simples et correctes en français. "
            "Pas de blabla corporatif, pas de politesse artificielle. "
            "Utilise impérativement le contexte de vos échanges passés pour lui répondre."
        )
        
        self.conversation_history = self._load_memory_from_storage()

    # --- MÉTHODES DE SOUVERAINETÉ CRYPTOGRAPHIQUE ---

    def sign_transaction(self, tx_data: dict) -> dict:
        """Signe cryptographiquement une transaction avec l'identité du nœud."""
        # On retire la signature si elle existait déjà pour signer le payload brut
        tx_data.pop("signature", None)
        tx_data.pop("sender_public_key", None)
        
        msg = json.dumps(tx_data, sort_keys=True)
        signature = self.identity.sign_message(msg)
        
        tx_data["sender_public_key"] = self.node_id
        tx_data["signature"] = signature.hex()
        return tx_data

    @staticmethod
    def verify_incoming_transaction(tx_data: dict) -> bool:
        """Vérifie l'authenticité d'une transaction reçue d'un tiers."""
        pub_key = tx_data.get("sender_public_key")
        sig_hex = tx_data.get("signature")
        
        if not pub_key or not sig_hex:
            return False
            
        # Recopie des données sans les champs de signature pour la vérification
        clean_tx = dict(tx_data)
        clean_tx.pop("signature", None)
        clean_tx.pop("sender_public_key", None)
        
        msg = json.dumps(clean_tx, sort_keys=True)
        try:
            signature_bytes = bytes.fromhex(sig_hex)
            return NeoCIdentity.verify_signature(pub_key, msg, signature_bytes)
        except Exception:
            return False

    # --- MÉTHODES DU PROTOCOLE MONÉTAIRE ---

    def update_network_graph(self, graph_data: dict) -> dict:
        """Met à jour la topologie du réseau et calcule les scores de Trust."""
        self.network_graph = graph_data
        self.trust_scores = compute_node_trust(self.network_graph)
        return self.trust_scores

    def process_transaction(self, raw_tx: dict) -> dict:
        """Traite une transaction, vérifie sa signature, applique le démurrage et alimente le socle."""
        # Optionnel : rejet strict si la signature est invalide (sauf pour le bootstrap initial)
        if "signature" in raw_tx and not self.verify_incoming_transaction(raw_tx):
            return {"status": "error", "message": "Signature cryptographique invalide."}

        processed_tx, self.base_pool = process_neoc_transaction(raw_tx, self.base_pool)
        
        if processed_tx.get("type") == "QUADRATIC_FUNDING_CONTRIBUTION":
            sender_id = processed_tx.get("sender", {}).get("node_id", "unknown")
            self.pending_contributions.append({
                "project_id": processed_tx.get("recipient", {}).get("vault_id", "unknown"),
                "contributor_id": sender_id,
                "amount": processed_tx.get("payload", {}).get("demurrage_applied", {}).get("net_amount", 0.0),
                "trust_score": self.trust_scores.get(sender_id, 0.10)
            })
            
        return processed_tx

    def execute_funding_cycle(self) -> dict:
        """Déclenche la redistribution quadratique du pool socle vers les projets."""
        if not self.pending_contributions:
            return {}

        results = calculate_quadratic_funding(self.pending_contributions, self.base_pool)
        self.pending_contributions.clear()
        return results

    # --- MÉTHODES DU ROUTEUR COGNITIF & MÉMOIRE ---

    def _load_memory_from_storage(self):
        base_structure = [{"role": "system", "content": self.system_instructions}]
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    stored_history = json.load(f)
                    if stored_history and stored_history[0].get("role") == "system":
                        stored_history[0]["content"] = self.system_instructions
                        return stored_history
                    else:
                        return base_structure + stored_history
            except Exception:
                return base_structure
        return base_structure

    def _save_memory_to_storage(self):
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[Alerte Sauvegarde] : {str(e)}")

    def _determine_intent(self, query):
        query_lower = query.lower()
        heavy_keywords = ['code', 'python', 'script', 'p2p', 'socket', 'crypto', 'consensus', 'dev', 'git']
        if any(keyword in query_lower for keyword in heavy_keywords):
            return "HEAVY_LOGIC"
        return "GENERAL_SYNTHESIS"

    def execute_protocol(self, query):
        """
        Point d'entrée principal pour les requêtes texte : retourne un dictionnaire structuré.
        """
        intent = self._determine_intent(query)
        backup_history = list(self.conversation_history)
        self.conversation_history.append({"role": "user", "content": query})
        
        if len(self.conversation_history) > self.max_memory_len:
            self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-(self.max_memory_len - 1):]

        payload = {
            "model": self.model_name,
            "messages": self.conversation_history,
            "stream": False,
            "options": {
                "temperature": 0.1 if intent == "HEAVY_LOGIC" else 0.7,
                "top_p": 0.9
            }
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            self.local_url, 
            data=data, 
            headers={'Content-Type': 'application/json'},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                result = json.loads(response.read().decode('utf-8'))
                response_text = result.get("message", {}).get("content", "[-] Signal vide.")
                
                self.conversation_history.append({"role": "assistant", "content": response_text})
                self._save_memory_to_storage()
                
                return {
                    "status": "success",
                    "intent": intent,
                    "response": response_text
                }
        except Exception as e:
            self.conversation_history = backup_history
            return {
                "status": "error",
                "intent": intent,
                "error": str(e)
    }
            
