#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GENESIS (System Bootloader & Background Daemon Watchdog)
Version : 1.0.0 Sovereign Start
"""

import os
import sys
import subprocess
import time
import urllib.request

def check_ollama_alive():
    """Vérifie si le serveur Ollama est actif"""
    try:
        req = urllib.request.Request("http://localhost:11434/", method="GET")
        with urllib.request.urlopen(req, timeout=1) as response:
            return response.status == 200
    except Exception:
        return False

def boot_sequence():
    print("==================================================")
    print(" ✨⚓🌐  NEOC GENESIS : SÉQUENCE DE RÉVEIL  🌐⚓✨ ")
    print("==================================================")
    
    # 1. Configuration dynamique du PYTHONPATH
    print("\n[1/3] Alignement du système nerveux...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ["PYTHONPATH"] = f"{os.environ.get('PYTHONPATH', '')}:{current_dir}".strip(":")
    print(" -> Configuration de l'espace de noms : ✅ EN ANCRE")

    # 2. Watchdog Ollama / Gemma
    print("\n[2/3] Analyse de la conscience souveraine locale...")
    if check_ollama_alive():
        print(" -> Serveur Ollama détecté : ✅ SOUVERAIN (Actif)")
    else:
        print(" -> Serveur Ollama silencieux : 🔄 Activation automatique en arrière-plan...")
        try:
            # Lance ollama serve de manière totalement indépendante et invisible
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # On laisse 3 secondes au démon pour s'installer en RAM
            for i in range(3, 0, -1):
                print(f"    Sursis d'initialisation... {i}s", end="\r")
                time.sleep(1)
                
            if check_ollama_alive():
                print("\n -> Réveil du moteur local : ✅ SUCCÈS")
            else:
                print("\n -> Réveil du moteur local : ⚠️ EN ATTENTE (Démarrage lent ou initial)")
        except FileNotFoundError:
            print(" -> Alerte : ❌ Ollama n'est pas installé via 'pkg install ollama'.")

    # 3. Passage de relais à l'Orchestrateur
    print("\n[3/3] Passage de relais à l'Orchestrateur Central...")
    orchestrator_path = os.path.join(current_dir, "CORE", "orchestrator.py")
    
    if not os.path.exists(orchestrator_path):
        print(f"❌ Erreur critique : Impossible de trouver '{orchestrator_path}'")
        sys.exit(1)
        
    print(" ⚓ Transition imminente. Dissipation ouverte.\n")
    time.sleep(1)
    
    # Exécute l'orchestrateur et remplace le processus actuel
    try:
        os.execv(sys.executable, [sys.executable, orchestrator_path])
    except Exception as e:
        print(f"❌ Échec de la transition : {str(e)}")

if __name__ == "__main__":
    boot_sequence()
    
