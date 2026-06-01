#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GENESiS (System Bootloader & Background Daemon Watchdog)
Version : 1.0.1 Sovereign Stability
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
    
    # 1. Configuration dynamique du PYTHONPATH et de l'environnement
    print("\n[1/3] Alignement du système nerveux...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Sécurisation du chemin pour Python et le système
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    os.environ["PYTHONPATH"] = f"{current_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
    
    print(" -> Configuration de l'espace de noms : ✅ EN ANCRE")

    # 2. Watchdog Ollama / Gemma (Boucle active dynamique)
    print("\n[2/3] Analyse de la conscience souveraine locale...")
    if check_ollama_alive():
        print(" -> Serveur Ollama détecté : ✅ SOUVERAIN (Actif)")
    else:
        print(" -> Serveur Ollama silencieux : 🔄 Activation automatique...")
        try:
            # Lance ollama serve de manière totalement indépendante et invisible
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Boucle active de vérification (max 6 secondes, vérification toutes les 0.5s)
            ollama_ready = False
            for attempt in range(12):
                print(f"    Sursis d'initialisation dynamique... {((12 - attempt) * 0.5):.1f}s", end="\r")
                time.sleep(0.5)
                if check_ollama_alive():
                    ollama_ready = True
                    break
                
            if ollama_ready:
                print("\n -> Réveil du moteur local : ✅ SUCCÈS")
            else:
                print("\n -> Réveil du moteur local : ⚠️ EN ATTENTE (Démarrage lent ou initial)")
        except FileNotFoundError:
            print(" -> Alerte : ❌ Ollama n'est pas installé ou inaccessible dans le PATH.")

    # 3. Passage de relais à l'Orchestrateur
    print("\n[3/3] Passage de relais à l'Orchestrateur Central...")
    orchestrator_path = os.path.join(current_dir, "CORE", "orchestrator.py")
    
    if not os.path.exists(orchestrator_path):
        print(f"❌ Erreur critique : Impossible de trouver '{orchestrator_path}'")
        sys.exit(1)
        
    print(" ⚓ Transition imminente. Dissipation ouverte.\n")
    time.sleep(0.5)
    
    # Changement de répertoire pour que l'orchestrateur s'exécute dans son contexte natif
    os.chdir(current_dir)
    
    # Exécute l'orchestrateur et remplace le processus actuel avec arguments sécurisés
    try:
        os.execv(sys.executable, [sys.executable, orchestrator_path])
    except Exception as e:
        print(f"❌ Échec de la transition : {str(e)}")

if __name__ == "__main__":
    boot_sequence()
    
