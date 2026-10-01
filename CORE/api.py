import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 1. Imports Mémoire & Orchestrateur
try:
    from CORE.orchestrator import NeoCOrchestrator
    from CORE.MEMORY.bridge import NeoCBridge
except ImportError:
    from orchestrator import NeoCOrchestrator
    from MEMORY.bridge import NeoCBridge

# 2. Import Sécurisé pour Equity Constraint
try:
    try:
        from CORE.equity_constraint import equity_eval
    except ImportError:
        from equity_constraint import equity_eval
except (ImportError, AttributeError):
    def equity_eval(user_input: str, response_text: str):
        return {
            "traceability": "Pass-through (Local Node)",
            "reversible": True,
            "uncertainty_score": 0.0
        }

app = FastAPI(
    title="NeoC Core Node",
    description="Nœud souverain d'IA locale avec mémoire en graphe et contraintes d'équité.",
    version="0.2.0"
)

# Configuration et montage du répertoire static
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialisation de l'orchestrateur
orchestrator = NeoCOrchestrator()

# Modèles de données Pydantic
class ChatPayload(BaseModel):
    message: str

class FeedbackPayload(BaseModel):
    node_id: str
    value: int  # +1 ou -1

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html introuvable dans static/")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat_endpoint(payload: ChatPayload):
    user_text = payload.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Le message ne peut pas être vide.")

    try:
        # Appel du vrai routeur cognitif (execute_protocol)
        result = orchestrator.execute_protocol(user_text)
        
        if result.get("status") == "error":
            raw_response = f"Erreur Ollama / LLM : {result.get('error')}"
        else:
            raw_response = result.get("response", "Pas de réponse générée.")

        node_id = "node_default"
        equity_meta = equity_eval(user_text, raw_response)

        return {
            "status": "success",
            "response": raw_response,
            "node_id": node_id,
            "equity": equity_meta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'exécution du nœud CORE : {str(e)}")

@app.post("/feedback")
async def feedback_endpoint(payload: FeedbackPayload):
    if payload.value not in (-1, 1):
        raise HTTPException(status_code=400, detail="La valeur de feedback doit être 1 ou -1.")

    try:
        orchestrator.apply_memory_feedback(float(payload.value))
        return {
            "status": "success",
            "node_id": payload.node_id,
            "feedback_applied": payload.value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de plasticité mémoire : {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
    
