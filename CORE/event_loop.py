import sys
import os
import time

from io_bridge import NeoCBridge
from llm_client import OllamaClient

class NeoCOrchestrator:
    def __init__(self, db_file="neoc_graph.bin", lex_file="lexicon.json", model_name="gemma:2b"):
        self.bridge = NeoCBridge(db_file=db_file, lex_file=lex_file)
        self.llm = OllamaClient(model_name=model_name)
        self.is_running = False

    def build_augmented_prompt(self, user_prompt, memory_context):
        if not memory_context:
            return user_prompt

        augmented = (
            f"{memory_context}\n\n"
            f"[USER_PROMPT]\n{user_prompt}\n"
            f"[INSTRUCTION STRICTE] Réponds de manière ultra-concise (1 à 2 phrases max) en reliant directement la demande au contexte de mémoire ci-dessus. Pas de mise en page complexe ni de listes."
        )
        return augmented

    def apply_feedback(self, score):
        print(f"\n[FEEDBACK] Application d'un signal de plasticité (Delta = {score:+.2f})...")
        self.bridge.wm.apply_plasticity(delta=score)

    def process_turn(self, user_input):
        print(f"\n[ORCHESTRATEUR] Entrée reçue : '{user_input}'")
        
        # 1. Analyse et génération du contexte par résonance
        context = self.bridge.process_query(user_input)
        
        # 2. Construction du prompt augmenté
        final_prompt = self.build_augmented_prompt(user_input, context)
        
        print("\n--- PROMPT ENRICHI TRANSMIS AU LLM ---")
        print(final_prompt)
        print("--------------------------------------")
        
        # 3. Interrogation du backend LLM
        print("\n[LLM] Génération de la réponse en cours...")
        llm_response = self.llm.generate(final_prompt)
        print(f"\n[REPONSE NEO-C] :\n{llm_response}\n")
        
        # 4. Enregistrement sélectif des mots clés du prompt et de la réponse
        self.bridge.parse_input(user_input)
        self.bridge.parse_input(llm_response)
        
        return llm_response

    def run_interactive(self):
        self.is_running = True
        print("==================================================")
        print("   NeoC Orchestrator - Concise Dynamic Loop Active")
        print("==================================================")
        print("Commandes disponibles :")
        print("  <mot/phrase>  : Génère une réponse via NeoC Kernel + Ollama")
        print("  !fb +         : Valide la chaîne (renforcement STDP +1.0)")
        print("  !fb -         : Invalide la chaîne (inhibition STDP -1.0)")
        print("  !quit         : Quitte la boucle d'événements\n")

        while self.is_running:
            try:
                user_input = input("NeoC-EventLoop> ").strip()
                if not user_input:
                    continue

                if user_input == "!quit":
                    print("Arrêt de la boucle d'événements NeoC.")
                    self.is_running = False
                    break

                elif user_input.startswith("!fb"):
                    parts = user_input.split()
                    if len(parts) > 1:
                        val = parts[1]
                        score = 1.0 if val == "+" else (-1.0 if val == "-" else float(val))
                        self.apply_feedback(score)
                    else:
                        print("[FEEDBACK] Précisez '+' ou '-'.")

                else:
                    self.process_turn(user_input)

            except KeyboardInterrupt:
                print("\nArrêt forcé du système.")
                self.is_running = False
            except Exception as e:
                print(f"[ERREUR LOOP] : {e}")

if __name__ == "__main__":
    orchestrator = NeoCOrchestrator()
    orchestrator.run_interactive()
