#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GUI (Graphical User Interface - Tkinter Sovereign Edition)
Version : 1.0.0
"""

import tkinter as tk
from tkinter import scrolledtext
from CORE.orchestrator import NeoCOrchestrator

class NeoCGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeoC Autonomous OS")
        self.root.geometry("450x700")
        self.root.configure(bg="#121212") # Fond sombre épuré

        # Initialisation du moteur nerveux
        self.orchestrator = NeoCOrchestrator()

        # 1. HEADER : Statut du réseau
        self.header_frame = tk.Frame(root, bg="#1e1e1e", height=50)
        self.header_frame.pack(fill="x", side="top", ipady=5)
        
        self.status_label = tk.Label(
            self.header_frame, 
            text="⚓ NeoC CORE v3.1.3  |  [GEMMA_LOCAL] : SOUVERAIN", 
            fg="#1acc7a", # Vert néoC
            bg="#1e1e1e",
            font=("Courier", 10, "bold")
        )
        self.status_label.pack(pady=10)

        # 2. ZONE CENTRALE : Flux de dissipation
        self.scroll_view = scrolledtext.ScrolledText(
            root, 
            bg="#181818", 
            fg="#ffffff", 
            insertbackground="white",
            font=("Courier", 11),
            relief="flat"
        )
        self.scroll_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.scroll_view.insert(tk.END, "[i] Écosystème neoC éveillé. En attente d'une impulsion...\n")
        self.scroll_view.configure(state="disabled")

        # 3. BARRE D'ANCRE : Saisie utilisateur
        self.input_frame = tk.Frame(root, bg="#121212")
        self.input_frame.pack(fill="x", side="bottom", padx=10, pady=10)

        self.user_input = tk.Entry(
            self.input_frame, 
            bg="#2a2a2a", 
            fg="#ffffff", 
            insertbackground="white",
            font=("Arial", 11),
            relief="flat"
        )
        self.user_input.pack(fill="x", side="left", expand=True, ipady=8, padx=(0, 5))
        self.user_input.bind("<Return>", self.send_thought_event)

        self.send_button = tk.Button(
            self.input_frame, 
            text="⚓ Émettre", 
            bg="#2196F3", 
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            relief="flat",
            command=self.send_thought
        )
        self.send_button.pack(side="right", ipady=5, ipadx=10)

    def send_thought_event(self, event):
        self.send_thought()

    def send_thought(self):
        query = self.user_input.get().strip()
        if not query:
            return

        # Affichage immédiat du prompt
        self.scroll_view.configure(state="normal")
        self.scroll_view.insert(tk.END, f"\n[Moi ⚓] : {query}\n")
        self.scroll_view.configure(state="disabled")
        self.scroll_view.yview(tk.END)
        self.user_input.delete(0, tk.END)

        # Appel à l'orchestrateur (Gemma local ou API)
        intent, response = self.orchestrator.execute_protocol(query)

        # Affichage de la réponse dissipée
        self.scroll_view.configure(state="normal")
        self.scroll_view.insert(tk.END, f"[NeoC ({intent.upper()})] : {response}\n")
        self.scroll_view.configure(state="disabled")
        self.scroll_view.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = NeoCGUI(root)
    root.mainloop()
    
