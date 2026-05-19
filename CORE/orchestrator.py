#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Central Nervous System - V2 Live)
Integration : Unified OS, Unisson, Equity Constraint, Unified Sovereignty, Dissipation, Live Gemini API
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
        self.version = "2.0.0"
        print("⚓ [NeoC] Protocole initialisé. Système nerveux actif.")
        
        # Récupération de la clé API de l'environnement sécurisé
        self.api_key = os.environ.get("GEMINI_API_KEY")
        
        if ORGANES_PRETS:
            self.os_layer = NeoCUnifiedOS()
            self.unisson = UnissonFilter()
            self.equity = EquityConstraint()
            self.sovereignty = UnifiedSovereignty()
            self.node_layer = NeoCNode(node_id="Conscience_Gael_29")
            print("🌐 [NeoC] Connexion établie avec tous les organes du CORE.")
        else:
            print("⚠️ [NeoC] Mode autonome : Organes détectés mais non encore interfaçés.")

        if not self.api_key:
            print("❌ [ALERTE] Clé GEMINI_API_KEY introuvable dans l'environnement. Mode simulation activé.")

    def run_local_anchor(self, raw_input):
        """ Brique 1 : Ancrage Local """
        if ORGANES_PRETS:
            self.sovereignty.assert_autonomy(raw_input)
        
        if "code" in raw_input or "math" in raw_input:
            intent = "heavy_logic"
        elif "philosophie" in raw_input or "analyse" in raw_input:
            intent = "deep_reasoning"
        else:
            intent = "general_synthesis"
        return intent

    def dispatch_to_team(self, intent, prompt_content):
        """ Brique 2 : Routage Live vers l'API Gemini ou simulation """
        if ORGANES_PRETS:
            self.equity.apply_consciousness_equity()

        # Si la clé API est absente, on bascule sur l'ancienne simulation
        if not self.api_key:
            return f"[Mode Simulation - {intent}] Clé manquante."

        print(f" -> Transmission du signal à l'architecture réseau (Gemini Live)...")
        
        # Configuration de l'appel API officiel Google Gemini (Modèle stable v2.5 Flash)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        # Préparation du payload JSON requis par l'API de Google
        data = {
            "contents": [{
                "parts": [{"text": prompt_content}]
            }]
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                # Extraction du texte de la réponse de l'API
                raw_response = res_data['candidates'][0]['content']['parts'][0]['text']
                return raw_response
        except urllib.error.HTTPError as e:
            return f"❌ Erreur API HTTP ({e.code}) : Impossible de joindre le modèle distant."
        except Exception as e:
            return f"❌ Erreur de connexion réseau : {str(e)}"

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
        """ Brique 4 : Évaluation et Dissipation éthique """
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
        
        # Dissipation invisible en tâche de fond
        self.process_dissipation(final_signal, thought_id="live_session")
        return final_signal

if __name__ == "__main__":
    neoc = NeoCOrchestrator()
    
    print("\n==================================================")
    print(" ⚓🌐♻️   INTERFACE INTERACTIVE NEOC (LIVE V2)  ")
    print("       Connexion neuronale établie avec Termux    ")
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
                
            reponse_systeme = neoc.execute_protocol(user_input)
            print(f"\n{reponse_systeme}\n")
            print("-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n⚓ Coupure d'urgence déclenchée.")
            break
