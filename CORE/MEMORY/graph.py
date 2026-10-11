"""
NeoC - Memory Graph Module (CORE/MEMORY/graph.py)
Gère le graphe de mémoire dynamique pour contextualiser les interactions et relier les concepts.
"""

import networkx as nx
import os
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger("NeoCMemoryGraph")

class MemoryGraph:
    def __init__(self, storage_path: str = "CORE/MEMORY/memory_db.json"):
        self.storage_path = storage_path
        self.graph = nx.DiGraph()
        self.load_memory()

    def load_memory(self):
        """Charge le graphe de mémoire depuis le stockage persistant s'il existe."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.graph = nx.node_link_graph(data)
                logger.info(f"🧠 Graphe de mémoire chargé avec succès ({self.graph.number_of_nodes()} nœuds).")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la mémoire : {e}")
                self.graph = nx.DiGraph()
        else:
            logger.info("🧠 Aucun stockage mémoriel trouvé. Initialisation d'un nouveau graphe vierge.")

    def save_memory(self):
        """Sauvegarde l'état actuel du graphe de mémoire sur le disque."""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            data = nx.node_link_data(self.graph)
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("💾 Graphe de mémoire sauvegardé.")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la mémoire : {e}")

    def add_interaction(self, user_id: str, input_text: str, output_text: str):
        """Ajoute une interaction (prompt/réponse) et crée des liens contextuels."""
        interaction_id = f"interaction_{self.graph.number_of_nodes() + 1}"
        
        # Ajout du nœud principal pour l'interaction
        self.graph.add_node(
            interaction_id, 
            type="interaction", 
            user_id=user_id, 
            input=input_text, 
            output=output_text
        )

        # Lien basique avec l'utilisateur ou la session
        if not self.graph.has_node(user_id):
            self.graph.add_node(user_id, type="entity")
        
        self.graph.add_edge(user_id, interaction_id, relation="emits")
        
        # Sauvegarde automatique après modification
        self.save_memory()

    def retrieve_context(self, prompt: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Récupère les éléments contextuels pertinents dans le graphe 
        en fonction du prompt (recherche par mots-clés ou historique récent).
        """
        context = []
        nodes = [n for n, d in self.graph.nodes(data=True) if d.get("type") == "interaction"]
        recent_nodes = nodes[-limit:] if nodes else []
        
        for node_id in recent_nodes:
            node_data = self.graph.nodes[node_id]
            context.append({
                "id": node_id,
                "input": node_data.get("input"),
                "output": node_data.get("output")
            })
            
        return context
