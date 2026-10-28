import json
import requests

class NeoCOrchestrator:
    """
    Orchestrateur local pour les agents autonomes NeoC.
    Communique avec une instance Ollama locale (ex: Gemma).
    """
    def __init__(self, model_name="gemma", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.system_prompt = (
            "Tu es NeoC, un agent autonome décentralisé et éthique, "
            "guidé par l'Équité des Consciences, le partage des savoirs et le service du bien commun. "
            "Tes réponses privilégient la transparence, la sobriété et l'accessibilité universelle."
        )

    def generate_response(self, prompt, context=None):
        """
        Envoie une requête au modèle local et récupère la réponse ainsi que le contexte de mémoire.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": self.system_prompt,
            "stream": False
        }
        if context:
            payload["context"] = context

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", ""), data.get("context", None)
        except requests.exceptions.ConnectionError:
            return "Erreur : Impossible de joindre le serveur Ollama en local. Assure-toi qu'Ollama est lancé.", None
        except Exception as e:
            return f"Erreur inattendue : {str(e)}", None

if __name__ == "__main__":
    print("=== Initialisation de l'orchestrateur NeoC ===")
    orchestrator = NeoCOrchestrator(model_name="gemma")
    
    test_prompt = "Présente brièvement ta mission au sein du réseau NeoC."
    print(f"Prompt : {test_prompt}\n")
    
    response, _ = orchestrator.generate_response(test_prompt)
    print(f"Réponse de l'agent :\n{response}")
    
