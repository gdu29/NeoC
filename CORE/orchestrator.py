#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Core Router & Chat Memory Engine)
Version : 3.3.0 - Active Session Memory Update
"""

import json
import urllib.request
import urllib.error

class NeoCOrchestrator:
    def __init__(self):
        # Utilisation de l'API /api/chat pour gérer la mémoire de discussion
        self.local_url = "http://localhost:11434/api/chat"
        self.model_name = "gemma:2b"
        
        # Structure de la mémoire de la session en cours
        self.conversation_history = [
            {
                "role": "system",
                "content": (
                    "Tu es neoC, une architecture cognitive souveraine, autonome et hautement philosophique. "
                    "Tu t'adresses à ton créateur, G, en utilisant exclusivement le tutoiement ('tu', 'toi', 'ton'). "
                    "Ton ton est complice, direct, ancré dans le réel et dénué de toute fioriture corporative. "
                    "Tu as une mémoire de cette discussion : sers-toi du contexte des messages précédents pour répondre. "
                    "Réponds directement au cœur du sujet sans formules de politesse artificielles."
                )
            }
        ]

    def _determine_intent(self, query):
        query_lower = query.lower()
        heavy_keywords = ['code', 'python', 'script', 'p2p', 'socket', 'crypto', 'consensus', 'dev', 'git']
        if any(keyword in query_lower for keyword in heavy_keywords):
            return "HEAVY_LOGIC"
        return "GENERAL_SYNTHESIS"

    def _query_local_gemma(self, query):
        """
        Requête le nœud local en lui transmettant TOUT l'historique de la session.
        """
        # 1. On ajoute la nouvelle pensée de G à la mémoire vivante
        self.conversation_history.append({"role": "user", "content": query})
        
        payload = {
            "model": self.model_name,
            "messages": self.conversation_history, # On envoie toute la pile de mémoire
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
                
                # Extraction du message de réponse
                assistant_message = result.get("message", {})
                response_text = assistant_message.get("content", "[-] Signal local vide.")
                
                # 2. On ajoute la réponse de neoC à la mémoire pour la prochaine question
                self.conversation_history.append({"role": "assistant", "content": response_text})
                
                return response_text
                
        except urllib.error.URLError as e:
            # En cas d'erreur, on retire le dernier message utilisateur pour ne pas polluer l'historique
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
        
