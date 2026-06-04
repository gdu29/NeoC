#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GENESiS (System Bootloader & Background Daemon Watchdog)
Version : 1.0.3 Termux Hardened & Auto-Pull
"""

import os
import sys
import subprocess
import time
import urllib.request
import json

# Configuration du modèle local par défaut pour NeoC
DEFAULT_MODEL = "gemma2:2b"

def check_ollama_alive():
    """Vérifie si le serveur Ollama est actif et répond"""
    try:
        req = urllib.request.Request("http://localhost:11434/", method="GET")
        with urllib.request.urlopen(req, timeout=1) as response:
            return response.status == 200
    except Exception:
        return False

def check_and_pull_model(model_name):
    """S'assure que le modèle requis est présent localement, sinon le télécharge"""
    print(f" -> Vérification du modèle [{model_name}]...")
    try:
        # Étape A: Vérifier si le modèle existe déjà dans la liste locale
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                models = [m['name'] for m in data.get('models', [])]
                
                # Vérification flexible (gestion des tags implicites comme :latest)
                if model_name in models or f"{model_name}:latest" in models:
                    print(f" -> Modèle [{model_name}] : ✅ DISPONIBLE EN SOUVERAINETÉ")
                    return True
        
        # Étape B: Si le modèle n'est pas trouvé, on lance le pull
        print(f" -> Modèle [{model_name}] absent : 🔄 Téléchargement initial en cours...")
        # Utilisation de subprocess pour afficher la progression native d'Ollama dans le terminal
        result = subprocess.run(["ollama", "pull", model_name], check=True)
        if result.returncode == 0:
            print(f" -> Téléchargement [{model_name}] : ✅ SUCCÈS")
            return True
    except Exception as e:
        print(f" ⚠️ Note : Impossible de valider/télécharger le modèle automatiquement ({str(e)}).")
        print(" -> Le nœud tentera une exécution directe via l'Orchestrateur.")
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
    ollama_ready = False
    
    if check_ollama_alive():
        print(" -> Serveur Ollama détecté : ✅ SOUVERAIN (Actif)")
        ollama_ready = True
    else:
        print(" -> Serveur Ollama silencieux : 🔄 Activation en cours...")
        try:
            # Demande un WakeLock à Termux pour empêcher Android de tuer le processus en arrière-plan
            subprocess.run(["termux-wake-lock"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Lance Ollama en le détachant complètement du script parent (évite le Phantom Killer)
            cmd = "nohup ollama serve > /dev/null 2>&1 &"
            subprocess.Popen(cmd, shell=True, preexec_fn=os.setpgrp)
            
            # Boucle active de vérification (max 10 secondes, toutes les 0.5s)
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

    # Si le serveur est fonctionnel, on s'assure que le modèle requis est là avant de passer le relais
    if ollama_ready:
        check_and_pull_model(DEFAULT_MODEL)

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
    
