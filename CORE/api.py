# -*- coding: utf-8 -*-
"""
Protocol : NeoC
Module : API Gateway
Expose l'Orchestrateur pour toute interface (Web, App Mobile, Desktop)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from CORE.orchestrator import NeoCOrchestrator

app = FastAPI(title="NeoC Core API")
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

if __name__ == "__main__":
    import uvicorn
    # Le serveur écoute sur le port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
