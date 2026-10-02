# -*- coding: utf-8 -*-
"""
Protocol : NeoC
Module   : MEMORY/bridge.py
Role     : Pont entre le lexique, la mémoire de travail (WorkingMemory) et le graphe
"""

import os
import json
import re
from CORE.MEMORY.graph import NeoCGraph

# ---------------------------------------------------------------------------
# Dictionnaire exhaustif de stop-words français (NeoC Filter)
# ---------------------------------------------------------------------------
FRENCH_STOP_WORDS = {
    # Articles & Déterminants
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "desquelles", "desquels",
    "duquel", "au", "aux", "ce", "cet", "cette", "ces", "mon", "ton", "son", "ma",
    "ta", "sa", "mes", "tes", "ses", "notre", "votre", "leur", "nos", "vos", "leurs",
    
    # Pronoms
    "je", "j", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles", "me", "m",
    "te", "t", "se", "s", "lui", "y", "en", "moi", "toi", "soi", "cela", "ceci",
    "celui", "celle", "ceux", "celles", "qui", "que", "quoi", "dont", "où", "lequel",
    "laquelle", "lesquels", "lesquelles", "quelqu", "quelque", "quelques",
    
    # Verbes auxiliaires et modaux courants (et conjugaisons)
    "être", "est", "sont", "été", "étant", "suis", "es", "sommes", "êtes", "était",
    "étaient", "avoir", "ai", "as", "a", "avons", "avez", "ont", "eu", "ayant",
    "faire", "fait", "fais", "faisons", "faites", "font", "dire", "dit",
    "dis", "disons", "dites", "disent", "pouvoir", "peux", "peut", "pouvons",
    "pouvez", "peuvent", "vouloir", "veux", "veut", "voulons", "voulez", "veulent",
    "devoir", "dois", "doit", "devons", "devez", "doivent", "aller", "vais", "vas",
    "va", "allons", "allez", "vont", "parler", "parle", "parles", "parlons", "parlez",
    
    # Prépositions & Conjonctions
    "à", "avec", "par", "pour", "en", "vers", "sans", "sous", "sur", "dans",
    "chez", "pendant", "durant", "selon", "malgré", "outre", "entre", "contre",
    "après", "avant", "depuis", "dès", "devant", "derrière", "jusqu", "jusque",
    "et", "ou", "mais", "donc", "or", "ni", "car", "si", "comme", "quand",
    "lorsque", "puisque", "quoique",
    
    # Adverbes & Mots outils / Remplissage
    "pas", "ne", "plus", "moins", "tres", "très", "bien", "aussi", "encore", "toujours",
    "jamais", "trop", "peu", "beaucoup", "assez", "ici", "là", "oui", "non", "souvent",
    "parfois", "alors", "ainsi", "comment", "pourquoi", "quel", "quelle",
    "quels", "quelles", "sujet", "complexe", "chose", "merci", "salut", "bonjour"
}


class NeoCBridge:
    def __init__(self, db_file="neoc_graph.bin", lex_file="lexicon.json"):
        self.db_file = db_file
        self.lex_file = lex_file
        self.graph = NeoCGraph()
        self.lexicon = {}      # {word: id}
        self.rev_lexicon = {}  # {id: word}
        
        # Tampons pour conserver la séparation des concepts entre la question et la réponse
        self.last_query_nodes = []
        self.last_response_nodes = []
        
        self._load_lexicon()

    def _load_lexicon(self):
        """Charge le lexique en s'assurant que la structure {mot: ID} est respectée."""
        if os.path.exists(self.lex_file):
            try:
                with open(self.lex_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.lexicon = {str(k): int(v) for k, v in data.items()}
                        self.rev_lexicon = {int(v): str(k) for k, v in data.items()}
            except Exception as e:
                print(f"[Alerte Bridge] Échec du chargement du lexique : {e}")

    def _save_lexicon(self):
        """Sauvegarde le dictionnaire {mot: ID} au format JSON."""
        try:
            with open(self.lex_file, "w", encoding="utf-8") as f:
                json.dump(self.lexicon, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[Alerte Bridge] Échec de sauvegarde du lexique : {e}")

    def clean_tokens(self, text: str) -> list:
        """Découpe le texte, retire la ponctuation et filtre les stop-words."""
        tokens = re.findall(r'\b\w+\b', text.lower())
        filtered = [
            t for t in tokens 
            if t not in FRENCH_STOP_WORDS and len(t) > 2 and not t.isdigit()
        ]
        return filtered

    def _get_or_create_node_id(self, word: str) -> int:
        if word not in self.lexicon:
            node_id = len(self.lexicon)
            self.lexicon[word] = node_id
            self.rev_lexicon[node_id] = word
            self._save_lexicon()
            print(f"[LEXIQUE] Nouveau concept clé enregistré : '{word}' -> ID {node_id}")
            return node_id
        return self.lexicon[word]

    def parse_input(self, text: str) -> list:
        """Extrait les mots-clés du texte et renvoie leurs IDs de nœud."""
        tokens = self.clean_tokens(text)
        node_ids = [self._get_or_create_node_id(t) for t in tokens]
        return node_ids

    def process_query(self, query: str) -> str:
        """
        Gère la requête utilisateur, extrait les nœuds d'entrée et
        construit le contexte de résonance.
        """
        self.last_query_nodes = self.parse_input(query)
        
        connected_concepts = []
        for src in self.last_query_nodes:
            for tgt, weight in self.graph.adj.get(src, {}).items():
                if weight > 0.3:
                    src_word = self.rev_lexicon.get(src, str(src))
                    tgt_word = self.rev_lexicon.get(tgt, str(tgt))
                    connected_concepts.append(f"{src_word} -> {tgt_word}")

        if connected_concepts:
            return f"[CONTEXTE MÉMOIRE DE TRAVAIL : {', '.join(connected_concepts)}]"
        return ""

    def register_response(self, response_text: str):
        """Enregistre les concepts clés de la réponse générée par l'IA."""
        self.last_response_nodes = self.parse_input(response_text)

    def apply_plasticity(self, delta: float):
        """
        Applique la plasticité STDP entre les concepts de la requête
        et ceux de la réponse avec affichage détaillé dans le terminal.
        """
        if not self.last_query_nodes or not self.last_response_nodes:
            print("[STDP] Pas de nœuds à associer (tampons vides).")
            return

        print(f"\n--- APPLICATION STDP (Delta: {delta}) ---")
        for src in self.last_query_nodes:
            src_word = self.rev_lexicon.get(src, str(src))
            for tgt in self.last_response_nodes:
                tgt_word = self.rev_lexicon.get(tgt, str(tgt))
                print(f"[STDP Feedback] Ancrage : '{src_word}' (ID {src}) -> '{tgt_word}' (ID {tgt})")

        self.graph.apply_plasticity_between_sets(
            source_nodes=self.last_query_nodes,
            target_nodes=self.last_response_nodes,
            delta=delta
        )
        print("---------------------------------------\n")
        
