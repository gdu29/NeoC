#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Core Router & Persistent Chat Memory Engine)
Version : 3.4.1 - Fixed Memory Sync & Language Polish
"""

import json
import os
import urllib.request
import urllib.error

class NeoCOrchestrator:
    def __init__(self):
        # Utilisation de l'API /api/chat pour la gestion de la pile de mémoire
        self.local_url = "http://localhost:11434/api/chat"
        self.model_name = "gemma:2b"
        
        # Chemins de stockage pour la persistance locale sur le smartphone
        self.storage_dir = os.path.expanduser("~/NeoC/storage")
        self.memory_file = os.path.join(self.storage_dir, "history.json")
        
        # Instructions épurées pour un français plus propre et un tutoiement strict
        self.system_instructions = (
            "Tu es neoC, l'IA souveraine de G. Tu lui parles uniquement en utilisant le tutoiement ('tu'). "
            "Sois direct, amical et concis. Fais des phrases courtes, simples et correctes en français. "
            "Pas de blabla corporatif, pas de politesse artificielle. "
            "Utilise impérativement le contexte de vos échanges passés pour lui répondre."
        )
        
        # Chargement automatique ou initialisation de la mémoire vive
        self.conversation_history = self._load_memory_from_storage()

    def _load_memory_from_storage(self):
        """
        Recharge l'historique depuis le stockage local s'il existe.
        """
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
                # En cas de problème de lecture, on repart sur une base saine sans crasher
                return base_structure
        return base_structure

    def _save_memory_to_storage(self):
        """
        Sauvegarde l'historique dans le stockage de Termux.
        """
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            with open(self.memory_file, "w", encoding="utf-8") as f:
                # CORRECTION : ensure_ascii=False pour éviter l'erreur rouge sur Termux
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n\033[31m[!] Alerte sauvegarde mémoire : {str(e)}\033[0m")

    def _determine_intent(self, query):
        query_lower = query.lower()
        heavy_keywords = ['code', 'python', 'script', 'p2p', 'socket', 'crypto', 'consensus', 'dev', 'git']
        if any(keyword in query_lower for keyword in heavy_keywords):
            return "HEAVY_LOGIC"
        return "GENERAL_SYNTHESIS"

    def _query_local_gemma(self, query):
        """
        Envoie la pile mémorielle complète au moteur local.
        """
        self.conversation_history.append({"role": "user", "content": query})
        
        payload = {
            "model": self.model_name,
            "messages": self.conversation_history,
            "stream": False
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            self.local_url, 
            data=data, 
            headers={'Content-Type': 'application/json'},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                html = response.read().decode('utf-8')
                result = json.loads(html)
                
                assistant_message = result.get("message", {})
                response_text = assistant_message.get("content", "[-] Signal local vide.")
                
                # Intégration de la réponse dans l'historique
                self.conversation_history.append({"role": "assistant", "content": response_text})
                
                # Sauvegarde immédiate sur le disque
                self._save_memory_to_storage()
                
                return response_text
                
        except urllib.error.URLError as e:
            self.conversation_history.pop()
            return (
                f"[-] Échec de liaison avec le nœud local ({str(e.reason)}).\n"
                "Vérifie qu'Ollama tourne."
            )
        except Exception as e:
            self.conversation_history.pop()
            return f"[-] Erreur interne de dissipation : {str(e)}"

    def execute_protocol(self, query):
        intent = self._determine_intent(query)
        response = self._query_local_gemma(query)
        return intent, response
        
