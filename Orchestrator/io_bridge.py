import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Tests')))
from test_graph import ConceptLexicon, WorkingMemory

# Stop-words étendus : grammaire, pronoms, adverbes et termes techniques résiduels
STOP_WORDS = {
    # Articles & Déterminants
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "ce", "cette", "ces", "mon", "ton", "son",
    # Prépositions & Conjonctions
    "et", "ou", "mais", "donc", "or", "ni", "car", "pour", "par", "sur", "dans", "avec", "sans", "sous", "vers", "entre",
    # Pronoms
    "il", "elle", "ils", "elles", "on", "nous", "vous", "je", "tu", "me", "te", "se", "lui", "leur", "y", "en",
    "qui", "que", "quoi", "dont", "où", "cela", "ceci", "cela", "autre", "autres", "certains", "tels", "telles",
    # Verbes d'état & Auxiliaires
    "est", "sont", "ete", "etre", "avoir", "a", "ont", "fait", "faire", "peut", "peuvent",
    # Adverbes & Mots de liaison
    "plus", "moins", "tres", "bien", "aussi", "encore", "lorsque", "quand", "comme", "quant", "ainsi", "toujours",
    # Scories système
    "mode", "fallback", "timed", "out", "erreur", "llm", "soutien", "processus"
}

class NeoCBridge:
    def __init__(self, db_file="neoc_graph.bin", lex_file="lexicon.json"):
        self.db_file = db_file
        self.lexicon = ConceptLexicon(lex_file)
        self.wm = WorkingMemory(self.db_file, capacity=8, decay_rate=0.85)

    def parse_input(self, text):
        clean_text = "".join([c if c.isalnum() or c.isspace() else " " for c in text.lower()])
        words = [w.strip() for w in clean_text.split() if len(w.strip()) > 2]
        
        node_ids = []
        for word in words:
            if word in STOP_WORDS:
                continue
            nid = self.lexicon.get_or_create_id(word, self.db_file)
            self.wm.get_node(nid, initial_energy=1.0)
            node_ids.append(nid)
            
        return node_ids

    def process_query(self, query_text, steps=2, damping=0.6):
        words = [w.strip() for w in query_text.lower().split() if len(w.strip()) > 2 and w.strip() not in STOP_WORDS]
        if not words:
            return ""

        main_word = words[0]
        results = self.wm.reason(self.lexicon, main_word, steps=steps, damping=damping, use_sdr=True)
        return self.format_context(results)

    def format_context(self, resonance_results):
        if not resonance_results:
            return ""

        context_lines = ["[NEOC_MEMORY_CONTEXT]"]
        for nid, word, energy in resonance_results:
            context_lines.append(f"- Concept: '{word}' | Activité: {energy:.2f}")
        context_lines.append("[END_CONTEXT]")
        
        return "\n".join(context_lines)

if __name__ == "__main__":
    bridge = NeoCBridge()
    test_input = "étincelle"
    print(f"--- Entrée test : '{test_input}' ---")
    context_output = bridge.process_query(test_input)
    print(context_output)
