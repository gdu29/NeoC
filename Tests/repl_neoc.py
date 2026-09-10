import os
import sys
from test_graph import ConceptLexicon, WorkingMemory, read_node

def start_repl():
    db_file = "neoc_graph.bin"
    lex_file = "lexicon.json"

    lexicon = ConceptLexicon(lex_file)
    wm = WorkingMemory(db_file, capacity=4, decay_rate=0.85)

    print("==================================================")
    print("   NeoC Kernel - Interface d'Amorçage (REPL)")
    print("==================================================")
    print("Commandes disponibles :")
    print("  <mot>         : Active/crée un concept en mémoire de travail")
    print("  !learn <d>    : Excite le lien causal (delta > 0)")
    print("  !inhibit <d>  : Inhibe le lien causal (delta < 0, ex: !inhibit -1.0)")
    print("  !prop [s] [d] : Propage l'activation/inhibition")
    print("  !inspect <m>  : Affiche l'état d'un mot sur SSD")
    print("  !state        : Affiche l'état d'activation de la mémoire")
    print("  !quit         : Quitte l'interface")
    print("--------------------------------------------------\n")

    while True:
        try:
            user_input = input("NeoC> ").strip()
            if not user_input:
                continue

            if user_input == "!quit":
                print("Fermeture du kernel NeoC.")
                break

            elif user_input.startswith("!learn"):
                parts = user_input.split()
                delta = float(parts[1]) if len(parts) > 1 else 1.0
                wm.apply_plasticity(delta=delta)

            elif user_input.startswith("!inhibit"):
                parts = user_input.split()
                delta = float(parts[1]) if len(parts) > 1 else -1.0
                # Force le delta en valeur négative
                wm.apply_plasticity(delta=-abs(delta))

            elif user_input.startswith("!prop"):
                parts = user_input.split()
                steps = int(parts[1]) if len(parts) > 1 else 1
                damping = float(parts[2]) if len(parts) > 2 else 0.5
                wm.propagate(steps=steps, damping=damping)
                print(f"[PROPAGATION] Diffusée sur {steps} pas (dégât={damping}).")
                print("  Activations actuelles :")
                for nid, act in wm.activations.items():
                    print(f"    - {lexicon.get_word(nid)} (ID {nid}) : {act:.2f}")

            elif user_input == "!state":
                print("  Mémoire active (RAM) :")
                for nid in wm.slots:
                    act = wm.activations.get(nid, 0.0)
                    trace = wm.eligibility_traces.get(nid, 0.0)
                    print(f"    - {lexicon.get_word(nid)} (ID {nid}) | Énergie: {act:.2f} | Trace STDP: {trace:.2f}")

            elif user_input.startswith("!inspect"):
                parts = user_input.split()
                if len(parts) > 1:
                    word = parts[1].lower()
                    if word in lexicon.word2id:
                        node_id = lexicon.word2id[word]
                        node = read_node(db_file, node_id)
                        if node:
                            ptrs = node[2:6]
                            linked_words = [lexicon.get_word(p) for p in ptrs if p != 0]
                            act = wm.activations.get(node_id, 0.0)
                            print(f"  [DISQUE] Nœud {node_id} ('{word}')")
                            print(f"  Poids du nœud : {node[6]:.2f} | Énergie RAM : {act:.2f}")
                            print(f"  Pointeurs bruts : {ptrs}")
                            print(f"  Liens causaux actifs : {linked_words if linked_words else 'Aucun'}")
                    else:
                        print(f"  Mot '{word}' inconnu dans le lexique.")

            else:
                words = user_input.split()
                for w in words:
                    node_id = lexicon.get_or_create_id(w, db_file)
                    wm.get_node(node_id)
                print(f"  RAM Active : {[lexicon.get_word(nid) for nid in wm.eligibility_traces.keys()]}")

        except Exception as e:
            print(f"Erreur : {e}")

if __name__ == "__main__":
    start_repl()
