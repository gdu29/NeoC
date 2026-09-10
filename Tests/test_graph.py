import struct
import os
import hashlib
import json
from collections import OrderedDict

NODE_FORMAT = "<Q 16s 4Q d"
NODE_SIZE = struct.calcsize(NODE_FORMAT)  # 64 octets

def text_to_sdr(text, total_bits=128, active_bits=4):
    hash_digest = hashlib.sha256(text.encode('utf-8')).digest()
    positions = set()
    i = 0
    while len(positions) < active_bits and i < len(hash_digest):
        pos = hash_digest[i] % total_bits
        positions.add(pos)
        i += 1
        
    sdr_bytes = bytearray(16)
    for pos in positions:
        byte_index = pos // 8
        bit_index = pos % 8
        sdr_bytes[byte_index] |= (1 << bit_index)
        
    return bytes(sdr_bytes)

def sdr_overlap(sdr1_bytes, sdr2_bytes):
    overlap = 0
    for b1, b2 in zip(sdr1_bytes, sdr2_bytes):
        overlap += bin(b1 & b2).count('1')
    return overlap

def write_node(file_path, node_id, sdr_bytes, pointers, weight):
    mode = "r+b" if os.path.exists(file_path) else "w+b"
    with open(file_path, mode) as f:
        f.seek(node_id * NODE_SIZE)
        packed_data = struct.pack(NODE_FORMAT, node_id, sdr_bytes, *pointers, weight)
        f.write(packed_data)
        f.flush()
        os.fsync(f.fileno())

def read_node(file_path, node_id):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        f.seek(node_id * NODE_SIZE)
        data = f.read(NODE_SIZE)
        if not data or len(data) < NODE_SIZE:
            return None
        return struct.unpack(NODE_FORMAT, data)

def add_causal_link(file_path, parent_id, child_id):
    node = read_node(file_path, parent_id)
    if not node:
        return False
    pointers = list(node[2:6])
    if child_id in pointers:
        return True
    
    added = False
    for i in range(4):
        if pointers[i] == 0 and child_id != 0:
            pointers[i] = child_id
            added = True
            break
            
    if not added:
        print(f"[AVERTISSEMENT] Nœud {parent_id} : Capacité maximale atteinte !")
        return False

    write_node(file_path, parent_id, node[1], tuple(pointers), node[6])
    return True

