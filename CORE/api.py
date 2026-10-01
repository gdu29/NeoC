import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Imports des modules internes du CORE NeoC (Pointés vers CORE.MEMORY.bridge)
try:
    from CORE.orchestrator import NeoCOrchestrator
    from CORE.MEMORY.bridge import NeoCBridge
    from CORE.equity_constraint import equity_eval
except ImportError:
    # Alternative si exécuté directement depuis le dossier CORE
    from orchestrator import NeoCOrchestrator
    from MEMORY.bridge import NeoCBridge
    from equity_constraint import equity_eval

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

# Initialisation des composants du noyau
memory_bridge = NeoCBridge()
orchestrator = NeoCOrchestrator(memory_bridge=memory_bridge)

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
        # Traitement via l'orchestrateur (interrogation LLM local + enrichissement mémoire)
        response_data = await orchestrator.process_input(user_text)
        
        # Formatage de la réponse
        raw_response = response_data.get("text", "Pas de réponse générée.")
        node_id = response_data.get("node_id", "node_default")
        
        # Traçabilité et vérification d'équité
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
        # Mise à jour de la mémoire via la mémoire de travail de NeoCBridge
        memory_bridge.wm.apply_plasticity(delta=payload.value)
        return {
            "status": "success",
            "node_id": payload.node_id,
            "feedback_applied": payload.value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de plasticité mémoire : {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
    
