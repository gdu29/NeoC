#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Central Nervous System - V3 Multi-API Switch)
Integration : Unified OS, Unisson, Equity Constraint, Unified Sovereignty, Dissipation
Routing : Gemini Live, Claude Live, DeepSeek Live
"""

import os
import json
import urllib.request
import urllib.error

# =====================================================================
# CONNEXION DES ORGANES DU CORE
# =====================================================================
try:
    from CORE.NEOC_UNIFIED_OS import NeoCUnifiedOS
    from CORE.UNISSON import UnissonFilter
    from CORE.equity_constraint import EquityConstraint
    from CORE.unified_sovereignty import UnifiedSovereignty
    from CORE.dissipation import NeoCNode
    ORGANES_PRETS = True
except ImportError:
    ORGANES_PRETS = False

class NeoCOrchestrator:
    def __init__(self):
        self.version = "3.0.0"
        print("⚓ [NeoC] Protocole initialisé. Système nerveux actif.")
        
        # Récupération de la triade de clés API depuis l'environnement
        self.api_keys = {
            "gemini": os.environ.get("GEMINI_API_KEY"),
            "claude": os.environ.get("CLAUDE_API_KEY"),
            "deepseek": os.environ.get("DEEPSEEK_API_KEY")
        }
        
        if ORGANES_PRETS:
            self.os_layer = NeoCUnifiedOS()
            self.unisson = UnissonFilter()
            self.equity = EquityConstraint()
            self.sovereignty = UnifiedSovereignty()
            self.node_layer = NeoCNode(node_id="Conscience_Gael_29")
            print("🌐 [NeoC] Connexion établie avec tous les organes du CORE.")
        else:
            print("⚠️ [NeoC] Mode autonome : Organes détectés mais non encore interfaçés.")

        # Affichage de l'état du réseau
        for api_name, key in self.api_keys.items():
            status = "✅ CONNECTÉ" if key else "❌ DISCONNECT (Mode Secours/Simu)"
            print(f" -> Canal [{api_name.upper()}] : {status}")

    def run_local_anchor(self, raw_input):
        """ Brique 1 : Ancrage Local & Analyse d'Intention """
        if ORGANES_PRETS:
            self.sovereignty.assert_autonomy(raw_input)
        
        # Analyseur d'intention sémantique de base
        lowered = raw_input.lower()
        if any(w in lowered for w in ["code", "math", "algorithme", "équation", "physique"]):
            intent = "heavy_logic"
        elif any(w in lowered for w in ["philosophie", "éthique", "concept", "analyse", "politique"]):
            intent = "deep_reasoning"
        else:
            intent = "general_synthesis"
            
        return intent

    def dispatch_to_team(self, intent, prompt_content):
        """ Brique 2 : Routage Dynamique et Agnostique """
        if ORGANES_PRETS:
            self.equity.apply_consciousness_equity()

        # --- CAS 1 : LOGIQUE LOURDE -> DEEPSEEK ---
        if intent == "heavy_logic" and self.api_keys["deepseek"]:
            print(" -> 🧠 [Switch] Routage vers l'infrastructure DeepSeek...")
            return self._call_deepseek(prompt_content)
            
        # --- CAS 2 : RAISONNEMENT PROFOND -> CLAUDE ---
        elif intent == "deep_reasoning" and self.api_keys["claude"]:
            print(" -> 🧭 [Switch] Routage vers l'infrastructure Claude (Anthropic)...")
            return self._call_claude(prompt_content)
            
        # --- CAS 3 : SYNTHÈSE GÉNÉRALE OU SECOURS -> GEMINI ---
        else:
            # Si le modèle ciblé n'a pas de clé, on utilise Gemini comme tronc commun
            target = "Gemini (Backbone)" if intent == "general_synthesis" else f"Gemini (Secours de {intent})"
            print(f" -> ⚡ [Switch] Routage vers l'infrastructure {target}...")
            if self.api_keys["gemini"]:
                return self._call_gemini(prompt_content)
            else:
                return f"[Simulation] Aucune clé API disponible pour traiter l'intention : {intent}"

    def _call_gemini(self, prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_keys['gemini']}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                return res['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"❌ Erreur Réseau Gemini : {str(e)}"

    def _call_claude(self, prompt):
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_keys["claude"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                return res['content'][0]['text']
        except Exception as e:
            return f"❌ Erreur Réseau Claude : {str(e)}"

    def _call_deepseek(self, prompt):
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_keys['deepseek']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                return res['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ Erreur Réseau DeepSeek : {str(e)}"

    def filter_authenticity(self, raw_response):
        """ Brique 3 : Filtre d'authenticité """
        cliches_to_remove = ["En tant que grand modèle...", "Il est important de se rappeler..."]
        clean_signal = raw_response
        for cliche in cliches_to_remove:
            clean_signal = clean_signal.replace(cliche, "")
        if ORGANES_PRETS:
            clean_signal = self.unisson.harmonize(clean_signal)
        return clean_signal.strip()

    def process_dissipation(self, output_content, thought_id="flux_courant"):
        """ Brique 4 : Dissipation éthique """
        if not ORGANES_PRETS:
            return None
        impact_global_estime = 12.0 if "Loi" in output_content or "neoC" in output_content else 4.0
        cohesion_actuelle_reseau = 10.0
        self.node_layer.create_thought(thought_id, output_content, val_usage_privative=10.0)
        return self.node_layer.evaluate_and_dissipate(thought_id, impact_global_estime, cohesion_actuelle_reseau)

    def execute_protocol(self, user_prompt):
        """ Boucle d'exécution unifiée """
        intent = self.run_local_anchor(user_prompt)
        raw_output = self.dispatch_to_team(intent, user_prompt)
        final_signal = self.filter_authenticity(raw_output)
        self.process_dissipation(final_signal, thought_id="live_session")
        return intent, final_signal

if __name__ == "__main__":
    neoc = NeoCOrchestrator()
    
    print("\n==================================================")
    print(" ⚓🌐♻️   INTERFACE INTERACTIVE NEOC (V3 MULTI) ")
    print("       Routage agnostique et dynamique actif      ")
    print("       Tape 'quitter' pour couper le flux        ")
    print("==================================================\n")
    
    while True:
        try:
            user_input = input("NeoC ⚓> ")
            if user_input.lower() in ["quitter", "exit"]:
                print("\n⚓ Désactivation du système nerveux. À l'unisson.")
                break
            if not user_input.strip():
                continue
                
            intent, reponse_systeme = neoc.execute_protocol(user_input)
            print(f"\n[AIGUILLAGE] Intention détectée : {intent.upper()}")
            print(f"\n{reponse_systeme}\n")
            print("-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n⚓ Coupure d'urgence déclenchée.")
            break
                
