import sys
import os
import time

from io_bridge import NeoCBridge

class NeoCOrchestrator:
    def __init__(self, db_file="neoc_graph.bin", lex_file="lexicon.json"):
        self.bridge = NeoCBridge(db_file=db_file, lex_file=lex_file)
        self.is_running = False

    def build_augmented_prompt(self, user_prompt, memory_context):
        """ Assemble le contexte émergent de NeoC avec la demande de l'utilisateur """
        if not memory_context:
            return user_prompt

        augmented = (
            f"{memory_context}\n\n"
            f"[USER_PROMPT]\n{user_prompt}\n"
            f"[INSTRUCTION] Réponds en tenant compte du contexte de mémoire associative ci-dessus."
        )
        return augmented

    def process_turn(self, user_input):
        """ Traite une boucle cognitive complète (Un tour de parole) """
        print(f"\n[ORCHESTRATEUR] Entrée reçue : '{user_input}'")
        
        # 1. Analyse et génération du contexte par résonance
        context = self.bridge.process_query(user_input)
        
        # 2. Construction du prompt augmenté
        final_prompt = self.build_augmented_prompt(user_input, context)
        
        print("\n--- PROMPT ENRICHI TRANSMIS AU LLM ---")
        print(final_prompt)
        print("--------------------------------------\n")
        
        # 3. Mettre à jour la plasticité/apprentissage à partir des nouveaux mots de l'entrée
        self.bridge.parse_input(user_input)
        
        return final_prompt

    def run_interactive(self):
        """ Boucle d'écoute interactive """
        self.is_running = True
        print("==================================================")
        print("   NeoC Orchestrator - Event Loop Active")
        print("==================================================")
        print("Tape une phrase ou un mot-clé (ou '!quit' pour sortir).\n")

        while self.is_running:
            try:
                user_input = input("NeoC-EventLoop> ").strip()
                if not user_input:
                    continue

                if user_input == "!quit":
                    print("Arrêt de la boucle d'événements NeoC.")
                    self.is_running = False
                    break

                self.process_turn(user_input)

            except KeyboardInterrupt:
                print("\nArrêt forcé du système.")
                self.is_running = False
            except Exception as e:
                print(f"[ERREUR LOOP] : {e}")

if __name__ == "__main__":
    orchestrator = NeoCOrchestrator()
    orchestrator.run_interactive()
