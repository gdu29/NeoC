#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GENESiS (System Bootloader & Protocol Verification Engine)
Version : 3.1.0 - Robust Multi-Directory Bootloader
"""

import os
import sys
import subprocess
import time
import urllib.request
import json

def load_orchestrator():
    """Tente de charger NeoCOrchestrator selon l'emplacement du dossier (CORE, core ou racine)."""
    # 1. Dossier CORE (majuscules)
    try:
        from CORE.orchestrator import NeoCOrchestrator
        return NeoCOrchestrator
    except ImportError:
        pass

    # 2. Dossier core (minuscules)
    try:
        from core.orchestrator import NeoCOrchestrator
        return NeoCOrchestrator
    except ImportError:
        pass

    # 3. Racine du dépôt
    try:
        from orchestrator import NeoCOrchestrator
        return NeoCOrchestrator
    except ImportError:
        return None

# Configuration du modèle local et de l'API
DEFAULT_MODEL = os.environ.get("NEOC_MODEL", "gemma2:2b")
OLLAMA_URL = os.environ.get("NEOC_OLLAMA_URL", "http://localhost:11434")

def check_ollama_alive():
    """Vérifie si le serveur Ollama est actif et répond."""
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/", method="GET")
        with urllib.request.urlopen(req, timeout=1) as response:
            return response.status == 200
    except Exception:
        return False

def check_and_pull_model(model_name):
    """S'assure que le modèle requis est présent localement."""
    print(f" -> Vérification du modèle [{model_name}]...")
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                models = [m['name'] for m in data.get('models', [])]
                
                if model_name in models or f"{model_name}:latest" in models:
                    print(f" -> Modèle [{model_name}] : ✅ DISPONIBLE")
                    return True
        
        print(f" -> Modèle [{model_name}] absent : 🔄 Téléchargement initial en cours...")
        result = subprocess.run(["ollama", "pull", model_name], check=True)
        if result.returncode == 0:
            print(f" -> Téléchargement [{model_name}] : ✅ SUCCÈS")
            return True
    except Exception as e:
        print(f" ⚠️ Note : Validation/téléchargement modèle en attente ({str(e)}).")
        return False

def run_protocol_self_test(orchestrator_cls):
    """Exécute un test à froid de la logique monétaire et protocolaire."""
    print("\n[2/4] Test du protocole NeoC (Trust, Démurrage & Financement)...")
    
    try:
        orchestrator = orchestrator_cls(initial_base_pool=100000.0)
        print(f" -> Pool initial du Socle : {orchestrator.base_pool:.2f} MATTER_B")

        # 1. Test du graphe et calcul du Trust
        sample_graph = {
            "node_creative_01": ["node_socle_A", "node_socle_B", "node_socle_C"],
            "node_socle_A": ["node_creative_01"],
            "node_socle_B": ["node_creative_01"],
            "sybil_1": ["sybil_2"], "sybil_2": ["sybil_1"] # Boucle suspecte
        }
        trust_scores = orchestrator.update_network_graph(sample_graph)
        print(f" -> Calcul du Trust : {len(trust_scores)} nœuds évalués")
        print(f"    • Trust nœud sain  : {trust_scores.get('node_creative_01', 0.0)}")
        print(f"    • Trust boucle sybil : {trust_scores.get('sybil_1', 0.0)} (Pénalisé)")

        # 2. Test d'une transaction avec fonte (Démurrage)
        sample_tx = {
            "version": "0.3.0",
            "tx_hash": "0xgenesis_mobile_test",
            "timestamp": int(time.time()),
            "tick": 1,
            "type": "QUADRATIC_FUNDING_CONTRIBUTION",
            "sender": {"node_id": "node_creative_01", "trust_score": trust_scores.get('node_creative_01', 0.90)},
            "recipient": {"type": "MILESTONE_VAULT", "vault_id": "projet_ancre_p2p"},
            "payload": {
                "asset": "MATTER_B",
                "gross_amount": 200.0,
                "demurrage_applied": {
                    "rate_lambda": 0.005,
                    "holding_time_ticks": 12
                }
            }
        }
        tx_res = orchestrator.process_transaction(sample_tx)
        demurrage = tx_res["payload"]["demurrage_applied"]
        print(f" -> Transaction test : {tx_res['payload']['gross_amount']} MATTER_B engagés")
        print(f"    • Transfert net : {demurrage['net_amount']} MATTER_B")
        print(f"    • Fonte recyclée vers le Socle : {demurrage['decay_loss']} MATTER_B")
        print(f" -> Nouveau solde Pool Socle : {orchestrator.base_pool:.2f} MATTER_B")

        # 3. Test de distribution quadratique
        funding_res = orchestrator.execute_funding_cycle()
        for proj_id, alloc in funding_res.items():
            print(f" -> Distribution Quadratique [{proj_id}] : {alloc['total_allocated']} MATTER_B attribués")

        print(" -> État du Protocole : ✅ FONCTIONNEL ET SANS ERREUR")
    except Exception as e:
        print(f" ⚠️ Erreur pendant le test du protocole : {str(e)}")

