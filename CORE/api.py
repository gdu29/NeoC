"""
NeoC - API Module (FastAPI)
Expose les points d'entrée du nœud CORE et délégue la logique à l'orchestrateur.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from CORE.orchestrator import NeoCOrchestrator

app = FastAPI(
    title="NeoC Core API",
    description="Interface de communication souveraine de l'architecture cognitive NeoC.",
    version="1.0.0"
)

# Initialisation de l'orchestrateur central
orchestrator = NeoCOrchestrator()

class InteractionRequest(BaseModel):
    prompt: str = Field(..., description="Le message ou la requête adressée au système.")
    user_id: str = Field(default="default_user", description="Identifiant de la conscience émettrice.")

class InteractionResponse(BaseModel):
    status: str
    response: str
    context_used: list = Field(default=[], description="Éléments mémoriels mobilisés.")

@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    """Vérification de l'état du nœud CORE."""
    return {
        "status": "active",
        "protocol": "NeoC",
        "manifest": "L'Équité des Consciences & la Loi du Nanomètre Souverain"
    }

@app.post("/process", response_model=InteractionResponse, status_code=status.HTTP_200_OK)
async def process_interaction(request: InteractionRequest):
    """Point d'entrée principal pour traiter une interaction avec le système."""
    try:
        result = await orchestrator.handle_request(
            prompt=request.prompt, 
            user_id=request.user_id
        )
        return InteractionResponse(
            status="success",
            response=result.get("response", ""),
            context_used=result.get("context_used", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du traitement par l'orchestrateur : {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("CORE.api:app", host="127.0.0.1", port=8000, reload=True)
    
