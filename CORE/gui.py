#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : GUI (Graphical User Interface - Kivy Sovereign Edition)
Version : 1.0.0
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from CORE.orchestrator import NeoCOrchestrator

class NeoCGUI(BoxLayout):
    def __init__(self, **kwargs):
        super(NeoCGUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Initialisation de l'écosystème en arrière-plan
        self.orchestrator = NeoCOrchestrator()
        
        # 1. HEADER : Statut du réseau et des canaux
        self.header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        self.status_label = Label(
            text="⚓ NeoC CORE v3.1.3  |  [GEMMA_LOCAL] : CONNECTÉ", 
            markup=True,
            color=(0.1, 0.8, 0.4, 1) # Vert néoC
        )
        self.header_layout.add_widget(self.status_label)
        self.add_widget(self.header_layout)
        
        # 2. ZONE CENTRALE : Flux de pensées dissipé
        self.scroll_view = ScrollView(size_hint_y=0.75)
        self.terminal_output = Label(
            text="[i] Écosystème neoC éveillé. En attente d'une impulsion...\n",
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True
        )
        self.terminal_output.bind(texture_size=self.terminal_output.setter('size'))
        self.scroll_view.add_widget(self.terminal_output)
        self.add_widget(self.scroll_view)
        
        # 3. BARRE D'ANCRE : Saisie utilisateur
        self.input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=5)
        self.user_input = TextInput(
            hint_text="Projeter une pensée philosophique ou logique...",
            multiline=False,
            size_hint_x=0.8
        )
        self.user_input.bind(on_text_validate=self.send_thought)
        
        self.send_button = Button(
            text="⚓ Émettre",
            size_hint_x=0.2,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.send_button.bind(on_press=self.send_thought)
        
        self.input_layout.add_widget(self.user_input)
        self.input_layout.add_widget(self.send_button)
        self.add_widget(self.input_layout)

    def send_thought(self, instance):
        query = self.user_input.text.strip()
        if not query:
            return
            
        # Affichage immédiat de l'émission dans la zone centrale
        self.terminal_output.text += f"\n[b][Moi ⚓][/b] : {query}\n"
        self.user_input.text = ""
        
        # Traitement via l'orchestrateur (Routage agnostique / local gemma)
        intent, response = self.orchestrator.execute_protocol(query)
        
        # Dissipation graphique du signal reçu
        self.terminal_output.text += f"[b][NeoC ({intent.upper()})][/b] : {response}\n"

class NeoCPlatform(App):
    def build(self):
        self.title = "NeoC Autonomous OS"
        return NeoCGUI()

if __name__ == "__main__":
    NeoCPlatform().run()
      
