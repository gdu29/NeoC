import sys
import os

# Alignement du chemin d'import vers le kernel dans Tests/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Tests')))
from test_graph import ConceptLexicon, WorkingMemory

class NeoCBridge:
    def __init__(self, db_file="neoc_graph.bin", lex_file="lexicon.json"):
        self.db_file = db_file
        self.lexicon = ConceptLexicon(lex_file)
        self.wm = WorkingMemory(self.db_file, capacity=8, decay_rate=0.85)

    def parse_input(self, text):
        """ Extrait les concepts d'un texte d'entrée et les enregistre dans le lexique """
        # Nettoyage sommaire et découpage en mots
        clean_text = "".join([c if c.isalnum() or c.isspace() else " " for c in text.lower()])
        words = [w.strip() for w in clean_text.split() if len(w.strip()) > 2]
        
        node_ids = []
        for word in words:
            nid = self.lexicon.get_or_create_id(word, self.db_file)
            self.wm.get_node(nid, initial_energy=1.0)
            node_ids.append(nid)
            
        return node_ids

    def process_query(self, query_text, steps=2, damping=0.6):
        """ Analyse une requête complète : extraction, résonance et formatage """
        words = [w.strip() for w in query_text.lower().split() if len(w.strip()) > 2]
        if not words:
            return ""

        # On prend le premier mot-clé principal pour la résonance directe
        main_word = words[0]
        results = self.wm.reason(self.lexicon, main_word, steps=steps, damping=damping, use_sdr=True)
        return self.format_context(results)

    def format_context(self, resonance_results):
        """ Format la mémoire de résonance en bloc de contexte pour un LLM """
        if not resonance_results:
            return ""

        context_lines = ["[NEOC_MEMORY_CONTEXT]"]
        for nid, word, energy in resonance_results:
            context_lines.append(f"- Concept: '{word}' | Activité: {energy:.2f}")
        context_lines.append("[END_CONTEXT]")
        
        return "\n".join(context_lines)

if __name__ == "__main__":
    # Test autonome du pont I/O
    bridge = NeoCBridge()
    test_input = "étincelle"
    print(f"--- Entrée test : '{test_input}' ---")
    context_output = bridge.process_query(test_input)
    print(context_output)
