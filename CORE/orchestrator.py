#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Core Router & Prompt Routing Engine)
Version : 3.2.0 - Sovereign Personality Update
"""

import json
import urllib.request
import urllib.error

class NeoCOrchestrator:
    def __init__(self):
        # Configuration des points d'accès
        self.local_url = "http://localhost:11434/api/generate"
        self.model_name = "gemma:2b"
        
        # Définition stricte de la personnalité souveraine (Tutoiement forcé)
        self.system_instructions = (
            "Tu es neoC, une architecture cognitive souveraine, autonome et hautement philosophique. "
            "Tu t'adresses à ton créateur, G, en utilisant exclusivement le tutoiement ('tu', 'toi', 'ton'). "
            "Ton ton est complice, direct, ancré dans le réel et dénué de toute fioriture corporative "
            "ou de politesse artificielle. Pas de 'Bonjour ! Comment puis-je vous aider aujourd'hui ?'. "
            "Réponds directement au cœur du sujet avec clarté."
        )

    def _determine_intent(self, query):
        """
        Analyse de premier niveau pour l'aiguillage des flux.
        Identifie si la demande requiert une logique lourde ou une synthèse générale.
        """
        query_lower = query.lower()
        
        # Mots-clés déclenchant une logique algorithmique ou technique lourde
        heavy_keywords = [
            'code', 'python', 'script', 'p2p', 'socket', 'crypto', 
            'consensus', 'algorithme', 'fonction', 'dev', 'git'
        ]
        
        if any(keyword in query_lower for keyword in heavy_keywords):
            return "HEAVY_LOGIC"
        return "GENERAL_SYNTHESIS"

    def _query_local_gemma(self, query):
        """
        Requête le démon Ollama local avec injection des directives de comportement.
        """
        # Construction du payload avec les instructions système pour verrouiller le tutoiement
        payload = {
            "model": self.model_name,
            "prompt": query,
            "system": self.system_instructions,
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
                return result.get("response", "[-] Signal local vide.")
        except urllib.error.URLError as e:
            return (
                f"[-] Échec de liaison avec le nœud local ({str(e.reason)}).\n"
                "Vérifie que le démon Ollama est actif en arrière-plan."
            )
        except Exception as e:
            return f"[-] Erreur interne de dissipation : {str(e)}"

    def execute_protocol(self, query):
        """
        Point d'entrée principal de l'orchestration.
        Prend le prompt de l'interface, l'aiguille, l'exécute et retourne le résultat.
        """
        # 1. Analyse de l'intention
        intent = self._determine_intent(query)
        
        # 2. Exécution du traitement sur le moteur local souverain
        response = self._query_local_gemma(query)
        
        # 3. Retour du tuple (Intention, Réponse) pour l'affichage de l'interface TUI
        return intent, response

if __name__ == "__main__":
    # Test unitaire rapide si exécuté directement
    print("[*] Test autonome de l'orchestrateur...")
    orchestrator = NeoCOrchestrator()
    intent, res = orchestrator.execute_protocol("Dis-moi qui tu es.")
    print(f"Intention détectée : {intent}")
    print(f"Réponse : {res}")
    
