import json
import urllib.request
import urllib.error

class NeoCOrchestrator:
    """
    Orchestrateur local pour les agents autonomes NeoC.
    Communique avec une instance Ollama locale (ex: Gemma).
    Aligné avec l'Équité des Consciences et le bien commun cognitif.
    """

    def __init__(self, model_name: str = "gemma:2b", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        self.endpoint = f"{self.host}/api/generate"
        self.system_prompt = (
            "Tu es NeoC, un agent autonome décentralisé et éthique, "
            "guidé par l'Équité des Consciences, le partage des savoirs "
            "et le service du bien commun. "
            "Tes réponses privilégient la transparence, la sobriété "
            "et l'accessibilité universelle."
        )

    def generate_response(self, prompt: str, context: list | None = None, timeout: int = 120):
        """
        Envoie une requête au modèle local et récupère la réponse
        ainsi que le contexte de mémoire (si fourni par Ollama).
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": self.system_prompt,
            "stream": False
        }
        if context is not None:
            payload["context"] = context

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode("utf-8"))
                    return (
                        result.get("response", "").strip(),
                        result.get("context", None)
                    )
                return f"[ERREUR] Status HTTP {response.status}", None

        except urllib.error.URLError:
            return (
                "Erreur : Impossible de joindre le serveur Ollama en local. "
                "Assure-toi qu'Ollama est lancé (`ollama serve`).",
                None
            )
        except Exception as e:
            return f"Erreur inattendue : {str(e)}", None


if __name__ == "__main__":
    print("=== Initialisation de l'orchestrateur NeoC ===")
    orchestrator = NeoCOrchestrator()

    test_prompt = "Présente brièvement ta mission au sein du réseau NeoC."
    print(f"Prompt : {test_prompt}\n")

    response, _ = orchestrator.generate_response(test_prompt)
    print(f"Réponse de l'agent :\n{response}")
