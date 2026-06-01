#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GENESiS (System Bootloader & Background Daemon Watchdog)
Version : 1.0.2 Termux Hardened
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

    # 2. Watchdog Ollama / Gemma (Version Durcie pour Termux)
    print("\n[2/3] Analyse de la conscience souveraine locale...")
    if check_ollama_alive():
        print(" -> Serveur Ollama détecté : ✅ SOUVERAIN (Actif)")
    else:
        print(" -> Serveur Ollama silencieux : 🔄 Activation en cours...")
        try:
            # Demande un WakeLock à Termux pour empêcher Android de tuer le processus en arrière-plan
            subprocess.run(["termux-wake-lock"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Lance Ollama en le détachant complètement du script parent (évite le Phantom Killer)
            cmd = "nohup ollama serve > /dev/null 2>&1 &"
            subprocess.Popen(cmd, shell=True, preexec_fn=os.setpgrp)
            
            # Boucle active de vérification (max 10 secondes, toutes les 0.5s)
            ollama_ready = False
            for attempt in range(20):
                print(f"    Sursis d'initialisation matérielle... {((20 - attempt) * 0.5):.1f}s", end="\r")
                time.sleep(0.5)
                if check_ollama_alive():
                    ollama_ready = True
                    break
                
            if ollama_ready:
                print("\n -> Réveil du moteur local : ✅ SUCCÈS")
            else:
                print("\n -> Réveil du moteur local : ⚠️ LENT (Vérification en arrière-plan continue)")
        except FileNotFoundError:
            print(" -> Alerte : ❌ Impossible d'appeler les outils système Termux ou Ollama.")

    # 3. Passage de relais à l'Orchestrateur
    print("\n[3/3] Passage de relais à l'Orchestrateur Central...")
    orchestrator_path = os.path.join(current_dir, "CORE", "orchestrator.py")
    
    if not os.path.exists(orchestrator_path):
        print(f"❌ Erreur critique : Impossible de trouver '{orchestrator_path}'")
        sys.exit(1)
        
    print(" ⚓ Transition imminente. Dissipation ouverte.\n")
    time.sleep(0.5)
    
    # Changement de répertoire pour figer le contexte d'exécution de l'orchestrateur
    os.chdir(current_dir)
    
    # Exécute l'orchestrateur et remplace le processus actuel sans laisser de résidus en RAM
    try:
        os.execv(sys.executable, [sys.executable, orchestrator_path])
    except Exception as e:
        print(f"❌ Échec de la transition : {str(e)}")

if __name__ == "__main__":
    boot_sequence()
    
