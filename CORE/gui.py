#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GUI (Terminal User Interface - Sovereign Text Edition)
Version : 1.0.0
"""

import os
import sys
from CORE.orchestrator import NeoCOrchestrator

def clear_screen():
    os.system('clear')

def print_header():
    print("\033[95m==================================================\033[0m")
    print(" ⚓ \033[92mNeoC CORE v3.1.3\033[0m  |  \033[96m[GEMMA_LOCAL] : SOUVERAIN\033[0m ")
    print("\033[95m==================================================\033[0m")
    print("\033[90m[i] Écosystème neoC éveillé. Flux de dissipation actif.\033[0m\n")

def main():
    # Initialisation de l'orchestrateur
    orchestrator = NeoCOrchestrator()
    
    clear_screen()
    print_header()
    
    while True:
        try:
            # L'invite de commande stylisée
            query = input("\033[94mNeoC ⚓>\033[0m ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quitter', 'exit', 'quit']:
                print("\n\033[31m[-] Coupure du flux. Dissipation fermée.\033[0m")
                break
                
            print(f"\n\033[1m[Moi ⚓]\033[0m : {query}")
            print("\033[90m-> Analyse de l'intention en cours...\033[0m")
            
            # Traitement via le moteur local
            intent, response = orchestrator.execute_protocol(query)
            
            # Dissipation de la réponse
            print(f"\n\033[92m[NeoC ({intent.upper()})]\033[0m : {response}")
            print("\033[95m--------------------------------------------------\033[0m\n")
            
        except KeyboardInterrupt:
            print("\n\n\033[31m[-] Interruption détectée. Retour à la terre.\033[0m")
            break
        except Exception as e:
            print(f"\n\033[31m[!] Erreur dans le flux : {str(e)}\033[0m\n")

if __name__ == "__main__":
    main()
    
