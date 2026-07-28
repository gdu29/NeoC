#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GENESiS (System Bootloader & API Gateway Launcher)
Version : 2.0.0 - Universal API Watchdog
"""

import os
import sys
import subprocess
import time
import urllib.request
import json

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
    """S'assure que le modèle requis est présent localement, sinon le télécharge."""
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
        print(f" ⚠️ Note : Impossible de valider/télécharger le modèle automatiquement ({str(e)}).")
        return False

def boot_sequence():
    print("==================================================")
    print(" ✨⚓🌐  NEOC GENESIS : SÉQUENCE DE RÉVEIL  🌐⚓✨ ")
    print("==================================================")
    
    # 1. Configuration du PYTHONPATH
    print("\n[1/3] Alignement du système...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    os.environ["PYTHONPATH"] = f"{current_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
    print(" -> Configuration de l'espace de noms : ✅ OK")

    # 2. Watchdog Ollama (Détection d'environnement Termux optionnelle)
    print("\n[2/3] Analyse du moteur IA local...")
    ollama_ready = False
    
    if check_ollama_alive():
        print(" -> Serveur Ollama détecté : ✅ ACTIF")
        ollama_ready = True
    else:
        print(" -> Serveur Ollama silencieux : 🔄 Démarrage du service...")
        try:
            # Tente le wake-lock uniquement si l'outil Termux est présent
            subprocess.run(["termux-wake-lock"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (FileNotFoundError, Exception):
            pass  # Hors d'un environnement Termux, ignoré silencieusement

        try:
            cmd = "nohup ollama serve > /dev/null 2>&1 &"
            subprocess.Popen(cmd, shell=True, preexec_fn=os.setpgrp if hasattr(os, 'setpgrp') else None)
            
            for attempt in range(20):
                print(f"    Initialisation en cours... {((20 - attempt) * 0.5):.1f}s", end="\r")
                time.sleep(0.5)
                if check_ollama_alive():
                    ollama_ready = True
                    break
                
            if ollama_ready:
                print("\n -> Réveil du moteur local : ✅ SUCCÈS")
            else:
                print("\n -> Réveil du moteur local : ⚠️ LENT (Vérification continue)")
        except Exception as e:
            print(f" -> Alerte : ❌ Échec de lancement Ollama ({str(e)}).")

    if ollama_ready:
        check_and_pull_model(DEFAULT_MODEL)

    # 3. Lancement du serveur API (Gateway)
    print("\n[3/3] Démarrage du serveur API NeoC...")
    api_path = os.path.join(current_dir, "api.py")
    
    if not os.path.exists(api_path):
        # Sécurité si le fichier api.py est placé dans un sous-dossier CORE
        api_path = os.path.join(current_dir, "CORE", "api.py")
    
    if not os.path.exists(api_path):
        print(f"❌ Erreur critique : Impossible de trouver 'api.py'")
        sys.exit(1)
        
    print(f" ⚓ Passage de relais à l'API Gateway (`{os.path.basename(api_path)}`).\n")
    time.sleep(0.5)
    
    os.chdir(current_dir)
    
    try:
        # Remplace le processus Genesis par le serveur API
        os.execv(sys.executable, [sys.executable, api_path])
    except Exception as e:
        print(f"❌ Échec de la transition : {str(e)}")

if __name__ == "__main__":
    boot_sequence()
            
