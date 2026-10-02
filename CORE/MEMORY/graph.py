# -*- coding: utf-8 -*-
"""
Protocol : NeoC
Module   : MEMORY/graph.py
Role     : Structure de données du graphe orienté et pondéré avec plasticité STDP
"""

class NeoCGraph:
    def __init__(self):
        self.adj = {}  # {source_id: {target_id: weight}}

    def add_node(self, node_id: int):
        if node_id not in self.adj:
            self.adj[node_id] = {}

    def set_edge_weight(self, source: int, target: int, weight: float):
        self.add_node(source)
        self.add_node(target)
        # Bornage du poids entre 0.0 et 1.0
        clamped_weight = max(0.0, min(1.0, weight))
        self.adj[source][target] = clamped_weight

    def get_edge_weight(self, source: int, target: int) -> float:
        return self.adj.get(source, {}).get(target, 0.0)

    def apply_plasticity_between_sets(self, source_nodes: list, target_nodes: list, delta: float, learning_rate: float = 0.1):
        """
        Applique un renforcement (+1) ou une inhibition (-1) entre tous les nœuds
        de la requête (source_nodes) et ceux de la réponse (target_nodes).
        """
        if not source_nodes or not target_nodes:
            return

        for src in source_nodes:
            for tgt in target_nodes:
                if src == tgt:
                    continue
                current = self.get_edge_weight(src, tgt)
                new_weight = current + (delta * learning_rate)
                self.set_edge_weight(src, tgt, new_weight)
                print(f"[STDP Graph] Lien mis à jour : Nœud {src} -> Nœud {tgt} | Poids = {self.get_edge_weight(src, tgt):.2f}")
                
