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

def write_node(file_path, node_id, sdr_bytes, pointers, weight):
    mode = "r+b" if os.path.exists(file_path) else "w+b"
    with open(file_path, mode) as f:
        f.seek(node_id * NODE_SIZE)
        packed_data = struct.pack(NODE_FORMAT, node_id, sdr_bytes, *pointers, weight)
        f.write(packed_data)

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
    if child_id not in pointers:
        for i in range(4):
            if pointers[i] == 0:
                pointers[i] = child_id
                break
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

# -----------------------------------------------------------------------------
# REGISTRE DE TRAVAIL
# -----------------------------------------------------------------------------
class WorkingMemory:
    def __init__(self, db_file, capacity=4):
        self.db_file = db_file
        self.capacity = capacity
        self.slots = OrderedDict()
        self.eligibility_traces = {}

    def get_node(self, node_id):
        self.eligibility_traces[node_id] = 1.0

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

    def apply_plasticity(self, delta):
        active_ids = list(self.eligibility_traces.keys())
        if len(active_ids) < 2 or delta <= 0:
            return

        parent_id = active_ids[-2]
        child_id = active_ids[-1]
        
        add_causal_link(self.db_file, parent_id, child_id)
        updated_parent = read_node(self.db_file, parent_id)
        new_weight = min(2.0, updated_parent[6] + (0.1 * delta))
        write_node(self.db_file, parent_id, updated_parent[1], updated_parent[2:6], new_weight)
        
        print(f"[STDP] Lien préservé sur SSD : Nœud {parent_id} -> Nœud {child_id}")

# --- TEST DE PERSISTANCE CONTINUE ---
if __name__ == "__main__":
    db_file = "neoc_graph.bin"
    lex_file = "lexicon.json"

    lexicon = ConceptLexicon(lex_file)
    wm = WorkingMemory(db_file, capacity=4)

    print("--- ÉTAT ACTUEL DE LA BASE DE CONNAISSANCES ---")
    print(f"Nombre de concepts en mémoire persistante : {len(lexicon.word2id)}")
    for wid, wtext in lexicon.id2word.items():
        n = read_node(db_file, wid)
        ptrs = n[2:6] if n else ()
        print(f" - ID {wid} ('{wtext}') -> Pointe vers : {ptrs}")

    print("\n--- AJOUT D'UNE NOUVELLE SÉQUENCE SANS EFFACER L'ANCIENNE ---")
    # On ajoute deux nouveaux concepts
    id_a = lexicon.get_or_create_id("chaleur", db_file)
    id_b = lexicon.get_or_create_id("fumée", db_file)

    wm.get_node(id_a)
    wm.get_node(id_b)
    wm.apply_plasticity(delta=1.0)
EOF
