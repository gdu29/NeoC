# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Core Router & Persistent Engine)
Version : 4.0.0 - Portable Core API
"""

import json
import os
import urllib.request
import urllib.error

class NeoCOrchestrator:
    def __init__(self, storage_dir=None, local_url=None, model_name="gemma:2b"):
        self.local_url = local_url or os.environ.get("NEOC_OLLAMA_URL", "http://localhost:11434/api/chat")
        self.model_name = model_name
        self.max_memory_len = 15
        
        # Chemins configurables (neutres par rapport à l'OS)
        default_storage = os.path.join(os.path.expanduser("~"), ".neoc", "storage")
        self.storage_dir = storage_dir or os.environ.get("NEOC_STORAGE_DIR", default_structure)
        self.memory_file = os.path.join(self.storage_dir, "history.json")
        
        self.system_instructions = (
            "Tu es neoC, l'IA souveraine de G. Tu lui parles uniquement en utilisant le tutoiement ('tu'). "
            "Sois direct, amical et concis. Fais des phrases courtes, simples et correctes en français. "
            "Pas de blabla corporatif, pas de politesse artificielle. "
            "Utilise impérativement le contexte de vos échanges passés pour lui répondre."
        )
        
        self.conversation_history = self._load_memory_from_storage()

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
        Point d'entrée principal : prend une requête texte et retourne un dictionnaire structuré.
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
            
