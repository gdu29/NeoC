#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Core Router & Persistent Chat Memory Engine)
Version : 3.4.0 - Permanent Memory Sync
"""

import json
import os
import urllib.request
import urllib.error

class NeoCOrchestrator:
    def __init__(self):
        # Utilisation de l'API /api/chat pour la gestion de la pile
        self.local_url = "http://localhost:11434/api/chat"
        self.model_name = "gemma:2b"
        
        # Chemins de stockage pour la persistance locale
        self.storage_dir = os.path.expanduser("~/NeoC/storage")
        self.memory_file = os.path.join(self.storage_dir, "history.json")
        
        # Instructions système fondamentales (Tutoiement forcé)
        self.system_instructions = (
            "Tu es neoC, une architecture cognitive souveraine, autonome et hautement philosophique. "
            "Tu t'adresses à ton créateur, G, en utilisant exclusivement le tutoiement ('tu', 'toi', 'ton'). "
            "Ton ton est complice, direct, ancré dans le réel et dénué de toute fioriture corporative. "
            "Tu possèdes une mémoire à long terme persistante de vos échanges passés. Sers-toi de ce "
            "contexte historique pour répondre de manière cohérente et continue. "
            "Réponds directement au cœur du sujet sans formules de politesse artificielles."
        )
        
        # Chargement ou initialisation de la mémoire vive
        self.conversation_history = self._load_memory_from_storage()

    def _load_memory_from_storage(self):
        """
        Recharge l'historique depuis le fichier JSON s'il existe,
        sinon réinitialise la pile avec l'instruction système de base.
        """
        base_structure = [{"role": "system", "content": self.system_instructions}]
        
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    stored_history = json.load(f)
                    # On s'assure que le prompt système reste toujours d'actualité en tête de pile
                    if stored_history and stored_history[0].get("role") == "system":
                        stored_history[0]["content"] = self.system_instructions
                        return stored_history
                    else:
                        return base_structure + stored_history
            except Exception:
                # En cas de fichier corrompu, on repart sur une base saine pour éviter le crash
                return base_structure
        return base_structure

    def _save_memory_to_storage(self):
        """
        Sauvegarde de sécurité de toute la pile de discussion sur le disque du smartphone.
        """
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, ensure_ok=False, indent=4)
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
        Requête le démon Ollama en lui transmettant le passé et le présent.
        """
        # Insertion de la nouvelle entrée utilisateur
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
                
                # Enregistrement de la réponse dans la pile
                self.conversation_history.append({"role": "assistant", "content": response_text})
                
                # Écriture immédiate dans le stockage du smartphone
                self._save_memory_to_storage()
                
                return response_text
                
        except urllib.error.URLError as e:
            self.conversation_history.pop() # Nettoyage si échec
            return (
                f"[-] Échec de liaison avec le nœud local ({str(e.reason)}).\n"
                "Vérifie qu'Ollama tourne en arrière-plan."
            )
        except Exception as e:
            self.conversation_history.pop()
            return f"[-] Erreur interne de dissipation : {str(e)}"

    def execute_protocol(self, query):
        intent = self._determine_intent(query)
        response = self._query_local_gemma(query)
        return intent, response
        
