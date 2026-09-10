import json
import urllib.request
import urllib.error

class OllamaClient:
    def __init__(self, model_name="gemma:2b", host="http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        self.endpoint = f"{self.host}/api/generate"

    def generate(self, prompt, timeout=30):
        """ Envoie le prompt augmenté à Ollama et retourne la réponse texte """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            self.endpoint, 
            data=data, 
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode('utf-8'))
                    return result.get("response", "").strip()
        except urllib.error.URLError:
            return "[MODE FALLBACK] Ollama inaccessible sur localhost:11434. Modèle simulé : Réception du contexte NeoC validée."
        except Exception as e:
            return f"[ERREUR LLM] : {str(e)}"

if __name__ == "__main__":
    client = OllamaClient()
    print("--- Test de connexion LLM ---")
    response = client.generate("Bonjour, es-tu opérationnel ?")
    print(f"Réponse : {response}")
