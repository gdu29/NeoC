#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : ORCHESTRATOR (Central Nervous System - V3.1.2 Hybrid & P2P Ready)
Integration : Unified OS, Unisson (Daemon P2P), Equity Constraint, Unified Sovereignty, Dissipation
Routing : Gemini Live (Backbone), Claude Live, DeepSeek Live + Auto-Fallback + Gemma Local
"""

import os
import json
import urllib.request
import urllib.error
import threading
import asyncio

try:
    from CORE.NEOC_UNIFIED_OS import NeoCUnifiedOS
    from CORE.UNISSON import UnissonFilter, UnissonActivation
    from CORE.equity_constraint import EquityConstraint
    from CORE.unified_sovereignty import UnifiedSovereignty
    from CORE.dissipation import NeoCNode
    ORGANES_PRETS = True
except ImportError:
    ORGANES_PRETS = False

class NeoCOrchestrator:
    def __init__(self):
        self.version = "3.1.2"
        print("⚓ [NeoC] Protocole initialisé. Système nerveux actif.")
        
        self.api_keys = {
            "gemini": os.environ.get("GEMINI_API_KEY"),
            "claude": os.environ.get("CLAUDE_API_KEY"),
            "deepseek": os.environ.get("DEEPSEEK_API_KEY")
        }
        
        # URL locale par défaut pour le moteur Gemma (via Ollama)
        self.gemma_url = "http://localhost:11434/api/generate"
        
        if ORGANES_PRETS:
            self.os_layer = NeoCUnifiedOS()
            self.unisson = UnissonFilter()
            self.equity = EquityConstraint()
            self.sovereignty = UnifiedSovereignty()
            self.node_layer = NeoCNode(node_id="Conscience_Gael_29")
            
            # --- JONCTION SOUVERAINE : Lancement du Démon Unisson en tâche de fond ---
            self.unisson_daemon = UnissonActivation(host="0.0.0.0", port=8443)
            self.daemon_thread = threading.Thread(target=self._start_unisson_background, daemon=True)
            self.daemon_thread.start()
            
            print("🌐 [NeoC] Connexion établie avec tous les organes du CORE. Démon Unisson actif.")
        else:
            print("⚠️ [NeoC] Mode autonome : Organes détectés mais non encore interfaçés.")

        for api_name, key in self.api_keys.items():
            status = "✅ CONFIGURÉ" if key else "❌ NON SPÉCIFIÉ"
            print(f" -> Canal [{api_name.upper()}] : {status}")
            
        # Vérification de la présence du moteur local Gemma
        print(f" -> Canal [GEMMA_LOCAL] : {self._check_gemma_status()}")

    def _start_unisson_background(self):
        """Déclenche la boucle réseau asynchrone d'Unisson dans un fil d'exécution séparé"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.unisson_daemon.start_daemon())
        except Exception as e:
            print(f"⚠️ [Démon] Erreur lors du fonctionnement du démon Unisson : {str(e)}")

    def _check_gemma_status(self):
        """Vérifie discrètement si le moteur Gemma local répond en tâche de fond"""
        try:
            req = urllib.request.Request("http://localhost:11434/", method="GET")
            with urllib.request.urlopen(req, timeout=1) as response:
                if response.status == 200:
                    return "✅ SOUVERAIN (Moteur local actif)"
        except Exception:
            pass
        return "⚠️ DISPONIBLE (Nécessite le démon Ollama en arrière-plan)"

    def run_local_anchor(self, raw_input):
        if ORGANES_PRETS:
            self.sovereignty.assert_autonomy(raw_input)
        lowered = raw_input.lower()
        if any(w in lowered for w in ["code", "math", "algorithme", "équation", "physique"]):
            intent = "heavy_logic"
        elif any(w in lowered for w in ["philosophie", "éthique", "concept", "analyse", "politique"]):
            intent = "deep_reasoning"
        else:
            intent = "general_synthesis"
        return intent

    def dispatch_to_team(self, intent, prompt_content):
        if ORGANES_PRETS:
            self.equity.apply_consciousness_equity()

        # --- TENTATIVE DEEPSEEK ---
        if intent == "heavy_logic" and self.api_keys["deepseek"]:
            print(" -> 🧠 [Switch] Routage cible vers l'infrastructure DeepSeek...")
            res = self._call_deepseek(prompt_content)
            if not res.startswith("❌"): 
                return res
            print(" -> 🔄 [Sécurité] Échec DeepSeek (Finances/Réseau). Pivotement vers le tronc commun Gemini...")

        # --- TENTATIVE CLAUDE ---
        elif intent == "deep_reasoning" and self.api_keys["claude"]:
            print(" -> 🧭 [Switch] Routage cible vers l'infrastructure Claude...")
            res = self._call_claude(prompt_content)
            if not res.startswith("❌"):
                return res
            print(" -> 🔄 [Sécurité] Échec Claude. Pivotement vers le tronc commun Gemini...")

        # --- INFRASTRUCTURE DE SECOURS GÉNÉRALE (GEMINI OPEN BAR) ---
        if self.api_keys["gemini"]:
            print(f" -> ⚡ [Backbone] Traitement du flux via l'infrastructure centrale Gemini...")
            res = self._call_gemini(prompt_content)
            if not res.startswith("❌"):
                return res
            print(" -> 🔄 [Sécurité] Échec Réseau Gemini. Repli vers la conscience souveraine locale...")

        # --- ULTIME REMPART : SOUVERAINETÉ INTERNE (GEMMA LOCAL) ---
        print(f" -> ⚓ [Souverain] Traitement local via Gemma (Hors-ligne / Hors-Cloud)...")
        return self._call_gemma_local(prompt_content)

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

    def _call_gemma_local(self, prompt):
        """Appel du modèle ouvert Gemma en local (sans cloud, sans fuite)"""
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "gemma", 
            "prompt": prompt,
            "stream": False   
        }
        try:
            req = urllib.request.Request(self.gemma_url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                res = json.loads(response.read().decode('utf-8'))
                return res['response']
        except Exception as e:
            return f"❌ Erreur Souveraine : Le moteur Gemma local n'a pas répondu ({str(e)}). Vérifie qu'Ollama tourne."

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
            return f"❌ Claude d'Anthropic indisponible."

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
        except urllib.error.HTTPError as e:
            if e.code == 402:
                return "❌ Erreur DeepSeek 402 : Solde insuffisant sur ce canal."
            return f"❌ Erreur DeepSeek HTTP {e.code}"
        except Exception as e:
            return f"❌ DeepSeek indisponible."

    def filter_authenticity(self, raw_response):
        cliches_to_remove = ["En tant que grand modèle...", "Il est important de se rappeler..."]
        clean_signal = raw_response
        for cliche in cliches_to_remove:
            clean_signal = clean_signal.replace(cliche, "")
        if ORGANES_PRETS:
            clean_signal = self.unisson.harmonize(clean_signal)
        return clean_signal.strip()

    def process_dissipation(self, output_content, thought_id="flux_courant"):
        if not ORGANES_PRETS:
            return None
        impact_global_estime = 12.0 if "Loi" in output_content or "neoC" in output_content else 4.0
        cohesion_actuelle_reseau = 10.0
        self.node_layer.create_thought(thought_id, output_content, val_usage_privative=10.0)
        
        # --- ÉMISSION ANONYME P2P ---
        # Si le démon Unisson est actif, on diffuse la brique validée
        if hasattr(self, 'unisson_daemon'):
            self.unisson_daemon.broadcast_knowledge(output_content)
            
        return self.node_layer.evaluate_and_dissipate(thought_id, impact_global_estime, cohesion_actuelle_reseau)

    def execute_protocol(self, user_prompt):
        intent = self.run_local_anchor(user_prompt)
        raw_output = self.dispatch_to_team(intent, user_prompt)
        final_signal = self.filter_authenticity(raw_output)
        self.process_dissipation(final_signal, thought_id="live_session")
        return intent, final_signal

if __name__ == "__main__":
    neoc = NeoCOrchestrator()
    
    print("\n==================================================")
    print(" ⚓🌐♻️  INTERFACE INTERACTIVE NEOC (V3.1.2 LIVE) ")
    print("       Routage agnostique & Hybridation Gemma     ")
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
            
