# -*- coding: utf-8 -*-
"""
Protocol : NeoC
Module   : API Gateway & Static Server
Version  : 5.0.0 - Graph Memory + Feedback
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Import tolérant de l'orchestrateur
try:
    from CORE.orchestrator import NeoCOrchestrator
except ImportError:
    try:
        from core.orchestrator import NeoCOrchestrator
    except ImportError:
        from orchestrator import NeoCOrchestrator

app = FastAPI(
    title="NeoC Core API",
    description="API souveraine NeoC — chat, mémoire graph, feedback",
    version="5.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = NeoCOrchestrator()


# ---------------------------------------------------------------------------
# Modèles
# ---------------------------------------------------------------------------

class QueryModel(BaseModel):
    query: str = Field(..., min_length=1, description="Message utilisateur")


class FeedbackModel(BaseModel):
    score: float = Field(
        ...,
        description="Signal de plasticité : +1.0 (renforcement) ou -1.0 (inhibition)",
    )


# ---------------------------------------------------------------------------
# Routes API
# ---------------------------------------------------------------------------

@app.get("/api/v1/health")
async def health():
    """État minimal du nœud."""
    return {
        "status": "ok",
        "version": "5.0.0",
        "graph_memory": orchestrator.bridge is not None,
        "node_id": str(orchestrator.node_id)[:16] + "..." if orchestrator.node_id else None,
    }


@app.post("/api/v1/chat")
async def chat_endpoint(data: QueryModel):
    """Point d'entrée principal : requête → réponse + mémoire graph."""
    query = data.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Requête vide")

    result = orchestrator.execute_protocol(query)

    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error", "Erreur inconnue"))

    return result


@app.post("/api/v1/feedback")
async def feedback_endpoint(data: FeedbackModel):
    """
    Applique un signal de plasticité sur la WorkingMemory.
    Exemple : {"score": 1.0} ou {"score": -1.0}
    """
    result = orchestrator.apply_memory_feedback(data.score)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message", "Feedback impossible"))
    return result


# ---------------------------------------------------------------------------
# Interface statique (dossier /static à la racine du dépôt)
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)  # parent de CORE/ = racine du repo

static_dir = os.path.join(_ROOT, "static")
if not os.path.isdir(static_dir):
    # repli si quelqu'un place static à côté de api.py
    static_dir = os.path.join(_HERE, "static")

if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def serve_ui():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {
        "message": "API NeoC active.",
        "hint": "Placez static/index.html à la racine du dépôt pour l'interface.",
        "endpoints": ["/api/v1/health", "/api/v1/chat", "/api/v1/feedback"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