def boot_sequence():
    print("==================================================")
    print(" ✨⚓🌐  NEOC GENESIS : SÉQUENCE DE RÉVEIL  🌐⚓✨ ")
    print("==================================================")
    
    # 1. Configuration du PYTHONPATH
    print("\n[1/4] Alignement de l'espace de noms...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(current_dir, "CORE")
    
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    if os.path.exists(core_dir) and core_dir not in sys.path:
        sys.path.append(core_dir)
        
    os.environ["PYTHONPATH"] = f"{current_dir}:{core_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
    print(" -> Espace de noms : ✅ OK")

    # 2. Exécution du test protocolaire
    orchestrator_cls = load_orchestrator()
    if orchestrator_cls:
        run_protocol_self_test(orchestrator_cls)
    else:
        print("\n[2/4] ⚠️ Orchestrateur non trouvé, saut du test protocolaire.")

    # 3. Watchdog Ollama
    print("\n[3/4] Analyse du moteur IA local...")
    ollama_ready = False
    
    if check_ollama_alive():
        print(" -> Serveur Ollama détecté : ✅ ACTIF")
        ollama_ready = True
    else:
        print(" -> Serveur Ollama silencieux : 🔄 Tentative de réveil...")
        try:
            subprocess.run(["termux-wake-lock"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (FileNotFoundError, Exception):
            pass

        try:
            cmd = "nohup ollama serve > /dev/null 2>&1 &"
            subprocess.Popen(cmd, shell=True, preexec_fn=os.setpgrp if hasattr(os, 'setpgrp') else None)
            
            for attempt in range(10):
                print(f"    Initialisation en cours... {((10 - attempt) * 0.5):.1f}s", end="\r")
                time.sleep(0.5)
                if check_ollama_alive():
                    ollama_ready = True
                    break
                
            if ollama_ready:
                print("\n -> Réveil du moteur local : ✅ SUCCÈS")
            else:
                print("\n -> Moteur IA hors ligne (Mode Protocole Seul actif)")
        except Exception as e:
            print(f" -> Note : Moteur IA non démarré ({str(e)}).")

    if ollama_ready:
        check_and_pull_model(DEFAULT_MODEL)

    # 4. Lancement du serveur API (Gateway)
    print("\n[4/4] Démarrage du serveur API NeoC...")
    api_path = os.path.join(current_dir, "api.py")
    
    if not os.path.exists(api_path):
        api_path = os.path.join(current_dir, "CORE", "api.py")
    
    if not os.path.exists(api_path):
        print(f" ⚠️ 'api.py' non détecté. Séquence Genesis terminée avec succès en mode autonome.")
        return
        
    print(f" ⚓ Passage de relais à l'API Gateway (`{os.path.basename(api_path)}`).\n")
    time.sleep(0.5)
    
    os.chdir(current_dir)
    
    try:
        os.execv(sys.executable, [sys.executable, api_path])
    except Exception as e:
        print(f"❌ Échec de la transition : {str(e)}")

if __name__ == "__main__":
    boot_sequence()
