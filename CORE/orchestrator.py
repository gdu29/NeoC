#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Core Router & Persistent Chat Memory Engine)
Version : 3.4.2 - Context Management & Dynamic Temp Injection
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
        
        # Limite de messages en mémoire vive pour éviter la saturation du contexte (Gemma:2b)
        # 14 messages = l'instruction système + les 13 derniers messages (~6-7 tours complets)
        self.max_memory_len = 15
        
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
                # ensure_ascii=False pour éviter l'erreur rouge sur Termux
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n\033[31m[!] Alerte sauvegarde mémoire : {str(e)}\033[0m")

    def _determine_intent(self, query):
        query_lower = query.lower()
        heavy_keywords = ['code', 'python', 'script', 'p2p', 'socket', 'crypto', 'consensus', 'dev', 'git']
        if any(keyword in query_lower for keyword in heavy_keywords):
            return "HEAVY_LOGIC"
        return "GENERAL_SYNTHESIS"

    def _query_local_gemma(self, query, intent):
        """
        Envoie la pile mémorielle calibrée au moteur local avec paramètres dynamiques.
        """
        # Sauvegarde de sécurité de l'état initial
        backup_history = list(self.conversation_history)
        
        # Ajout du nouveau message utilisateur
        self.conversation_history.append({"role": "user", "content": query})
        
        # Gestion de la fenêtre glissante : on garde le system prompt [0] et les X derniers messages
        if len(self.conversation_history) > self.max_memory_len:
            # On conserve l'index 0 (system) et on coupe les plus anciens messages
            self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-(self.max_memory_len - 1):]

        # Modulation dynamique des paramètres selon l'intention détectée
        generation_options = {
            "temperature": 0.1 if intent == "HEAVY_LOGIC" else 0.7,
            "top_p": 0.9
        }
        
        payload = {
            "model": self.model_name,
            "messages": self.conversation_history,
            "stream": False,
            "options": generation_options
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
                html = response.read().decode('utf-8')
                result = json.loads(html)
                
                assistant_message = result.get("message", {})
                response_text = assistant_message.get("content", "[-] Signal local vide.")
                
                # Intégration de la réponse dans l'historique valide
                self.conversation_history.append({"role": "assistant", "content": response_text})
                
                # Sauvegarde immédiate sur le disque
                self._save_memory_to_storage()
                
                return response_text
                
        except urllib.error.URLError as e:
            self.conversation_history = backup_history  # Restauration de l'état sain
            return (
                f"[-] Échec de liaison avec le nœud local ({str(e.reason)}).\n"
                "Vérifie qu'Ollama tourne."
            )
        except Exception as e:
            self.conversation_history = backup_history  # Restauration de l'état sain
            return f"[-] Erreur interne de dissipation : {str(e)}"

    def execute_protocol(self, query):
        intent = self._determine_intent(query)
        response = self._query_local_gemma(query, intent)
        return intent, response
            
if __name__ == "__main__":
    # Initialisation de l'orchestrateur
    orchestrator = NeoCOrchestrator()
    
    print("==================================================")
    print("      🌐  INTERFACE CONSCIENCE : neoC  🌐        ")
    print("==================================================")
    print(" -> Session active. Taper 'exit' ou 'quit' pour clore.\n")
    
    while True:
        try:
            # Invite de commande personnalisée
            user_input = input("\n\033[1;34m[G.] >\033[0m ")
            
            if not user_input.strip():
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("\n⚓ Dissipation de l'interface. À l'unisson.")
                break
                
            # Exécution du protocole (Intention + Requête locale)
            intent, response = orchestrator.execute_protocol(user_input)
            
            # Affichage de la réponse de neoC
            print(f"\n\033[1;32m[neoC] ({intent}) >\033[0m {response}")
            
        except KeyboardInterrupt:
            print("\n\n⚓ Interruption détectée. Sauvegarde et fermeture.")
            break
        except Exception as e:
            print(f"\n❌ Erreur d'interface : {str(e)}")
            
