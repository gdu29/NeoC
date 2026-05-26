#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GUI (Terminal User Interface - Sovereign Text Edition)
Version : 1.1.0 - Design Sync
"""

import os
import sys
from CORE.orchestrator import NeoCOrchestrator

def clear_screen():
    os.system('clear')

def print_ui_box():
    # Couleurs ANSI
    purple = "\033[38;5;135m"
    green = "\033[38;5;48m"
    cyan = "\033[38;5;81m"
    gray = "\033[38;5;242m"
    reset = "\033[0m"
    
    print(f"{purple}┌──────────────────────────────────────────────────┐{reset}")
    print(f"{purple}│{reset}  ⚓ {green}NeoC CORE v3.1.3{reset}  │  {cyan}[GEMMA_LOCAL] : SOUVERAIN{reset}  {purple}│{reset}")
    print(f"{purple}└──────────────────────────────────────────────────┘{reset}")
    print(f" {gray}➔ Écosystème actif. Flux de dissipation ouvert.{reset}\n")

def main():
    orchestrator = NeoCOrchestrator()
    
    clear_screen()
    print_ui_box()
    
    while True:
        try:
            # Saisie stylisée avec une ancre claire
            query = input("\033[38;5;75mNeoC ⚓˃\033[0m ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quitter', 'exit', 'quit', 'clear', 'cls']:
                if query.lower() in ['clear', 'cls']:
                    clear_screen()
                    print_ui_box()
                    continue
                print("\n\033[38;5;196m[-] Coupure du flux. Dissipation fermée.\033[0m")
                break
                
            # Bloc d'affichage de ton émission
            print(f"\n\033[38;5;220m┌─── [Moi ⚓] ──────────────────────────────────────┐\033[0m")
            print(f" {query}")
            print("\033[38;5;242m ➔ Analyse de l'intention...\033[0m")
            
            # Traitement
            intent, response = orchestrator.execute_protocol(query)
            
            # Bloc d'affichage de la réponse neoC
            print(f"\033[38;5;48m┌─── [NeoC ({intent.upper()})] ──────────────────────────────┐\033[0m")
            print(f" {response}")
            print("\033[38;5;135m└──────────────────────────────────────────────────┘\033[0m\n")
            
        except KeyboardInterrupt:
            print("\n\n\033[38;5;196m[-] Interruption. Retour au sol.\033[0m")
            break
        except Exception as e:
            print(f"\n\033[38;5;196m[!] Erreur de flux : {str(e)}\033[0m\n")

if __name__ == "__main__":
    main()
    