# -----------------------------------------------------------------------------
# TABLE DE CORRESPONDANCE PERSISTANTE
# -----------------------------------------------------------------------------
class ConceptLexicon:
    def __init__(self, index_file="lexicon.json"):
        self.index_file = index_file
        self.word2id = {}
        self.id2word = {}
        self.load()

    def load(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.word2id = data.get("word2id", {})
                self.id2word = {int(k): v for k, v in data.get("id2word", {}).items()}

    def save(self):
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump({"word2id": self.word2id, "id2word": self.id2word}, f, ensure_ascii=False, indent=2)

    def get_or_create_id(self, word, db_file):
        word = word.lower().strip()
        if word in self.word2id:
            return self.word2id[word]

        new_id = len(self.word2id)
        self.word2id[word] = new_id
        self.id2word[new_id] = word
        self.save()

        sdr = text_to_sdr(word)
        write_node(db_file, node_id=new_id, sdr_bytes=sdr, pointers=(0, 0, 0, 0), weight=1.0)
        print(f"[LEXIQUE] Nouveau concept enregistré : '{word}' -> ID {new_id}")
        return new_id

    def get_word(self, node_id):
        return self.id2word.get(node_id, f"Inconnu ({node_id})")

    def find_similar(self, db_file, target_word, top_k=3):
        target_sdr = text_to_sdr(target_word)
        scores = []

        for word, nid in self.word2id.items():
            if word == target_word.lower():
                continue
            node = read_node(db_file, nid)
            if node:
                overlap = sdr_overlap(target_sdr, node[1])
                if overlap > 0:
                    scores.append((nid, word, overlap))

        scores.sort(key=lambda x: x[2], reverse=True)
        return scores[:top_k]

# -----------------------------------------------------------------------------
# REGISTRE DE TRAVAIL & MOTEUR D'INFÉRENCE/RÉSONANCE
# -----------------------------------------------------------------------------
class WorkingMemory:
    def __init__(self, db_file, capacity=8, decay_rate=0.85):
        self.db_file = db_file
        self.capacity = capacity
        self.decay_rate = decay_rate
        self.slots = OrderedDict()
        self.eligibility_traces = {}
        self.activations = {}

    def get_node(self, node_id, initial_energy=1.0):
        for nid in list(self.eligibility_traces.keys()):
            self.eligibility_traces[nid] *= self.decay_rate
            if self.eligibility_traces[nid] < 0.05:
                del self.eligibility_traces[nid]

        self.eligibility_traces[node_id] = 1.0
        self.activations[node_id] = max(0.0, self.activations.get(node_id, 0.0) + initial_energy)

        if node_id in self.slots:
            self.slots.move_to_end(node_id)
            return self.slots[node_id]

        node = read_node(self.db_file, node_id)
        if not node:
            return None

        if len(self.slots) >= self.capacity:
            evicted_id, _ = self.slots.popitem(last=False)

        self.slots[node_id] = node
        return node

    def propagate(self, steps=1, damping=0.5, threshold=0.05):
        for step in range(steps):
            new_activations = self.activations.copy()
            for node_id, energy in list(self.activations.items()):
                if abs(energy) < threshold:
                    continue

                node = read_node(self.db_file, node_id)
                if not node:
                    continue

                pointers = [p for p in node[2:6] if p != 0]
                weight = node[6]
                
                if pointers:
                    delta_energy = (energy * damping * weight) / len(pointers)
                    for child_id in pointers:
                        current_val = new_activations.get(child_id, 0.0)
                        updated_val = max(0.0, current_val + delta_energy)
                        new_activations[child_id] = updated_val
                        
                        if child_id not in self.slots and updated_val >= threshold:
                            self.get_node(child_id, initial_energy=0.0)

            self.activations = new_activations

    def apply_plasticity(self, delta):
        active_ids = list(self.eligibility_traces.keys())
        if len(active_ids) < 2 or delta == 0:
            return

        parent_id = active_ids[-2]
        child_id = active_ids[-1]
        trace_factor = self.eligibility_traces.get(parent_id, 1.0)
        
        if add_causal_link(self.db_file, parent_id, child_id):
            updated_parent = read_node(self.db_file, parent_id)
            current_weight = updated_parent[6]
            new_weight = max(-2.0, min(2.0, current_weight + (0.1 * delta * trace_factor)))
            write_node(self.db_file, parent_id, updated_parent[1], updated_parent[2:6], new_weight)
            
            tag = "Inhibition (Lien -)" if delta < 0 else "Excitation (Lien +)"
            print(f"[STDP] {tag} (Poids={new_weight:.2f}) : Nœud {parent_id} -> Nœud {child_id}")

    def reason(self, lexicon, query_word, steps=2, damping=0.5, use_sdr=True):
        """ Déclenche une boucle de résonance complète à partir d'un mot-clé """
        # Réinitialisation des activations courantes
        self.activations.clear()

        if query_word not in lexicon.word2id:
            return []

        target_id = lexicon.word2id[query_word]
        self.get_node(target_id, initial_energy=1.0)

        # 1. Amorçage SDR (Activation par résonance sémantique)
        if use_sdr:
            matches = lexicon.find_similar(self.db_file, query_word, top_k=2)
            for nid, w, overlap in matches:
                sdr_energy = 0.2 * (overlap / 4.0)
                self.get_node(nid, initial_energy=sdr_energy)

        # 2. Propagation Causale
        self.propagate(steps=steps, damping=damping)

        # Trier les résultats par niveau d'énergie émergente
        results = [(nid, lexicon.get_word(nid), act) for nid, act in self.activations.items() if act > 0.01]
        results.sort(key=lambda x: x[2], reverse=True)
        return results
