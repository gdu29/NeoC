import sys
import os
import time

from io_bridge import NeoCBridge

class NeoCOrchestrator:
    def __init__(self, db_file="neoc_graph.bin", lex_file="lexicon.json"):
        self.bridge = NeoCBridge(db_file=db_file, lex_file=lex_file)
        self.is_running = False

    def build_augmented_prompt(self, user_prompt, memory_context):
        if not memory_context:
            return user_prompt

        augmented = (
            f"{memory_context}\n\n"
            f"[USER_PROMPT]\n{user_prompt}\n"
            f"[INSTRUCTION] Réponds en tenant compte du contexte de mémoire associative ci-dessus."
        )
        return augmented

    def apply_feedback(self, score):
        """
        Boucle de rétroaction (Feedback Loop) :
        Ajuste la plasticité STDP de la mémoire de travail selon le signal de retour.
        score > 0 : Renforcement (apprentissage)
        score < 0 : Inhibition (correction)
        """
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
        print("--------------------------------------\n")
        
        # 3. Enregistrement des nouveaux mots dans la mémoire de travail
        self.bridge.parse_input(user_input)
        
        return final_prompt

    def run_interactive(self):
        self.is_running = True
        print("==================================================")
        print("   NeoC Orchestrator - Event & Feedback Loop Active")
        print("==================================================")
        print("Commandes disponibles :")
        print("  <mot/phrase>  : Traite l'entrée et affiche le prompt augmenté")
        print("  !fb +         : Valide la chaîne (renforcement STDP +1.0)")
        print("  !fb -         : Invalide la chaîne (inhibition STDP -1.0)")
        print("  !fb <valeur>  : Applique un delta de rétroaction sur mesure")
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
                        if val == "+":
                            score = 1.0
                        elif val == "-":
                            score = -1.0
                        else:
                            score = float(val)
                        self.apply_feedback(score)
                    else:
                        print("[FEEDBACK] Précisez '+' (-1.0 à +1.0).")

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
