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
    print("  <mot>       : Active/crée un concept en mémoire de travail")
    print("  !learn <d>  : Déclenche la plasticité avec le signal delta")
    print("  !inspect <m>: Affiche les liens causaux d'un mot sur le SSD")
    print("  !quit       : Quitte l'interface")
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

            elif user_input.startswith("!inspect"):
                parts = user_input.split()
                if len(parts) > 1:
                    word = parts[1].lower()
                    if word in lexicon.word2id:
                        node_id = lexicon.word2id[word]
                        node = read_node(db_file, node_id)
                        if node:
                            ptrs = node[2:6]
                            # Filtrage strict : 0 est un slot vide sauf si le parent pointe explicitement vers l'ID 0
                            linked_words = [lexicon.get_word(p) for p in ptrs if p != 0]
                            print(f"  [DISQUE] Nœud {node_id} ('{word}')")
                            print(f"  Poids : {node[6]:.2f}")
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
