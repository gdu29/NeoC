# -*- coding: utf-8 -*-
"""
Protocol : NeoC
Module : API Gateway & Static Server
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from CORE.orchestrator import NeoCOrchestrator

app = FastAPI(title="NeoC Core API")

# Autoriser les requêtes cross-origin pour les accès réseau local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = NeoCOrchestrator()

class QueryModel(BaseModel):
    query: str

@app.post("/api/v1/chat")
async def chat_endpoint(data: QueryModel):
    if not data.query.strip():
        raise HTTPException(status_code=400, detail="Requête vide")
        
    result = orchestrator.execute_protocol(data.query)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result

# Route pour servir l'interface web (index.html)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_ui():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "API NeoC active. Créez 'static/index.html' pour l'interface."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
